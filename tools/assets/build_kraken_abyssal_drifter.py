"""Build deterministic GLBs and a review sheet for The Abyssal Drifter.

Set ABYSSAL_LOD to LOD0, LOD1, or LOD2; ABYSSAL_OUT to the GLB destination;
and ABYSSAL_SKIP_PREVIEW=1 for headless production builds.
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
LOD = os.environ.get("ABYSSAL_LOD", "LOD0").upper()
DETAILS = {
    "LOD0": {"round": 16, "tube": 7, "tentacle": 8, "limit": 25000},
    "LOD1": {"round": 12, "tube": 5, "tentacle": 6, "limit": 12000},
    "LOD2": {"round": 7, "tube": 3, "tentacle": 3, "limit": 5000},
}
if LOD not in DETAILS:
    raise ValueError(f"Unknown ABYSSAL_LOD: {LOD}")
DETAIL = DETAILS[LOD]
OUT = Path(os.environ.get("ABYSSAL_OUT", ROOT / "candidates/abyssal-drifter-candidate-1.glb"))
PREVIEW = Path(os.environ.get("ABYSSAL_PREVIEW", ROOT / "candidates/abyssal-drifter-candidate-1-preview.png"))
CANDIDATE = os.environ.get("ABYSSAL_CANDIDATE", "1")

INDIGO = np.array([0.075, 0.035, 0.24, 1.0], np.float32)
PURPLE = np.array([0.25, 0.075, 0.48, 1.0], np.float32)
CYAN = np.array([0.02, 0.78, 0.90, 1.0], np.float32)
COPPER = np.array([0.58, 0.25, 0.09, 1.0], np.float32)
ORANGE = np.array([1.0, 0.28, 0.015, 1.0], np.float32)
BLACK = np.array([0.018, 0.012, 0.035, 1.0], np.float32)
TOOTH = np.array([0.80, 0.69, 0.45, 1.0], np.float32)


def add_ellipsoid(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.ellipsoid(size, DETAIL["round"], max(6, DETAIL["round"] // 2), color), at, rotation))


def add_cyl(geo, radius, length, at, axis, color, rotation=None, seg=None):
    geo.add(base.transform(base.cylinder(radius, length, seg or DETAIL["round"], axis, color), at, rotation))


def rot_z(angle):
    cosine, sine = math.cos(angle), math.sin(angle)
    return np.array([[cosine, -sine, 0], [sine, cosine, 0], [0, 0, 1]])


def tentacle(geo, points, radii, color):
    """Create a readable organic limb from overlapping tapered joint forms."""
    count = max(2, DETAIL["tentacle"])
    source = np.asarray(points, float)
    for index in range(count):
        t = index / (count - 1)
        scaled = t * (len(source) - 1)
        left = min(int(scaled), len(source) - 2)
        local = scaled - left
        point = source[left] * (1 - local) + source[left + 1] * local
        radius = radii[0] * (1 - t) + radii[1] * t
        add_ellipsoid(geo, (radius * 2.0, radius * 1.65, radius * 2.35), point, color)


def build_geometry():
    parts = {}
    chassis, organic = base.Geo(), base.Geo()
    add_ellipsoid(chassis, (2.30, 0.72, 3.45), (0, 0.72, 0.05), INDIGO)
    add_ellipsoid(chassis, (2.00, 0.58, 2.55), (0, 1.02, 0.12), PURPLE)
    # Dark recessed cockpit with raised living shell shoulders.
    add_ellipsoid(organic, (1.30, 0.18, 1.12), (0, 1.26, 0.20), BLACK)
    for x in (-0.78, 0.78):
        add_ellipsoid(organic, (0.36, 0.55, 1.55), (x, 1.23, 0.15), INDIGO)
    parts["Chassis"] = [(chassis, 0), (organic, 0)]

    accent, glow, face = base.Geo(), base.Geo(), base.Geo()
    # Copper shell ribs and cyan bioluminescent seams.
    for x in (-0.91, 0.91):
        add_cyl(accent, 0.055, 2.75, (x, 0.86, 0.05), "z", COPPER)
        tentacle(glow, [(x, 1.08, 0.85), (x * 1.12, 1.40, 1.28), (x * 0.65, 1.72, 1.63)], (0.13, 0.045), CYAN)
    # Small bioluminescent sucker markings stay on the shell flanks. They do
    # not form hoops or cross the cockpit/body centerline.
    for side in (-1, 1):
        for index, z in enumerate((-0.82, -0.30, 0.25, 0.78)):
            add_ellipsoid(glow, (0.10, 0.075, 0.045), (side * (1.03 - index * 0.025), 0.98, z), CYAN)

    # Definitive monster face at authored -Z front: orange eyes, black maw, teeth.
    add_ellipsoid(face, (1.78, 0.72, 0.32), (0, 0.79, -1.67), PURPLE)
    add_ellipsoid(face, (0.92, 0.36, 0.13), (0, 0.61, -1.86), BLACK)
    for x in (-0.53, 0.53):
        add_ellipsoid(glow, (0.38, 0.27, 0.16), (x, 0.91, -1.87), ORANGE, base.rot_y(-0.16 * (1 if x > 0 else -1)))
    for x in np.linspace(-0.34, 0.34, 5):
        add_ellipsoid(face, (0.10, 0.23, 0.09), (x, 0.68, -1.94), TOOTH)
        add_ellipsoid(face, (0.09, 0.19, 0.08), (x + 0.04, 0.54, -1.94), TOOTH)
    # Front bumper tentacles curl around the face without hiding the eyes.
    tentacle(accent, [(-0.82, 0.76, -1.48), (-1.15, 0.58, -1.75), (-0.95, 0.38, -1.98), (-0.58, 0.46, -1.88)], (0.22, 0.07), PURPLE)
    tentacle(accent, [(0.82, 0.76, -1.48), (1.15, 0.58, -1.75), (0.95, 0.38, -1.98), (0.58, 0.46, -1.88)], (0.22, 0.07), PURPLE)
    parts["AccentMesh"] = [(accent, 1), (face, 1), (glow, 3)]

    steering = base.Geo()
    # The wheel lies in the XY plane so its full ring faces the seated driver
    # and remains readable from the front/rear review angles.
    steering.add(base.transform(
        base.torus(0.34, 0.055, DETAIL["round"], DETAIL["tube"], "y", COPPER),
        rotation=base.rot_x(math.pi / 2),
    ))
    for angle in (0, math.pi * 2 / 3, math.pi * 4 / 3):
        steering.add(base.transform(base.box((0.56, 0.045, 0.045), CYAN), rotation=rot_z(angle)))
    add_cyl(steering, 0.09, 0.08, (0, 0, 0), "z", PURPLE)
    # A substantial organic dashboard pod and copper steering column connect
    # the wheel to the shell. The wheel itself sits fully above the pod rather
    # than intersecting the kart body.
    add_ellipsoid(steering, (0.54, 0.24, 0.42), (0, -0.52, -0.13), INDIGO)
    add_ellipsoid(steering, (0.39, 0.14, 0.30), (0, -0.43, -0.11), PURPLE)
    # Negative local Z is the nose-facing side of the wheel. The column stays
    # there, away from Kraken and the cockpit, and terminates at the hub.
    add_cyl(steering, 0.070, 0.52, (0, -0.25, -0.10), "y", COPPER, base.rot_x(0.10))
    steering.add(base.transform(
        base.torus(0.12, 0.028, DETAIL["round"], DETAIL["tube"], "y", CYAN),
        (0, -0.43, -0.12),
    ))
    parts["SteeringWheel"] = [(steering, 1)]

    for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"):
        tire, turbine = base.Geo(), base.Geo()
        tire.add(base.torus(0.43, 0.17, DETAIL["round"], DETAIL["tube"], "x", BLACK))
        turbine.add(base.torus(0.29, 0.045, DETAIL["round"], max(5, DETAIL["tube"] - 2), "x", CYAN))
        add_cyl(turbine, 0.13, 0.24, (0, 0, 0), "x", PURPLE)
        parts[name] = [(tire, 2), (turbine, 3)]

    for name in ("Exhaust_L", "Exhaust_R"):
        exhaust = base.Geo()
        add_cyl(exhaust, 0.13, 0.65, (0, 0, 0), "z", COPPER, base.rot_x(-0.10))
        exhaust.add(base.transform(base.torus(0.14, 0.035, DETAIL["round"], DETAIL["tube"], "x", CYAN), (0, 0, 0.32)))
        parts[name] = [(exhaust, 1)]
    return parts


TRANSLATIONS = {
    "Chassis": (0, 0, 0), "AccentMesh": (0, 0, 0),
    "SteeringWheel": (0, 1.73, -0.28),
    "Wheel_FL": (-1.34, 0.49, -1.05), "Wheel_FR": (1.34, 0.49, -1.05),
    "Wheel_RL": (-1.34, 0.49, 1.12), "Wheel_RR": (1.34, 0.49, 1.12),
    "Exhaust_L": (-0.68, 0.78, 1.73), "Exhaust_R": (0.68, 0.78, 1.73),
    "DriverMount": (0, 1.48, 0.10), "ItemMountRear": (0, 1.20, 1.96),
    "ItemMountForward": (0, 0.92, -2.03),
}

MATERIALS = [
    {"name": "AbyssalShell", "alphaMode": "OPAQUE", "doubleSided": True,
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.08, "roughnessFactor": 0.58}},
    {"name": "CopperAndOrganicAccent", "alphaMode": "OPAQUE", "doubleSided": True,
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.38, "roughnessFactor": 0.43}},
    {"name": "TurbineTire", "alphaMode": "OPAQUE", "doubleSided": True,
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.02, "roughnessFactor": 0.88}},
    {"name": "Bioluminescence", "alphaMode": "OPAQUE", "doubleSided": True,
     "emissiveFactor": [0.02, 0.52, 0.68],
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.15, "roughnessFactor": 0.30}},
]


def export_glb(parts):
    doc = {
        "asset": {"version": "2.0", "generator": "Accurate Artistry procedural Abyssal Drifter builder"},
        "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [], "meshes": [],
        "materials": MATERIALS, "buffers": [{}], "bufferViews": [], "accessors": [],
        "extras": {"lod": LOD, "forward": "-Z", "units": "meters", "approvedName": "The Abyssal Drifter"},
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
            packed_indices = indices.astype(np.uint16 if len(positions) < 65536 else np.uint32)
            exported.append({
                "attributes": {
                    "POSITION": accessor(positions, "VEC3", 5126, 34962, True),
                    "NORMAL": accessor(normals, "VEC3", 5126, 34962),
                    "COLOR_0": accessor(colors, "VEC4", 5126, 34962),
                },
                "indices": accessor(packed_indices, "SCALAR", 5123 if packed_indices.dtype == np.uint16 else 5125, 34963),
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
    OUT.write_bytes(
        struct.pack("<4sII", b"glTF", 2, total_bytes)
        + struct.pack("<I4s", len(json_chunk), b"JSON") + json_chunk
        + struct.pack("<I4s", len(blob), b"BIN\0") + blob
    )
    return total_triangles, doc


def preview(parts):
    triangles, colors = [], []
    light = np.array([-0.45, 0.85, -0.30]); light /= np.linalg.norm(light)
    for name, primitives in parts.items():
        translation = np.asarray(TRANSLATIONS[name])
        for geo, _material in primitives:
            p, _n, c, indices = geo.arrays(); p = p + translation
            for tri_indices in indices.reshape(-1, 3):
                tri = p[tri_indices]
                normal = np.cross(tri[1] - tri[0], tri[2] - tri[0]); length = np.linalg.norm(normal)
                if length < 1e-9:
                    continue
                normal /= length
                shade = 0.65 + 0.35 * max(0, float(np.dot(normal, light)))
                color = c[tri_indices].mean(axis=0).copy(); color[:3] = np.clip(color[:3] * shade + 0.035, 0, 1)
                triangles.append(tri[:, [0, 2, 1]]); colors.append(color)
    fig = plt.figure(figsize=(14, 12), dpi=150, facecolor="#090715")
    views = [(20, -42, "Front three-quarter • maw at -Z"), (20, 138, "Rear three-quarter"),
             (72, -90, "Top geometry"), (10, -90, "Left profile")]
    for index, (elevation, azimuth, title) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, index, projection="3d", computed_zorder=False)
        ax.set_facecolor("#090715")
        ax.add_collection3d(Poly3DCollection(triangles, facecolors=colors, edgecolor=(0, 0, 0, 0.10), linewidth=0.12))
        ax.set_xlim(-2.05, 2.05); ax.set_ylim(-2.20, 2.20); ax.set_zlim(0, 2.15)
        ax.set_box_aspect((4.1, 4.4, 2.15)); ax.view_init(elevation, azimuth); ax.set_axis_off()
        ax.set_title(title, color="#dffbff", fontsize=14, pad=4)
    fig.suptitle(f"THE ABYSSAL DRIFTER • {LOD} CANDIDATE {CANDIDATE}", color="#56edf4", fontsize=21, fontweight="bold", y=0.98)
    fig.text(0.5, 0.018, "Orange-eyed toothed maw at front • cyan living seams • copper trim • tentacle bodywork • turbine wheels",
             ha="center", color="#c2b5df", fontsize=11)
    plt.subplots_adjust(left=0.01, right=0.99, top=0.94, bottom=0.04, wspace=0.01, hspace=0.02)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PREVIEW, facecolor=fig.get_facecolor()); plt.close(fig)


def main():
    parts = build_geometry()
    triangles, doc = export_glb(parts)
    if os.environ.get("ABYSSAL_SKIP_PREVIEW") != "1":
        preview(parts)
    required = {"KartRoot", "Chassis", "AccentMesh", "SteeringWheel", "Wheel_FL", "Wheel_FR", "Wheel_RL",
                "Wheel_RR", "Exhaust_L", "Exhaust_R", "DriverMount", "ItemMountRear", "ItemMountForward"}
    actual = {node["name"] for node in doc["nodes"]}
    assert required <= actual and triangles <= DETAIL["limit"] and len(doc["materials"]) <= 4
    print(json.dumps({"glb": str(OUT), "lod": LOD, "triangleLimit": DETAIL["limit"], "triangles": triangles,
                      "materials": len(doc["materials"]), "nodes": len(doc["nodes"]), "bytes": OUT.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
