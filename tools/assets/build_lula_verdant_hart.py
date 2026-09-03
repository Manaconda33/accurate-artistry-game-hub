"""Build deterministic review GLBs for Lula's Verdant Hart."""

import math
import os
from pathlib import Path

import numpy as np

import build_manaconda_wayfinder as base
import build_keeg_mycelial_majesty as shared

ROOT = Path(__file__).resolve().parent
LOD = os.environ.get("VERDANT_HART_LOD", "LOD0").upper()
DETAILS = {"LOD0": (12, 6, 6), "LOD1": (7, 4, 4), "LOD2": (5, 3, 3)}
if LOD not in DETAILS:
    raise ValueError(f"Unknown VERDANT_HART_LOD: {LOD}")
ROUND, TUBE, RINGS = DETAILS[LOD]
OUT = Path(os.environ.get("VERDANT_HART_OUT", ROOT / "candidates/verdant-hart-candidate-1.glb"))
PREVIEW = Path(os.environ.get("VERDANT_HART_PREVIEW", ROOT / "candidates/verdant-hart-candidate-1-preview.png"))

DARK = np.array([0.035, 0.012, 0.003, 1], np.float32)
WOOD = np.array([0.14, 0.040, 0.006, 1], np.float32)
CARVED = np.array([0.30, 0.105, 0.012, 1], np.float32)
LEAF = np.array([0.09, 0.55, 0.04, 1], np.float32)
GLOW = np.array([0.82, 0.56, 0.035, 1], np.float32)
TIRE = np.array([0.010, 0.013, 0.008, 1], np.float32)


def ell(g, size, at, color, rotation=None):
    g.add(base.transform(base.ellipsoid(size, ROUND, RINGS, color), at, rotation))


def box(g, size, at, color, rotation=None):
    g.add(base.transform(base.box(size, color), at, rotation))


def cyl(g, radius, length, at, axis, color, rotation=None):
    g.add(base.transform(base.cylinder(radius, length, ROUND, axis, color), at, rotation))


def rot_axis(axis, angle):
    x, y, z = axis
    k = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]], dtype=float)
    return np.eye(3) + math.sin(angle) * k + (1 - math.cos(angle)) * (k @ k)


def branch(g, start, end, radius, color=CARVED):
    a, b = np.asarray(start, float), np.asarray(end, float)
    delta = b - a
    length = float(np.linalg.norm(delta))
    direction = delta / length
    up = np.array([0.0, 1.0, 0.0])
    axis = np.cross(up, direction)
    dot = float(np.clip(np.dot(up, direction), -1, 1))
    if np.linalg.norm(axis) < 1e-8:
        rotation = np.eye(3) if dot > 0 else base.rot_x(math.pi)
    else:
        axis /= np.linalg.norm(axis)
        rotation = rot_axis(axis, math.acos(dot))
    # Root paths are open-ended tubes whose ends are buried inside organic
    # joints. Removing planar caps prevents bright cut faces at every bend.
    g.add(base.transform(base.cylinder(radius, length, ROUND, "y", color, capped=False), (a + b) / 2, rotation))


def root_path(g, points, start_radius, end_radius=None, color=CARVED):
    """Build a continuous tapered root by overlapping every segment and joint."""
    end_radius = end_radius if end_radius is not None else start_radius * 0.42
    count = len(points) - 1
    # Organic collars hide the flat cylinder cuts and make the path read as one root.
    ell(g, (start_radius * 3.20,) * 3, points[0], color)
    for index, (start, end) in enumerate(zip(points, points[1:])):
        t = index / max(1, count)
        radius = start_radius + (end_radius - start_radius) * t
        branch(g, start, end, radius, color)
        next_t = (index + 1) / max(1, count)
        next_radius = start_radius + (end_radius - start_radius) * next_t
        # ellipsoid() accepts full dimensions, so this is deliberately >2r.
        collar = max(radius, next_radius) * (3.20 if index < count - 1 else 2.55)
        ell(g, (collar,) * 3, end, color)


def leaf(g, at, scale=1.0, angle=0.0):
    """An embedded leaf blade plus a short stem that visibly anchors it to a root."""
    x, y, z = at
    # Broad pointed blade, paired with a smaller blade and buried stem.
    ell(g, (0.24 * scale, 0.09 * scale, 0.52 * scale), at, LEAF, rot_z(angle))
    ell(g, (0.18 * scale, 0.08 * scale, 0.40 * scale),
        (x + 0.11 * scale * math.cos(angle), y, z + 0.12 * scale), LEAF, rot_z(angle + .65))
    branch(g, (x, y - 0.025, z - 0.18 * scale), (x, y - 0.055, z + 0.18 * scale), 0.035 * scale, LEAF)


def rot_z(angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def build_geometry():
    parts = {}
    chassis = base.Geo()
    # A low, long wooden hull supports the root skin; the dark inset is the cockpit,
    # not a separate buggy body.
    ell(chassis, (1.86, 0.38, 3.18), (0, 0.65, 0.02), DARK)
    ell(chassis, (1.66, 0.40, 2.90), (0, 0.76, 0.02), WOOD)
    ell(chassis, (1.02, 0.24, 1.20), (0, 1.08, 0.43), DARK)
    ell(chassis, (0.82, 0.26, 0.80), (0, 1.12, 0.50), TIRE)
    parts["Chassis"] = [(chassis, 0)]

    accent = base.Geo()
    foliage = base.Geo()
    # Primary roots define one uninterrupted nose-to-tail silhouette.
    for side in (-1, 1):
        root_path(accent, [(0.28*side,0.72,1.63),(1.03*side,0.86,1.12),(1.20*side,0.98,0.22),(1.08*side,0.96,-0.88),(0.72*side,0.99,-1.58),(0.40*side,0.88,-2.04)], .16, .09, WOOD)
        root_path(accent, [(0.12*side,0.58,1.78),(0.76*side,0.58,1.48),(1.18*side,0.56,0.75),(1.18*side,0.55,-0.70),(0.70*side,0.60,-1.78)], .13, .07, CARVED)
        root_path(accent, [(0.30*side,1.06,1.40),(0.92*side,1.25,0.92),(1.14*side,1.30,0.15),(1.00*side,1.27,-0.73),(0.61*side,1.20,-1.40)], .115, .065, CARVED)

    # Layered carved stag face: broad brow, tapered muzzle, inset nose, curled cheeks.
    ell(accent, (1.03, 0.48, 0.70), (0, 0.92, -1.62), WOOD)
    ell(accent, (0.74, 0.38, 0.69), (0, 0.76, -1.96), CARVED)
    ell(accent, (0.45, 0.25, 0.42), (0, 0.64, -2.30), WOOD)
    ell(accent, (0.27, 0.13, 0.13), (0, 0.60, -2.50), DARK)
    for side in (-1, 1):
        ell(accent, (0.16, 0.10, 0.08), (0.39 * side, 0.94, -2.18), GLOW)
        root_path(accent, [(0.55*side,.66,-2.32),(.83*side,.64,-2.12),(.92*side,.78,-1.90),(.76*side,.91,-1.72)], .10, .055, DARK)
        ell(accent, (0.37, 0.09, 0.22), (0.82 * side, 1.14, -1.76), CARVED, rot_z(0.50 * side))
    # Inlaid leaf crest follows the forehead plane.
    ell(foliage, (0.26, 0.10, 0.58), (0, 1.03, -2.08), LEAF)
    for side in (-1, 1):
        ell(foliage, (0.20, 0.09, 0.45), (0.17 * side, 1.02, -2.06), LEAF, rot_z(-.28*side))

    # Antlers grow from thick brow roots; all forks overlap their parent stems.
    for side in (-1, 1):
        root_path(accent, [(0.43*side,1.16,-1.68),(0.62*side,1.40,-1.58),(0.82*side,1.59,-1.42),(1.08*side,1.73,-1.18)], .16, .085, WOOD)
        root_path(accent, [(0.78*side,1.56,-1.43),(0.73*side,1.82,-1.39),(0.77*side,2.03,-1.31)], .09, .045, CARVED)
        root_path(accent, [(1.01*side,1.69,-1.22),(1.28*side,1.86,-1.02),(1.46*side,1.98,-.84)], .08, .04, CARVED)
        root_path(accent, [(1.23*side,1.82,-1.05),(1.41*side,1.75,-.76),(1.54*side,1.76,-.55)], .07, .035, CARVED)

        # Thick growth knots fuse each antler tree into the carved brow.
        ell(accent, (.25, .22, .24), (.43*side, 1.16, -1.68), WOOD)
        ell(accent, (.18, .17, .18), (.78*side, 1.56, -1.43), CARVED)
        ell(accent, (.16, .15, .16), (1.23*side, 1.82, -1.05), CARVED)

    # Secondary vines cross and physically bind the major roots.
    for side in (-1, 1):
        root_path(foliage, [(.34*side,.79,1.54),(.82*side,1.02,.74),(.76*side,1.12,-.26),(.43*side,1.02,-1.36)], .065, .035, LEAF)

        # Visible foliage grows from, and slightly sinks into, the structural roots.
        leaf(foliage, (.96*side, 1.17, .64), 1.10, .35*side)
        leaf(foliage, (.82*side, 1.13, -.86), 1.00, .30*side)
        if LOD != "LOD2":
            leaf(foliage, (1.07*side, 1.18, -.08), .95, -.42*side)
            leaf(foliage, (1.18*side, .70, 1.18), .85, -.25*side)
    # Foliage is its own material primitive so viewers cannot wash it into wood.
    parts["AccentMesh"] = [(accent, 1), (foliage, 3)]

    steering = base.Geo()
    tilt = math.radians(24)
    steering.add(base.transform(base.torus(0.31, 0.045, ROUND, TUBE, "y", DARK), rotation=base.rot_x(math.pi / 2 + tilt)))
    for angle in (0, math.tau / 3, math.tau * 2 / 3):
        c, s = math.cos(angle), math.sin(angle)
        rz = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        steering.add(base.transform(base.box((0.43, 0.04, 0.04), CARVED), rotation=base.rot_x(tilt) @ rz))
    branch(steering, (0, -0.05, -0.02), (0, -0.48, -0.46), 0.052)
    parts["SteeringWheel"] = [(steering, 2)]

    for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"):
        wheel = base.Geo()
        wheel.add(base.torus(0.46, 0.14, ROUND, TUBE, "x", TIRE))
        cyl(wheel, 0.31, 0.34, (0, 0, 0), "x", DARK)
        cyl(wheel, 0.17, 0.39, (0, 0, 0), "x", WOOD)
        for angle in range(0, 360, 72):
            rad = math.radians(angle)
            ell(wheel, (0.05, 0.14, 0.27), (0, math.cos(rad) * 0.22, math.sin(rad) * 0.22), LEAF, base.rot_x(rad))
        parts[name] = [(wheel, 3)]

    # Required exhaust nodes are restrained wooden root outlets, not neon thrusters.
    for name in ("Exhaust_L", "Exhaust_R"):
        exhaust = base.Geo()
        cyl(exhaust, 0.13, 0.34, (0, 0, 0), "z", WOOD)
        ell(exhaust, (0.15, 0.15, 0.10), (0, 0, 0.18), DARK)
        parts[name] = [(exhaust, 4)]
    return parts


TRANSLATIONS = {
    "Chassis": (0, 0, 0), "AccentMesh": (0, 0, 0), "SteeringWheel": (0, 1.45, -0.34),
    "Wheel_FL": (-1.24, 0.50, -1.10), "Wheel_FR": (1.24, 0.50, -1.10),
    "Wheel_RL": (-1.24, 0.50, 1.12), "Wheel_RR": (1.24, 0.50, 1.12),
    "Exhaust_L": (-0.48, 0.72, 1.78), "Exhaust_R": (0.48, 0.72, 1.78),
    "DriverMount": (0, 1.40, 0.28), "ItemMountRear": (0, 1.14, 2.04),
    "ItemMountForward": (0, 0.88, -2.28),
}

MATERIALS = [
    {"name": "DarkRoot", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.045, 0.020, 0.006, 1], "metallicFactor": 0.02, "roughnessFactor": 0.86}},
    {"name": "LivingWood", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.25, 0.09, 0.018, 1], "metallicFactor": 0.01, "roughnessFactor": 0.78}},
    {"name": "CarvedWood", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [0.38, 0.17, 0.025, 1], "metallicFactor": 0.01, "roughnessFactor": 0.69}},
    {"name": "LeafWheel", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0, "roughnessFactor": 0.92}},
    {"name": "VerdantGlow", "alphaMode": "OPAQUE", "doubleSided": True, "emissiveFactor": [0.42, 0.70, 0.06], "pbrMetallicRoughness": {"baseColorFactor": [0.62, 0.90, 0.12, 1], "metallicFactor": 0.02, "roughnessFactor": 0.24}},
]


def main():
    shared.LOD, shared.OUT, shared.PREVIEW = LOD, OUT, PREVIEW
    shared.TRANSLATIONS, shared.MATERIALS = TRANSLATIONS, MATERIALS
    shared.APPROVED_NAME = "The Verdant Hart"
    shared.GENERATOR = "Minigame Mayhem procedural Verdant Hart builder"
    shared.PREVIEW_TITLE, shared.CANDIDATE = "THE VERDANT HART", "4"
    shared.USE_VERTEX_COLORS = True
    shared.MATERIAL_TEXTURE_RGBA = shared.PREVIEW_MATERIAL_RGBA = None
    shared.PREVIEW_VIEWS = [
        "Front three-quarter • stag face and rooted antlers at -Z",
        "Rear three-quarter • living-root body and restrained outlets",
        "Top • open cockpit inside woven timber chassis",
        "Left profile • low woodland-racer stance",
    ]
    shared.PREVIEW_FOOTER = "Living-root chassis • integrated stag nose • structural antlers • leaf-inlaid wheels • verdant magic"
    parts = build_geometry()
    triangles, doc = shared.export_glb(parts)
    if os.environ.get("VERDANT_HART_SKIP_PREVIEW") != "1":
        shared.preview(parts)
    required = {"KartRoot", "Chassis", "AccentMesh", "SteeringWheel", "Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR", "Exhaust_L", "Exhaust_R", "DriverMount", "ItemMountRear", "ItemMountForward"}
    assert required <= {node["name"] for node in doc["nodes"]}
    assert triangles <= {"LOD0": 25000, "LOD1": 12000, "LOD2": 5000}[LOD]
    print({"glb": str(OUT), "preview": str(PREVIEW), "lod": LOD, "triangles": triangles, "materials": len(doc["materials"]), "nodes": len(doc["nodes"])})


if __name__ == "__main__":
    main()
