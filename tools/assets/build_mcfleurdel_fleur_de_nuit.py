"""Build deterministic Fleur de Nuit GLBs and a review sheet."""

import math
import os
from pathlib import Path

import numpy as np

import build_manaconda_wayfinder as base
import build_keeg_mycelial_majesty as shared


ROOT = Path(__file__).resolve().parent
LOD = os.environ.get("FLEUR_DE_NUIT_LOD", "LOD0").upper()
DETAILS = {
    "LOD0": {"round": 16, "tube": 8},
    "LOD1": {"round": 12, "tube": 6},
    "LOD2": {"round": 6, "tube": 3},
}
if LOD not in DETAILS:
    raise ValueError(f"Unknown FLEUR_DE_NUIT_LOD: {LOD}")
DETAIL = DETAILS[LOD]
OUT = Path(os.environ.get("FLEUR_DE_NUIT_OUT", ROOT / "candidates/fleur-de-nuit-candidate-9.glb"))
PREVIEW = Path(os.environ.get("FLEUR_DE_NUIT_PREVIEW", ROOT / "candidates/fleur-de-nuit-candidate-9-preview.png"))

BLACK = np.array([0.035, 0.026, 0.052, 1.0], np.float32)
LACQUER = np.array([0.13, 0.075, 0.16, 1.0], np.float32)
BODY_DARK = np.array([0.78, 0.72, 0.84, 1.0], np.float32)
BODY_LIGHT = np.array([0.96, 0.84, 1.0, 1.0], np.float32)
SILVER = np.array([0.70, 0.74, 0.82, 1.0], np.float32)
PLUM = np.array([0.32, 0.025, 0.18, 1.0], np.float32)
VIOLET = np.array([0.68, 0.12, 0.92, 1.0], np.float32)
TIRE = np.array([0.012, 0.010, 0.017, 1.0], np.float32)
WAX = np.array([0.88, 0.79, 0.67, 1.0], np.float32)


def ell(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.ellipsoid(size, DETAIL["round"], max(5, DETAIL["round"] // 2), color), at, rotation))


def box(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.box(size, color), at, rotation))


def cyl(geo, radius, length, at, axis, color, rotation=None):
    geo.add(base.transform(base.cylinder(radius, length, DETAIL["round"], axis, color), at, rotation))


def rot_z(angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def fleur(geo, at, scale, color, vertical=False):
    x, y, z = at
    # Central blade and paired lobes form a readable, structural fleur-de-lis.
    box(geo, (0.16 * scale, 0.08 * scale, 0.74 * scale), (x, y, z), color)
    ell(geo, (0.30 * scale, 0.10 * scale, 0.42 * scale),
        (x - 0.23 * scale, y, z + 0.02 * scale), color, base.rot_y(-0.55))
    ell(geo, (0.30 * scale, 0.10 * scale, 0.42 * scale),
        (x + 0.23 * scale, y, z + 0.02 * scale), color, base.rot_y(0.55))
    ell(geo, (0.20 * scale, 0.10 * scale, 0.42 * scale),
        (x, y + (0.04 if vertical else 0), z - 0.28 * scale), color)


def fleur_nose(geo, at, scale, color):
    """Raised fleur-de-lis in the vertical XY plane of the -Z nose."""
    x, y, z = at
    box(geo, (0.16 * scale, 0.78 * scale, 0.10 * scale), (x, y, z), color)
    ell(geo, (0.34 * scale, 0.46 * scale, 0.12 * scale),
        (x - 0.24 * scale, y + 0.04 * scale, z), color, rot_z(0.52))
    ell(geo, (0.34 * scale, 0.46 * scale, 0.12 * scale),
        (x + 0.24 * scale, y + 0.04 * scale, z), color, rot_z(-0.52))
    ell(geo, (0.23 * scale, 0.43 * scale, 0.12 * scale),
        (x, y + 0.35 * scale, z), color)
    box(geo, (0.66 * scale, 0.11 * scale, 0.12 * scale),
        (x, y - 0.18 * scale, z), color)


def build_geometry():
    parts = {}
    chassis, cockpit = base.Geo(), base.Geo()
    # Material 0 carries the actual black lacquer so viewers that ignore
    # COLOR_0 still render the chassis correctly.
    ell(chassis, (2.28, 0.52, 3.72), (0, 0.56, 0.02), BODY_DARK)
    ell(chassis, (2.18, 0.52, 3.38), (0, 0.78, -0.10), BODY_LIGHT)
    ell(chassis, (2.04, 0.50, 1.52), (0, 0.86, -1.50), BODY_DARK)
    ell(chassis, (1.55, 0.60, 0.80), (0, 1.10, -1.72), BODY_LIGHT)
    ell(chassis, (2.04, 0.46, 1.12), (0, 0.84, 1.38), BODY_DARK)
    # Plum upholstered throne is recessed within a silver cockpit surround.
    ell(cockpit, (1.24, 0.18, 1.15), (0, 1.23, 0.22), PLUM)
    ell(cockpit, (1.12, 0.58, 0.28), (0, 1.55, 0.76), PLUM)
    ell(cockpit, (1.42, 0.36, 0.22), (0, 1.38, 0.88), SILVER)
    for x in (-0.76, 0.76):
        ell(cockpit, (0.22, 0.40, 1.25), (x, 1.25, 0.12), SILVER)
        ell(cockpit, (0.14, 0.30, 1.12), (x, 1.30, 0.10), BLACK)
    parts["Chassis"] = [(chassis, 0), (cockpit, 2)]

    accent, glow, shield = base.Geo(), base.Geo(), base.Geo()
    # Attached lower blades and side scrollwork frame the lacquer body.
    # Thin attached silver edge blades leave the black lacquer shell dominant.
    box(accent, (2.18, 0.10, 0.12), (0, 0.43, -1.58), SILVER)
    box(accent, (2.18, 0.10, 0.12), (0, 0.43, 1.46), SILVER)
    for x in (-1.08, 1.08):
        ell(accent, (0.13, 0.17, 2.66), (x, 0.90, -0.06), SILVER)
        for z in (-0.84, 0.02, 0.88):
            accent.add(base.transform(base.torus(0.19, 0.038, DETAIL["round"], DETAIL["tube"], "y", SILVER),
                                      (x, 1.01, z), base.rot_x(math.pi / 2)))
    for x in (-1.12, 1.12):
        for z in (-1.08, 1.12):
            ell(accent, (0.42, 0.22, 0.82), (x, 0.91, z), LACQUER)
            ell(accent, (0.27, 0.11, 0.68), (x, 1.04, z), SILVER)
    # Layered nose shield points toward canonical -Z.
    ell(shield, (1.44, 0.72, 0.24), (0, 0.94, -2.02), BLACK)
    ell(shield, (1.18, 0.58, 0.20), (0, 0.96, -2.17), BLACK)
    fleur_nose(accent, (0, 1.00, -2.36), 0.82, SILVER)
    # Four candle housings grow from the body; wax and flame never float.
    wax = base.Geo()
    for index, (x, z) in enumerate(((-1.03, -1.22), (1.03, -1.22), (-1.02, 0.94), (1.02, 0.94))):
        ell(accent, (0.31, 0.15, 0.34), (x, 1.05, z), SILVER)
        height = 0.32 if index % 2 == 0 else 0.39
        cyl(wax, 0.12, height, (x, 1.20 + height / 2, z), "y", WAX)
        ell(wax, (0.28, 0.07, 0.28), (x, 1.22 + height, z), WAX)
        # Uneven attached wax drips break the lipstick silhouette.
        for dx, drop in ((-0.07, 0.15), (0.045, 0.10)):
            cyl(wax, 0.026, drop, (x + dx, 1.20 + height - drop / 2, z + 0.09), "y", WAX)
        ell(glow, (0.15, 0.32, 0.11), (x, 1.34 + height, z), VIOLET)
        ell(glow, (0.07, 0.19, 0.06), (x, 1.47 + height, z), VIOLET)
    parts["AccentMesh"] = [(accent, 1), (glow, 3), (wax, 5), (shield, 4)]

    steering = base.Geo()
    tilt = math.radians(17)
    steering.add(base.transform(base.torus(0.36, 0.050, DETAIL["round"], DETAIL["tube"], "y", BLACK),
                                rotation=base.rot_x(math.pi / 2 + tilt)))
    for angle in (0, math.pi * 2 / 3, math.pi * 4 / 3):
        steering.add(base.transform(base.box((0.54, 0.045, 0.045), SILVER),
                                    rotation=base.rot_x(tilt) @ np.array([[math.cos(angle), -math.sin(angle), 0], [math.sin(angle), math.cos(angle), 0], [0, 0, 1]])))
    cyl(steering, 0.06, 0.86, (0, -0.30, -0.30), "z", SILVER, base.rot_x(math.radians(135)))
    cyl(steering, 0.12, 0.20, (0, -0.59, -0.59), "z", PLUM, base.rot_x(math.radians(135)))
    parts["SteeringWheel"] = [(steering, 1)]

    for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"):
        tire, hub = base.Geo(), base.Geo()
        tire.add(base.torus(0.48, 0.17, DETAIL["round"], DETAIL["tube"], "x", TIRE))
        tire.add(base.torus(0.30, 0.055, DETAIL["round"], DETAIL["tube"], "x", SILVER))
        cyl(hub, 0.23, 0.34, (0, 0, 0), "x", PLUM)
        fleur(hub, (0, 0, -0.17), 0.28, SILVER)
        parts[name] = [(tire, 4), (hub, 1)]

    for name in ("Exhaust_L", "Exhaust_R"):
        metal, flame = base.Geo(), base.Geo()
        cyl(metal, 0.17, 0.62, (0, 0, 0), "z", SILVER, base.rot_x(-0.12))
        ell(flame, (0.18, 0.18, 0.48), (0, 0, 0.50), VIOLET)
        parts[name] = [(metal, 1), (flame, 3)]
    return parts


TRANSLATIONS = {
    "Chassis": (0, 0, 0), "AccentMesh": (0, 0, 0),
    "SteeringWheel": (0, 1.71, -0.45),
    "Wheel_FL": (-1.40, 0.52, -1.08), "Wheel_FR": (1.40, 0.52, -1.08),
    "Wheel_RL": (-1.40, 0.52, 1.12), "Wheel_RR": (1.40, 0.52, 1.12),
    "Exhaust_L": (-0.62, 0.82, 1.68), "Exhaust_R": (0.62, 0.82, 1.68),
    "DriverMount": (0, 1.54, 0.22), "ItemMountRear": (0, 1.18, 2.00),
    "ItemMountForward": (0, 0.92, -2.20),
}

MATERIALS = [
    {"name": "BlackLacquer", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.055, 0.035, 0.075, 1], "metallicFactor": 0.22, "roughnessFactor": 0.34}},
    {"name": "SilverFiligree", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.70, 0.74, 0.82, 1], "metallicFactor": 0.78, "roughnessFactor": 0.22}},
    {"name": "PlumUpholstery", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.32, 0.025, 0.18, 1], "metallicFactor": 0.08, "roughnessFactor": 0.62}},
    {"name": "VioletFlame", "alphaMode": "OPAQUE", "doubleSided": True, "emissiveFactor": [0.58, 0.06, 0.82], "pbrMetallicRoughness": {"baseColorFactor": [0.68, 0.12, 0.92, 1], "metallicFactor": 0.08, "roughnessFactor": 0.20}},
    {"name": "Tire", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.012, 0.010, 0.017, 1], "metallicFactor": 0.02, "roughnessFactor": 0.92}},
    {"name": "AgedIvoryWax", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.88, 0.79, 0.67, 1], "metallicFactor": 0.0, "roughnessFactor": 0.88}},
]


def main():
    shared.LOD = LOD
    shared.OUT = OUT
    shared.PREVIEW = PREVIEW
    shared.TRANSLATIONS = TRANSLATIONS
    dummy_material = {"name": "UnusedViewerCompatibilitySlot", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.0, "roughnessFactor": 1.0}}
    shared.MATERIALS = [dummy_material, *MATERIALS]
    shared.APPROVED_NAME = "The Fleur de Nuit"
    shared.GENERATOR = "Minigame Mayhem procedural Fleur de Nuit builder"
    shared.PREVIEW_TITLE = "THE FLEUR DE NUIT"
    shared.CANDIDATE = "9"
    shared.USE_VERTEX_COLORS = False
    shared.MATERIAL_TEXTURE_RGBA = [(255, 255, 255, 255), (14, 9, 19, 255), (178, 189, 209, 255), (82, 6, 46, 255), (173, 31, 235, 255), (3, 3, 4, 255), (224, 201, 171, 255)]
    shared.PREVIEW_MATERIAL_RGBA = shared.MATERIAL_TEXTURE_RGBA
    shared.PREVIEW_VIEWS = ["Front three-quarter • fleur-de-lis shield at -Z", "Rear three-quarter • integrated violet exhausts", "Top • plum throne cockpit and attached filigree", "Left profile • low gothic grand-tourer stance"]
    shared.PREVIEW_FOOTER = "Black lacquer roadster • attached silver filigree • plum throne cockpit • integrated violet candle fixtures • fleur-de-lis shield"
    parts = build_geometry()
    # Use the exact tire-black material for the body shell. Samsung's viewer
    # has already proven this material renders black under its environment.
    parts = {name: [(geo, 5 if name == "Chassis" and material == 0 else material + 1)
                    for geo, material in primitives]
             for name, primitives in parts.items()}
    shared.export_glb(parts)
    if os.environ.get("FLEUR_DE_NUIT_SKIP_PREVIEW") != "1":
        shared.preview(parts)


if __name__ == "__main__":
    main()
