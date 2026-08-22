"""Build deterministic GLBs and a review sheet for Krios's The Hornbreaker.

Set HORNBREAKER_LOD to LOD0, LOD1, or LOD2; HORNBREAKER_OUT to the GLB
destination; and HORNBREAKER_SKIP_PREVIEW=1 for headless production builds.
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
LOD = os.environ.get("HORNBREAKER_LOD", "LOD0").upper()
DETAILS = {
    "LOD0": {"round": 12, "tube": 5, "horn": 8, "studs": 8, "limit": 25000},
    "LOD1": {"round": 9, "tube": 4, "horn": 6, "studs": 6, "limit": 12000},
    "LOD2": {"round": 6, "tube": 3, "horn": 4, "studs": 4, "limit": 5000},
}
if LOD not in DETAILS:
    raise ValueError(f"Unknown HORNBREAKER_LOD: {LOD}")
DETAIL = DETAILS[LOD]
OUT = Path(os.environ.get("HORNBREAKER_OUT", ROOT / "candidates/hornbreaker-candidate-1.glb"))
PREVIEW = Path(os.environ.get("HORNBREAKER_PREVIEW", ROOT / "candidates/hornbreaker-candidate-1-preview.png"))
CANDIDATE = os.environ.get("HORNBREAKER_CANDIDATE", "1")

DARK_STEEL = np.array([0.075, 0.065, 0.07, 1.0], np.float32)
GUNMETAL = np.array([0.17, 0.15, 0.16, 1.0], np.float32)
INFERNAL_RED = np.array([0.52, 0.018, 0.012, 1.0], np.float32)
EMBER = np.array([1.0, 0.17, 0.015, 1.0], np.float32)
TIRE = np.array([0.018, 0.014, 0.015, 1.0], np.float32)
HORN = np.array([0.055, 0.045, 0.045, 1.0], np.float32)
BRASS = np.array([0.48, 0.24, 0.055, 1.0], np.float32)


def add_ellipsoid(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.ellipsoid(size, DETAIL["round"], max(5, DETAIL["round"] // 2), color), at, rotation))


def add_box(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.box(size, color), at, rotation))


def add_cyl(geo, radius, length, at, axis, color, rotation=None, seg=None):
    geo.add(base.transform(base.cylinder(radius, length, seg or DETAIL["round"], axis, color), at, rotation))


def rot_z(angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def align_axis(source, target):
    """Return a rotation matrix that aligns one normalized axis to another."""
    source = np.asarray(source, dtype=float); source /= np.linalg.norm(source)
    target = np.asarray(target, dtype=float); target /= np.linalg.norm(target)
    cross = np.cross(source, target); dot = float(np.dot(source, target))
    if np.linalg.norm(cross) < 1e-8:
        return np.eye(3) if dot > 0 else base.rot_x(math.pi)
    skew = np.array([[0, -cross[2], cross[1]],
                     [cross[2], 0, -cross[0]],
                     [-cross[1], cross[0], 0]])
    return np.eye(3) + skew + skew @ skew * ((1 - dot) / np.dot(cross, cross))


def horn_curve(geo, side):
    """Create a single connected, tapered C-shaped ram horn with a pointed tip."""
    # Two joined cubic curves produce a readable ram-horn silhouette from the front:
    # heavy root, outward/downward curl, then an inward-facing spear point.
    controls = np.array([
        [side * 0.72, 1.08, -2.04],  # straight, recessed root at the prow
        [side * 0.72, 1.08, -2.34],
        [side * 1.54, 1.06, -2.43],
        [side * 1.66, 0.65, -2.68],
        [side * 1.62, 0.28, -2.83],
        [side * 1.13, 0.20, -2.94],
        [side * 0.65, 0.49, -3.02],
    ], dtype=float)
    samples_per_half = max(8, DETAIL["horn"] * 2)

    def bezier(points, t):
        u = 1.0 - t
        return (u ** 3 * points[0] + 3 * u * u * t * points[1]
                + 3 * u * t * t * points[2] + t ** 3 * points[3])

    centers = []
    for half, points in enumerate((controls[:4], controls[3:])):
        for index in range(samples_per_half + 1):
            if half and index == 0:
                continue
            centers.append(bezier(points, index / samples_per_half))
    centers = np.asarray(centers)
    ring_segments = max(7, DETAIL["round"])
    positions, normals, colors, indices = [], [], [], []
    last = len(centers) - 1
    for index, center in enumerate(centers):
        t = index / last
        tangent = centers[min(index + 1, last)] - centers[max(index - 1, 0)]
        tangent /= np.linalg.norm(tangent)
        radial_a = np.cross(tangent, np.array([0.0, 0.0, 1.0]))
        radial_a /= np.linalg.norm(radial_a)
        radial_b = np.cross(tangent, radial_a)
        # Pronounced annular growth ridges read as horn texture without disconnected beads.
        taper = (1.0 - t) ** 0.72
        ridge = 1.0 + (0.075 * math.sin(t * math.pi * 18.0) * taper)
        radius = (0.315 * taper + 0.012) * ridge
        if index == last:
            radius = 0.004
        for segment in range(ring_segments):
            angle = 2 * math.pi * segment / ring_segments
            normal = math.cos(angle) * radial_a + math.sin(angle) * radial_b
            positions.append(center + normal * radius)
            normals.append(normal)
            # Alternating subtle warm/dark ridges preserve the black-horn visual lock.
            band = 0.86 + 0.14 * max(0.0, math.sin(t * math.pi * 18.0))
            colors.append(HORN * np.array([band, band, band, 1.0]))
    for ring in range(last):
        for segment in range(ring_segments):
            nxt = (segment + 1) % ring_segments
            a = ring * ring_segments + segment
            b = ring * ring_segments + nxt
            c = (ring + 1) * ring_segments + segment
            d = (ring + 1) * ring_segments + nxt
            indices.extend((a, c, b, b, c, d))
    # Close the root face as well as embedding it in the socket. This prevents the
    # open-tube appearance in GLB/AR viewers even when the camera clips close.
    root_center = len(positions)
    root_tangent = centers[1] - centers[0]
    root_tangent /= np.linalg.norm(root_tangent)
    positions.append(centers[0] - root_tangent * 0.008)
    normals.append(-root_tangent)
    colors.append(HORN)
    for segment in range(ring_segments):
        nxt = (segment + 1) % ring_segments
        indices.extend((root_center, nxt, segment))
    geo.add((positions, normals, colors, indices))


def build_geometry():
    parts = {}
    chassis, cockpit = base.Geo(), base.Geo()
    # Low, broad hot-rod body with an armored prow and open heavyweight cockpit.
    add_ellipsoid(chassis, (2.55, 0.64, 3.70), (0, 0.68, 0.02), DARK_STEEL)
    add_ellipsoid(chassis, (2.18, 0.48, 2.58), (0, 0.97, -0.12), GUNMETAL)
    add_box(chassis, (2.16, 0.28, 0.66), (0, 0.87, -1.63), DARK_STEEL)
    add_box(chassis, (1.72, 0.30, 0.54), (0, 1.06, 1.46), GUNMETAL)
    add_ellipsoid(cockpit, (1.64, 0.18, 1.24), (0, 1.26, 0.28), TIRE)
    for x in (-0.91, 0.91):
        add_ellipsoid(cockpit, (0.29, 0.49, 1.46), (x, 1.27, 0.25), DARK_STEEL)
    add_ellipsoid(cockpit, (1.86, 0.40, 0.31), (0, 1.26, 0.88), DARK_STEEL)
    parts["Chassis"] = [(chassis, 0), (cockpit, 0)]

    accent, horns = base.Geo(), base.Geo()
    # Thick red armor rails and front flame-chevron graphics.
    for x in (-1.03, 1.03):
        add_cyl(accent, 0.07, 2.78, (x, 0.87, -0.02), "z", INFERNAL_RED)
    for z, width in ((-1.47, 1.72), (-1.22, 1.28), (-0.96, 0.86)):
        add_box(accent, (width, 0.075, 0.12), (0, 1.22, z), INFERNAL_RED)
    for side in (-1, 1):
        horn_curve(horns, side)
        # Open, direction-aligned sockets: the horn begins at the front opening
        # instead of intersecting a capped cylinder or decorative solid disc.
        root = np.array([side * 0.72, 1.08, -2.04])
        tangent = np.array([0.0, 0.0, -1.0])
        tangent /= np.linalg.norm(tangent)
        socket_center = root - tangent * 0.17
        horns.add(base.transform(
            base.cylinder(0.40, 0.38, DETAIL["round"], "z", HORN, capped=False),
            socket_center, align_axis((0, 0, 1), tangent)))
        # Seal only the chassis-facing end; the horn-facing mouth stays open.
        add_cyl(horns, 0.40, 0.045, (side * 0.72, 1.08, -1.665), "z", HORN)
        accent.add(base.transform(
            base.torus(0.39, 0.05, DETAIL["round"], max(4, DETAIL["tube"]), "y", BRASS),
            root + tangent * 0.025, align_axis((0, 1, 0), tangent)))
    # One recessed armored yoke fixes both sealed housings into the prow rather
    # than leaving two independent tubes perched on its leading edge.
    add_box(horns, (1.78, 0.70, 0.18), (0, 1.08, -1.61), GUNMETAL)
    add_box(accent, (1.20, 0.10, 0.055), (0, 1.08, -1.715), INFERNAL_RED)
    # Central reinforced battering plate keeps the horn bases visually connected.
    add_box(accent, (1.46, 0.48, 0.24), (0, 0.84, -1.91), GUNMETAL)
    add_box(accent, (0.66, 0.15, 0.09), (0, 0.87, -2.045), INFERNAL_RED)
    parts["AccentMesh"] = [(accent, 1), (horns, 0)]

    steering = base.Geo()
    steering.add(base.transform(
        base.torus(0.38, 0.060, DETAIL["round"], DETAIL["tube"], "y", GUNMETAL),
        rotation=base.rot_x(math.pi / 2),
    ))
    for angle in (0, math.pi * 2 / 3, math.pi * 4 / 3):
        steering.add(base.transform(base.box((0.60, 0.05, 0.05), INFERNAL_RED), rotation=rot_z(angle)))
    add_cyl(steering, 0.095, 0.10, (0, 0, 0), "z", BRASS)
    # Wheel clears the dash; the nose-side column connects directly to an armored pod.
    add_box(steering, (0.72, 0.32, 0.46), (0, -0.55, -0.16), DARK_STEEL)
    add_box(steering, (0.48, 0.17, 0.30), (0, -0.39, -0.12), INFERNAL_RED)
    add_cyl(steering, 0.075, 0.56, (0, -0.26, -0.12), "y", BRASS, base.rot_x(0.08))
    parts["SteeringWheel"] = [(steering, 1)]

    for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"):
        tire, hub = base.Geo(), base.Geo()
        tire.add(base.torus(0.50, 0.22, DETAIL["round"], DETAIL["tube"], "x", TIRE))
        tire.add(base.torus(0.50, 0.055, DETAIL["round"], max(3, DETAIL["tube"] - 2), "x", GUNMETAL))
        add_cyl(hub, 0.19, 0.32, (0, 0, 0), "x", INFERNAL_RED)
        add_cyl(hub, 0.095, 0.40, (0, 0, 0), "x", BRASS)
        for index in range(DETAIL["studs"]):
            angle = 2 * math.pi * index / DETAIL["studs"]
            y, z = 0.57 * math.cos(angle), 0.57 * math.sin(angle)
            for x in (-0.20, 0.20):
                add_ellipsoid(tire, (0.12, 0.15, 0.15), (x, y, z), GUNMETAL)
        parts[name] = [(tire, 2), (hub, 1)]

    for name in ("Exhaust_L", "Exhaust_R"):
        exhaust, fire = base.Geo(), base.Geo()
        add_cyl(exhaust, 0.16, 0.84, (0, 0, 0), "z", GUNMETAL, base.rot_x(-0.14))
        exhaust.add(base.transform(base.torus(0.17, 0.045, DETAIL["round"], DETAIL["tube"], "x", BRASS), (0, 0, 0.40)))
        add_ellipsoid(fire, (0.24, 0.22, 0.76), (0, 0.01, 0.71), EMBER)
        add_ellipsoid(fire, (0.11, 0.10, 0.46), (0, 0.01, 0.97), BRASS)
        parts[name] = [(exhaust, 1), (fire, 3)]
    return parts


TRANSLATIONS = {
    "Chassis": (0, 0, 0), "AccentMesh": (0, 0, 0),
    "SteeringWheel": (0, 1.78, -0.20),
    "Wheel_FL": (-1.48, 0.52, -1.08), "Wheel_FR": (1.48, 0.52, -1.08),
    "Wheel_RL": (-1.48, 0.52, 1.14), "Wheel_RR": (1.48, 0.52, 1.14),
    "Exhaust_L": (-0.69, 0.79, 1.72), "Exhaust_R": (0.69, 0.79, 1.72),
    "DriverMount": (0, 1.54, 0.28), "ItemMountRear": (0, 1.20, 2.05),
    "ItemMountForward": (0, 0.92, -2.20),
}

MATERIALS = [
    {"name": "WeatheredDarkSteel", "alphaMode": "OPAQUE", "doubleSided": True,
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.62, "roughnessFactor": 0.48}},
    {"name": "InfernalRedAndBrass", "alphaMode": "OPAQUE", "doubleSided": True,
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.46, "roughnessFactor": 0.38}},
    {"name": "RuggedTire", "alphaMode": "OPAQUE", "doubleSided": True,
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.03, "roughnessFactor": 0.91}},
    {"name": "ExhaustFlame", "alphaMode": "OPAQUE", "doubleSided": True,
     "emissiveFactor": [0.82, 0.08, 0.01],
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.08, "roughnessFactor": 0.31}},
]


def export_glb(parts):
    doc = {
        "asset": {"version": "2.0", "generator": "Accurate Artistry procedural Hornbreaker builder"},
        "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [], "meshes": [],
        "materials": MATERIALS, "buffers": [{}], "bufferViews": [], "accessors": [],
        "extras": {"lod": LOD, "forward": "-Z", "units": "meters", "approvedName": "The Hornbreaker"},
    }
    blob = bytearray()

    def accessor(array, kind, component, target=None, minmax=False):
        while len(blob) % 4:
            blob.append(0)
        offset = len(blob); raw = array.tobytes(); blob.extend(raw)
        view = {"buffer": 0, "byteOffset": offset, "byteLength": len(raw)}
        if target:
            view["target"] = target
        doc["bufferViews"].append(view)
        item = {"bufferView": len(doc["bufferViews"]) - 1, "componentType": component,
                "count": len(array), "type": kind}
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
            packed = indices.astype(np.uint16 if len(positions) < 65536 else np.uint32)
            exported.append({
                "attributes": {
                    "POSITION": accessor(positions, "VEC3", 5126, 34962, True),
                    "NORMAL": accessor(normals, "VEC3", 5126, 34962),
                    "COLOR_0": accessor(colors, "VEC4", 5126, 34962),
                },
                "indices": accessor(packed, "SCALAR", 5123 if packed.dtype == np.uint16 else 5125, 34963),
                "material": material, "mode": 4,
            })
        doc["meshes"].append({"name": name, "primitives": exported})
        mesh_index[name] = len(doc["meshes"]) - 1

    names = ["KartRoot", "Chassis", "AccentMesh", "SteeringWheel", "Wheel_FL", "Wheel_FR",
             "Wheel_RL", "Wheel_RR", "Exhaust_L", "Exhaust_R", "DriverMount", "ItemMountRear",
             "ItemMountForward"]
    doc["nodes"].append({"name": "KartRoot", "children": list(range(1, len(names))),
                         "extras": {"triangleCount": total_triangles, "principalMaterials": 4}})
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
    OUT.write_bytes(struct.pack("<4sII", b"glTF", 2, total_bytes)
                    + struct.pack("<I4s", len(json_chunk), b"JSON") + json_chunk
                    + struct.pack("<I4s", len(blob), b"BIN\0") + blob)
    return total_triangles, doc


def preview(parts):
    triangles, colors = [], []
    light = np.array([-0.45, 0.85, -0.30]); light /= np.linalg.norm(light)
    for name, primitives in parts.items():
        translation = np.asarray(TRANSLATIONS[name])
        for geo, _material in primitives:
            p, _n, c, indices = geo.arrays(); p = p + translation
            for ids in indices.reshape(-1, 3):
                tri = p[ids]
                normal = np.cross(tri[1] - tri[0], tri[2] - tri[0]); length = np.linalg.norm(normal)
                if length < 1e-9:
                    continue
                normal /= length
                shade = 0.64 + 0.36 * max(0, float(np.dot(normal, light)))
                color = c[ids].mean(axis=0).copy(); color[:3] = np.clip(color[:3] * shade + 0.025, 0, 1)
                triangles.append(tri[:, [0, 2, 1]]); colors.append(color)
    fig = plt.figure(figsize=(14, 12), dpi=150, facecolor="#0b0708")
    views = [(20, -42, "Front three-quarter • integrated horns at -Z"),
             (20, 138, "Rear three-quarter • twin exhaust flame"),
             (72, -90, "Top • open heavyweight cockpit"), (10, -90, "Left profile • low hot-rod stance")]
    for index, (elevation, azimuth, title) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, index, projection="3d", computed_zorder=False)
        ax.set_facecolor("#0b0708")
        ax.add_collection3d(Poly3DCollection(triangles, facecolors=colors, edgecolor=(0, 0, 0, 0.13), linewidth=0.12))
        ax.set_xlim(-2.20, 2.20); ax.set_ylim(-2.35, 2.35); ax.set_zlim(0, 2.25)
        ax.set_box_aspect((4.4, 4.7, 2.25)); ax.view_init(elevation, azimuth); ax.set_axis_off()
        ax.set_title(title, color="#ffe6d8", fontsize=13, pad=4)
    fig.suptitle(f"THE HORNBREAKER • {LOD} CANDIDATE {CANDIDATE}", color="#ff4b24", fontsize=21, fontweight="bold", y=0.98)
    fig.text(0.5, 0.018, "Weathered dark steel • red armor and flame marks • integrated ram horns • studded tires • twin flaming exhausts",
             ha="center", color="#d2b7aa", fontsize=11)
    plt.subplots_adjust(left=0.01, right=0.99, top=0.94, bottom=0.04, wspace=0.01, hspace=0.02)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PREVIEW, facecolor=fig.get_facecolor()); plt.close(fig)


def main():
    parts = build_geometry()
    triangles, doc = export_glb(parts)
    if os.environ.get("HORNBREAKER_SKIP_PREVIEW") != "1":
        preview(parts)
    required = {"KartRoot", "Chassis", "AccentMesh", "SteeringWheel", "Wheel_FL", "Wheel_FR", "Wheel_RL",
                "Wheel_RR", "Exhaust_L", "Exhaust_R", "DriverMount", "ItemMountRear", "ItemMountForward"}
    actual = {node["name"] for node in doc["nodes"]}
    assert required <= actual and triangles <= DETAIL["limit"] and len(doc["materials"]) <= 4
    print(json.dumps({"glb": str(OUT), "lod": LOD, "triangleLimit": DETAIL["limit"], "triangles": triangles,
                      "materials": len(doc["materials"]), "nodes": len(doc["nodes"]), "bytes": OUT.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
