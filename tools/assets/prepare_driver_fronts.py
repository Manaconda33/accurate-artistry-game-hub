#!/usr/bin/env python3
"""Prepare approved front driver art and repair Accu's wheel apertures.

Approved source candidates can contain a baked light checkerboard or flat
black matte. This tool removes only edge-connected neutral pixels, produces premultiplied-alpha
512x512 runtime sprites, and clears the neutral checker remnants inside three
known Accu steering-wheel apertures without redrawing character art.
"""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


def neighboring(mask: np.ndarray) -> np.ndarray:
    expanded = mask.copy()
    expanded[1:] |= mask[:-1]
    expanded[:-1] |= mask[1:]
    expanded[:, 1:] |= mask[:, :-1]
    expanded[:, :-1] |= mask[:, 1:]
    return expanded


def edge_connected_neutral_background(rgb: np.ndarray) -> np.ndarray:
    maximum = rgb.max(axis=2)
    minimum = rgb.min(axis=2)
    corner_samples = np.concatenate(
        (rgb[0, :], rgb[-1, :], rgb[:, 0], rgb[:, -1]), axis=0
    )
    border_median = np.median(corner_samples, axis=0)
    dark_matte = float(border_median.max()) < 64
    if dark_matte:
        # Keep the threshold deliberately tight so black hair, horns, and outlines
        # remain foreground even when they touch the silhouette edge.
        candidate = (maximum <= 10) & ((maximum - minimum) <= 8)
    else:
        candidate = (minimum >= 208) & ((maximum - minimum) <= 24)
    height, width = candidate.shape
    background = np.zeros_like(candidate)
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        queue.extend(((0, x), (height - 1, x)))
    for y in range(height):
        queue.extend(((y, 0), (y, width - 1)))

    while queue:
        y, x = queue.popleft()
        if background[y, x] or not candidate[y, x]:
            continue
        background[y, x] = True
        if y:
            queue.append((y - 1, x))
        if y + 1 < height:
            queue.append((y + 1, x))
        if x:
            queue.append((y, x - 1))
        if x + 1 < width:
            queue.append((y, x + 1))

    # Absorb only neutral antialias spill adjoining confirmed background.
    if dark_matte:
        edge = neighboring(background) & ~background
        background |= edge & (maximum <= 20) & ((maximum - minimum) <= 14)
    else:
        for _ in range(2):
            edge = neighboring(background) & ~background
            spill = edge & (minimum >= 190) & ((maximum - minimum) <= 42)
            if not spill.any():
                break
            background |= spill
    return background


def enclosed_upper_neutral_background(
    rgb: np.ndarray, background: np.ndarray, minimum_pixels: int = 200
) -> np.ndarray:
    """Find large enclosed pale-matte islands in the upper character silhouette.

    This is opt-in for silhouettes such as Krios's closed horn loops. The size
    and location gates keep small neutral highlights, teeth, and metal details.
    """
    maximum = rgb.max(axis=2)
    minimum = rgb.min(axis=2)
    candidate = (
        ~background
        & (minimum >= 150)
        & ((maximum - minimum) <= 70)
    )
    height, width = candidate.shape
    visited = np.zeros_like(candidate)
    enclosed = np.zeros_like(candidate)
    minimum_y = round(height * 0.12)
    maximum_y = round(height * 0.42)

    for start_y, start_x in zip(*np.where(candidate & ~visited)):
        queue: deque[tuple[int, int]] = deque([(int(start_y), int(start_x))])
        component: list[tuple[int, int]] = []
        top = int(start_y)
        while queue:
            y, x = queue.popleft()
            if visited[y, x] or not candidate[y, x]:
                continue
            visited[y, x] = True
            component.append((y, x))
            top = min(top, y)
            if y:
                queue.append((y - 1, x))
            if y + 1 < height:
                queue.append((y + 1, x))
            if x:
                queue.append((y, x - 1))
            if x + 1 < width:
                queue.append((y, x + 1))
        if len(component) >= minimum_pixels and minimum_y <= top <= maximum_y:
            ys, xs = zip(*component)
            enclosed[np.asarray(ys), np.asarray(xs)] = True
    return enclosed


def premultiplied_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    premultiplied = np.concatenate((rgba[:, :, :3] * alpha, rgba[:, :, 3:4]), axis=2)
    channels = [
        np.asarray(
            Image.fromarray(np.clip(premultiplied[:, :, channel], 0, 255).astype(np.uint8)).resize(
                size, Image.Resampling.LANCZOS
            ),
            dtype=np.float32,
        )
        for channel in range(4)
    ]
    resized = np.stack(channels, axis=2)
    resized_alpha = resized[:, :, 3:4]
    rgb = np.divide(
        resized[:, :, :3] * 255.0,
        resized_alpha,
        out=np.zeros_like(resized[:, :, :3]),
        where=resized_alpha > 0,
    )
    return Image.fromarray(
        np.concatenate((np.clip(rgb, 0, 255), resized_alpha), axis=2).astype(np.uint8), "RGBA"
    )


def prepare_front(
    source: Path,
    target: Path,
    size: int = 512,
    padding: float = 0.025,
    clear_enclosed_upper_matte: bool = False,
) -> None:
    rgb = np.asarray(Image.open(source).convert("RGB"))
    background = edge_connected_neutral_background(rgb)
    if clear_enclosed_upper_matte:
        background |= enclosed_upper_neutral_background(rgb, background)
    rgba = np.dstack((rgb, np.where(background, 0, 255).astype(np.uint8)))
    rgba[background, :3] = 0
    image = Image.fromarray(rgba, "RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"No foreground found in {source}")
    image = image.crop(bbox)
    usable = max(1, round(size * (1 - 2 * padding)))
    scale = min(usable / image.width, usable / image.height)
    resized = premultiplied_resize(
        image, (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    )
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((size - resized.width) // 2, (size - resized.height) // 2))
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target, format="PNG", optimize=True)


ACCU_APERTURES = {
    "steer-left.png": (122, 258, 42, 35),
    "steer-right.png": (397, 219, 42, 30),
    "victory.png": (111, 309, 36, 29),
}


def repair_accu_aperture(path: Path, aperture: tuple[int, int, int, int]) -> int:
    rgba = np.asarray(Image.open(path).convert("RGBA")).copy()
    rgb = rgba[:, :, :3]
    alpha = rgba[:, :, 3]
    maximum = rgb.max(axis=2)
    minimum = rgb.min(axis=2)
    center_x, center_y, radius_x, radius_y = aperture
    y, x = np.ogrid[: rgba.shape[0], : rgba.shape[1]]
    inside = ((x - center_x) / radius_x) ** 2 + ((y - center_y) / radius_y) ** 2 <= 1
    remove = inside & (alpha > 0) & (minimum >= 185) & ((maximum - minimum) <= 35)
    for _ in range(2):
        edge = neighboring(remove) & inside & ~remove & (alpha > 0)
        spill = edge & (minimum >= 145) & ((maximum - minimum) <= 75)
        if not spill.any():
            break
        remove |= spill
    rgba[remove] = 0
    Image.fromarray(rgba, "RGBA").save(path, format="PNG", optimize=True)
    return int(remove.sum())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lavi", required=True, type=Path)
    parser.add_argument("--manaconda", required=True, type=Path)
    parser.add_argument("--accu", required=True, type=Path)
    parser.add_argument("--asset-root", required=True, type=Path)
    args = parser.parse_args()

    approved = {
        "aa-02": args.lavi,
        "aa-09": args.manaconda,
        "aa-11": args.accu,
    }
    for character_id, source in approved.items():
        target = args.asset_root / character_id / "driver/front.png"
        prepare_front(source, target)
        print({"source": str(source), "target": str(target)})

    accu_driver = args.asset_root / "aa-11/driver"
    for filename, aperture in ACCU_APERTURES.items():
        removed = repair_accu_aperture(accu_driver / filename, aperture)
        print({"target": str(accu_driver / filename), "removed": removed})


if __name__ == "__main__":
    main()
