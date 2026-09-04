"""Build deterministic review GLBs for Dragon Queen's Sovereign Wyrm.

Set SOVEREIGN_WYRM_LOD to LOD0, LOD1, or LOD2; SOVEREIGN_WYRM_OUT to
the destination GLB; and SOVEREIGN_WYRM_SKIP_PREVIEW=1 for headless builds.
"""

import math
import os
from pathlib import Path

import numpy as np

import build_keeg_mycelial_majesty as shared
import build_manaconda_wayfinder as base


ROOT = Path(__file__).resolve().parent
LOD = os.environ.get("SOVEREIGN_WYRM_LOD", "LOD0").upper()
DETAILS = {
    "LOD0": {"round": 16, "tube": 8, "rings": 8, "limit": 25000},
    "LOD1": {"round": 12, "tube": 6, "rings": 6, "limit": 12000},
    "LOD2": {"round": 8, "tube": 4, "rings": 4, "limit": 5000},
}
if LOD not in DETAILS:
    raise ValueError(f"Unknown SOVEREIGN_WYRM_LOD: {LOD}")
DETAIL = DETAILS[LOD]
OUT = Path(
    os.environ.get(
        "SOVEREIGN_WYRM_OUT",
        ROOT / "candidates/sovereign-wyrm-candidate-1.glb",
    )
)
PREVIEW = Path(
    os.environ.get(
        "SOVEREIGN_WYRM_PREVIEW",
        ROOT / "candidates/sovereign-wyrm-candidate-1-preview.png",
    )
)

MIDNIGHT = np.array([0.025, 0.060, 0.24, 1.0], np.float32)
NAVY = np.array([0.030, 0.105, 0.42, 1.0], np.float32)
NAVY_LIT = np.array([0.065, 0.22, 0.64, 1.0], np.float32)
GOLD = np.array([0.86, 0.52, 0.10, 1.0], np.float32)
GOLD_DARK = np.array([0.43, 0.20, 0.035, 1.0], np.float32)
TIRE = np.array([0.012, 0.014, 0.025, 1.0], np.float32)
JEWEL = np.array([0.03, 0.48, 1.0, 1.0], np.float32)


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
            base.cylinder(
                radius,
                length,
                DETAIL["round"],
                axis,
                color,
                capped=capped,
            ),
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
            base.cylinder(
                radius,
                length,
                DETAIL["round"],
                "y",
                color,
                capped=capped,
            ),
            (start + end) / 2,
            rotation,
        )
    )


def polygon_prism(points, thickness, color):
    """Create a convex plate in the XY plane with thickness along Z."""
    points = np.asarray(points, dtype=float)
    front_z = -thickness / 2
    rear_z = thickness / 2
    positions, normals, indices = [], [], []

    def triangle(vertices, normal):
        start = len(positions)
        positions.extend(vertices)
        normals.extend([normal] * 3)
        indices.extend((start, start + 1, start + 2))

    for index in range(1, len(points) - 1):
        triangle(
            [
                (points[0, 0], points[0, 1], front_z),
                (points[index + 1, 0], points[index + 1, 1], front_z),
                (points[index, 0], points[index, 1], front_z),
            ],
            (0, 0, -1),
        )
        triangle(
            [
                (points[0, 0], points[0, 1], rear_z),
                (points[index, 0], points[index, 1], rear_z),
                (points[index + 1, 0], points[index + 1, 1], rear_z),
            ],
            (0, 0, 1),
        )

    for index, point in enumerate(points):
        following = points[(index + 1) % len(points)]
        edge = following - point
        normal = np.array([edge[1], -edge[0], 0.0])
        normal /= max(np.linalg.norm(normal), 1e-9)
        a = (point[0], point[1], front_z)
        b = (following[0], following[1], front_z)
        c = (following[0], following[1], rear_z)
        d = (point[0], point[1], rear_z)
        triangle([a, b, c], normal)
        triangle([a, c, d], normal)
    return positions, normals, color, indices


def add_nose_shield(frame, glow):
    """Mount the dragon shield directly to the -Z prow."""
    center = (0, 0.96, -2.17)
    # The boss and paired stays overlap the hood and shield so the heraldry
    # cannot read as a floating badge from either side view.
    cyl(frame, 0.17, 0.46, (0, 0.91, -1.91), "z", GOLD_DARK)
    for x in (-0.42, 0.42):
        branch(frame, (x, 0.70, -1.76), (x, 0.78, -2.10), 0.055, GOLD_DARK)
    shield_points = [(-0.72, 0.38), (0.72, 0.38), (0.64, -0.18), (0, -0.60), (-0.64, -0.18)]
    frame.add(base.transform(polygon_prism(shield_points, 0.22, GOLD), center))
    inset_points = [(x * 0.78, y * 0.78) for x, y in shield_points]
    frame.add(base.transform(polygon_prism(inset_points, 0.16, MIDNIGHT), (0, 0.96, -2.31)))
    # A compact gold dragon mark remains readable as an S-shaped body with
    # a raised head, two wings, and a curled tail at gameplay distance.
    z = -2.42
    dragon_points = [
        (-0.15, 0.69, z),
        (0.10, 0.79, z),
        (-0.07, 0.97, z),
        (0.13, 1.14, z),
    ]
    for start, end in zip(dragon_points, dragon_points[1:]):
        branch(frame, start, end, 0.035, GOLD, capped=False)
    branch(frame, (-0.02, 0.92, z), (-0.34, 1.09, z), 0.025, GOLD, capped=False)
    branch(frame, (-0.02, 0.92, z), (0.33, 0.98, z), 0.025, GOLD, capped=False)
    branch(frame, (-0.15, 0.69, z), (-0.35, 0.63, z), 0.022, GOLD, capped=False)
    ell(frame, (0.16, 0.12, 0.07), (0.16, 1.17, z), GOLD)
    ell(glow, (0.09, 0.09, 0.06), (0.17, 1.19, z - 0.04), JEWEL)


def build_geometry():
    parts = {}

    chassis, cockpit = base.Geo(), base.Geo()
    # Low, long royal grand-tourer body. The lit prow layers taper toward -Z.
    ell(chassis, (2.48, 0.54, 4.12), (0, 0.62, -0.04), MIDNIGHT)
    ell(chassis, (2.32, 0.58, 3.74), (0, 0.78, -0.10), NAVY)
    ell(chassis, (2.18, 0.66, 1.90), (0, 0.91, -1.42), NAVY)
    ell(chassis, (1.70, 0.38, 1.34), (0, 1.16, -1.58), NAVY_LIT)

    # Split rear shoulders leave a central route for Dragon Queen's tail.
    for x in (-0.70, 0.70):
        ell(chassis, (1.05, 0.60, 1.42), (x, 0.90, 1.24), NAVY)
        ell(chassis, (0.82, 0.34, 1.06), (x, 1.15, 1.32), NAVY_LIT)

    # The dark open cockpit is broad and low, with short side bolsters that do
    # not cover the driver's wings. A second dark inset marks the tail channel.
    ell(cockpit, (1.56, 0.16, 1.30), (0, 1.28, 0.16), TIRE)
    ell(cockpit, (0.68, 0.14, 1.84), (0, 1.15, 1.00), TIRE)
    for x in (-0.84, 0.84):
        ell(cockpit, (0.23, 0.34, 1.35), (x, 1.22, 0.16), MIDNIGHT)
    ell(cockpit, (1.40, 0.32, 0.24), (0, 1.32, 0.78), MIDNIGHT)
    parts["Chassis"] = [(chassis, 0), (cockpit, 2)]

    accent, glow = base.Geo(), base.Geo()

    # Gold architectural rails are embedded into the body along the full
    # wheelbase. Cross-members and hood ribs make the trim structural.
    for x in (-1.08, 1.08):
        branch(accent, (x, 0.72, -1.73), (x, 0.76, 1.60), 0.065, GOLD_DARK)
        branch(accent, (x, 0.88, -1.55), (x, 1.06, -0.68), 0.052, GOLD)
    for z in (-1.72, 1.62):
        branch(accent, (-1.06, 0.74, z), (1.06, 0.74, z), 0.065, GOLD_DARK)
    for x in (-0.52, 0.52):
        branch(accent, (x, 1.08, -1.86), (x, 1.20, -0.83), 0.052, GOLD)

    # Low swept prow blades echo dragon horns without becoming weapons.
    for side in (-1, 1):
        branch(
            accent,
            (side * 0.93, 0.84, -1.66),
            (side * 1.18, 0.72, -2.02),
            0.075,
            GOLD,
        )
        branch(
            accent,
            (side * 1.18, 0.72, -2.02),
            (side * 0.88, 0.68, -2.19),
            0.055,
            GOLD,
        )

    # Joined chevrons read as scale trim without becoming detached gold dots.
    scale_count = 4 if LOD == "LOD0" else 3 if LOD == "LOD1" else 2
    for side in (-1, 1):
        for index in range(scale_count):
            z = -0.64 + index * (1.62 / max(1, scale_count - 1))
            branch(
                accent,
                (side * 1.04, 0.87, z + 0.20),
                (side * 1.16, 1.03, z),
                0.045,
                GOLD,
                capped=False,
            )
            branch(
                accent,
                (side * 1.16, 1.03, z),
                (side * 1.04, 0.87, z - 0.20),
                0.045,
                GOLD,
                capped=False,
            )

    # Gold channel rails continue behind the cockpit and physically overlap
    # the rear shoulders. The central opening remains clear for the long tail.
    for x in (-0.37, 0.37):
        branch(accent, (x, 1.19, 0.62), (x, 1.08, 1.79), 0.052, GOLD)
    branch(accent, (-0.37, 1.08, 1.77), (0.37, 1.08, 1.77), 0.052, GOLD_DARK)

    add_nose_shield(accent, glow)

    # Jewel headlamps sit inside gold housings attached to the upper prow.
    for x in (-0.72, 0.72):
        ell(accent, (0.52, 0.30, 0.30), (x, 1.11, -1.79), GOLD)
        ell(glow, (0.34, 0.20, 0.22), (x, 1.13, -1.95), JEWEL)
    parts["AccentMesh"] = [(accent, 1), (glow, 3)]

    # Exactly one modeled steering control. Its column terminates inside the
    # dashboard so no floating shaft appears in three-quarter views.
    steering = base.Geo()
    tilt = math.radians(16)
    steering.add(
        base.transform(
            base.torus(0.33, 0.055, DETAIL["round"], DETAIL["tube"], "y", GOLD),
            rotation=base.rot_x(math.pi / 2 + tilt),
        )
    )
    for angle in (0, math.tau / 3, math.tau * 2 / 3):
        steering.add(
            base.transform(
                base.box((0.46, 0.044, 0.044), GOLD_DARK),
                rotation=base.rot_x(tilt) @ rot_z(angle),
            )
        )
    ell(steering, (0.18, 0.18, 0.10), (0, 0, 0), JEWEL, base.rot_x(tilt))
    cyl(
        steering,
        0.068,
        0.84,
        (0, -0.30, -0.30),
        "z",
        GOLD_DARK,
        base.rot_x(math.radians(135)),
    )
    cyl(
        steering,
        0.12,
        0.18,
        (0, -0.58, -0.58),
        "z",
        NAVY,
        base.rot_x(math.radians(135)),
    )
    parts["SteeringWheel"] = [(steering, 1)]

    for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"):
        tire, hub, jewel = base.Geo(), base.Geo(), base.Geo()
        tire.add(base.torus(0.51, 0.20, DETAIL["round"], DETAIL["tube"], "x", TIRE))
        tire.add(base.torus(0.46, 0.055, DETAIL["round"], DETAIL["tube"], "x", GOLD_DARK))
        cyl(hub, 0.29, 0.38, (0, 0, 0), "x", GOLD)
        cyl(hub, 0.20, 0.42, (0, 0, 0), "x", NAVY)
        ell(jewel, (0.18, 0.16, 0.16), (0, 0, 0), JEWEL)
        parts[name] = [(tire, 2), (hub, 1), (jewel, 3)]

    for name in ("Exhaust_L", "Exhaust_R"):
        exhaust, magic = base.Geo(), base.Geo()
        cyl(exhaust, 0.17, 0.62, (0, 0, 0), "z", GOLD_DARK, base.rot_x(-0.10))
        exhaust.add(
            base.transform(
                base.torus(0.18, 0.045, DETAIL["round"], DETAIL["tube"], "x", GOLD),
                (0, 0, 0.32),
            )
        )
        ell(magic, (0.18, 0.18, 0.42), (0, 0, 0.46), JEWEL)
        parts[name] = [(exhaust, 1), (magic, 3)]
    return parts


TRANSLATIONS = {
    "Chassis": (0, 0, 0),
    "AccentMesh": (0, 0, 0),
    "SteeringWheel": (0, 1.50, -0.45),
    "Wheel_FL": (-1.43, 0.53, -1.12),
    "Wheel_FR": (1.43, 0.53, -1.12),
    "Wheel_RL": (-1.43, 0.53, 1.20),
    "Wheel_RR": (1.43, 0.53, 1.20),
    "Exhaust_L": (-0.66, 0.81, 1.76),
    "Exhaust_R": (0.66, 0.81, 1.76),
    "DriverMount": (0, 1.48, 0.24),
    "ItemMountRear": (0, 1.14, 1.98),
    "ItemMountForward": (0, 0.92, -2.26),
}


MATERIALS = [
    {
        "name": "MidnightRoyalBody",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "metallicFactor": 0.12,
            "roughnessFactor": 0.36,
        },
    },
    {
        "name": "SculptedRoyalGold",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "metallicFactor": 0.72,
            "roughnessFactor": 0.28,
        },
    },
    {
        "name": "SubstantialTireAndCockpit",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.92,
        },
    },
    {
        "name": "BlueJewelLight",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "emissiveFactor": [0.02, 0.30, 0.88],
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "metallicFactor": 0.15,
            "roughnessFactor": 0.24,
        },
    },
]


def main():
    shared.LOD = LOD
    shared.OUT = OUT
    shared.PREVIEW = PREVIEW
    shared.TRANSLATIONS = TRANSLATIONS
    shared.MATERIALS = MATERIALS
    shared.APPROVED_NAME = "The Sovereign Wyrm"
    shared.GENERATOR = "Minigame Mayhem procedural Sovereign Wyrm builder"
    shared.PREVIEW_TITLE = "THE SOVEREIGN WYRM"
    shared.CANDIDATE = "2"
    shared.USE_VERTEX_COLORS = True
    shared.MATERIAL_TEXTURE_RGBA = None
    shared.PREVIEW_MATERIAL_RGBA = None
    shared.PREVIEW_VIEWS = [
        "Front three-quarter: mounted dragon shield at -Z",
        "Rear three-quarter: open tail channel and twin exhausts",
        "Top: broad wing clearance and long cockpit",
        "Left profile: low royal grand-tourer stance",
    ]
    shared.PREVIEW_FOOTER = (
        "Midnight-blue body | structural gold trim | blue jewel lights | "
        "substantial tires | dragon shield | open tail channel"
    )

    parts = build_geometry()
    triangles, doc = shared.export_glb(parts)
    if os.environ.get("SOVEREIGN_WYRM_SKIP_PREVIEW") != "1":
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
