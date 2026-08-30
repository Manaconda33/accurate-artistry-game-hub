#!/usr/bin/env python3
"""Normalize Lula chase-camera skin to the approved portrait/front palette."""

from __future__ import annotations

import argparse
import colorsys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
DRIVER_DIR = ROOT / "public/assets/characters/aa-03/driver"

# Deliberately tight regions around exposed skin. Color qualification below keeps
# bracers, clothing, hair, and dark linework out of the final masks.
REGIONS: dict[str, tuple[tuple[int, int, int, int], ...]] = {
    "rear.png": (
        (170, 55, 215, 132),
        (298, 55, 345, 132),
        (104, 138, 181, 286),
        (329, 138, 406, 286),
    ),
    "steer-left.png": (
        (174, 54, 236, 166),
        (114, 178, 231, 312),
    ),
    "steer-right.png": (
        (269, 54, 331, 171),
        (319, 173, 416, 302),
    ),
    "hit.png": (
        (88, 72, 181, 177),
        (23, 96, 147, 313),
        (363, 0, 477, 208),
    ),
    "victory.png": (
        (194, 38, 352, 228),
        (133, 98, 252, 302),
    ),
}


def rgb_to_hsv(rgb: np.ndarray) -> np.ndarray:
    flat = rgb.reshape(-1, 3) / 255.0
    return np.asarray([colorsys.rgb_to_hsv(*pixel) for pixel in flat]).reshape(
        *rgb.shape[:2], 3
    )


def skin_mask(pixels: np.ndarray, regions: tuple[tuple[int, int, int, int], ...]) -> np.ndarray:
    region_mask = np.zeros(pixels.shape[:2], dtype=bool)
    for x0, y0, x1, y1 in regions:
        region_mask[y0:y1, x0:x1] = True

    rgb = pixels[:, :, :3]
    hsv = rgb_to_hsv(rgb)
    red = rgb[:, :, 0].astype(float)
    green = rgb[:, :, 1].astype(float)
    blue = rgb[:, :, 2].astype(float)
    hue = hsv[:, :, 0] * 360.0
    already_normalized = (np.abs(hue - 28.5) <= 2.0) & (hsv[:, :, 1] <= 0.55)

    return (
        region_mask
        & (pixels[:, :, 3] > 0)
        & (hue < 50.0)
        & (hsv[:, :, 1] > 0.25)
        & (hsv[:, :, 2] > 0.28)
        & (red > green * 1.15)
        & (green > blue * 1.05)
        & ~already_normalized
    )


def normalize_skin(pixels: np.ndarray, mask: np.ndarray) -> np.ndarray:
    result = pixels.copy()
    hsv = rgb_to_hsv(pixels[:, :, :3])

    # Authority: the approved portrait/front sprites. Preserve each source
    # pixel's value/shading while moving hue and saturation into that palette.
    source_sat = hsv[:, :, 1]
    target_hue = 28.5 / 360.0
    target_sat = np.clip(0.40 + (source_sat - np.median(source_sat[mask])) * 0.18, 0.30, 0.52)
    target_val = np.clip(hsv[:, :, 2] * 1.06 + 0.025, 0.0, 0.96)

    ys, xs = np.nonzero(mask)
    for y, x in zip(ys, xs, strict=True):
        red, green, blue = colorsys.hsv_to_rgb(target_hue, target_sat[y, x], target_val[y, x])
        result[y, x, :3] = np.rint(np.asarray((red, green, blue)) * 255).astype(np.uint8)
    return result


def write_preview(image: Image.Image, mask: np.ndarray, destination: Path) -> None:
    preview = image.convert("RGBA")
    overlay = Image.new("RGBA", preview.size, (0, 0, 0, 0))
    overlay_pixels = np.zeros((*mask.shape, 4), dtype=np.uint8)
    overlay_pixels[mask] = (0, 255, 255, 185)
    overlay = Image.fromarray(overlay_pixels, "RGBA")
    preview = Image.alpha_composite(preview, overlay)
    draw = ImageDraw.Draw(preview)
    draw.text((8, 8), destination.stem, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
    preview.save(destination)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write corrected sprites in place")
    parser.add_argument("--preview-dir", type=Path, help="write cyan mask previews")
    args = parser.parse_args()

    if not args.apply and args.preview_dir is None:
        parser.error("choose --apply and/or --preview-dir")

    if args.preview_dir:
        args.preview_dir.mkdir(parents=True, exist_ok=True)

    for filename, regions in REGIONS.items():
        path = DRIVER_DIR / filename
        image = Image.open(path).convert("RGBA")
        pixels = np.asarray(image).copy()
        mask = skin_mask(pixels, regions)
        if not mask.any():
            print(f"{filename}: already normalized")
            continue

        if args.preview_dir:
            write_preview(image, mask, args.preview_dir / filename)

        if args.apply:
            corrected = normalize_skin(pixels, mask)
            Image.fromarray(corrected, "RGBA").save(path, optimize=True)

        print(f"{filename}: {int(mask.sum())} skin pixels")


if __name__ == "__main__":
    main()
