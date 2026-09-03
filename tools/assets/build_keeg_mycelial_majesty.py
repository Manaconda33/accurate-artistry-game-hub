"""Build a deterministic GLB and review sheet for Keeg's Mycelial Majesty.

Set MYCELIAL_LOD to LOD0, LOD1, or LOD2; MYCELIAL_OUT to the GLB
destination; and MYCELIAL_SKIP_PREVIEW=1 for headless production builds.
"""

import json
import math
import os
import struct
import zlib
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import build_manaconda_wayfinder as base


ROOT = Path(__file__).resolve().parent
LOD = os.environ.get("MYCELIAL_LOD", "LOD0").upper()
DETAILS = {
    "LOD0": {"round": 16, "tube": 8, "limit": 25000},
    "LOD1": {"round": 12, "tube": 6, "limit": 12000},
    "LOD2": {"round": 6, "tube": 3, "limit": 5000},
}
if LOD not in DETAILS:
    raise ValueError(f"Unknown MYCELIAL_LOD: {LOD}")
DETAIL = DETAILS[LOD]
OUT = Path(os.environ.get("MYCELIAL_OUT", ROOT / "candidates/mycelial-majesty-candidate-3.glb"))
PREVIEW = Path(os.environ.get("MYCELIAL_PREVIEW", ROOT / "candidates/mycelial-majesty-candidate-3-preview.png"))
CANDIDATE = os.environ.get("MYCELIAL_CANDIDATE", "3")
APPROVED_NAME = "The Mycelial Majesty"
GENERATOR = "Minigame Mayhem procedural Mycelial Majesty builder"
PREVIEW_TITLE = "THE MYCELIAL MAJESTY"
PREVIEW_VIEWS = ["Front three-quarter • mushroom crest at -Z", "Rear three-quarter • arcane exhaust housings", "Top • open cockpit and attached filigree", "Left profile • low enchanted grand-tourer stance"]
PREVIEW_FOOTER = "Royal purple grand-tourer • attached silver filigree • conventional arcane wheels • mushroom crest • open cockpit"
USE_VERTEX_COLORS = True
MATERIAL_TEXTURE_RGBA = None
PREVIEW_MATERIAL_RGBA = None

ROYAL_PURPLE = np.array([0.23, 0.025, 0.48, 1.0], np.float32)
LAVENDER = np.array([0.63, 0.20, 0.95, 1.0], np.float32)
SILVER = np.array([0.68, 0.72, 0.82, 1.0], np.float32)
CHARCOAL = np.array([0.045, 0.035, 0.065, 1.0], np.float32)
TIRE = np.array([0.018, 0.014, 0.025, 1.0], np.float32)
GLOW = np.array([0.82, 0.34, 1.0, 1.0], np.float32)
PASTEL = np.array([0.90, 0.63, 1.0, 1.0], np.float32)


def add_ellipsoid(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.ellipsoid(size, DETAIL["round"], max(5, DETAIL["round"] // 2), color), at, rotation))


def add_box(geo, size, at, color, rotation=None):
    geo.add(base.transform(base.box(size, color), at, rotation))


def add_cyl(geo, radius, length, at, axis, color, rotation=None, seg=None):
    geo.add(base.transform(base.cylinder(radius, length, seg or DETAIL["round"], axis, color), at, rotation))


def rot_z(angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def add_mushroom(geo, at, scale=1.0):
    x, y, z = at
    add_cyl(geo, 0.10 * scale, 0.30 * scale, (x, y - 0.12 * scale, z), "y", PASTEL)
    add_ellipsoid(geo, (0.42 * scale, 0.20 * scale, 0.42 * scale), (x, y + 0.08 * scale, z), GLOW)
    for dx, dz in ((-0.09, -0.04), (0.09, -0.04), (0, 0.08)):
        add_ellipsoid(geo, (0.05 * scale, 0.025 * scale, 0.05 * scale),
                      (x + dx * scale, y + 0.17 * scale, z + dz * scale), SILVER)


def build_geometry():
    parts = {}
    chassis, cockpit = base.Geo(), base.Geo()
    # Substantial enclosed grand-tourer body. Dark lower armor keeps the luminous
    # upper shell from reading as one inflated plastic shape.
    add_ellipsoid(chassis, (2.30, 0.58, 3.82), (0, 0.60, 0.05), CHARCOAL)
    add_ellipsoid(chassis, (2.26, 0.64, 3.56), (0, 0.78, -0.04), ROYAL_PURPLE)
    add_ellipsoid(chassis, (2.12, 0.38, 2.54), (0, 1.08, -0.18), LAVENDER)
    # Layered prow tapers toward -Z and carries the visual weight of the reference.
    add_ellipsoid(chassis, (2.18, 0.70, 1.72), (0, 0.88, -1.42), ROYAL_PURPLE)
    add_ellipsoid(chassis, (1.74, 0.42, 1.28), (0, 1.18, -1.52), LAVENDER)
    # Unified rear cowl instead of exposed rectangular hardware.
    add_ellipsoid(chassis, (2.18, 0.58, 1.16), (0, 0.90, 1.38), ROYAL_PURPLE)
    add_ellipsoid(chassis, (1.64, 0.32, 0.82), (0, 1.18, 1.46), LAVENDER)
    # Recessed upholstered cockpit and a defined backrest/dashboard surround.
    add_ellipsoid(cockpit, (1.34, 0.16, 1.22), (0, 1.29, 0.28), CHARCOAL)
    add_ellipsoid(cockpit, (1.02, 0.26, 0.76), (0, 1.35, 0.48), CHARCOAL)
    add_ellipsoid(cockpit, (1.48, 0.34, 0.28), (0, 1.38, 0.92), ROYAL_PURPLE)
    for x in (-0.78, 0.78):
        add_ellipsoid(cockpit, (0.26, 0.40, 1.32), (x, 1.28, 0.20), SILVER)
        add_ellipsoid(cockpit, (0.16, 0.32, 1.18), (x, 1.34, 0.18), ROYAL_PURPLE)
    parts["Chassis"] = [(chassis, 0), (cockpit, 3)]

    accent, magic = base.Geo(), base.Geo()
    # Enclosed sculpted fenders wrap each wheel and merge into the body.
    for x in (-0.82, 0.82):
        for z in (-1.08, 1.12):
            side = -1 if x < 0 else 1
            # Do not place a solid ellipsoid over the wheel: without a boolean
            # wheel opening it becomes a tire intersection, not a true fender.
            add_ellipsoid(accent, (0.23, 0.12, 0.60), (x + side * 0.04, 1.10, z), SILVER)
            add_ellipsoid(accent, (0.17, 0.08, 0.48), (x + side * 0.04, 1.15, z), ROYAL_PURPLE)
            add_cyl(accent, 0.09, 0.64, (x + side * 0.25, 0.60, z), "x", SILVER)
    # Silver lower blade and side inlays are attached to the shell, not exposed rails.
    add_ellipsoid(accent, (2.34, 0.16, 3.30), (0, 0.48, -0.02), SILVER)
    add_ellipsoid(accent, (2.18, 0.14, 3.08), (0, 0.52, -0.02), CHARCOAL)
    for x in (-1.08, 1.08):
        add_ellipsoid(accent, (0.16, 0.20, 2.72), (x, 0.92, -0.06), SILVER)
        for z in (-0.72, 0.12, 0.92):
            accent.add(base.transform(base.torus(0.20, 0.042, DETAIL["round"], DETAIL["tube"], "y", SILVER),
                                      (x, 1.02, z), base.rot_x(math.pi / 2)))
    # Large framed shield medallion, layered proud of the nose.
    add_ellipsoid(accent, (1.58, 0.82, 0.26), (0, 0.92, -2.04), SILVER)
    add_ellipsoid(accent, (1.30, 0.66, 0.22), (0, 0.94, -2.18), ROYAL_PURPLE)
    add_ellipsoid(accent, (0.92, 0.48, 0.16), (0, 0.96, -2.31), CHARCOAL)
    add_cyl(magic, 0.12, 0.38, (0, 0.82, -2.43), "y", PASTEL)
    add_ellipsoid(magic, (0.62, 0.25, 0.18), (0, 1.10, -2.43), GLOW)
    for x in (-0.16, 0, 0.16):
        add_ellipsoid(magic, (0.055, 0.035, 0.035), (x, 1.11, -2.25), SILVER)
    # Jewel-like mushroom lamps emerge from sculpted housings.
    for x in (-0.92, 0.92):
        add_ellipsoid(accent, (0.46, 0.19, 0.52), (x, 1.18, -0.96), SILVER)
        add_ellipsoid(accent, (0.36, 0.15, 0.42), (x, 1.25, -0.96), ROYAL_PURPLE)
        add_mushroom(magic, (x, 1.34, -0.96), 0.50)
    # Rear arcane exhausts are nested into the continuous cowl.
    for x in (-0.64, 0.64):
        add_ellipsoid(accent, (0.58, 0.44, 0.58), (x, 1.10, 1.62), SILVER)
        add_ellipsoid(accent, (0.44, 0.34, 0.44), (x, 1.12, 1.76), CHARCOAL)
        magic.add(base.transform(base.torus(0.18, 0.050, DETAIL["round"], DETAIL["tube"], "x", GLOW),
                                 (x, 1.13, 1.92)))
    parts["AccentMesh"] = [(accent, 1), (magic, 3)]

    steering = base.Geo()
    wheel_tilt = math.radians(16)
    steering.add(base.transform(base.torus(0.36, 0.050, DETAIL["round"], DETAIL["tube"], "y", CHARCOAL),
                                rotation=base.rot_x(math.pi / 2 + wheel_tilt)))
    for angle in (0, math.pi * 2 / 3, math.pi * 4 / 3):
        steering.add(base.transform(base.box((0.54, 0.045, 0.045), SILVER),
                                    rotation=base.rot_x(wheel_tilt) @ rot_z(angle)))
    add_cyl(steering, 0.085, 0.12, (0, 0, 0), "z", GLOW, base.rot_x(wheel_tilt))
    # Diagonal column runs from the hub forward/down into the dashboard shell.
    add_cyl(steering, 0.060, 0.86, (0, -0.30, -0.30), "z", SILVER,
            base.rot_x(math.radians(135)))
    # Reinforced collar overlaps the dashboard shell so the shaft has a visible,
    # structural chassis termination rather than a floating endpoint.
    add_cyl(steering, 0.115, 0.18, (0, -0.58, -0.58), "z", ROYAL_PURPLE,
            base.rot_x(math.radians(135)))
    parts["SteeringWheel"] = [(steering, 1)]

    for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"):
        tire, hub = base.Geo(), base.Geo()
        tire.add(base.torus(0.49, 0.17, DETAIL["round"], DETAIL["tube"], "x", TIRE))
        tire.add(base.torus(0.49, 0.060, DETAIL["round"], DETAIL["tube"], "x", GLOW))
        tire.add(base.torus(0.31, 0.055, DETAIL["round"], DETAIL["tube"], "x", SILVER))
        add_cyl(hub, 0.25, 0.32, (0, 0, 0), "x", ROYAL_PURPLE)
        add_cyl(hub, 0.12, 0.40, (0, 0, 0), "x", GLOW)
        parts[name] = [(tire, 2), (hub, 1)]

    for name in ("Exhaust_L", "Exhaust_R"):
        exhaust, glow = base.Geo(), base.Geo()
        add_cyl(exhaust, 0.18, 0.64, (0, 0, 0), "z", SILVER, base.rot_x(-0.12))
        exhaust.add(base.transform(base.torus(0.19, 0.045, DETAIL["round"], DETAIL["tube"], "x", ROYAL_PURPLE),
                                   (0, 0, 0.34)))
        add_ellipsoid(glow, (0.21, 0.21, 0.48), (0, 0.01, 0.52), GLOW)
        parts[name] = [(exhaust, 1), (glow, 3)]
    return parts


TRANSLATIONS = {
    "Chassis": (0, 0, 0), "AccentMesh": (0, 0, 0),
    "SteeringWheel": (0, 1.72, -0.48),
    "Wheel_FL": (-1.42, 0.54, -1.05), "Wheel_FR": (1.42, 0.54, -1.05),
    "Wheel_RL": (-1.42, 0.54, 1.13), "Wheel_RR": (1.42, 0.54, 1.13),
    "Exhaust_L": (-0.62, 0.84, 1.72), "Exhaust_R": (0.62, 0.84, 1.72),
    "DriverMount": (0, 1.55, 0.25), "ItemMountRear": (0, 1.18, 2.02),
    "ItemMountForward": (0, 0.91, -2.20),
}

MATERIALS = [
    {"name": "RoyalPurpleBody", "alphaMode": "OPAQUE", "doubleSided": True,
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.38, "roughnessFactor": 0.30}},
    {"name": "SilverFiligree", "alphaMode": "OPAQUE", "doubleSided": True,
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.72, "roughnessFactor": 0.24}},
    {"name": "ConventionalTire", "alphaMode": "OPAQUE", "doubleSided": True,
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.02, "roughnessFactor": 0.90}},
    {"name": "LavenderArcaneGlow", "alphaMode": "OPAQUE", "doubleSided": True,
     "emissiveFactor": [0.55, 0.12, 0.82],
     "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.12, "roughnessFactor": 0.22}},
]


def export_glb(parts):
    doc = {
        "asset": {"version": "2.0", "generator": GENERATOR},
        "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [], "meshes": [],
        "materials": MATERIALS, "buffers": [{}], "bufferViews": [], "accessors": [],
        "extras": {"lod": LOD, "forward": "-Z", "units": "meters", "approvedName": APPROVED_NAME},
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

    if MATERIAL_TEXTURE_RGBA:
        doc["images"], doc["textures"], doc["samplers"] = [], [], [{"magFilter": 9729, "minFilter": 9729, "wrapS": 10497, "wrapT": 10497}]
        # Texture 0 is intentionally unused. Some mobile viewers incorrectly
        # treat a valid texture index of zero as a false/missing value.
        texture_colors = [(255, 255, 255, 255), *MATERIAL_TEXTURE_RGBA]
        for index, rgba in enumerate(texture_colors):
            raw = bytes([0, *rgba])
            compressed = zlib.compress(raw, 9)
            def chunk(kind, payload):
                return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
            png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")
            while len(blob) % 4:
                blob.append(0)
            offset = len(blob); blob.extend(png)
            doc["bufferViews"].append({"buffer": 0, "byteOffset": offset, "byteLength": len(png)})
            doc["images"].append({"bufferView": len(doc["bufferViews"]) - 1, "mimeType": "image/png", "name": f"MaterialColor{index}"})
            doc["textures"].append({"sampler": 0, "source": index})
            if index > 0:
                material = MATERIALS[index - 1]
                material["pbrMetallicRoughness"]["baseColorFactor"] = [1, 1, 1, 1]
                material["pbrMetallicRoughness"]["baseColorTexture"] = {"index": index, "texCoord": 0}

    mesh_index, total_triangles = {}, 0
    for name, primitives in parts.items():
        exported = []
        for geo, material in primitives:
            positions, normals, colors, indices = geo.arrays()
            total_triangles += len(indices) // 3
            packed = indices.astype(np.uint16 if len(positions) < 65536 else np.uint32)
            attributes = {
                "POSITION": accessor(positions, "VEC3", 5126, 34962, True),
                "NORMAL": accessor(normals, "VEC3", 5126, 34962)}
            if USE_VERTEX_COLORS:
                attributes["COLOR_0"] = accessor(colors, "VEC4", 5126, 34962)
            if MATERIAL_TEXTURE_RGBA:
                attributes["TEXCOORD_0"] = accessor(np.zeros((len(positions), 2), dtype=np.float32), "VEC2", 5126, 34962)
            exported.append({"attributes": attributes,
                "indices": accessor(packed, "SCALAR", 5123 if packed.dtype == np.uint16 else 5125, 34963),
                "material": material, "mode": 4})
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
        for geo, material in primitives:
            p, _n, c, indices = geo.arrays(); p = p + translation
            for ids in indices.reshape(-1, 3):
                tri = p[ids]
                normal = np.cross(tri[1] - tri[0], tri[2] - tri[0]); length = np.linalg.norm(normal)
                if length < 1e-9:
                    continue
                normal /= length
                shade = 0.62 + 0.38 * max(0, float(np.dot(normal, light)))
                if PREVIEW_MATERIAL_RGBA:
                    color = np.asarray(PREVIEW_MATERIAL_RGBA[material], dtype=np.float32) / 255.0
                else:
                    color = c[ids].mean(axis=0).copy()
                color[:3] = np.clip(color[:3] * shade + 0.035, 0, 1)
                triangles.append(tri[:, [0, 2, 1]]); colors.append(color)
    fig = plt.figure(figsize=(14, 12), dpi=150, facecolor="#090616")
    views = [(20, -42, PREVIEW_VIEWS[0]), (20, 138, PREVIEW_VIEWS[1]),
             (72, -90, PREVIEW_VIEWS[2]), (10, -90, PREVIEW_VIEWS[3])]
    for index, (elevation, azimuth, title) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, index, projection="3d", computed_zorder=False)
        ax.set_facecolor("#090616")
        ax.add_collection3d(Poly3DCollection(triangles, facecolors=colors, edgecolor=(0, 0, 0, 0.12), linewidth=0.12))
        ax.set_xlim(-2.15, 2.15); ax.set_ylim(-2.35, 2.35); ax.set_zlim(0, 2.20)
        ax.set_box_aspect((4.3, 4.7, 2.2)); ax.view_init(elevation, azimuth); ax.set_axis_off()
        ax.set_title(title, color="#f1dfff", fontsize=13, pad=4)
    fig.suptitle(f"{PREVIEW_TITLE} • {LOD} CANDIDATE {CANDIDATE}", color="#d890ff", fontsize=20, fontweight="bold", y=0.98)
    fig.text(0.5, 0.018, PREVIEW_FOOTER,
             ha="center", color="#c8b2dc", fontsize=11)
    plt.subplots_adjust(left=0.01, right=0.99, top=0.94, bottom=0.04, wspace=0.01, hspace=0.02)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PREVIEW, facecolor=fig.get_facecolor()); plt.close(fig)


def main():
    parts = build_geometry()
    triangles, doc = export_glb(parts)
    if os.environ.get("MYCELIAL_SKIP_PREVIEW") != "1":
        preview(parts)
    required = {"KartRoot", "Chassis", "AccentMesh", "SteeringWheel", "Wheel_FL", "Wheel_FR", "Wheel_RL",
                "Wheel_RR", "Exhaust_L", "Exhaust_R", "DriverMount", "ItemMountRear", "ItemMountForward"}
    actual = {node["name"] for node in doc["nodes"]}
    assert required <= actual and triangles <= DETAIL["limit"] and len(doc["materials"]) <= 4
    print(json.dumps({"glb": str(OUT), "preview": str(PREVIEW), "lod": LOD,
                      "triangleLimit": DETAIL["limit"], "triangles": triangles,
                      "materials": len(doc["materials"]), "nodes": len(doc["nodes"]),
                      "bytes": OUT.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
