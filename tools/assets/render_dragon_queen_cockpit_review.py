"""Render Dragon Queen cockpit-placement evidence with runtime transforms."""

import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import build_dragon_queen_sovereign_wyrm as sovereign


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(
    os.environ.get(
        "DRAGON_QUEEN_COCKPIT_REVIEW",
        ROOT / "candidates/dragon-queen-cockpit-review.png",
    )
)
DRIVER_ROOT = ROOT / "public/assets/characters/aa-06/driver"
SPRITE_POSITION = np.array([0.0, 0.95, -0.12])
SPRITE_SIZE = 1.45


def runtime_geometry(parts):
    raw = []
    bounds = []
    light = np.array([-0.45, 0.85, -0.30])
    light /= np.linalg.norm(light)
    for name, primitives in parts.items():
        translation = np.asarray(sovereign.TRANSLATIONS[name])
        for geo, _material in primitives:
            positions, _normals, colors, indices = geo.arrays()
            positions = positions + translation
            bounds.append(positions)
            for ids in indices.reshape(-1, 3):
                triangle = positions[ids]
                normal = np.cross(triangle[1] - triangle[0], triangle[2] - triangle[0])
                length = np.linalg.norm(normal)
                if length < 1e-9:
                    continue
                normal /= length
                shade = 0.62 + 0.38 * max(0, float(np.dot(normal, light)))
                color = colors[ids].mean(axis=0).copy()
                color[:3] = np.clip(color[:3] * shade + 0.035, 0, 1)
                raw.append((triangle, color))

    all_positions = np.concatenate(bounds)
    size = all_positions.max(axis=0) - all_positions.min(axis=0)
    scale = 2.9 / max(size[0], size[2], 0.001)
    ground_offset = -(all_positions[:, 1].min() * scale) - 0.42

    triangles = []
    colors = []
    for triangle, color in raw:
        transformed = triangle.copy()
        transformed[:, 0] *= -scale
        transformed[:, 1] = transformed[:, 1] * scale + ground_offset
        transformed[:, 2] *= -scale
        triangles.append(transformed[:, [0, 2, 1]])
        colors.append(color)
    return triangles, colors, scale, ground_offset


def sprite_faces(path):
    image = Image.open(path).convert("RGBA")
    image.thumbnail((96, 96), Image.Resampling.LANCZOS)
    pixels = np.asarray(image, dtype=np.float32) / 255.0
    height, width = pixels.shape[:2]
    pixel_width = SPRITE_SIZE / width
    pixel_height = SPRITE_SIZE / height
    left = SPRITE_POSITION[0] - SPRITE_SIZE / 2
    top = SPRITE_POSITION[1] + SPRITE_SIZE / 2
    z = SPRITE_POSITION[2]
    faces = []
    colors = []
    for row in range(height):
        upper = top - row * pixel_height
        lower = upper - pixel_height
        for column in range(width):
            color = pixels[row, column]
            if color[3] < 0.04:
                continue
            x0 = left + column * pixel_width
            x1 = x0 + pixel_width
            faces.append(
                np.array(
                    [
                        [x0, z, lower],
                        [x1, z, lower],
                        [x1, z, upper],
                        [x0, z, upper],
                    ]
                )
            )
            colors.append(color)
    return faces, colors


def main():
    parts = sovereign.build_geometry()
    kart_triangles, kart_colors, scale, ground_offset = runtime_geometry(parts)
    views = [
        ("rear.png", 12, -90, "Chase camera: rear"),
        ("steer-left.png", 12, -90, "Chase camera: steer left"),
        ("front.png", 12, 90, "Front camera: neutral"),
        ("front-steer-right.png", 12, 90, "Front camera: steer right"),
    ]

    fig = plt.figure(figsize=(14, 10), dpi=150, facecolor="#080b19")
    for index, (filename, elevation, azimuth, title) in enumerate(views, 1):
        sprite_triangles, sprite_colors = sprite_faces(DRIVER_ROOT / filename)
        ax = fig.add_subplot(2, 2, index, projection="3d", computed_zorder=False)
        ax.set_facecolor("#080b19")
        ax.add_collection3d(
            Poly3DCollection(
                [*kart_triangles, *sprite_triangles],
                facecolors=[*kart_colors, *sprite_colors],
                edgecolor=(0, 0, 0, 0.08),
                linewidth=0.06,
            )
        )
        ax.set_xlim(-1.65, 1.65)
        ax.set_ylim(-1.65, 1.65)
        ax.set_zlim(-0.15, 1.80)
        ax.set_box_aspect((3.3, 3.3, 1.95))
        ax.view_init(elevation, azimuth)
        ax.set_axis_off()
        ax.set_title(title, color="#f1d38a", fontsize=14, pad=2)

    fig.suptitle(
        "DRAGON QUEEN + THE SOVEREIGN WYRM | LOCAL COCKPIT PLACEMENT",
        color="#e6b64c",
        fontsize=18,
        fontweight="bold",
        y=0.98,
    )
    fig.text(
        0.5,
        0.018,
        (
            f"Runtime model scale {scale:.4f} | ground offset {ground_offset:.4f} | "
            "driver position [0, 0.95, -0.12] | sprite size 1.45"
        ),
        ha="center",
        color="#b9c7e9",
        fontsize=10,
    )
    plt.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.05, wspace=0.01, hspace=0.05)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(OUTPUT)


if __name__ == "__main__":
    main()
