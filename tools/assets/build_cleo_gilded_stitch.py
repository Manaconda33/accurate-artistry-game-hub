"""Build deterministic GLBs and a review sheet for Cleo's Gilded Stitch.

Set GILDED_STITCH_LOD to LOD0, LOD1, or LOD2; GILDED_STITCH_OUT to the
destination GLB; and GILDED_STITCH_SKIP_PREVIEW=1 for a headless build.
"""

import json
import math
import os
import struct
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import build_manaconda_wayfinder as base


ROOT = Path(__file__).resolve().parent
LOD = os.environ.get("GILDED_STITCH_LOD", "LOD0").upper()
DETAILS = {
    "LOD0": {"round": 16, "tube": 6, "scroll": 7, "limit": 25000},
    "LOD1": {"round": 14, "tube": 6, "scroll": 6, "limit": 12000},
    "LOD2": {"round": 8, "tube": 4, "scroll": 3, "limit": 5000},
}
if LOD not in DETAILS:
    raise ValueError(f"Unknown GILDED_STITCH_LOD: {LOD}")
DETAIL = DETAILS[LOD]
OUT = Path(os.environ.get("GILDED_STITCH_OUT", ROOT / "candidates/gilded-stitch-candidate-3.glb"))
PREVIEW = Path(
    os.environ.get(
        "GILDED_STITCH_PREVIEW",
        ROOT / "candidates/gilded-stitch-candidate-3-preview.png",
    )
)
CANDIDATE = os.environ.get("GILDED_STITCH_CANDIDATE", "3")

NAVY = np.array([0.025, 0.07, 0.16, 1.0], np.float32)
NAVY_LIT = np.array([0.055, 0.13, 0.27, 1.0], np.float32)
GOLD = np.array([0.78, 0.43, 0.10, 1.0], np.float32)
BRASS = np.array([0.56, 0.27, 0.055, 1.0], np.float32)
WOOD = np.array([0.46, 0.20, 0.065, 1.0], np.float32)
WOOD_LIT = np.array([0.72, 0.40, 0.14, 1.0], np.float32)
DARK = np.array([0.018, 0.025, 0.045, 1.0], np.float32)
STEEL = np.array([0.46, 0.50, 0.55, 1.0], np.float32)


def add_box(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.box(size, color), at, rotation))


def add_ellipsoid(geo, size, at, color, rotation=None):
    geo.add(
        base.transform(
            base.ellipsoid(
                size,
                DETAIL["round"],
                max(5, DETAIL["round"] // 2),
                color,
            ),
            at,
            rotation,
        )
    )


def add_cyl(geo, radius, length, at, axis, color, rotation=None, seg=None):
    geo.add(
        base.transform(
            base.cylinder(radius, length, seg or DETAIL["round"], axis, color),
            at,
            rotation,
        )
    )


def rot_z(angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def align_z(direction):
    """Return a rotation matrix aligning local positive Z with direction."""
    target = np.asarray(direction, float)
    target /= max(np.linalg.norm(target), 1e-9)
    source = np.array([0.0, 0.0, 1.0])
    cross = np.cross(source, target)
    sine = np.linalg.norm(cross)
    cosine = float(np.dot(source, target))
    if sine < 1e-9:
        return np.eye(3) if cosine > 0 else base.rot_x(math.pi)
    axis = cross / sine
    skew = np.array(
        [[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]]
    )
    return np.eye(3) + skew * sine + (skew @ skew) * (1 - cosine)


def add_segment(geo, start, end, radius, color):
    start, end = np.asarray(start, float), np.asarray(end, float)
    vector = end - start
    length = np.linalg.norm(vector)
    midpoint = (start + end) / 2
    add_cyl(
        geo,
        radius,
        length,
        midpoint,
        "z",
        color,
        align_z(vector),
        max(8, DETAIL["round"]),
    )


def gold_scroll(geo, center, side=1, scale=1.0):
    """Build a continuous shallow S-curve inlay attached to a side panel."""
    count = max(5, DETAIL["scroll"] + 2)
    points = []
    for index in range(count):
        t = index / (count - 1)
        points.append(
            (
                center[0] + side * 0.008,
                center[1] + scale * 0.10 * math.sin(t * math.pi * 2),
                center[2] + scale * 0.62 * (t - 0.5),
            )
        )
    for start, end in zip(points, points[1:]):
        add_segment(geo, start, end, scale * 0.026, GOLD)
    # Two attached leaves make the continuous line read as floral scrollwork.
    for index, tilt in ((2, 0.55), (count - 3, -0.55)):
        point = points[index]
        add_ellipsoid(
            geo,
            (scale * 0.055, scale * 0.10, scale * 0.20),
            point,
            GOLD,
            base.rot_x(tilt),
        )


def build_geometry():
    parts = {}

    chassis, inset = base.Geo(), base.Geo()
    # A low sewing-machine table/base defines the kart silhouette.
    add_box(chassis, (2.38, 0.34, 3.55), (0, 0.58, 0.05), NAVY)
    add_box(chassis, (2.16, 0.18, 3.28), (0, 0.80, 0.05), NAVY_LIT)
    add_box(chassis, (2.30, 0.14, 0.28), (0, 0.88, -1.52), GOLD)
    add_box(chassis, (2.30, 0.14, 0.24), (0, 0.88, 1.54), GOLD)
    # The cockpit is deliberately rear-biased, reserving the front half of the
    # table for a clear sewing-machine silhouette and exposed needle assembly.
    add_ellipsoid(inset, (1.40, 0.12, 0.98), (0, 0.93, 0.88), DARK)
    for x in (-0.74, 0.74):
        add_ellipsoid(inset, (0.20, 0.38, 1.18), (x, 1.05, 0.88), NAVY)
    add_ellipsoid(inset, (1.55, 0.30, 0.24), (0, 1.06, 1.38), NAVY)
    parts["Chassis"] = [(chassis, 0), (inset, 3)]

    machine, ornament, hardware = base.Geo(), base.Geo(), base.Geo()
    # Definitive vintage sewing-machine silhouette at authored -Z front: a
    # tall rear pillar, long overhanging arm, open throat, and needle at the
    # extreme nose. This replaces Candidate 1's block-like front housing.
    add_box(machine, (1.34, 1.34, 0.54), (0, 1.48, -0.48), NAVY)
    add_ellipsoid(machine, (1.46, 0.55, 1.48), (0, 2.02, -1.02), NAVY_LIT)
    add_box(machine, (1.36, 0.38, 1.24), (0, 2.00, -1.04), NAVY_LIT)
    add_ellipsoid(machine, (1.38, 0.48, 0.54), (0, 1.98, -1.55), NAVY_LIT)
    # Raised throat plate, descending needle bar, needle, and presser foot.
    add_box(hardware, (0.82, 0.08, 0.52), (0, 1.04, -1.49), GOLD)
    add_cyl(hardware, 0.075, 0.66, (0, 1.61, -1.56), "y", BRASS)
    add_cyl(hardware, 0.025, 0.62, (0, 1.27, -1.56), "y", STEEL)
    add_box(hardware, (0.36, 0.06, 0.26), (0, 1.06, -1.56), STEEL)
    add_box(hardware, (0.08, 0.20, 0.22), (0.15, 1.16, -1.56), BRASS)

    # Top thread spool and spindle.
    add_cyl(ornament, 0.20, 0.52, (-0.34, 2.46, -0.62), "y", WOOD_LIT)
    add_cyl(ornament, 0.25, 0.08, (-0.34, 2.71, -0.62), "y", GOLD)
    add_cyl(ornament, 0.25, 0.08, (-0.34, 2.21, -0.62), "y", GOLD)
    add_cyl(hardware, 0.035, 0.66, (-0.34, 2.48, -0.62), "y", STEEL)

    # Candidate 1's side handwheel was visually indistinguishable from the
    # steering wheel. Use a narrow rectangular maker's plate instead.
    add_box(ornament, (0.10, 0.24, 0.54), (-0.70, 1.62, -0.46), GOLD)

    # Continuous gilded inlays intersect the navy side panels; no detached
    # beads or floating ornament meshes are used.
    for side in (-1, 1):
        for z in (-0.72, 0.02, 0.76):
            gold_scroll(ornament, (side * 1.195, 0.62, z), side, 0.62)
        add_cyl(ornament, 0.035, 2.86, (side * 1.19, 0.83, 0.02), "z", GOLD)
    add_box(ornament, (0.88, 0.055, 0.08), (0, 1.91, -1.335), GOLD)
    add_box(ornament, (0.52, 0.055, 0.08), (0, 1.76, -1.335), GOLD)
    parts["AccentMesh"] = [(machine, 0), (ornament, 1), (hardware, 3)]

    # A compact gilded steering wheel sits behind the machine head, with its
    # column on the nose-facing side and a visible dashboard connection.
    steering = base.Geo()
    steering.add(
        base.transform(
            base.torus(0.33, 0.055, DETAIL["round"], DETAIL["tube"], "y", GOLD),
            rotation=base.rot_x(math.pi / 2),
        )
    )
    for angle in (0, math.pi * 2 / 3, math.pi * 4 / 3):
        steering.add(
            base.transform(
                base.box((0.50, 0.04, 0.04), BRASS), rotation=rot_z(angle)
            )
        )
    add_cyl(steering, 0.085, 0.10, (0, 0, 0), "z", GOLD)
    add_box(steering, (0.66, 0.28, 0.38), (0, -0.50, -0.12), NAVY)
    add_box(steering, (0.48, 0.13, 0.24), (0, -0.37, -0.10), GOLD)
    add_cyl(steering, 0.065, 0.52, (0, -0.25, -0.10), "y", BRASS)
    parts["SteeringWheel"] = [(steering, 1)]

    # Wooden spool wheels use flanged faces, wound thread grooves, and gold hubs.
    for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"):
        wheel, hub = base.Geo(), base.Geo()
        add_cyl(wheel, 0.43, 0.34, (0, 0, 0), "x", WOOD)
        for x in (-0.20, 0.20):
            add_cyl(wheel, 0.50, 0.10, (x, 0, 0), "x", WOOD_LIT)
        for x in (-0.13, -0.065, 0, 0.065, 0.13):
            wheel.add(
                base.transform(
                    base.torus(
                        0.38,
                        0.018,
                        DETAIL["round"],
                        max(4, DETAIL["tube"] - 2),
                        "x",
                        GOLD,
                    ),
                    (x, 0, 0),
                )
            )
        add_cyl(hub, 0.13, 0.48, (0, 0, 0), "x", GOLD)
        parts[name] = [(wheel, 2), (hub, 1)]

    for name in ("Exhaust_L", "Exhaust_R"):
        exhaust = base.Geo()
        add_cyl(exhaust, 0.12, 0.62, (0, 0, 0), "z", BRASS)
        exhaust.add(
            base.transform(
                base.torus(
                    0.13,
                    0.032,
                    DETAIL["round"],
                    DETAIL["tube"],
                    "x",
                    GOLD,
                ),
                (0, 0, 0.31),
            )
        )
        parts[name] = [(exhaust, 1)]
    return parts


TRANSLATIONS = {
    "Chassis": (0, 0, 0),
    "AccentMesh": (0, 0, 0),
    "SteeringWheel": (0, 1.66, 0.34),
    "Wheel_FL": (-1.56, 0.51, -1.08),
    "Wheel_FR": (1.56, 0.51, -1.08),
    "Wheel_RL": (-1.56, 0.51, 1.10),
    "Wheel_RR": (1.56, 0.51, 1.10),
    "Exhaust_L": (-0.62, 0.75, 1.76),
    "Exhaust_R": (0.62, 0.75, 1.76),
    "DriverMount": (0, 1.42, 0.92),
    "ItemMountRear": (0, 1.12, 1.98),
    "ItemMountForward": (0, 0.92, -2.02),
}

MATERIALS = [
    {
        "name": "NavyEnamel",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "metallicFactor": 0.28,
            "roughnessFactor": 0.34,
        },
    },
    {
        "name": "GildedBrass",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "metallicFactor": 0.72,
            "roughnessFactor": 0.28,
        },
    },
    {
        "name": "WarmSpoolWood",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "metallicFactor": 0.02,
            "roughnessFactor": 0.76,
        },
    },
    {
        "name": "DarkAndSteelHardware",
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "metallicFactor": 0.52,
            "roughnessFactor": 0.42,
        },
    },
]


def export_glb(parts):
    doc = {
        "asset": {
            "version": "2.0",
            "generator": "Minigame Mayhem procedural Gilded Stitch builder",
        },
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [],
        "meshes": [],
        "materials": MATERIALS,
        "buffers": [{}],
        "bufferViews": [],
        "accessors": [],
        "extras": {
            "lod": LOD,
            "forward": "-Z",
            "units": "meters",
            "approvedName": "The Gilded Stitch",
        },
    }
    blob = bytearray()

    def accessor(array, kind, component, target=None, minmax=False):
        while len(blob) % 4:
            blob.append(0)
        offset = len(blob)
        raw = array.tobytes()
        blob.extend(raw)
        view = {"buffer": 0, "byteOffset": offset, "byteLength": len(raw)}
        if target:
            view["target"] = target
        doc["bufferViews"].append(view)
        item = {
            "bufferView": len(doc["bufferViews"]) - 1,
            "componentType": component,
            "count": len(array),
            "type": kind,
        }
        if minmax:
            item.update(min=array.min(axis=0).tolist(), max=array.max(axis=0).tolist())
        doc["accessors"].append(item)
        return len(doc["accessors"]) - 1

    mesh_index, total_triangles = {}, 0
    for name, primitives in parts.items():
        exported = []
        for geo, material in primitives:
            positions, normals, colors, indices = geo.arrays()
            total_triangles += len(indices) // 3
            packed_indices = indices.astype(
                np.uint16 if len(positions) < 65536 else np.uint32
            )
            exported.append(
                {
                    "attributes": {
                        "POSITION": accessor(positions, "VEC3", 5126, 34962, True),
                        "NORMAL": accessor(normals, "VEC3", 5126, 34962),
                        "COLOR_0": accessor(colors, "VEC4", 5126, 34962),
                    },
                    "indices": accessor(
                        packed_indices,
                        "SCALAR",
                        5123 if packed_indices.dtype == np.uint16 else 5125,
                        34963,
                    ),
                    "material": material,
                    "mode": 4,
                }
            )
        doc["meshes"].append({"name": name, "primitives": exported})
        mesh_index[name] = len(doc["meshes"]) - 1

    names = [
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
    ]
    doc["nodes"].append(
        {
            "name": "KartRoot",
            "children": list(range(1, len(names))),
            "extras": {"triangleCount": total_triangles, "principalMaterials": 4},
        }
    )
    for name in names[1:]:
        node = {"name": name, "translation": TRANSLATIONS[name]}
        if name in mesh_index:
            node["mesh"] = mesh_index[name]
        doc["nodes"].append(node)

    doc["buffers"][0]["byteLength"] = len(blob)
    json_chunk = json.dumps(doc, separators=(",", ":")).encode()
    json_chunk += b" " * ((4 - len(json_chunk) % 4) % 4)
    blob += b"\0" * ((4 - len(blob) % 4) % 4)
    total_bytes = 12 + 8 + len(json_chunk) + 8 + len(blob)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(
        struct.pack("<4sII", b"glTF", 2, total_bytes)
        + struct.pack("<I4s", len(json_chunk), b"JSON")
        + json_chunk
        + struct.pack("<I4s", len(blob), b"BIN\0")
        + blob
    )
    return total_triangles, doc


def preview(parts):
    triangles, colors = [], []
    light = np.array([-0.45, 0.85, -0.30])
    light /= np.linalg.norm(light)
    for name, primitives in parts.items():
        translation = np.asarray(TRANSLATIONS[name])
        for geo, _material in primitives:
            positions, _normals, vertex_colors, indices = geo.arrays()
            positions = positions + translation
            for tri_indices in indices.reshape(-1, 3):
                tri = positions[tri_indices]
                normal = np.cross(tri[1] - tri[0], tri[2] - tri[0])
                length = np.linalg.norm(normal)
                if length < 1e-9:
                    continue
                normal /= length
                shade = 0.64 + 0.36 * max(0, float(np.dot(normal, light)))
                color = vertex_colors[tri_indices].mean(axis=0).copy()
                color[:3] = np.clip(color[:3] * shade + 0.035, 0, 1)
                triangles.append(tri[:, [0, 2, 1]])
                colors.append(color)
    fig = plt.figure(figsize=(14, 12), dpi=150, facecolor="#090d18")
    views = [
        (20, -42, "Front three-quarter • machine head at -Z"),
        (20, 138, "Rear three-quarter • cockpit clearance"),
        (70, -90, "Top geometry • table silhouette"),
        (10, -90, "Left profile • sewing-machine read"),
    ]
    for index, (elevation, azimuth, title) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, index, projection="3d", computed_zorder=False)
        ax.set_facecolor("#090d18")
        ax.add_collection3d(
            Poly3DCollection(
                triangles,
                facecolors=colors,
                edgecolor=(0, 0, 0, 0.10),
                linewidth=0.12,
            )
        )
        ax.set_xlim(-2.05, 2.05)
        ax.set_ylim(-2.20, 2.20)
        ax.set_zlim(0, 2.65)
        ax.set_box_aspect((4.1, 4.4, 2.65))
        ax.view_init(elevation, azimuth)
        ax.set_axis_off()
        ax.set_title(title, color="#fff0c5", fontsize=14, pad=4)
    fig.suptitle(
        f"THE GILDED STITCH • {LOD} CANDIDATE {CANDIDATE}",
        color="#e6ad43",
        fontsize=21,
        fontweight="bold",
        y=0.98,
    )
    fig.text(
        0.5,
        0.018,
        "Navy enamel • raised gold scrollwork • wooden spool wheels • working sewing-machine silhouette",
        ha="center",
        color="#d7c294",
        fontsize=11,
    )
    plt.subplots_adjust(
        left=0.01,
        right=0.99,
        top=0.94,
        bottom=0.04,
        wspace=0.01,
        hspace=0.02,
    )
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PREVIEW, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    parts = build_geometry()
    triangles, doc = export_glb(parts)
    if os.environ.get("GILDED_STITCH_SKIP_PREVIEW") != "1":
        preview(parts)
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
    assert len(doc["materials"]) <= 4
    print(
        json.dumps(
            {
                "glb": str(OUT),
                "preview": str(PREVIEW),
                "lod": LOD,
                "triangleLimit": DETAIL["limit"],
                "triangles": triangles,
                "materials": len(doc["materials"]),
                "nodes": len(doc["nodes"]),
                "bytes": OUT.stat().st_size,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
