"""Build deterministic review GLBs for Jennifer's Hearthwarden.

Set HEARTHWARDEN_LOD to LOD0, LOD1, or LOD2; HEARTHWARDEN_OUT to the
destination GLB; and HEARTHWARDEN_SKIP_PREVIEW=1 for headless builds.
"""

import math
import os
from pathlib import Path

import numpy as np

import build_keeg_mycelial_majesty as shared
import build_manaconda_wayfinder as base


ROOT = Path(__file__).resolve().parent
LOD = os.environ.get("HEARTHWARDEN_LOD", "LOD0").upper()
DETAILS = {
    "LOD0": {"round": 16, "tube": 8, "rings": 8, "limit": 25000},
    "LOD1": {"round": 12, "tube": 6, "rings": 6, "limit": 12000},
    "LOD2": {"round": 8, "tube": 4, "rings": 4, "limit": 5000},
}
if LOD not in DETAILS:
    raise ValueError(f"Unknown HEARTHWARDEN_LOD: {LOD}")
DETAIL = DETAILS[LOD]
OUT = Path(os.environ.get("HEARTHWARDEN_OUT", ROOT / "candidates/hearthwarden-candidate-1.glb"))
PREVIEW = Path(
    os.environ.get(
        "HEARTHWARDEN_PREVIEW",
        ROOT / "candidates/hearthwarden-candidate-1-preview.png",
    )
)

PEAR_DARK = np.array([0.16, 0.060, 0.020, 1.0], np.float32)
PEAR_WOOD = np.array([0.38, 0.175, 0.055, 1.0], np.float32)
WILLOW = np.array([0.53, 0.30, 0.10, 1.0], np.float32)
FOREST = np.array([0.045, 0.22, 0.11, 1.0], np.float32)
FOREST_LIT = np.array([0.075, 0.34, 0.19, 1.0], np.float32)
BRONZE = np.array([0.48, 0.25, 0.075, 1.0], np.float32)
BRONZE_DARK = np.array([0.24, 0.11, 0.035, 1.0], np.float32)
TURQUOISE = np.array([0.035, 0.53, 0.49, 1.0], np.float32)
TIRE = np.array([0.018, 0.021, 0.019, 1.0], np.float32)
AMETHYST = np.array([0.50, 0.13, 0.72, 1.0], np.float32)
HERB = np.array([0.21, 0.46, 0.16, 1.0], np.float32)


def ell(geo, size, at, color, rotation=None):
    geo.add(
        base.transform(
            base.ellipsoid(size, DETAIL["round"], DETAIL["rings"], color),
            at,
            rotation,
        )
    )


def box(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.box(size, color), at, rotation))


def cyl(geo, radius, length, at, axis, color, rotation=None, capped=True):
    geo.add(
        base.transform(
            base.cylinder(radius, length, DETAIL["round"], axis, color, capped=capped),
            at,
            rotation,
        )
    )


def rot_z(angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def rot_axis(axis, angle):
    x, y, z = axis
    k = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]], dtype=float)
    return np.eye(3) + math.sin(angle) * k + (1 - math.cos(angle)) * (k @ k)


def branch(geo, start, end, radius, color, capped=True):
    """Join two points with a cylindrical working-wood member."""
    start = np.asarray(start, float)
    end = np.asarray(end, float)
    delta = end - start
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
    geo.add(
        base.transform(
            base.cylinder(radius, length, DETAIL["round"], "y", color, capped=capped),
            (start + end) / 2,
            rotation,
        )
    )


def add_willow_panel(geo, x, side):
    """Build a framed, deliberately woven side basket rather than living vines."""
    z_front, z_rear = -0.78, 1.18
    y_low, y_high = 0.66, 1.22
    for z in (z_front, z_rear):
        branch(geo, (x, y_low, z), (x, y_high, z), 0.045, PEAR_WOOD)
    for y in (y_low, y_high):
        branch(geo, (x, y, z_front), (x, y, z_rear), 0.045, PEAR_WOOD)
    # Alternating diagonals communicate hand-woven willow without becoming
    # foliage or a structural root network.
    strand_count = 5 if LOD == "LOD0" else 4 if LOD == "LOD1" else 3
    span = z_rear - z_front
    for index in range(strand_count):
        z = z_front + span * (index + 0.35) / strand_count
        offset = span * 0.40 / strand_count
        branch(geo, (x + side * 0.005, y_low + 0.03, z - offset),
               (x + side * 0.005, y_high - 0.03, z + offset), 0.025, WILLOW, capped=False)
        branch(geo, (x + side * 0.010, y_high - 0.03, z - offset),
               (x + side * 0.010, y_low + 0.03, z + offset), 0.025, WILLOW, capped=False)


def add_tree_medallion(frame, inlay):
    """Add a readable tree-of-life badge on the -Z prow."""
    center = (0, 0.83, -2.04)
    # A stout pear-wood boss and paired bronze stays tie the badge into the
    # hood and front frame. Their overlap remains visible from side angles.
    cyl(frame, 0.13, 0.42, (0, 0.83, -1.89), "z", PEAR_DARK)
    for x in (-0.34, 0.34):
        branch(frame, (x, 0.62, -1.70), (x, 0.62, -2.03), 0.055, BRONZE)
    frame.add(
        base.transform(
            base.torus(0.49, 0.075, DETAIL["round"], DETAIL["tube"], "y", BRONZE),
            center,
            base.rot_x(math.pi / 2),
        )
    )
    ell(frame, (0.86, 0.86, 0.10), (0, 0.83, -2.045), FOREST)
    # The trunk and crown sit slightly ahead of the green inset.
    z = -2.105
    branch(inlay, (0, 0.47, z), (0, 1.08, z), 0.045, BRONZE)
    branch(inlay, (0, 0.62, z), (-0.26, 0.46, z), 0.030, BRONZE)
    branch(inlay, (0, 0.62, z), (0.26, 0.46, z), 0.030, BRONZE)
    branch(inlay, (0, 0.88, z), (-0.28, 1.08, z), 0.030, BRONZE)
    branch(inlay, (0, 0.88, z), (0.28, 1.08, z), 0.030, BRONZE)
    for x, y, size in ((0, 1.15, .24), (-.24, 1.06, .20), (.24, 1.06, .20),
                       (-.31, .88, .18), (.31, .88, .18)):
        ell(inlay, (size, size, 0.08), (x, y, z), TURQUOISE)


def add_staff(wood, glow):
    """Mount Jennifer's six-foot gnarled pear-wood staff on kart-left."""
    points = [(-1.16, 0.72, 1.15), (-1.20, 1.30, 1.21),
              (-1.13, 1.92, 1.15), (-1.20, 2.54, 1.20)]
    radii = [0.072, 0.066, 0.058]
    for start, end, radius in zip(points, points[1:], radii):
        branch(wood, start, end, radius, PEAR_DARK, capped=False)
    for point, size in ((points[1], .16), (points[2], .14)):
        ell(wood, (size, size, size), point, PEAR_WOOD)
    branch(wood, points[-1], (-1.39, 2.73, 1.20), 0.048, PEAR_DARK)
    branch(wood, points[-1], (-1.02, 2.77, 1.20), 0.048, PEAR_DARK)
    ell(glow, (0.27, 0.34, 0.24), (-1.20, 2.78, 1.20), AMETHYST, rot_z(math.pi / 4))


def build_geometry():
    parts = {}

    chassis, body = base.Geo(), base.Geo()
    # A broad plank platform and boxed working frame establish the converted
    # apothecary-wagon construction. Rounded green panels soften it into a kart.
    box(chassis, (2.34, 0.30, 3.40), (0, 0.64, 0.02), PEAR_DARK)
    box(chassis, (2.12, 0.18, 3.18), (0, 0.84, 0.02), PEAR_WOOD)
    for x in (-1.08, 1.08):
        cyl(chassis, 0.085, 3.50, (x, 0.69, 0.02), "z", PEAR_WOOD)
    for z in (-1.62, 1.66):
        cyl(chassis, 0.085, 2.22, (0, 0.69, z), "x", PEAR_WOOD)
    # Low hood, rear apothecary cowl, and a dark open cockpit.
    ell(body, (2.18, 0.62, 1.46), (0, 0.91, -1.15), FOREST)
    ell(body, (1.86, 0.38, 1.12), (0, 1.15, -1.22), FOREST_LIT)
    ell(body, (2.14, 0.54, 0.92), (0, 0.98, 1.30), FOREST)
    ell(body, (1.46, 0.18, 1.16), (0, 1.13, 0.18), TIRE)
    ell(body, (1.22, 0.18, 0.82), (0, 1.17, 0.28), PEAR_DARK)
    # Upholstered backrest and broad bolsters fit Jennifer's sturdy silhouette.
    ell(body, (1.58, 0.42, 0.30), (0, 1.30, 0.76), FOREST)
    for x in (-0.77, 0.77):
        ell(body, (0.24, 0.36, 1.30), (x, 1.22, 0.18), PEAR_WOOD)
    parts["Chassis"] = [(chassis, 0), (body, 0)]

    accent, glow = base.Geo(), base.Geo()
    # Constructed willow basket panels remain visibly separate from the frame.
    add_willow_panel(accent, -1.13, -1)
    add_willow_panel(accent, 1.13, 1)

    # Aged bronze brackets and turquoise fasteners mark mechanical joints.
    for x in (-1.12, 1.12):
        for z in (-1.47, 1.48):
            box(accent, (0.16, 0.28, 0.28), (x, 0.78, z), BRONZE)
            ell(glow, (0.075, 0.075, 0.075), (x * 1.012, 0.86, z - 0.02), TURQUOISE)
    for x in (-0.74, 0.74):
        box(accent, (0.13, 0.16, 0.36), (x, 1.16, -1.73), BRONZE)

    add_tree_medallion(accent, glow)

    # Reinforced Newfoundland perch on kart-right (+X) with a low retaining rail.
    box(accent, (0.92, 0.18, 1.14), (0.72, 1.14, 1.02), PEAR_WOOD)
    box(accent, (0.76, 0.09, 0.96), (0.72, 1.25, 1.02), FOREST)
    for z in (0.54, 1.50):
        branch(accent, (1.16, 1.18, z), (1.16, 1.58, z), 0.045, BRONZE)
    branch(accent, (1.16, 1.58, 0.54), (1.16, 1.58, 1.50), 0.045, BRONZE)
    # Two frame braces carry the dog's working weight into the rear rail.
    branch(accent, (0.32, 1.10, 0.54), (1.08, 0.73, 0.54), 0.055, BRONZE_DARK)
    branch(accent, (0.32, 1.10, 1.50), (1.08, 0.73, 1.50), 0.055, BRONZE_DARK)

    add_staff(accent, glow)

    # Secured remedy drawers and herb bundles read as working cargo, not foliage.
    for x in (-0.34, 0.34):
        box(accent, (0.54, 0.34, 0.52), (x, 1.15, 1.48), WILLOW)
        box(accent, (0.12, 0.08, 0.06), (x, 1.16, 1.205), BRONZE)
    if LOD != "LOD2":
        for x in (-0.34, 0, 0.34):
            # Sink each stem below the drawer's top face so no daylight can
            # appear between the remedy box and its secured herb bundle.
            branch(glow, (x, 1.28, 1.53), (x + 0.05, 1.66, 1.49), 0.022, HERB, capped=False)
            ell(glow, (0.12, 0.05, 0.18), (x + 0.08, 1.58, 1.48), HERB, rot_z(0.45))
    parts["AccentMesh"] = [(accent, 1), (glow, 3)]

    # Exactly one modeled steering wheel. Driver sprites remain wheel-free.
    steering = base.Geo()
    tilt = math.radians(18)
    steering.add(
        base.transform(
            base.torus(0.36, 0.055, DETAIL["round"], DETAIL["tube"], "y", PEAR_DARK),
            rotation=base.rot_x(math.pi / 2 + tilt),
        )
    )
    for angle in (0, math.tau / 3, math.tau * 2 / 3):
        steering.add(
            base.transform(
                base.box((0.52, 0.045, 0.045), BRONZE),
                rotation=base.rot_x(tilt) @ rot_z(angle),
            )
        )
    cyl(steering, 0.075, 0.64, (0, -0.24, -0.24), "z", BRONZE_DARK,
        base.rot_x(math.radians(135)))
    parts["SteeringWheel"] = [(steering, 1)]

    for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"):
        tire, hub = base.Geo(), base.Geo()
        tire.add(base.torus(0.51, 0.19, DETAIL["round"], DETAIL["tube"], "x", TIRE))
        # A second shallow torus gives the wide tire a work-ready shoulder.
        tire.add(base.torus(0.44, 0.065, DETAIL["round"], DETAIL["tube"], "x", PEAR_DARK))
        cyl(hub, 0.29, 0.38, (0, 0, 0), "x", BRONZE)
        hub.add(base.torus(0.24, 0.040, DETAIL["round"], DETAIL["tube"], "x", TURQUOISE))
        cyl(hub, 0.11, 0.43, (0, 0, 0), "x", BRONZE_DARK)
        parts[name] = [(tire, 2), (hub, 1)]

    # Restrained teal outlets imply practical enchantment rather than thrusters.
    for name in ("Exhaust_L", "Exhaust_R"):
        exhaust, magic = base.Geo(), base.Geo()
        cyl(exhaust, 0.14, 0.52, (0, 0, 0), "z", BRONZE_DARK, base.rot_x(-0.10))
        exhaust.add(
            base.transform(
                base.torus(0.15, 0.035, DETAIL["round"], DETAIL["tube"], "x", BRONZE),
                (0, 0, 0.27),
            )
        )
        ell(magic, (0.12, 0.12, 0.22), (0, 0, 0.34), TURQUOISE)
        parts[name] = [(exhaust, 1), (magic, 3)]
    return parts


TRANSLATIONS = {
    "Chassis": (0, 0, 0),
    "AccentMesh": (0, 0, 0),
    "SteeringWheel": (0, 1.56, -0.42),
    "Wheel_FL": (-1.39, 0.53, -1.05),
    "Wheel_FR": (1.39, 0.53, -1.05),
    "Wheel_RL": (-1.39, 0.53, 1.12),
    "Wheel_RR": (1.39, 0.53, 1.12),
    "Exhaust_L": (-0.54, 0.79, 1.73),
    "Exhaust_R": (0.54, 0.79, 1.73),
    "DriverMount": (0, 1.48, 0.20),
    "ItemMountRear": (0, 1.20, 1.96),
    "ItemMountForward": (0, 0.91, -2.14),
}


MATERIALS = [
    {
        "name": "PearWoodAndForestPanels",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.84,
        },
    },
    {
        "name": "AgedBronzeAndWillow",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "metallicFactor": 0.46,
            "roughnessFactor": 0.58,
        },
    },
    {
        "name": "WideFieldTires",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.93,
        },
    },
    {
        "name": "RestrainedDruidicGlow",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "emissiveFactor": [0.08, 0.30, 0.27],
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "metallicFactor": 0.08,
            "roughnessFactor": 0.34,
        },
    },
]


def main():
    shared.LOD = LOD
    shared.OUT = OUT
    shared.PREVIEW = PREVIEW
    shared.TRANSLATIONS = TRANSLATIONS
    shared.MATERIALS = MATERIALS
    shared.APPROVED_NAME = "The Hearthwarden"
    shared.GENERATOR = "Minigame Mayhem procedural Hearthwarden builder"
    shared.PREVIEW_TITLE = "THE HEARTHWARDEN"
    shared.CANDIDATE = "2"
    shared.USE_VERTEX_COLORS = True
    shared.MATERIAL_TEXTURE_RGBA = None
    shared.PREVIEW_MATERIAL_RGBA = None
    shared.PREVIEW_VIEWS = [
        "Front three-quarter • tree-of-life medallion at -Z",
        "Rear three-quarter • right dog perch and left staff rack",
        "Top • broad cockpit and working apothecary cargo",
        "Left profile • low all-surface field-roadster stance",
    ]
    shared.PREVIEW_FOOTER = (
        "Constructed pear wood • woven willow • aged bronze • forest-green panels • "
        "right dog perch • left amethyst staff"
    )

    parts = build_geometry()
    triangles, doc = shared.export_glb(parts)
    if os.environ.get("HEARTHWARDEN_SKIP_PREVIEW") != "1":
        shared.preview(parts)

    required = {
        "KartRoot",
        "Chassis",
        "AccentMesh",
        "SteeringWheel",
        "Wheel_FL",
        "Wheel_FR",
        "Wheel_RL",
        "Wheel_RR",
        "Exhaust_L",
        "Exhaust_R",
        "DriverMount",
        "ItemMountRear",
        "ItemMountForward",
    }
    actual = {node["name"] for node in doc["nodes"]}
    assert required <= actual
    assert triangles <= DETAIL["limit"]
    assert len(doc["materials"]) == 4
    assert doc["extras"]["forward"] == "-Z"
    assert sum(node["name"] == "SteeringWheel" for node in doc["nodes"]) == 1
    print(
        {
            "glb": str(OUT),
            "preview": str(PREVIEW),
            "lod": LOD,
            "triangles": triangles,
            "triangleLimit": DETAIL["limit"],
            "materials": len(doc["materials"]),
            "nodes": len(doc["nodes"]),
        }
    )


if __name__ == "__main__":
    main()
