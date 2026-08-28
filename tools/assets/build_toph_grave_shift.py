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
OUT = Path(os.environ.get("GRAVE_SHIFT_OUT", ROOT / "candidates/grave-shift-candidate-1.glb"))
PREVIEW = Path(os.environ.get("GRAVE_SHIFT_PREVIEW", ROOT / "candidates/grave-shift-candidate-1-preview.png"))

BLACK = np.array([0.018, 0.016, 0.024, 1.0], np.float32)
PURPLE = np.array([0.20, 0.035, 0.34, 1.0], np.float32)
PURPLE_LIT = np.array([0.48, 0.08, 0.72, 1.0], np.float32)
BRONZE = np.array([0.30, 0.16, 0.075, 1.0], np.float32)
BRONZE_LIT = np.array([0.55, 0.30, 0.12, 1.0], np.float32)
BONE = np.array([0.64, 0.57, 0.46, 1.0], np.float32)
TIRE = np.array([0.012, 0.011, 0.015, 1.0], np.float32)
GLOW = np.array([0.64, 0.10, 1.0, 1.0], np.float32)

def ell(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.ellipsoid(size, DETAIL["round"], max(5, DETAIL["round"] // 2), color), at, rotation))

def box(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.box(size, color), at, rotation))

def cyl(geo, radius, length, at, axis, color, rotation=None):
    geo.add(base.transform(base.cylinder(radius, length, DETAIL["round"], axis, color), at, rotation))

def spike(geo, at, scale, rotation=None):
    # Tapered thorn assembled from overlapping ellipsoids; structurally rooted.
    x, y, z = at
    ell(geo, (0.18 * scale, 0.34 * scale, 0.70 * scale), (x, y, z), BRONZE_LIT, rotation)
    ell(geo, (0.09 * scale, 0.20 * scale, 0.46 * scale), (x, y + 0.12 * scale, z - 0.27 * scale), BONE, rotation)

def build_geometry():
    parts = {}
    chassis, cockpit = base.Geo(), base.Geo()
    # Low wedge body over a visible bronze frame.
    ell(chassis, (2.30, 0.48, 3.56), (0, 0.63, 0.02), BLACK)
    ell(chassis, (2.08, 0.38, 2.72), (0, 0.86, -0.18), PURPLE)
    ell(chassis, (1.82, 0.46, 1.30), (0, 0.92, -1.42), BLACK)
    ell(chassis, (1.96, 0.36, 1.02), (0, 0.84, 1.34), PURPLE)
    # Open cockpit with a dark recessed seat and purple bolsters.
    ell(cockpit, (1.28, 0.16, 1.22), (0, 1.18, 0.25), BLACK)
    ell(cockpit, (1.00, 0.30, 0.66), (0, 1.28, 0.46), BLACK)
    ell(cockpit, (1.46, 0.34, 0.26), (0, 1.30, 0.86), PURPLE)
    for x in (-0.76, 0.76):
        ell(cockpit, (0.24, 0.36, 1.28), (x, 1.18, 0.20), PURPLE)
    parts["Chassis"] = [(chassis, 0), (cockpit, 1)]

    frame, crest, glow = base.Geo(), base.Geo(), base.Geo()
    # Exposed connected frame rails and crossmembers.
    for x in (-1.06, 1.06):
        cyl(frame, 0.075, 3.34, (x, 0.62, 0), "z", BRONZE)
    for z in (-1.32, -0.54, 0.64, 1.34):
        cyl(frame, 0.075, 2.18, (0, 0.62, z), "x", BRONZE)
    # Each hub has a visible axle connection to the chassis.
    for z in (-1.06, 1.12):
        cyl(frame, 0.11, 2.82, (0, 0.54, z), "x", BRONZE_LIT)
    # Angular side armor and thorn rails.
    for x in (-1.12, 1.12):
        box(frame, (0.13, 0.24, 2.62), (x, 0.88, 0.00), BRONZE)
        for z in (-0.86, 0.02, 0.86):
            spike(frame, (x, 1.06, z), 0.52, base.rot_y(-0.30 if x < 0 else 0.30))
    # Integrated nose shield at canonical -Z.
    ell(crest, (1.48, 0.72, 0.24), (0, 0.92, -1.98), BRONZE)
    ell(crest, (1.20, 0.60, 0.20), (0, 0.94, -2.13), BLACK)
    # Readable skull: cranium, cheekbones, jaw, eye sockets, nasal notch.
    ell(crest, (0.72, 0.62, 0.18), (0, 1.04, -2.25), BONE)
    ell(crest, (0.76, 0.24, 0.17), (0, 0.79, -2.25), BONE)
    for x in (-0.20, 0.20):
        ell(crest, (0.18, 0.15, 0.08), (x, 1.08, -2.36), BLACK)
    ell(crest, (0.10, 0.13, 0.08), (0, 0.92, -2.36), BLACK)
    for x in (-0.42, 0.42):
        spike(crest, (x, 1.21, -2.20), 0.88, base.rot_y(-0.42 if x < 0 else 0.42))
    # Purple lighting is nested into the nose and rear housings.
    for x in (-0.62, 0.62):
        ell(glow, (0.28, 0.17, 0.12), (x, 0.83, -2.26), GLOW)
        ell(frame, (0.48, 0.38, 0.52), (x, 0.92, 1.58), BRONZE)
        ell(frame, (0.34, 0.27, 0.36), (x, 0.93, 1.73), BLACK)
    parts["AccentMesh"] = [(frame, 2), (crest, 4), (glow, 3)]

    steering = base.Geo()
    tilt = math.radians(18)
    steering.add(base.transform(base.torus(0.35, 0.052, DETAIL["round"], DETAIL["tube"], "y", BLACK),
                                rotation=base.rot_x(math.pi / 2 + tilt)))
    for angle in (0, math.pi * 2 / 3, math.pi * 4 / 3):
        c, s = math.cos(angle), math.sin(angle)
        rz = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        steering.add(base.transform(base.box((0.52, 0.045, 0.045), BRONZE_LIT), rotation=base.rot_x(tilt) @ rz))
    cyl(steering, 0.06, 0.88, (0, -0.31, -0.31), "z", BRONZE, base.rot_x(math.radians(135)))
    cyl(steering, 0.12, 0.22, (0, -0.61, -0.61), "z", PURPLE, base.rot_x(math.radians(135)))
    parts["SteeringWheel"] = [(steering, 2)]

    for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"):
        tire, hub = base.Geo(), base.Geo()
        tire.add(base.torus(0.54, 0.20, DETAIL["round"], DETAIL["tube"], "x", TIRE))
        tire.add(base.torus(0.34, 0.060, DETAIL["round"], DETAIL["tube"], "x", BRONZE_LIT))
        cyl(hub, 0.27, 0.38, (0, 0, 0), "x", PURPLE)
        cyl(hub, 0.11, 0.46, (0, 0, 0), "x", BRONZE_LIT)
        parts[name] = [(tire, 5), (hub, 2)]

    for name in ("Exhaust_L", "Exhaust_R"):
        metal, flame = base.Geo(), base.Geo()
        cyl(metal, 0.19, 0.66, (0, 0, 0), "z", BRONZE_LIT, base.rot_x(-0.12))
        metal.add(base.transform(base.torus(0.20, 0.045, DETAIL["round"], DETAIL["tube"], "x", BLACK), (0, 0, 0.35)))
        ell(flame, (0.22, 0.22, 0.58), (0, 0.01, 0.55), GLOW)
        parts[name] = [(metal, 2), (flame, 3)]
    return parts

TRANSLATIONS = {
    "Chassis": (0, 0, 0), "AccentMesh": (0, 0, 0),
    "SteeringWheel": (0, 1.60, -0.46),
    "Wheel_FL": (-1.44, 0.54, -1.06), "Wheel_FR": (1.44, 0.54, -1.06),
    "Wheel_RL": (-1.44, 0.54, 1.12), "Wheel_RR": (1.44, 0.54, 1.12),
    "Exhaust_L": (-0.62, 0.84, 1.72), "Exhaust_R": (0.62, 0.84, 1.72),
    "DriverMount": (0, 1.47, 0.20), "ItemMountRear": (0, 1.14, 2.02),
    "ItemMountForward": (0, 0.91, -2.22),
}

MATERIALS = [
    {"name": "BlackBody", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.018, 0.016, 0.024, 1], "metallicFactor": 0.24, "roughnessFactor": 0.38}},
    {"name": "DeepPurpleArmor", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.20, 0.035, 0.34, 1], "metallicFactor": 0.28, "roughnessFactor": 0.34}},
    {"name": "DarkBronzeFrame", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.38, 0.20, 0.08, 1], "metallicFactor": 0.68, "roughnessFactor": 0.30}},
    {"name": "PurpleEnergy", "alphaMode": "OPAQUE", "doubleSided": True, "emissiveFactor": [0.48, 0.05, 0.82], "pbrMetallicRoughness": {"baseColorFactor": [0.64, 0.10, 1.0, 1], "metallicFactor": 0.08, "roughnessFactor": 0.22}},
    {"name": "AgedBone", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.64, 0.57, 0.46, 1], "metallicFactor": 0.02, "roughnessFactor": 0.76}},
    {"name": "WideTire", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.012, 0.011, 0.015, 1], "metallicFactor": 0.02, "roughnessFactor": 0.94}},
]

def main():
    shared.LOD = LOD
    shared.OUT = OUT
    shared.PREVIEW = PREVIEW
    shared.TRANSLATIONS = TRANSLATIONS
    shared.MATERIALS = MATERIALS
    shared.APPROVED_NAME = "The Grave Shift"
    shared.GENERATOR = "Accurate Artistry procedural Grave Shift builder"
    shared.PREVIEW_TITLE = "THE GRAVE SHIFT"
    shared.CANDIDATE = "1"
    shared.USE_VERTEX_COLORS = True
    shared.MATERIAL_TEXTURE_RGBA = None
    shared.PREVIEW_MATERIAL_RGBA = None
    shared.PREVIEW_VIEWS = [
        "Front three-quarter • thorned skull shield at -Z",
        "Rear three-quarter • bronze frame and purple exhausts",
        "Top • open cockpit and connected axle structure",
        "Left profile • low aggressive street-racer stance",
    ]
    shared.PREVIEW_FOOTER = "Black and deep-purple street bruiser • exposed bronze frame • wide connected tires • integrated thorned-skull shield"
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
