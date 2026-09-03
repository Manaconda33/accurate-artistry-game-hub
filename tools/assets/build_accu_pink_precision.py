"""Build and preview Accu's Pink Precision kart candidate.

Candidate-only defaults write outside the runtime asset tree. Production use can
set PINK_PRECISION_OUT and PINK_PRECISION_PREVIEW explicitly after approval.
Requires Python 3, NumPy, and Matplotlib.
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
OUT = Path(os.environ.get("PINK_PRECISION_OUT", ROOT / "candidates/pink-precision-candidate-1.glb"))
PREVIEW = Path(os.environ.get("PINK_PRECISION_PREVIEW", ROOT / "candidates/pink-precision-candidate-1-preview.png"))
LOD = int(os.environ.get("PINK_PRECISION_LOD", "0"))
if LOD not in (0, 1, 2):
    raise ValueError("PINK_PRECISION_LOD must be 0, 1, or 2")

LOD_CONFIG = {
    0: {"track_straight": 13, "track_return": 7, "road_wheels": 5, "wheel_segments": 18,
        "hub_segments": 14, "collar_segments": 36, "collar_tube_segments": 10,
        "turret_segments": 32, "round_segments": 24, "steering_segments": 28,
        "steering_tube_segments": 8, "heart_segments": 24},
    1: {"track_straight": 10, "track_return": 5, "road_wheels": 4, "wheel_segments": 14,
        "hub_segments": 10, "collar_segments": 24, "collar_tube_segments": 8,
        "turret_segments": 20, "round_segments": 16, "steering_segments": 18,
        "steering_tube_segments": 6, "heart_segments": 18},
    2: {"track_straight": 7, "track_return": 4, "road_wheels": 3, "wheel_segments": 10,
        "hub_segments": 8, "collar_segments": 16, "collar_tube_segments": 6,
        "turret_segments": 14, "round_segments": 12, "steering_segments": 12,
        "steering_tube_segments": 5, "heart_segments": 12},
}[LOD]

PINK = np.array([0.92, 0.23, 0.48, 1.0], np.float32)
LIGHT_PINK = np.array([1.0, 0.55, 0.72, 1.0], np.float32)
RUBBER = np.array([0.055, 0.045, 0.065, 1.0], np.float32)
METAL = np.array([0.18, 0.16, 0.22, 1.0], np.float32)


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


def box(size, color=PINK):
    sx, sy, sz = np.asarray(size, float) / 2
    verts = np.array(
        [
            [-sx, -sy, -sz], [sx, -sy, -sz], [sx, sy, -sz], [-sx, sy, -sz],
            [-sx, -sy, sz], [sx, -sy, sz], [sx, sy, sz], [-sx, sy, sz],
        ]
    )
    faces = [[0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7], [0, 1, 5], [0, 5, 4],
             [3, 7, 6], [3, 6, 2], [0, 4, 7], [0, 7, 3], [1, 2, 6], [1, 6, 5]]
    p, n, idx = [], [], []
    for face in faces:
        a, b, c = [verts[q] for q in face]
        normal = np.cross(b - a, c - a)
        normal /= np.linalg.norm(normal)
        base = len(p)
        p += [a, b, c]
        n += [normal, normal, normal]
        idx += [base, base + 1, base + 2]
    return p, n, color, idx


def cylinder(radius, length, segments=24, axis="z", color=METAL, capped=True):
    p, n, idx = [], [], []
    for side in (-0.5, 0.5):
        for k in range(segments):
            angle = 2 * math.pi * k / segments
            p.append([radius * math.cos(angle), radius * math.sin(angle), side * length])
            n.append([math.cos(angle), math.sin(angle), 0])
    for k in range(segments):
        q = (k + 1) % segments
        idx += [k, q, segments + k, q, segments + q, segments + k]
    if capped:
        for side, sign in ((-0.5, -1), (0.5, 1)):
            center = len(p)
            p.append([0, 0, side * length])
            n.append([0, 0, sign])
            ring = len(p)
            for k in range(segments):
                angle = 2 * math.pi * k / segments
                p.append([radius * math.cos(angle), radius * math.sin(angle), side * length])
                n.append([0, 0, sign])
            for k in range(segments):
                q = (k + 1) % segments
                idx += [center, ring + q, ring + k] if sign < 0 else [center, ring + k, ring + q]
    p, n = np.asarray(p), np.asarray(n)
    if axis == "x":
        p, n = p[:, [2, 0, 1]], n[:, [2, 0, 1]]
    elif axis == "y":
        p, n = p[:, [0, 2, 1]], n[:, [0, 2, 1]]
    return p, n, color, idx


def torus(major, tube, segments=32, tube_segments=10, plane="xy", color=METAL):
    p, n, idx = [], [], []
    for a_i in range(segments):
        u = 2 * math.pi * a_i / segments
        for b_i in range(tube_segments):
            v = 2 * math.pi * b_i / tube_segments
            r = major + tube * math.cos(v)
            if plane == "xy":
                p.append([r * math.cos(u), r * math.sin(u), tube * math.sin(v)])
                n.append([math.cos(v) * math.cos(u), math.cos(v) * math.sin(u), math.sin(v)])
            else:
                p.append([r * math.cos(u), tube * math.sin(v), r * math.sin(u)])
                n.append([math.cos(v) * math.cos(u), math.sin(v), math.cos(v) * math.sin(u)])
    for a_i in range(segments):
        aa = (a_i + 1) % segments
        for b_i in range(tube_segments):
            bb = (b_i + 1) % tube_segments
            a = a_i * tube_segments + b_i
            b = aa * tube_segments + b_i
            c = a_i * tube_segments + bb
            d = aa * tube_segments + bb
            idx += [a, b, c, c, b, d]
    return p, n, color, idx


def transform(data, translation=(0, 0, 0), rotation=None, scale=(1, 1, 1)):
    p, n, c, idx = data
    p = np.asarray(p, float) * np.asarray(scale, float)
    n = np.asarray(n, float)
    if rotation is not None:
        p = p @ rotation.T
        n = n @ rotation.T
    p += np.asarray(translation, float)
    return p, n, c, idx


def rot_x(angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rounded_track(side):
    """Continuous rubber tread loop made from overlapping pads and road wheels."""
    geo = Geo()
    x = side * 1.16
    # Straight upper/lower runs.
    for y in (0.30, 0.88):
        for z in np.linspace(-1.30, 1.30, LOD_CONFIG["track_straight"]):
            geo.add(transform(box((0.34, 0.13, 0.27), RUBBER), (x, y, z)))
    # Rounded front/rear returns.
    for z_center in (-1.36, 1.36):
        for angle in np.linspace(-math.pi / 2, math.pi / 2, LOD_CONFIG["track_return"]):
            y = 0.59 + 0.30 * math.cos(angle)
            z = z_center + (0.30 * math.sin(angle) * (-1 if z_center < 0 else 1))
            geo.add(transform(box((0.34, 0.13, 0.25), RUBBER), (x, y, z), rot_x(angle)))
    # Visible road wheels inside the belt.
    wheel_positions = (-1.05, -0.53, 0, 0.53, 1.05) if LOD == 0 else np.linspace(-1.05, 1.05, LOD_CONFIG["road_wheels"])
    for z in wheel_positions:
        geo.add(transform(cylinder(0.255, 0.27, LOD_CONFIG["wheel_segments"], axis="x", color=METAL), (x, 0.57, z)))
        geo.add(transform(cylinder(0.10, 0.30, LOD_CONFIG["hub_segments"], axis="x", color=LIGHT_PINK), (x, 0.57, z)))
    return geo


def heart_prism(depth=0.10, color=LIGHT_PINK):
    outline = []
    for k in range(LOD_CONFIG["heart_segments"]):
        t = 2 * math.pi * k / LOD_CONFIG["heart_segments"]
        x = 0.24 * math.sin(t) ** 3
        y = 0.19 * (0.82 * math.cos(t) - 0.34 * math.cos(2 * t) - 0.16 * math.cos(3 * t) - 0.08 * math.cos(4 * t))
        outline.append([x, y, 0])
    p, n, idx = [], [], []
    for z, sign in ((-depth / 2, -1), (depth / 2, 1)):
        center = len(p)
        p.append([0, 0, z]); n.append([0, 0, sign])
        ring = len(p)
        for x, y, _ in outline:
            p.append([x, y, z]); n.append([0, 0, sign])
        for k in range(len(outline)):
            q = (k + 1) % len(outline)
            idx += [center, ring + q, ring + k] if sign < 0 else [center, ring + k, ring + q]
    for k in range(len(outline)):
        q = (k + 1) % len(outline)
        base = len(p)
        a, b = outline[k], outline[q]
        normal = np.array([b[1] - a[1], -(b[0] - a[0]), 0.0])
        normal /= max(np.linalg.norm(normal), 1e-8)
        p += [[a[0], a[1], -depth / 2], [b[0], b[1], -depth / 2], [a[0], a[1], depth / 2], [b[0], b[1], depth / 2]]
        n += [normal] * 4
        idx += [base, base + 1, base + 2, base + 2, base + 1, base + 3]
    return p, n, color, idx


def build_geometry():
    parts = {}
    chassis, accent = Geo(), Geo()
    # Low armored hull with sloped-looking layered plates.
    chassis.add(transform(box((1.82, 0.58, 2.70), PINK), (0, 0.72, 0.05)))
    chassis.add(transform(box((1.58, 0.38, 2.10), PINK), (0, 1.10, 0.02)))
    chassis.add(transform(box((1.35, 0.22, 0.62), PINK), (0, 1.20, -1.16), rot_x(-0.22)))
    # Protective front and rear bumpers.
    chassis.add(transform(box((1.90, 0.24, 0.22), METAL), (0, 0.48, -1.50)))
    chassis.add(transform(box((1.80, 0.20, 0.18), METAL), (0, 0.48, 1.48)))
    parts["Chassis"] = [(chassis, 0)]

    # Turret collar, open cockpit lip, and cannon.
    accent.add(transform(torus(0.62, 0.10, LOD_CONFIG["collar_segments"], LOD_CONFIG["collar_tube_segments"], plane="xz", color=LIGHT_PINK), (0, 1.36, 0.02)))
    accent.add(transform(cylinder(0.50, 0.20, LOD_CONFIG["turret_segments"], axis="y", color=PINK), (0, 1.30, -0.30)))
    accent.add(transform(cylinder(0.14, 1.42, LOD_CONFIG["round_segments"], axis="z", color=LIGHT_PINK), (0, 1.45, -1.03)))
    accent.add(transform(cylinder(0.20, 0.20, LOD_CONFIG["round_segments"], axis="z", color=METAL), (0, 1.45, -1.77)))
    # Rear radio antennas and compact exhausts.
    for x in (-0.52, 0.52):
        accent.add(transform(cylinder(0.025, 0.72, 10, axis="y", color=METAL), (x, 1.55, 0.92)))
        accent.add(transform(cylinder(0.09, 0.46, 16, axis="z", color=METAL), (x, 0.76, 1.50)))
    # Original heart bullseye and central sparkle on the nose.
    accent.add(transform(heart_prism(), (0, 0.82, -1.58)))
    accent.add(transform(box((0.045, 0.16, 0.04), PINK), (0, 0.82, -1.65)))
    accent.add(transform(box((0.16, 0.045, 0.04), PINK), (0, 0.82, -1.65)))
    parts["AccentMesh"] = [(accent, 1)]

    steering = Geo()
    steering.add(torus(0.28, 0.035, LOD_CONFIG["steering_segments"], LOD_CONFIG["steering_tube_segments"], plane="xy", color=METAL))
    steering.add(cylinder(0.025, 0.50, 10, axis="x", color=METAL))
    parts["SteeringWheel"] = [(steering, 3)]

    left_track, right_track = rounded_track(-1), rounded_track(1)
    # Required wheel nodes serve as front/rear track sprocket assemblies.
    parts["Wheel_FL"] = [(left_track, 2)]
    parts["Wheel_FR"] = [(right_track, 2)]
    parts["Wheel_RL"] = []
    parts["Wheel_RR"] = []
    parts["Exhaust_L"] = []
    parts["Exhaust_R"] = []
    return parts


MATERIALS = [
    {"name": "PinkArmor", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.38, "roughnessFactor": 0.40}},
    {"name": "PinkAccent", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.18, "roughnessFactor": 0.34}},
    {"name": "TrackRubber", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.05, "roughnessFactor": 0.82}},
    {"name": "DarkHardware", "alphaMode": "OPAQUE", "doubleSided": True, "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.65, "roughnessFactor": 0.44}},
]


TRANSLATIONS = {
    "Chassis": [0, 0, 0], "AccentMesh": [0, 0, 0], "SteeringWheel": [0, 1.46, 0.48],
    "Wheel_FL": [0, 0, 0], "Wheel_FR": [0, 0, 0], "Wheel_RL": [0, 0, 0], "Wheel_RR": [0, 0, 0],
    "Exhaust_L": [-0.52, 0.76, 1.50], "Exhaust_R": [0.52, 0.76, 1.50],
    "DriverMount": [0, 1.58, 0.18], "ItemMountRear": [0, 1.02, 1.72], "ItemMountForward": [0, 1.18, -1.88],
}


def export_glb(parts):
    doc = {"asset": {"version": "2.0", "generator": "Minigame Mayhem Pink Precision builder"}, "scene": 0,
           "scenes": [{"nodes": [0]}], "nodes": [], "meshes": [], "materials": MATERIALS, "buffers": [{}],
           "bufferViews": [], "accessors": [], "extras": {"lod": f"LOD{LOD}", "forward": "-Z", "units": "meters", "approvedName": "Pink Precision"}}
    blob = bytearray()

    def accessor(arr, kind, component, target=None, minmax=False):
        while len(blob) % 4:
            blob.append(0)
        offset = len(blob)
        raw = arr.tobytes()
        blob.extend(raw)
        view = {"buffer": 0, "byteOffset": offset, "byteLength": len(raw)}
        if target:
            view["target"] = target
        doc["bufferViews"].append(view)
        item = {"bufferView": len(doc["bufferViews"]) - 1, "componentType": component, "count": len(arr), "type": kind}
        if minmax:
            item.update(min=arr.min(axis=0).tolist(), max=arr.max(axis=0).tolist())
        doc["accessors"].append(item)
        return len(doc["accessors"]) - 1

    mesh_index, triangle_count = {}, 0
    for name, primitives in parts.items():
        rendered = []
        for geo, material in primitives:
            p, n, c, i = geo.arrays()
            if not len(i):
                continue
            triangle_count += len(i) // 3
            indices = i.astype(np.uint16 if len(p) < 65536 else np.uint32)
            rendered.append({"attributes": {"POSITION": accessor(p, "VEC3", 5126, 34962, True),
                                             "NORMAL": accessor(n, "VEC3", 5126, 34962),
                                             "COLOR_0": accessor(c, "VEC4", 5126, 34962)},
                             "indices": accessor(indices, "SCALAR", 5123 if indices.dtype == np.uint16 else 5125, 34963),
                             "material": material, "mode": 4})
        if rendered:
            doc["meshes"].append({"name": name, "primitives": rendered})
            mesh_index[name] = len(doc["meshes"]) - 1

    names = ["KartRoot", "Chassis", "AccentMesh", "SteeringWheel", "Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR",
             "Exhaust_L", "Exhaust_R", "DriverMount", "ItemMountRear", "ItemMountForward"]
    doc["nodes"].append({"name": "KartRoot", "children": list(range(1, len(names))), "extras": {"triangleCount": triangle_count, "principalMaterials": 4}})
    for name in names[1:]:
        node = {"name": name, "translation": TRANSLATIONS[name]}
        if name in mesh_index:
            node["mesh"] = mesh_index[name]
        doc["nodes"].append(node)
    doc["buffers"][0]["byteLength"] = len(blob)
    payload = json.dumps(doc, separators=(",", ":")).encode()
    payload += b" " * ((4 - len(payload) % 4) % 4)
    blob += b"\0" * ((4 - len(blob) % 4) % 4)
    total = 12 + 8 + len(payload) + 8 + len(blob)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(struct.pack("<4sII", b"glTF", 2, total) + struct.pack("<I4s", len(payload), b"JSON") + payload + struct.pack("<I4s", len(blob), b"BIN\0") + blob)
    return triangle_count, doc


def preview(parts):
    triangles, colors = [], []
    light = np.array([-0.45, 0.82, -0.35]); light /= np.linalg.norm(light)
    for name, primitives in parts.items():
        offset = np.asarray(TRANSLATIONS[name])
        for geo, _ in primitives:
            p, _, c, i = geo.arrays(); p = p + offset
            for face in i.reshape(-1, 3):
                tri = p[face]
                normal = np.cross(tri[1] - tri[0], tri[2] - tri[0])
                length = np.linalg.norm(normal)
                if length < 1e-8:
                    continue
                normal /= length
                shade = 0.68 + 0.32 * max(0, float(np.dot(normal, light)))
                color = c[face].mean(axis=0).copy(); color[:3] = np.clip(color[:3] * shade + 0.045, 0, 1)
                triangles.append(tri[:, [0, 2, 1]]); colors.append(color)
    fig = plt.figure(figsize=(14, 12), dpi=150, facecolor="#150f1b")
    views = [(22, -44, "Front chase three-quarter"), (20, 136, "Rear three-quarter"), (66, -42, "Cockpit, cannon, and treads"), (10, -90, "Side silhouette")]
    for index, (elevation, azimuth, title) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, index, projection="3d", computed_zorder=False); ax.set_facecolor("#150f1b")
        ax.add_collection3d(Poly3DCollection(triangles, facecolors=colors, edgecolor=(0, 0, 0, 0.09), linewidth=0.12))
        ax.set_xlim(-1.85, 1.85); ax.set_ylim(-2.05, 2.05); ax.set_zlim(0.0, 2.15)
        ax.set_box_aspect((3.7, 4.1, 2.15)); ax.view_init(elevation, azimuth); ax.set_axis_off()
        ax.set_title(title, color="#fff2f8", fontsize=14, pad=4)
    fig.suptitle("PINK PRECISION • LOD0 CANDIDATE 1", color="#ff80ad", fontsize=22, fontweight="bold", y=0.98)
    fig.text(0.5, 0.018, "Compact armored racer • continuous tread loops • working-cannon silhouette • original heart bullseye", ha="center", color="#d9bfd0", fontsize=11)
    plt.subplots_adjust(left=0.01, right=0.99, top=0.94, bottom=0.04, wspace=0.01, hspace=0.02)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True); fig.savefig(PREVIEW, facecolor=fig.get_facecolor()); plt.close(fig)


def main():
    parts = build_geometry()
    triangles, doc = export_glb(parts)
    if os.environ.get("PINK_PRECISION_SKIP_PREVIEW") != "1":
        preview(parts)
    required = {"KartRoot", "Chassis", "AccentMesh", "SteeringWheel", "Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR", "Exhaust_L", "Exhaust_R", "DriverMount", "ItemMountRear", "ItemMountForward"}
    actual = {node["name"] for node in doc["nodes"]}
    assert required <= actual
    triangle_limit = (25000, 12000, 5000)[LOD]
    assert triangles <= triangle_limit
    assert len(doc["materials"]) <= 4
    print(json.dumps({"glb": str(OUT), "preview": str(PREVIEW), "lod": LOD, "triangles": triangles, "triangleLimit": triangle_limit,
                      "materials": len(doc["materials"]), "nodes": len(doc["nodes"]), "bytes": OUT.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
