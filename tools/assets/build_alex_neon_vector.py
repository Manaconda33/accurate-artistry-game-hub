"""Build deterministic review GLBs for Alex's Neon Vector.

Set NEON_VECTOR_LOD to LOD0, LOD1, or LOD2; NEON_VECTOR_OUT to the
destination GLB; and NEON_VECTOR_SKIP_PREVIEW=1 for headless builds.
"""

import json
import math
import os
from pathlib import Path

import numpy as np

import build_keeg_mycelial_majesty as shared
import build_manaconda_wayfinder as base


ROOT = Path(__file__).resolve().parent
LOD = os.environ.get("NEON_VECTOR_LOD", "LOD0").upper()
DETAILS = {
    "LOD0": {"round": 16, "tube": 8, "rings": 8, "limit": 25000},
    "LOD1": {"round": 12, "tube": 6, "rings": 6, "limit": 12000},
    "LOD2": {"round": 8, "tube": 4, "rings": 4, "limit": 5000},
}
if LOD not in DETAILS:
    raise ValueError(f"Unknown NEON_VECTOR_LOD: {LOD}")
DETAIL = DETAILS[LOD]
OUT = Path(
    os.environ.get(
        "NEON_VECTOR_OUT",
        ROOT / "candidates/neon-vector-candidate-3.glb",
    )
)
PREVIEW = Path(
    os.environ.get(
        "NEON_VECTOR_PREVIEW",
        ROOT / "candidates/neon-vector-candidate-3-preview.png",
    )
)

GRAPHITE = np.array([0.075, 0.095, 0.170, 1.0], np.float32)
MIDNIGHT = np.array([0.070, 0.155, 0.310, 1.0], np.float32)
NAVY_LIT = np.array([0.10, 0.32, 0.56, 1.0], np.float32)
METAL = np.array([0.36, 0.42, 0.56, 1.0], np.float32)
TIRE = np.array([0.022, 0.028, 0.055, 1.0], np.float32)
CYAN = np.array([0.00, 0.86, 1.00, 1.0], np.float32)
MAGENTA = np.array([1.00, 0.02, 0.72, 1.0], np.float32)
VIOLET = np.array([0.60, 0.10, 1.00, 1.0], np.float32)


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
    """Join two points with a cylindrical structural or circuit member."""
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


def wedge_prism(front_z, rear_z, front_width, rear_width, bottom_y, front_top, rear_top, color):
    """Create a closed, flat-shaded tapered nose wedge."""
    vertices = np.array(
        [
            [-front_width / 2, bottom_y, front_z],
            [front_width / 2, bottom_y, front_z],
            [-front_width / 2, front_top, front_z],
            [front_width / 2, front_top, front_z],
            [-rear_width / 2, bottom_y, rear_z],
            [rear_width / 2, bottom_y, rear_z],
            [-rear_width / 2, rear_top, rear_z],
            [rear_width / 2, rear_top, rear_z],
        ],
        dtype=float,
    )
    faces = (
        (0, 1, 3), (0, 3, 2),
        (4, 7, 5), (4, 6, 7),
        (0, 4, 5), (0, 5, 1),
        (2, 3, 7), (2, 7, 6),
        (0, 2, 6), (0, 6, 4),
        (1, 5, 7), (1, 7, 3),
    )
    positions, normals, indices = [], [], []
    for face in faces:
        tri = vertices[list(face)]
        normal = np.cross(tri[1] - tri[0], tri[2] - tri[0])
        normal /= max(np.linalg.norm(normal), 1e-9)
        start = len(positions)
        positions.extend(tri)
        normals.extend([normal] * 3)
        indices.extend((start, start + 1, start + 2))
    return positions, normals, color, indices


def triangle_lines(geo, center, width, height, color, plane="xz", radius=0.032):
    """Make an attached three-segment play triangle."""
    x, y, z = center
    if plane == "xz":
        points = [
            (x - width / 2, y, z - height / 2),
            (x + width / 2, y, z),
            (x - width / 2, y, z + height / 2),
        ]
    else:  # yz plane, used on both faces of a wheel hub
        points = [
            (x, y - height / 2, z - width / 2),
            (x, y, z + width / 2),
            (x, y + height / 2, z - width / 2),
        ]
    for start, end in zip(points, points[1:] + points[:1]):
        branch(geo, start, end, radius, color, capped=False)


def hood_surface_y(z):
    """Top surface of the upper tapered prow, plus a tiny embedded offset."""
    ratio = np.clip((z + 1.90) / 1.24, 0.0, 1.0)
    return 0.87 + ratio * (1.15 - 0.87) + 0.006


def build_geometry():
    parts = {}

    chassis, cockpit = base.Geo(), base.Geo()
    # Compact central tub: low mass, narrow shoulders, exposed wheels.
    ell(chassis, (1.90, 0.42, 3.52), (0, 0.58, -0.02), GRAPHITE)
    ell(chassis, (1.68, 0.40, 2.90), (0, 0.76, -0.18), MIDNIGHT)
    # Layered faceted nose and rear deck.
    chassis.add(wedge_prism(-2.02, -0.42, 0.72, 1.54, 0.55, 0.75, 1.08, MIDNIGHT))
    chassis.add(wedge_prism(-1.90, -0.66, 0.46, 1.10, 0.78, 0.87, 1.15, NAVY_LIT))
    for x in (-0.53, 0.53):
        ell(chassis, (0.74, 0.48, 1.14), (x, 0.80, 1.12), MIDNIGHT)
    # Recessed seat, short bolsters and backrest keep the cockpit open.
    ell(cockpit, (1.20, 0.14, 1.18), (0, 1.03, 0.14), TIRE)
    ell(cockpit, (0.94, 0.22, 0.82), (0, 1.10, 0.34), GRAPHITE)
    for x in (-0.67, 0.67):
        ell(cockpit, (0.20, 0.30, 1.18), (x, 1.07, 0.18), GRAPHITE)
    box(cockpit, (1.10, 0.54, 0.18), (0, 1.28, 0.78), GRAPHITE, base.rot_x(-0.08))
    parts["Chassis"] = [(chassis, 0), (cockpit, 2)]

    accent, cyan_glow, magenta_glow = base.Geo(), base.Geo(), base.Geo()
    # A continuous lower perimeter and compact front splitter.
    for x in (-0.92, 0.92):
        branch(accent, (x, 0.52, -1.55), (x, 0.54, 1.42), 0.055, METAL)
    branch(accent, (-0.92, 0.52, -1.55), (0.92, 0.52, -1.55), 0.055, METAL)
    branch(accent, (-0.92, 0.54, 1.42), (0.92, 0.54, 1.42), 0.055, METAL)
    box(accent, (2.16, 0.12, 0.28), (0, 0.42, -1.91), GRAPHITE)
    for x in (-0.82, 0.82):
        box(accent, (0.42, 0.18, 0.48), (x, 0.49, -1.77), MIDNIGHT, base.rot_x(-0.05))
        branch(accent, (x * 0.72, 0.56, -1.54), (x, 0.50, -1.82), 0.060, METAL)

    # Exposed double-wishbone members visibly connect every hub to the tub.
    for x in (-1, 1):
        for z in (-1.12, 1.10):
            branch(accent, (x * 0.76, 0.49, z - 0.20), (x * 1.27, 0.49, z), 0.044, METAL)
            branch(accent, (x * 0.76, 0.73, z + 0.18), (x * 1.27, 0.53, z), 0.040, METAL)

    # Every nose segment follows the sloped prow and is slightly embedded.
    # This replaces Candidate 1's floating constant-height cylinders.
    nose_triangle = [
        (-0.24, hood_surface_y(-1.63), -1.63),
        (0.24, hood_surface_y(-1.36), -1.36),
        (-0.24, hood_surface_y(-1.09), -1.09),
    ]
    for start, end in zip(nose_triangle, nose_triangle[1:] + nose_triangle[:1]):
        branch(magenta_glow, start, end, 0.022, MAGENTA, capped=False)
    branch(
        cyan_glow,
        (0, hood_surface_y(-1.08), -1.08),
        (0, hood_surface_y(-0.74), -0.74),
        0.018,
        CYAN,
        capped=False,
    )
    for side, target in ((-1, cyan_glow), (1, magenta_glow)):
        branch(
            target,
            (side * 0.20, hood_surface_y(-1.02), -1.02),
            (side * 0.42, hood_surface_y(-0.65), -0.65),
            0.018,
            CYAN if side < 0 else MAGENTA,
            capped=False,
        )
        # Rear circuitry is embedded into the shoulder pods.
        branch(
            target,
            (side * 0.54, 1.015, 0.70),
            (side * 0.58, 1.005, 1.20),
            0.018,
            CYAN if side < 0 else MAGENTA,
            capped=False,
        )

    # Structural rear bridge carries the two exhaust nodes.
    branch(accent, (-0.70, 0.82, 1.36), (0.70, 0.82, 1.36), 0.070, METAL)
    # Two exposed neon conduits connect the cockpit back to the forward face
    # of each thruster. Their raised route clears the rear shoulder volumes;
    # the endpoints alone are slightly seated to make both connections solid.
    for side, target, color in (
        (-1, cyan_glow, CYAN),
        (1, magenta_glow, MAGENTA),
    ):
        x = side * 0.63
        points = [
            (x, 1.25, 0.73),
            (x, 1.37, 0.98),
            (x, 1.42, 1.20),
            (x, 1.29, 1.37),
        ]
        for start, end in zip(points, points[1:]):
            branch(target, start, end, 0.050, color, capped=False)
        for point in points[1:-1]:
            ell(target, (0.105, 0.105, 0.105), point, color)
    parts["AccentMesh"] = [(accent, 0), (cyan_glow, 1), (magenta_glow, 3)]

    # Exactly one modeled steering wheel with a visible dashboard termination.
    steering = base.Geo()
    tilt = math.radians(17)
    steering.add(
        base.transform(
            base.torus(0.33, 0.050, DETAIL["round"], DETAIL["tube"], "y", TIRE),
            rotation=base.rot_x(math.pi / 2 + tilt),
        )
    )
    for angle in (0, math.tau / 3, math.tau * 2 / 3):
        steering.add(
            base.transform(
                base.box((0.46, 0.040, 0.040), METAL),
                rotation=base.rot_x(tilt) @ rot_z(angle),
            )
        )
    # No emblem intersects the wheel: Candidate 1's rogue central triangle is removed.
    cyl(steering, 0.062, 0.72, (0, -0.26, -0.26), "z", METAL, base.rot_x(math.radians(135)))
    cyl(steering, 0.105, 0.16, (0, -0.51, -0.51), "z", MIDNIGHT, base.rot_x(math.radians(135)))
    parts["SteeringWheel"] = [(steering, 0)]

    for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"):
        tire, hub, cyan_ring, magenta_ring, hub_mark = (
            base.Geo(), base.Geo(), base.Geo(), base.Geo(), base.Geo()
        )
        tire.add(base.torus(0.48, 0.18, DETAIL["round"], DETAIL["tube"], "x", TIRE))
        cyan_ring.add(base.torus(0.46, 0.042, DETAIL["round"], DETAIL["tube"], "x", CYAN))
        magenta_ring.add(base.torus(0.34, 0.040, DETAIL["round"], DETAIL["tube"], "x", MAGENTA))
        cyl(hub, 0.27, 0.34, (0, 0, 0), "x", GRAPHITE)
        cyl(hub, 0.18, 0.39, (0, 0, 0), "x", METAL)
        for face in (-0.205, 0.205):
            triangle_lines(hub_mark, (face, 0, 0), 0.24, 0.27, MAGENTA, plane="yz", radius=0.018)
        parts[name] = [
            (tire, 2), (hub, 0), (cyan_ring, 1), (magenta_ring, 3), (hub_mark, 3)
        ]

    for name in ("Exhaust_L", "Exhaust_R"):
        exhaust, energy = base.Geo(), base.Geo()
        box(exhaust, (0.50, 0.48, 0.56), (0, 0, -0.02), MIDNIGHT, base.rot_x(-0.08))
        box(exhaust, (0.38, 0.34, 0.62), (0, 0.02, 0.04), GRAPHITE, base.rot_x(-0.08))
        exhaust.add(
            base.transform(
                base.torus(0.18, 0.045, DETAIL["round"], DETAIL["tube"], "x", MAGENTA),
                (0, 0, 0.31),
            )
        )
        ell(energy, (0.22, 0.20, 0.46), (0, 0.01, 0.52), VIOLET)
        parts[name] = [(exhaust, 0), (energy, 3)]
    return parts


TRANSLATIONS = {
    "Chassis": (0, 0, 0),
    "AccentMesh": (0, 0, 0),
    "SteeringWheel": (0, 1.33, -0.47),
    "Wheel_FL": (-1.40, 0.50, -1.12),
    "Wheel_FR": (1.40, 0.50, -1.12),
    "Wheel_RL": (-1.40, 0.50, 1.10),
    "Wheel_RR": (1.40, 0.50, 1.10),
    "Exhaust_L": (-0.63, 1.08, 1.64),
    "Exhaust_R": (0.63, 1.08, 1.64),
    "DriverMount": (0, 1.42, 0.18),
    "ItemMountRear": (0, 1.10, 1.98),
    "ItemMountForward": (0, 0.83, -2.10),
}


MATERIALS = [
    {
        "name": "GraphiteMidnightBodyAndStructure",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.055, 0.095, 0.20, 1],
            "metallicFactor": 0.38,
            "roughnessFactor": 0.28,
        },
    },
    {
        "name": "CyanVectorGlow",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.0, 0.72, 1.0, 1],
            "metallicFactor": 0.12,
            "roughnessFactor": 0.20,
        },
        "emissiveFactor": [0.0, 0.58, 0.82],
    },
    {
        "name": "WidePerformanceTire",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.012, 0.016, 0.032, 1],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.92,
        },
    },
    {
        "name": "MagentaVioletVectorGlow",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "emissiveFactor": [0.72, 0.01, 0.46],
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.96, 0.025, 0.66, 1],
            "metallicFactor": 0.12,
            "roughnessFactor": 0.20,
        },
    },
]


def main():
    shared.LOD = LOD
    shared.OUT = OUT
    shared.PREVIEW = PREVIEW
    shared.TRANSLATIONS = TRANSLATIONS
    shared.MATERIALS = MATERIALS
    shared.APPROVED_NAME = "The Neon Vector"
    shared.GENERATOR = "Minigame Mayhem procedural Neon Vector builder"
    shared.PREVIEW_TITLE = "THE NEON VECTOR"
    shared.CANDIDATE = "3"
    shared.USE_VERTEX_COLORS = False
    shared.MATERIAL_TEXTURE_RGBA = None
    shared.PREVIEW_MATERIAL_RGBA = [
        (18, 34, 74, 255),
        (0, 210, 255, 255),
        (7, 9, 22, 255),
        (255, 24, 178, 255),
    ]
    shared.PREVIEW_VIEWS = [
        "Front three-quarter • mounted play-triangle nose",
        "Rear three-quarter • bridged twin vector exhausts",
        "Top • compact open cockpit and circuit paths",
        "Left profile • low feather-sprinter stance",
    ]
    shared.PREVIEW_FOOTER = (
        "Graphite/navy faceted tub | cyan/magenta circuitry | ring-lit open wheels | "
        "single steering wheel | twin violet exhausts"
    )

    parts = build_geometry()
    triangles, doc = shared.export_glb(parts)
    if os.environ.get("NEON_VECTOR_SKIP_PREVIEW") != "1":
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
        json.dumps(
            {
                "glb": str(OUT),
                "preview": str(PREVIEW),
                "lod": LOD,
                "triangles": triangles,
                "triangleLimit": DETAIL["limit"],
                "materials": len(doc["materials"]),
                "nodes": len(doc["nodes"]),
                "bytes": OUT.stat().st_size,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
