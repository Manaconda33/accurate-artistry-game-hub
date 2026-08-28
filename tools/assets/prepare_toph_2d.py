#!/usr/bin/env python3
"""Prepare approved Toph art as deterministic transparent runtime PNGs."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


def connected_checkerboard_mask(rgb: np.ndarray) -> np.ndarray:
    """Return light neutral pixels connected to an image edge."""
    maximum = rgb.max(axis=2)
    minimum = rgb.min(axis=2)
    candidate = (minimum >= 214) & ((maximum - minimum) <= 18)
    height, width = candidate.shape
    background = np.zeros_like(candidate)
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        if candidate[0, x]:
            queue.append((0, x))
        if candidate[height - 1, x]:
            queue.append((height - 1, x))
    for y in range(height):
        if candidate[y, 0]:
            queue.append((y, 0))
        if candidate[y, width - 1]:
            queue.append((y, width - 1))

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
    return background


def prepare(source: Path, target: Path, size: int, padding: float) -> None:
    source_image = Image.open(source).convert("RGB")
    rgb = np.asarray(source_image)
    background = connected_checkerboard_mask(rgb)
    alpha = np.where(background, 0, 255).astype(np.uint8)
    rgba = np.dstack((rgb, alpha))
    image = Image.fromarray(rgba, "RGBA")

    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"No foreground found in {source}")
    image = image.crop(bbox)
    usable = max(1, round(size * (1 - 2 * padding)))
    image.thumbnail((usable, usable), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = ((size - image.width) // 2, (size - image.height) // 2)
    canvas.alpha_composite(image, offset)
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    files = {
        "portrait.png": ("portrait.png", 256, 0.035),
        "front.png": ("front.png", 512, 0.025),
        "rear.png": ("rear.png", 512, 0.025),
        "steer-left.png": ("steer-left.png", 512, 0.025),
        "steer-right.png": ("steer-right.png", 512, 0.025),
        "hit.png": ("hit.png", 512, 0.025),
        "victory.png": ("victory.png", 512, 0.025),
    }
    for output_name, (source_name, size, padding) in files.items():
        target = args.output_dir / ("portrait.png" if output_name == "portrait.png" else f"driver/{output_name}")
        prepare(args.source_dir / source_name, target, size, padding)


if __name__ == "__main__":
    main()
