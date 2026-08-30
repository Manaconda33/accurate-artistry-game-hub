#!/usr/bin/env python3
"""Remove residual generated white background from approved Lula runtime PNGs.

The original cleanup removed only light-neutral pixels connected directly to an
image edge. Antialiased color bands enclosed parts of that background, leaving
opaque white islands and ribbons. This repair classifies connected neutral
components against the existing alpha boundary and removes large enclosed
components while preserving small isolated highlights such as eyes.
"""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


FILES = (
    "portrait.png",
    "driver/front.png",
    "driver/rear.png",
    "driver/steer-left.png",
    "driver/steer-right.png",
    "driver/hit.png",
    "driver/victory.png",
)

# Only these small face regions may contain intentional neutral highlights.
# Everything else in Lula's approved green/brown package is background spill.
PROTECTED_RECTS = {
    "portrait.png": (82, 66, 180, 170),
    "driver/front.png": (205, 55, 310, 185),
    "driver/victory.png": (300, 82, 400, 205),
}


def neighboring(mask: np.ndarray) -> np.ndarray:
    expanded = mask.copy()
    expanded[1:] |= mask[:-1]
    expanded[:-1] |= mask[1:]
    expanded[:, 1:] |= mask[:, :-1]
    expanded[:, :-1] |= mask[:, 1:]
    return expanded


def background_components(
    rgb: np.ndarray, alpha: np.ndarray, protected_rect: tuple[int, int, int, int] | None
) -> np.ndarray:
    maximum = rgb.max(axis=2)
    minimum = rgb.min(axis=2)
    neutral = (minimum >= 165) & ((maximum - minimum) <= 65) & (alpha > 0)
    transparent_neighbor = neighboring(alpha == 0)
    height, width = neutral.shape
    visited = np.zeros_like(neutral)
    remove = np.zeros_like(neutral)

    for start_y, start_x in zip(*np.where(neutral)):
        if visited[start_y, start_x]:
            continue
        queue: deque[tuple[int, int]] = deque([(int(start_y), int(start_x))])
        visited[start_y, start_x] = True
        component: list[tuple[int, int]] = []
        touches_transparency = False

        while queue:
            y, x = queue.popleft()
            component.append((y, x))
            touches_transparency |= bool(transparent_neighbor[y, x])
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                next_y, next_x = y + dy, x + dx
                if (
                    0 <= next_y < height
                    and 0 <= next_x < width
                    and neutral[next_y, next_x]
                    and not visited[next_y, next_x]
                ):
                    visited[next_y, next_x] = True
                    queue.append((next_y, next_x))

        # Lula's palette contains no white costume detail. All neutral
        # components outside the explicit face protection zones are background.
        for y, x in component:
            protected = False
            if protected_rect is not None:
                left, top, right, bottom = protected_rect
                protected = left <= x < right and top <= y < bottom
            if not protected and (touches_transparency or len(component) >= 1):
                remove[y, x] = True

    # Remove two pixels of pale antialias spill only where it borders confirmed
    # background. Strongly colored hair, skin, and clothing are unaffected.
    for _ in range(2):
        edge = neighboring(remove) & ~remove & (alpha > 0)
        spill = edge & (minimum >= 150) & ((maximum - minimum) <= 100)
        if not spill.any():
            break
        remove |= spill
    return remove


def repair(path: Path, relative: str) -> tuple[int, int]:
    image = Image.open(path).convert("RGBA")
    rgba = np.array(image)
    remove = background_components(
        rgba[:, :, :3], rgba[:, :, 3], PROTECTED_RECTS.get(relative)
    )
    before = int((rgba[:, :, 3] > 0).sum())
    rgba[remove, 3] = 0
    rgba[remove, :3] = 0
    Image.fromarray(rgba, "RGBA").save(path, format="PNG", optimize=True)
    after = int((rgba[:, :, 3] > 0).sum())
    return before - after, after


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset-dir", required=True, type=Path)
    args = parser.parse_args()
    for relative in FILES:
        path = args.asset_dir / relative
        removed, remaining = repair(path, relative)
        print({"path": str(path), "removed": removed, "foreground": remaining})


if __name__ == "__main__":
    main()
