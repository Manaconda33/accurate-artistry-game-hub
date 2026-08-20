"""Build deterministic GLBs and a review sheet for Manaconda's Wayfinder.

Set WAYFINDER_LOD to LOD0, LOD1, or LOD2; WAYFINDER_OUT to the destination
GLB; and WAYFINDER_SKIP_PREVIEW=1 for a headless production build.
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


ROOT = Path(__file__).resolve().parent
LOD = os.environ.get("WAYFINDER_LOD", "LOD0").upper()
DETAILS = {
    "LOD0": {"round": 24, "wheel": (28, 12), "limit": 25000},
    "LOD1": {"round": 16, "wheel": (20, 8), "limit": 12000},
    "LOD2": {"round": 10, "wheel": (12, 6), "limit": 5000},
}
if LOD not in DETAILS:
    raise ValueError(f"Unknown WAYFINDER_LOD: {LOD}")
DETAIL = DETAILS[LOD]
OUT = Path(os.environ.get("WAYFINDER_OUT", ROOT / "wayfinder-candidate.glb"))
PREVIEW = Path(os.environ.get("WAYFINDER_PREVIEW", ROOT / "wayfinder-candidate-preview.png"))

WALNUT = np.array([0.20, 0.075, 0.025, 1.0], np.float32)
WOOD_LIT = np.array([0.38, 0.16, 0.055, 1.0], np.float32)
LEATHER = np.array([0.30, 0.12, 0.045, 1.0], np.float32)
BRASS = np.array([0.56, 0.30, 0.075, 1.0], np.float32)
COPPER = np.array([0.48, 0.19, 0.055, 1.0], np.float32)
INDIGO = np.array([0.10, 0.055, 0.31, 1.0], np.float32)
PARCHMENT = np.array([0.68, 0.50, 0.25, 1.0], np.float32)
TIRE = np.array([0.025, 0.022, 0.024, 1.0], np.float32)
CORE = np.array([0.07, 0.38, 0.78, 1.0], np.float32)


class Geo:
    def __init__(self):
        self.p, self.n, self.c, self.i = [], [], [], []

    def add(self, data):
        p, n, c, idx = data
        base = len(self.p)
        self.p.extend(np.asarray(p, np.float32))
        self.n.extend(np.asarray(n, np.float32))
        colors = np.asarray(c, np.float32)
        if colors.ndim == 1:
            colors = np.tile(colors, (len(p), 1))
        self.c.extend(colors)
        self.i.extend((np.asarray(idx, np.uint32) + base).tolist())

    def arrays(self):
        return (
            np.asarray(self.p, np.float32),
            np.asarray(self.n, np.float32),
            np.asarray(self.c, np.float32),
            np.asarray(self.i, np.uint32),
        )


def box(size, color):
    sx, sy, sz = np.asarray(size, float) / 2
    corners = np.array([
        [-sx, -sy, -sz], [sx, -sy, -sz], [sx, sy, -sz], [-sx, sy, -sz],
        [-sx, -sy, sz], [sx, -sy, sz], [sx, sy, sz], [-sx, sy, sz],
    ])
    faces = ((0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7),
             (0, 1, 5), (0, 5, 4), (3, 7, 6), (3, 6, 2),
             (0, 4, 7), (0, 7, 3), (1, 2, 6), (1, 6, 5))
    p, n, idx = [], [], []
    for face in faces:
        tri = corners[list(face)]
        normal = np.cross(tri[1] - tri[0], tri[2] - tri[0])
        normal /= np.linalg.norm(normal)
        base = len(p)
        p.extend(tri); n.extend([normal] * 3); idx.extend([base, base + 1, base + 2])
    return p, n, color, idx


def ellipsoid(size, seg, rings, color):
    rx, ry, rz = np.asarray(size, float) / 2
    p, n, idx = [], [], []
    for j in range(rings + 1):
        theta = math.pi * j / rings
        for k in range(seg + 1):
            phi = 2 * math.pi * k / seg
            point = np.array([rx * math.sin(theta) * math.cos(phi),
                              ry * math.cos(theta),
                              rz * math.sin(theta) * math.sin(phi)])
            normal = np.array([point[0] / (rx * rx), point[1] / (ry * ry), point[2] / (rz * rz)])
            normal /= max(np.linalg.norm(normal), 1e-9)
            p.append(point); n.append(normal)
    for j in range(rings):
        for k in range(seg):
            a = j * (seg + 1) + k; b = a + seg + 1
            idx.extend([a, b, a + 1, a + 1, b, b + 1])
    return p, n, color, idx


def cylinder(radius, length, seg, axis, color, capped=True):
    p, n, idx = [], [], []
    for side in (-0.5, 0.5):
        for k in range(seg):
            angle = 2 * math.pi * k / seg
            p.append([radius * math.cos(angle), radius * math.sin(angle), side * length])
            n.append([math.cos(angle), math.sin(angle), 0])
    for k in range(seg):
        q = (k + 1) % seg
        idx.extend([k, q, seg + k, q, seg + q, seg + k])
    if capped:
        for side, sign in ((-0.5, -1), (0.5, 1)):
            center = len(p); p.append([0, 0, side * length]); n.append([0, 0, sign])
            ring = len(p)
            for k in range(seg):
                angle = 2 * math.pi * k / seg
                p.append([radius * math.cos(angle), radius * math.sin(angle), side * length])
                n.append([0, 0, sign])
            for k in range(seg):
                q = (k + 1) % seg
                idx.extend([center, ring + q, ring + k] if sign < 0 else [center, ring + k, ring + q])
    p, n = np.asarray(p), np.asarray(n)
    if axis == "x":
        p = p[:, [2, 0, 1]]; n = n[:, [2, 0, 1]]
    elif axis == "y":
        p = p[:, [0, 2, 1]]; n = n[:, [0, 2, 1]]
    return p, n, color, idx


def torus(major, tube, seg, tube_seg, axis, color):
    p, n, idx = [], [], []
    for a_i in range(seg):
        u = 2 * math.pi * a_i / seg
        for b_i in range(tube_seg):
            v = 2 * math.pi * b_i / tube_seg
            point = np.array([(major + tube * math.cos(v)) * math.cos(u),
                              tube * math.sin(v),
                              (major + tube * math.cos(v)) * math.sin(u)])
            normal = np.array([math.cos(v) * math.cos(u), math.sin(v), math.cos(v) * math.sin(u)])
            if axis == "x":
                point = point[[1, 0, 2]]; normal = normal[[1, 0, 2]]
            p.append(point); n.append(normal)
    for a_i in range(seg):
        aa = (a_i + 1) % seg
        for b_i in range(tube_seg):
            bb = (b_i + 1) % tube_seg
            a = a_i * tube_seg + b_i; b = aa * tube_seg + b_i
            c = a_i * tube_seg + bb; d = aa * tube_seg + bb
            idx.extend([a, b, c, c, b, d])
    return p, n, color, idx


def rot_x(angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_y(angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def transform(data, translation=(0, 0, 0), rotation=None, scale=(1, 1, 1)):
    p, n, c, idx = data
    p = np.asarray(p, float) * np.asarray(scale)
    n = np.asarray(n, float)
    if rotation is not None:
        p = p @ rotation.T; n = n @ rotation.T
    p += np.asarray(translation)
    return p, n, c, idx


def add_box(geo, size, at, color, rotation=None):
    geo.add(transform(box(size, color), at, rotation))


def add_cyl(geo, radius, length, at, axis, color, rotation=None):
    geo.add(transform(cylinder(radius, length, DETAIL["round"], axis, color), at, rotation))


def build_geometry():
    parts = {}

    chassis, leather = Geo(), Geo()
    chassis.add(transform(ellipsoid((2.38, 0.72, 3.62), DETAIL["round"], DETAIL["round"] // 2, WALNUT), (0, 0.72, 0)))
    chassis.add(transform(ellipsoid((2.02, 0.54, 1.42), DETAIL["round"], DETAIL["round"] // 2, WOOD_LIT), (0, 0.98, -1.18)))
    add_box(chassis, (1.74, 0.18, 1.25), (0, 0.98, 0.08), WALNUT)
    add_box(chassis, (1.95, 0.28, 0.34), (0, 0.92, -1.63), WOOD_LIT)
    # Recessed cockpit reads as a dark opening enclosed by leather bolsters.
    leather.add(transform(ellipsoid((1.55, 0.18, 1.20), DETAIL["round"], DETAIL["round"] // 2, TIRE), (0, 1.115, 0.10)))
    for x in (-0.83, 0.83):
        leather.add(transform(ellipsoid((0.24, 0.38, 1.50), DETAIL["round"], DETAIL["round"] // 2, LEATHER), (x, 1.18, 0.10)))
    leather.add(transform(ellipsoid((1.72, 0.35, 0.28), DETAIL["round"], DETAIL["round"] // 2, LEATHER), (0, 1.18, 0.68)))
    parts["Chassis"] = [(chassis, 0), (leather, 1)]

    accent, glow = Geo(), Geo()
    # Copper frame rails and protective front grille.
    for x in (-1.02, 1.02):
        add_cyl(accent, 0.055, 3.10, (x, 0.78, 0), "z", BRASS)
    for z in (-1.52, 1.48):
        add_cyl(accent, 0.06, 2.08, (0, 0.78, z), "x", BRASS)
    add_box(accent, (1.38, 0.62, 0.10), (0, 0.76, -1.84), COPPER)
    for x in (-0.48, -0.24, 0, 0.24, 0.48):
        add_cyl(accent, 0.025, 0.55, (x, 0.77, -1.91), "y", BRASS)
    # Navigation core is always front-mounted, directly behind the grille.
    add_box(glow, (0.38, 0.38, 0.38), (0, 0.76, -1.72), CORE, rot_y(math.pi / 4))
    # Indigo bindings are restrained accents, not bodywork.
    add_box(accent, (1.54, 0.08, 0.16), (0, 1.37, 0.72), INDIGO)
    # Rear field satchel with flap and brass clasp.
    add_box(accent, (1.25, 0.70, 0.40), (0, 1.20, 1.34), LEATHER)
    add_box(accent, (1.08, 0.16, 0.44), (0, 1.48, 1.28), LEATHER, rot_x(-0.18))
    add_box(accent, (0.15, 0.20, 0.08), (0, 1.38, 1.04), BRASS)
    # Detachable parchment scroll case low on the kart's left side.
    add_cyl(accent, 0.15, 1.05, (-1.11, 0.76, 0.42), "z", PARCHMENT, rot_x(0.06))
    for z in (-0.10, 0.94):
        accent.add(transform(torus(0.16, 0.025, DETAIL["round"], max(5, DETAIL["round"] // 3), "x", LEATHER), (-1.11, 0.76, z)))
    parts["AccentMesh"] = [(accent, 1), (glow, 3)]

    # Manaconda's approved 2D driver frames already contain the steering
    # wheel. Keep the required SteeringWheel node as an empty runtime anchor;
    # visible geometry here would create a duplicate wheel and sprite clipping.

    for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"):
        wheel, hub = Geo(), Geo()
        wheel.add(torus(0.40, 0.16, *DETAIL["wheel"], "x", TIRE))
        add_cyl(hub, 0.22, 0.22, (0, 0, 0), "x", BRASS)
        parts[name] = [(wheel, 2), (hub, 1)]

    for name in ("Exhaust_L", "Exhaust_R"):
        exhaust = Geo()
        add_cyl(exhaust, 0.105, 0.62, (0, 0, 0), "z", COPPER, rot_x(-0.12))
        exhaust.add(transform(torus(0.11, 0.025, DETAIL["round"], max(5, DETAIL["round"] // 3), "x", BRASS), (0, 0, -0.31)))
        parts[name] = [(exhaust, 1)]
    return parts


MATERIALS = [
    {"name": "ChassisWood", "alphaMode": "OPAQUE", "doubleSided": True,
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.0, "roughnessFactor": 0.82}},
    {"name": "ExpeditionAccent", "alphaMode": "OPAQUE", "doubleSided": True,
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.36, "roughnessFactor": 0.56}},
    {"name": "TireRubber", "alphaMode": "OPAQUE", "doubleSided": True,
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.0, "roughnessFactor": 0.9}},
    {"name": "NavigationCore", "alphaMode": "OPAQUE", "doubleSided": True,
     "emissiveFactor": [0.04, 0.24, 0.62],
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.2, "roughnessFactor": 0.35}},
]

TRANSLATIONS = {
    "Chassis": (0, 0, 0), "AccentMesh": (0, 0, 0),
    "SteeringWheel": (0, 1.48, -0.48),
    "Wheel_FL": (-1.34, 0.50, -1.08), "Wheel_FR": (1.34, 0.50, -1.08),
    "Wheel_RL": (-1.34, 0.50, 1.10), "Wheel_RR": (1.34, 0.50, 1.10),
    "Exhaust_L": (-0.68, 0.79, 1.72), "Exhaust_R": (0.68, 0.79, 1.72),
    "DriverMount": (0, 1.48, 0.05), "ItemMountRear": (0, 1.18, 1.92),
    "ItemMountForward": (0, 0.98, -1.98),
}


def export_glb(parts):
    doc = {"asset": {"version": "2.0", "generator": "Accurate Artistry procedural Wayfinder builder"},
           "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [], "meshes": [],
           "materials": MATERIALS, "buffers": [{}], "bufferViews": [], "accessors": [],
           "extras": {"lod": LOD, "forward": "-Z", "units": "meters", "approvedName": "The Wayfinder"}}
    blob = bytearray()

    def accessor(arr, kind, component, target=None, minmax=False):
        while len(blob) % 4:
            blob.append(0)
        offset = len(blob); raw = arr.tobytes(); blob.extend(raw)
        view = {"buffer": 0, "byteOffset": offset, "byteLength": len(raw)}
        if target:
            view["target"] = target
        doc["bufferViews"].append(view)
        acc = {"bufferView": len(doc["bufferViews"]) - 1, "componentType": component,
               "count": len(arr), "type": kind}
        if minmax:
            acc.update(min=arr.min(axis=0).tolist(), max=arr.max(axis=0).tolist())
        doc["accessors"].append(acc)
        return len(doc["accessors"]) - 1

    mesh_index, total_tris = {}, 0
    for name, primitives in parts.items():
        exported = []
        for geo, material in primitives:
            p, n, c, i = geo.arrays(); total_tris += len(i) // 3
            ind = i.astype(np.uint16 if len(p) < 65536 else np.uint32)
            exported.append({"attributes": {
                "POSITION": accessor(p, "VEC3", 5126, 34962, True),
                "NORMAL": accessor(n, "VEC3", 5126, 34962),
                "COLOR_0": accessor(c, "VEC4", 5126, 34962)},
                "indices": accessor(ind, "SCALAR", 5123 if ind.dtype == np.uint16 else 5125, 34963),
                "material": material, "mode": 4})
        doc["meshes"].append({"name": name, "primitives": exported})
        mesh_index[name] = len(doc["meshes"]) - 1
    names = ["KartRoot", "Chassis", "AccentMesh", "SteeringWheel", "Wheel_FL", "Wheel_FR",
             "Wheel_RL", "Wheel_RR", "Exhaust_L", "Exhaust_R", "DriverMount", "ItemMountRear",
             "ItemMountForward"]
    doc["nodes"].append({"name": "KartRoot", "children": list(range(1, len(names))),
                         "extras": {"triangleCount": total_tris, "principalMaterials": 4}})
    for name in names[1:]:
        node = {"name": name, "translation": TRANSLATIONS[name]}
        if name in mesh_index:
            node["mesh"] = mesh_index[name]
        doc["nodes"].append(node)
    doc["buffers"][0]["byteLength"] = len(blob)
    js = json.dumps(doc, separators=(",", ":")).encode()
    js += b" " * ((4 - len(js) % 4) % 4)
    blob += b"\0" * ((4 - len(blob) % 4) % 4)
    total = 12 + 8 + len(js) + 8 + len(blob)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(struct.pack("<4sII", b"glTF", 2, total) + struct.pack("<I4s", len(js), b"JSON") + js +
                    struct.pack("<I4s", len(blob), b"BIN\0") + blob)
    return total_tris, doc


def preview(parts):
    triangles, colors = [], []
    light = np.array([-0.45, 0.85, -0.30]); light /= np.linalg.norm(light)
    for name, primitives in parts.items():
        translation = np.asarray(TRANSLATIONS[name])
        for geo, _material in primitives:
            p, _n, c, i = geo.arrays(); p = p + translation
            for tri_indices in i.reshape(-1, 3):
                tri = p[tri_indices]
                normal = np.cross(tri[1] - tri[0], tri[2] - tri[0]); length = np.linalg.norm(normal)
                if length < 1e-9:
                    continue
                normal /= length
                shade = 0.68 + 0.32 * max(0, float(np.dot(normal, light)))
                color = c[tri_indices].mean(axis=0).copy(); color[:3] = np.clip(color[:3] * shade + 0.045, 0, 1)
                triangles.append(tri[:, [0, 2, 1]]); colors.append(color)
    fig = plt.figure(figsize=(14, 12), dpi=150, facecolor="#10141b")
    views = [(22, -42, "Front three-quarter"), (20, 138, "Rear three-quarter"),
             (72, -90, "Top geometry"), (12, -90, "Left profile")]
    for index, (elevation, azimuth, title) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, index, projection="3d", computed_zorder=False)
        ax.set_facecolor("#10141b")
        ax.add_collection3d(Poly3DCollection(triangles, facecolors=colors, edgecolor=(0, 0, 0, 0.10), linewidth=0.12))
        ax.set_xlim(-2.05, 2.05); ax.set_ylim(-2.20, 2.20); ax.set_zlim(0, 2.05)
        ax.set_box_aspect((4.1, 4.4, 2.05)); ax.view_init(elevation, azimuth); ax.set_axis_off()
        ax.set_title(title, color="#edf2f3", fontsize=15, pad=4)
    fig.suptitle(f"THE WAYFINDER • {LOD} MODEL CANDIDATE", color="#d5ad58", fontsize=21, fontweight="bold", y=0.98)
    fig.text(0.5, 0.018, "Front navigation core • recessed cockpit • rear satchel • left scroll case • twin capped exhausts",
             ha="center", color="#b8c1cc", fontsize=11)
    plt.subplots_adjust(left=0.01, right=0.99, top=0.94, bottom=0.04, wspace=0.01, hspace=0.02)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PREVIEW, facecolor=fig.get_facecolor()); plt.close(fig)


def main():
    parts = build_geometry(); triangles, doc = export_glb(parts)
    if os.environ.get("WAYFINDER_SKIP_PREVIEW") != "1":
        preview(parts)
    required = {"KartRoot", "Chassis", "AccentMesh", "SteeringWheel", "Wheel_FL", "Wheel_FR", "Wheel_RL",
                "Wheel_RR", "Exhaust_L", "Exhaust_R", "DriverMount", "ItemMountRear", "ItemMountForward"}
    actual = {node["name"] for node in doc["nodes"]}
    assert required <= actual and triangles <= DETAIL["limit"] and len(doc["materials"]) <= 4
    print(json.dumps({"glb": str(OUT), "lod": LOD, "triangleLimit": DETAIL["limit"], "triangles": triangles,
                      "materials": len(doc["materials"]), "nodes": len(doc["nodes"]), "bytes": OUT.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
