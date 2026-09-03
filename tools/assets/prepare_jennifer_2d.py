#!/usr/bin/env python3
"""Prepare Jennifer's approved 2D art as deterministic runtime PNGs."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


FILES = {
    "portrait.png": ("portrait.png", 256, 0.035),
    "front.png": ("driver/front.png", 512, 0.025),
    "rear.png": ("driver/rear.png", 512, 0.025),
    "steer-left.png": ("driver/steer-left.png", 512, 0.025),
    "steer-right.png": ("driver/steer-right.png", 512, 0.025),
    "hit.png": ("driver/hit.png", 512, 0.025),
    "victory.png": ("driver/victory.png", 512, 0.025),
    "front-steer-left.png": ("driver/front-steer-left.png", 512, 0.025),
    "front-steer-right.png": ("driver/front-steer-right.png", 512, 0.025),
    "front-hit.png": ("driver/front-hit.png", 512, 0.025),
    "front-victory.png": ("driver/front-victory.png", 512, 0.025),
}


def neighboring(mask: np.ndarray) -> np.ndarray:
    expanded = mask.copy()
    expanded[1:] |= mask[:-1]
    expanded[:-1] |= mask[1:]
    expanded[:, 1:] |= mask[:, :-1]
    expanded[:, :-1] |= mask[:, 1:]
    return expanded


def edge_connected_checkerboard(rgb: np.ndarray) -> np.ndarray:
    """Return light neutral pixels connected to an image edge."""
    maximum = rgb.max(axis=2)
    minimum = rgb.min(axis=2)
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

    # Remove only pale antialias spill touching confirmed background. The
    # generated checkerboard blends a narrow neutral fringe into dark curls and
    # gray fur, so this runs at source resolution before the premultiplied resize.
    for _ in range(3):
        edge = neighboring(background) & ~background
        spill = edge & (minimum >= 145) & ((maximum - minimum) <= 110)
        if not spill.any():
            break
        background |= spill

    # Closed curl loops can surround small checkerboard pockets. Clear only
    # substantial pale-neutral components; tiny specular details remain intact.
    enclosed_candidate = (
        ~background & (minimum >= 220) & ((maximum - minimum) <= 25)
    )
    visited = np.zeros_like(enclosed_candidate)
    enclosed = np.zeros_like(enclosed_candidate)
    for start_y, start_x in zip(*np.where(enclosed_candidate & ~visited)):
        queue = deque([(int(start_y), int(start_x))])
        component: list[tuple[int, int]] = []
        while queue:
            y, x = queue.popleft()
            if visited[y, x] or not enclosed_candidate[y, x]:
                continue
            visited[y, x] = True
            component.append((y, x))
            if y:
                queue.append((y - 1, x))
            if y + 1 < height:
                queue.append((y + 1, x))
            if x:
                queue.append((y, x - 1))
            if x + 1 < width:
                queue.append((y, x + 1))
        if len(component) >= 8:
            ys, xs = zip(*component)
            enclosed[np.asarray(ys), np.asarray(xs)] = True
    for _ in range(2):
        enclosed = neighboring(enclosed)
    background |= enclosed

    # The approved exports also contain a baked pale outline around the outer
    # silhouette. Remove three source pixels, roughly one pixel after runtime
    # resizing, without touching any enclosed character detail.
    for _ in range(3):
        background = neighboring(background)
    return background


def premultiplied_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    premultiplied = np.concatenate((rgba[:, :, :3] * alpha, rgba[:, :, 3:4]), axis=2)
    channels = [
        np.asarray(
            Image.fromarray(
                np.clip(premultiplied[:, :, channel], 0, 255).astype(np.uint8)
            ).resize(size, Image.Resampling.LANCZOS),
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
        np.concatenate((np.clip(rgb, 0, 255), resized_alpha), axis=2).astype(np.uint8),
        "RGBA",
    )


def prepare(source: Path, target: Path, size: int, padding: float) -> None:
    rgb = np.asarray(Image.open(source).convert("RGB"))
    background = edge_connected_checkerboard(rgb)
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
        image,
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
    )
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = ((size - resized.width) // 2, (size - resized.height) // 2)
    canvas.alpha_composite(resized, offset)
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    for source_name, (target_name, size, padding) in FILES.items():
        source = args.source_dir / source_name
        target = args.output_dir / target_name
        prepare(source, target, size, padding)
        print({"source": str(source), "target": str(target), "size": size})


if __name__ == "__main__":
    main()
