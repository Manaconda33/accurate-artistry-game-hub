"""Build deterministic Grave Shift GLBs and review sheets for Toph."""

import math
import os
from pathlib import Path

import numpy as np

import build_manaconda_wayfinder as base
import build_keeg_mycelial_majesty as shared

ROOT = Path(__file__).resolve().parent
LOD = os.environ.get("GRAVE_SHIFT_LOD", "LOD0").upper()
DETAILS = {"LOD0": {"round": 18, "tube": 8}, "LOD1": {"round": 12, "tube": 6}, "LOD2": {"round": 7, "tube": 4}}
if LOD not in DETAILS:
    raise ValueError(f"Unknown GRAVE_SHIFT_LOD: {LOD}")
DETAIL = DETAILS[LOD]
OUT = Path(os.environ.get("GRAVE_SHIFT_OUT", ROOT / "candidates/grave-shift-candidate-2.glb"))
PREVIEW = Path(os.environ.get("GRAVE_SHIFT_PREVIEW", ROOT / "candidates/grave-shift-candidate-2-preview.png"))

BLACK = np.array([0.018, 0.016, 0.024, 1.0], np.float32)
PURPLE = np.array([0.25, 0.035, 0.46, 1.0], np.float32)
PURPLE_LIT = np.array([0.52, 0.10, 0.78, 1.0], np.float32)
BRONZE = np.array([0.34, 0.18, 0.07, 1.0], np.float32)
BRONZE_LIT = np.array([0.62, 0.35, 0.12, 1.0], np.float32)
BONE = np.array([0.70, 0.66, 0.76, 1.0], np.float32)
TIRE = np.array([0.012, 0.011, 0.015, 1.0], np.float32)
GLOW = np.array([0.68, 0.11, 1.0, 1.0], np.float32)
AMBER = np.array([1.0, 0.48, 0.06, 1.0], np.float32)

def ell(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.ellipsoid(size, DETAIL["round"], max(5, DETAIL["round"] // 2), color), at, rotation))

def box(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.box(size, color), at, rotation))

def cyl(geo, radius, length, at, axis, color, rotation=None):
    geo.add(base.transform(base.cylinder(radius, length, DETAIL["round"], axis, color), at, rotation))

def prism(geo, polygon, z_center, depth, color):
    """Extrude an XY polygon into a shallow relief plate."""
    count = len(polygon)
    front_z, back_z = z_center - depth / 2, z_center + depth / 2
    positions, normals, indices = [], [], []
    # Front and back triangle fans.
    for z, normal, reverse in ((front_z, (0, 0, -1), False), (back_z, (0, 0, 1), True)):
        start = len(positions)
        positions.extend([[x, y, z] for x, y in polygon])
        normals.extend([normal] * count)
        for index in range(1, count - 1):
            tri = [start, start + index, start + index + 1]
            indices.extend(reversed(tri) if reverse else tri)
    # Side quads.
    for index in range(count):
        nxt = (index + 1) % count
        x1, y1 = polygon[index]
        x2, y2 = polygon[nxt]
        edge = np.array([x2 - x1, y2 - y1, 0.0])
        normal = np.array([edge[1], -edge[0], 0.0])
        normal /= max(np.linalg.norm(normal), 1e-9)
        start = len(positions)
        positions.extend([[x1, y1, front_z], [x2, y2, front_z], [x2, y2, back_z], [x1, y1, back_z]])
        normals.extend([normal.tolist()] * 4)
        indices.extend([start, start + 1, start + 2, start, start + 2, start + 3])
    geo.add((positions, normals, color, indices))

def build_geometry():
    parts = {}
    chassis, cockpit = base.Geo(), base.Geo()
    # Cohesive low armored body with purple as the dominant surface.
    box(chassis, (2.28, 0.30, 3.46), (0, 0.55, 0.04), BLACK)
    ell(chassis, (2.18, 0.48, 3.12), (0, 0.78, -0.02), PURPLE)
    box(chassis, (2.38, 0.18, 0.44), (0, 0.50, -1.66), BRONZE)
    box(chassis, (2.16, 0.13, 0.28), (0, 0.49, -1.86), BLACK)
    # Integrated sidepods replace the exposed tubular-cart silhouette.
    for x in (-0.94, 0.94):
        ell(chassis, (0.58, 0.46, 2.54), (x, 0.80, -0.02), PURPLE)
        box(chassis, (0.14, 0.18, 2.30), (x + (-0.29 if x < 0 else 0.29), 0.70, -0.02), BRONZE)
    # Cockpit is open, recessed, and bounded by deliberate armor.
    ell(cockpit, (1.20, 0.16, 1.18), (0, 1.09, 0.28), BLACK)
    ell(cockpit, (0.94, 0.30, 0.64), (0, 1.18, 0.48), BLACK)
    ell(cockpit, (1.42, 0.34, 0.28), (0, 1.24, 0.90), PURPLE)
    for x in (-0.72, 0.72):
        ell(cockpit, (0.24, 0.36, 1.18), (x, 1.12, 0.24), BRONZE)
        ell(cockpit, (0.15, 0.28, 1.05), (x, 1.17, 0.22), PURPLE)
    parts["Chassis"] = [(chassis, 1), (cockpit, 0)]

    accent, emblem, glow = base.Geo(), base.Geo(), base.Geo()
    # Axles remain structurally connected but mostly tucked beneath the armor.
    for z in (-1.05, 1.10):
        cyl(accent, 0.105, 2.84, (0, 0.53, z), "x", BRONZE)
    # Bronze perimeter rails are integrated into the sidepods.
    for x in (-1.15, 1.15):
        box(accent, (0.10, 0.13, 2.74), (x, 0.72, -0.02), BRONZE_LIT)
    # Enclosed rear engine housing and flanking armor.
    box(accent, (1.78, 0.68, 0.88), (0, 0.93, 1.42), BRONZE)
    box(accent, (1.54, 0.54, 0.78), (0, 0.96, 1.48), BLACK)
    box(accent, (1.30, 0.40, 0.84), (0, 1.02, 1.52), PURPLE)
    for x in (-0.86, 0.86):
        ell(accent, (0.46, 0.52, 0.82), (x, 0.92, 1.40), PURPLE)
        box(accent, (0.12, 0.42, 0.76), (x + (-0.22 if x < 0 else 0.22), 0.92, 1.40), BRONZE)

    # Single tall trapezoidal nose shield: bronze border, purple face, black inset.
    outer = [(-0.82, 0.54), (0.82, 0.54), (0.70, 1.58), (0.42, 1.84), (-0.42, 1.84), (-0.70, 1.58)]
    inner = [(-0.67, 0.64), (0.67, 0.64), (0.57, 1.49), (0.34, 1.69), (-0.34, 1.69), (-0.57, 1.49)]
    inset = [(-0.58, 0.71), (0.58, 0.71), (0.49, 1.43), (0.29, 1.59), (-0.29, 1.59), (-0.49, 1.43)]
    prism(emblem, outer, -1.94, 0.16, BRONZE_LIT)
    prism(emblem, inner, -2.04, 0.13, PURPLE)
    prism(emblem, inset, -2.12, 0.08, PURPLE_LIT)

    # Angular thorn crown is rooted into the shield and shares its purple language.
    thorn_polys = [
        [(-0.56, 1.54), (-0.46, 1.72), (-0.70, 2.10), (-0.34, 1.77)],
        [(-0.30, 1.67), (-0.13, 1.75), (-0.18, 2.24), (0.03, 1.76)],
        [(0.03, 1.76), (0.18, 2.24), (0.13, 1.75), (0.30, 1.67)],
        [(0.34, 1.77), (0.70, 2.10), (0.46, 1.72), (0.56, 1.54)],
    ]
    for polygon in thorn_polys:
        prism(emblem, polygon, -2.14, 0.10, PURPLE_LIT)

    # Flat, graphic skull relief—angular eyes and jagged jaw, never a 3D face.
    skull = [(-0.34, 1.42), (-0.47, 1.29), (-0.43, 1.04), (-0.28, 0.92),
             (-0.24, 0.73), (-0.10, 0.62), (0.0, 0.70), (0.10, 0.62),
             (0.24, 0.73), (0.28, 0.92), (0.43, 1.04), (0.47, 1.29), (0.34, 1.42)]
    prism(emblem, skull, -2.19, 0.055, BONE)
    prism(emblem, [(-0.31, 1.24), (-0.08, 1.17), (-0.16, 1.03), (-0.36, 1.10)], -2.23, 0.035, BLACK)
    prism(emblem, [(0.08, 1.17), (0.31, 1.24), (0.36, 1.10), (0.16, 1.03)], -2.23, 0.035, BLACK)
    prism(emblem, [(-0.06, 0.97), (0.0, 1.08), (0.06, 0.97), (0.0, 0.89)], -2.23, 0.035, BLACK)
    for x in (-0.15, -0.05, 0.05, 0.15):
        box(emblem, (0.055, 0.13, 0.035), (x, 0.75, -2.24), BLACK)

    # Low amber lamps belong to the splitter, away from the emblem's face.
    for x in (-0.91, 0.91):
        box(glow, (0.30, 0.16, 0.08), (x, 0.57, -1.92), AMBER)
    parts["AccentMesh"] = [(accent, 2), (emblem, 4), (glow, 3)]

    steering = base.Geo()
    tilt = math.radians(24)
    steering.add(base.transform(base.torus(0.31, 0.045, DETAIL["round"], DETAIL["tube"], "y", BLACK),
                                rotation=base.rot_x(math.pi / 2 + tilt)))
    for angle in (0, math.pi * 2 / 3, math.pi * 4 / 3):
        c, s = math.cos(angle), math.sin(angle)
        rz = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        steering.add(base.transform(base.box((0.44, 0.04, 0.04), BRONZE_LIT), rotation=base.rot_x(tilt) @ rz))
    cyl(steering, 0.052, 0.70, (0, -0.25, -0.25), "z", BRONZE, base.rot_x(math.radians(135)))
    cyl(steering, 0.105, 0.20, (0, -0.49, -0.49), "z", PURPLE, base.rot_x(math.radians(135)))
    parts["SteeringWheel"] = [(steering, 2)]

    for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"):
        tire, hub = base.Geo(), base.Geo()
        tire.add(base.torus(0.49, 0.18, DETAIL["round"], DETAIL["tube"], "x", TIRE))
        tire.add(base.torus(0.30, 0.050, DETAIL["round"], DETAIL["tube"], "x", PURPLE_LIT))
        cyl(hub, 0.24, 0.36, (0, 0, 0), "x", PURPLE)
        cyl(hub, 0.10, 0.43, (0, 0, 0), "x", BRONZE_LIT)
        parts[name] = [(tire, 5), (hub, 2)]

    for name in ("Exhaust_L", "Exhaust_R"):
        housing, flame = base.Geo(), base.Geo()
        box(housing, (0.46, 0.46, 0.64), (0, 0, 0), BRONZE)
        cyl(housing, 0.17, 0.56, (0, 0, 0.32), "z", BLACK)
        ell(flame, (0.22, 0.22, 0.64), (0, 0, 0.72), GLOW)
        parts[name] = [(housing, 2), (flame, 3)]
    return parts

TRANSLATIONS = {
    "Chassis": (0, 0, 0), "AccentMesh": (0, 0, 0),
    "SteeringWheel": (0, 1.48, -0.42),
    "Wheel_FL": (-1.38, 0.52, -1.04), "Wheel_FR": (1.38, 0.52, -1.04),
    "Wheel_RL": (-1.38, 0.52, 1.10), "Wheel_RR": (1.38, 0.52, 1.10),
    "Exhaust_L": (-0.58, 0.90, 1.62), "Exhaust_R": (0.58, 0.90, 1.62),
    "DriverMount": (0, 1.42, 0.23), "ItemMountRear": (0, 1.18, 2.04),
    "ItemMountForward": (0, 0.90, -2.18),
}

MATERIALS = [
    {"name": "BlackUnderbody", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.018, 0.016, 0.024, 1], "metallicFactor": 0.24, "roughnessFactor": 0.38}},
    {"name": "PurpleBodywork", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.25, 0.035, 0.46, 1], "metallicFactor": 0.30, "roughnessFactor": 0.32}},
    {"name": "BronzeStructure", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.42, 0.23, 0.08, 1], "metallicFactor": 0.68, "roughnessFactor": 0.30}},
    {"name": "PurpleEnergy", "alphaMode": "OPAQUE", "doubleSided": True, "emissiveFactor": [0.50, 0.06, 0.84], "pbrMetallicRoughness": {"baseColorFactor": [0.68, 0.11, 1.0, 1], "metallicFactor": 0.08, "roughnessFactor": 0.22}},
    {"name": "SkullRelief", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.70, 0.66, 0.76, 1], "metallicFactor": 0.18, "roughnessFactor": 0.46}},
    {"name": "WideTire", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.012, 0.011, 0.015, 1], "metallicFactor": 0.02, "roughnessFactor": 0.94}},
]

def main():
    shared.LOD = LOD
    shared.OUT = OUT
    shared.PREVIEW = PREVIEW
    shared.TRANSLATIONS = TRANSLATIONS
    shared.MATERIALS = MATERIALS
    shared.APPROVED_NAME = "The Grave Shift"
    shared.GENERATOR = "Minigame Mayhem procedural Grave Shift builder"
    shared.PREVIEW_TITLE = "THE GRAVE SHIFT"
    shared.CANDIDATE = "2"
    shared.USE_VERTEX_COLORS = True
    shared.MATERIAL_TEXTURE_RGBA = None
    shared.PREVIEW_MATERIAL_RGBA = None
    shared.PREVIEW_VIEWS = [
        "Front three-quarter • flat skull shield and angular thorn crown at -Z",
        "Rear three-quarter • enclosed engine and twin purple exhausts",
        "Top • cohesive purple armor and open cockpit",
        "Left profile • low armored street-racer stance",
    ]
    shared.PREVIEW_FOOTER = "Purple-dominant armored bruiser • bronze perimeter • low splitter • integrated sidepods • graphic skull shield"
    parts = build_geometry()
    triangles, doc = shared.export_glb(parts)
    if os.environ.get("GRAVE_SHIFT_SKIP_PREVIEW") != "1":
        shared.preview(parts)
    required = {"KartRoot", "Chassis", "AccentMesh", "SteeringWheel", "Wheel_FL", "Wheel_FR", "Wheel_RL",
                "Wheel_RR", "Exhaust_L", "Exhaust_R", "DriverMount", "ItemMountRear", "ItemMountForward"}
    actual = {node["name"] for node in doc["nodes"]}
    assert required <= actual and triangles <= {"LOD0": 25000, "LOD1": 12000, "LOD2": 5000}[LOD]
    print({"glb": str(OUT), "preview": str(PREVIEW), "lod": LOD, "triangles": triangles,
           "materials": len(doc["materials"]), "nodes": len(doc["nodes"])})

if __name__ == "__main__":
    main()
