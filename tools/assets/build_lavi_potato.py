"""Build Lavi's Potato GLBs.

Requires Python 3, NumPy, and Matplotlib. Set POTATO_LOD to LOD0, LOD1, or
LOD2; POTATO_OUT to the destination GLB; and POTATO_SKIP_PREVIEW=1 for a
headless production build.
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
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parent
LOD = os.environ.get("POTATO_LOD", "LOD0").upper()
DETAILS = {
    "LOD0": {"body":(72,36),"axle":16,"eye":(12,6),"stem":9,"leaf":(12,6),"scuff":(10,5),"steer":(26,8,10),"wheel":(24,18,12),"exhaust":(16,18,6),"limit":25000},
    "LOD1": {"body":(48,24),"axle":12,"eye":(10,5),"stem":7,"leaf":(10,5),"scuff":(8,4),"steer":(22,7,8),"wheel":(20,14,10),"exhaust":(14,14,5),"limit":12000},
    "LOD2": {"body":(32,16),"axle":8,"eye":(8,4),"stem":6,"leaf":(8,4),"scuff":(7,3),"steer":(16,5,6),"wheel":(14,10,6),"exhaust":(10,10,4),"limit":5000},
}
if LOD not in DETAILS:
    raise ValueError(f"Unknown POTATO_LOD: {LOD}")
DETAIL = DETAILS[LOD]
OUT = Path(os.environ.get("POTATO_OUT", ROOT / "potato-kart-candidate-4.glb"))
PREVIEW = Path(os.environ.get("POTATO_PREVIEW", ROOT / "potato-kart-candidate-4-preview.png"))

SKIN = np.array([0.48, 0.245, 0.095, 1.0], np.float32)
SKIN_LIGHT = np.array([0.62, 0.34, 0.14, 1.0], np.float32)
SOIL = np.array([0.25, 0.12, 0.055, 1.0], np.float32)
SPROUT = np.array([0.22, 0.43, 0.12, 1.0], np.float32)
TIRE = np.array([0.035, 0.04, 0.038, 1.0], np.float32)
METAL = np.array([0.16, 0.18, 0.18, 1.0], np.float32)


class Geo:
    def __init__(self):
        self.p, self.n, self.c, self.i = [], [], [], []

    def add(self, p, n, c, idx):
        base = len(self.p)
        self.p.extend(np.asarray(p, np.float32))
        self.n.extend(np.asarray(n, np.float32))
        colors = np.asarray(c, np.float32)
        if colors.ndim == 1:
            colors = np.tile(colors, (len(p), 1))
        self.c.extend(colors)
        self.i.extend((np.asarray(idx, np.uint32) + base).tolist())

    def arrays(self):
        return (np.asarray(self.p, np.float32), np.asarray(self.n, np.float32),
                np.asarray(self.c, np.float32), np.asarray(self.i, np.uint32))


def uv_ellipsoid(rx, ry, rz, seg=36, rings=18, color=SKIN, irregular=False):
    p, n, idx, cols = [], [], [], []
    for j in range(rings + 1):
        th = math.pi * j / rings
        for k in range(seg + 1):
            ph = 2 * math.pi * k / seg
            s = math.sin(th)
            f = 1.0
            if irregular:
                f += 0.045 * math.sin(3 * ph + 0.6) * s * s
                f += 0.025 * math.sin(5 * th + 2 * ph)
                f += 0.018 * math.cos(7 * ph - th)
            x, y, z = rx * s * math.cos(ph) * f, ry * math.cos(th) * f, rz * s * math.sin(ph) * f
            if irregular and y < -0.45:
                y = -0.45 + (y + 0.45) * 0.55
            p.append([x, y, z])
            nn = np.array([x / (rx * rx), y / (ry * ry), z / (rz * rz)])
            nn /= max(np.linalg.norm(nn), 1e-8)
            n.append(nn)
            if irregular:
                m = 0.5 + 0.5 * math.sin(ph * 4.0 + th * 3.0)
                soil = max(0.0, math.sin(ph * 5.0 - th * 2.0) - 0.78)
                cc = SKIN * (0.86 + 0.16 * m)
                cc[:3] = cc[:3] * (1.0 - 0.28 * soil)
                cc[3] = 1
                cols.append(cc)
            else:
                cols.append(color)
    for j in range(rings):
        for k in range(seg):
            a = j * (seg + 1) + k
            b = a + seg + 1
            idx += [a, b, a + 1, a + 1, b, b + 1]
    return p, n, cols, idx


def cylinder(radius, length, seg=20, axis="z", color=METAL, capped=True):
    p, n, idx = [], [], []
    for side in (-0.5, 0.5):
        for k in range(seg):
            a = 2 * math.pi * k / seg
            v = np.array([radius * math.cos(a), radius * math.sin(a), side * length])
            nn = np.array([math.cos(a), math.sin(a), 0.0])
            p.append(v); n.append(nn)
    for k in range(seg):
        q = (k + 1) % seg
        idx += [k, q, seg + k, q, seg + q, seg + k]
    if capped:
        for side, sign in ((-0.5, -1), (0.5, 1)):
            center = len(p); p.append([0, 0, side * length]); n.append([0, 0, sign])
            ring = len(p)
            for k in range(seg):
                a = 2 * math.pi * k / seg
                p.append([radius * math.cos(a), radius * math.sin(a), side * length]); n.append([0, 0, sign])
            for k in range(seg):
                q = (k + 1) % seg
                idx += [center, ring + q, ring + k] if sign < 0 else [center, ring + k, ring + q]
    p, n = np.asarray(p), np.asarray(n)
    if axis == "x":
        p = p[:, [2, 0, 1]]; n = n[:, [2, 0, 1]]
    elif axis == "y":
        p = p[:, [0, 2, 1]]; n = n[:, [0, 2, 1]]
    return p, n, color, idx


def torus(major_x, major_z, tube, seg=30, tube_seg=10, plane="xz", color=METAL):
    p, n, idx = [], [], []
    for a_i in range(seg):
        u = 2 * math.pi * a_i / seg
        for b_i in range(tube_seg):
            v = 2 * math.pi * b_i / tube_seg
            if plane == "xz":
                pos = [(major_x + tube * math.cos(v)) * math.cos(u), tube * math.sin(v),
                       (major_z + tube * math.cos(v)) * math.sin(u)]
                nn = [math.cos(v) * math.cos(u), math.sin(v), math.cos(v) * math.sin(u)]
            else:
                pos = [(major_x + tube * math.cos(v)) * math.cos(u),
                       (major_z + tube * math.cos(v)) * math.sin(u), tube * math.sin(v)]
                nn = [math.cos(v) * math.cos(u), math.cos(v) * math.sin(u), math.sin(v)]
            p.append(pos); n.append(nn)
    for a_i in range(seg):
        aa = (a_i + 1) % seg
        for b_i in range(tube_seg):
            bb = (b_i + 1) % tube_seg
            x = a_i * tube_seg + b_i; y = aa * tube_seg + b_i
            idx += [x, y, x - b_i + bb, x - b_i + bb, y, y - b_i + bb]
    return p, n, color, idx


def box(size, color=TIRE):
    sx, sy, sz = np.asarray(size) / 2
    verts = [[-sx,-sy,-sz],[sx,-sy,-sz],[sx,sy,-sz],[-sx,sy,-sz],[-sx,-sy,sz],[sx,-sy,sz],[sx,sy,sz],[-sx,sy,sz]]
    faces = [[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[3,7,6],[3,6,2],[0,4,7],[0,7,3],[1,2,6],[1,6,5]]
    p, n, idx = [], [], []
    for f in faces:
        a,b,c = [np.array(verts[q],float) for q in f]; nn=np.cross(b-a,c-a); nn/=np.linalg.norm(nn)
        base=len(p); p += [a,b,c]; n += [nn,nn,nn]; idx += [base,base+1,base+2]
    return p,n,color,idx


def elliptical_wall(rx, rz, y_top, y_bottom, seg=40, color=TIRE):
    """Closed opaque cockpit wall, with normals facing into the opening."""
    p, n, idx = [], [], []
    for y in (y_top, y_bottom):
        for k in range(seg):
            a = 2 * math.pi * k / seg
            x, z = rx * math.cos(a), rz * math.sin(a)
            inward = np.array([-math.cos(a) / rx, 0, -math.sin(a) / rz])
            inward /= max(np.linalg.norm(inward), 1e-8)
            p.append([x, y, z]); n.append(inward)
    for k in range(seg):
        q = (k + 1) % seg
        idx += [k, seg + k, q, q, seg + k, seg + q]
    return p, n, color, idx


def transform(data, translation=(0,0,0), rotation=None, scale=(1,1,1)):
    p,n,c,idx=data; p=np.asarray(p,float)*np.asarray(scale); n=np.asarray(n,float)
    if rotation is not None:
        p=p@rotation.T; n=n@rotation.T
    p += np.asarray(translation)
    return p,n,c,idx


def cut_top_opening(data, center=(0, 0, 0), radii=(0.68, 0.72), min_y=1.28):
    """Remove top-facing potato triangles to form the actual cockpit cavity."""
    p,n,c,idx=data; p=np.asarray(p); idx=np.asarray(idx).reshape(-1,3)
    cx,_,cz=center; rx,rz=radii; kept=[]
    for tri in idx:
        points=p[tri]
        aperture=((points[:,0]-cx)/rx)**2 + ((points[:,2]-cz)/rz)**2
        enters_opening=np.any((aperture < 1.0) & (points[:,1] > min_y))
        if not enters_opening:
            kept.extend(tri.tolist())
    return p,n,c,kept


def recompute_vertex_normals(p, idx):
    p=np.asarray(p,float); idx=np.asarray(idx).reshape(-1,3)
    normals=np.zeros_like(p)
    for tri in idx:
        a,b,c=p[tri]
        face=np.cross(b-a,c-a)
        length=np.linalg.norm(face)
        if length > 1e-10:
            face /= length
            normals[tri] += face
    lengths=np.linalg.norm(normals,axis=1)
    valid=lengths > 1e-10
    normals[valid] /= lengths[valid,None]
    normals[~valid] = (0,1,0)
    return normals


def sculpt_cockpit(data):
    """Press a cockpit into the potato without deleting its upper surface."""
    p,n,c,idx=data
    p=np.asarray(p,float).copy(); c=np.asarray(c,np.float32).copy()
    for k,point in enumerate(p):
        if point[1] <= BODY_CENTER_Y:
            continue
        r=math.sqrt((point[0]/.70)**2 + ((point[2]-.02)/.76)**2)
        if r < .76:
            p[k,1]=1.115+.035*(r/.76)**2
            c[k]=TIRE
        elif r < 1.14:
            t=(r-.76)/(.38)
            t=t*t*(3-2*t)
            inner_y=1.15
            p[k,1]=inner_y*(1-t)+point[1]*t
            c[k]=TIRE*(1-t)+c[k]*t
    n=recompute_vertex_normals(p,idx)
    return p,n,c,idx


def rot_x(a):
    c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])


BODY_CENTER_Y = 0.82
BODY_RX, BODY_RY, BODY_RZ = 1.18, 0.78, 1.72


def body_top_y(x, z):
    remaining = 1.0 - (x / BODY_RX) ** 2 - (z / BODY_RZ) ** 2
    return BODY_CENTER_Y + BODY_RY * math.sqrt(max(remaining, 0.0))


def body_side_x(side, y, z):
    remaining = 1.0 - ((y - BODY_CENTER_Y) / BODY_RY) ** 2 - (z / BODY_RZ) ** 2
    return side * BODY_RX * math.sqrt(max(remaining, 0.0))


def build_geometry():
    parts = {}
    chassis_skin, chassis_hw = Geo(), Geo()
    potato=transform(uv_ellipsoid(BODY_RX,BODY_RY,BODY_RZ,*DETAIL["body"],irregular=True), translation=(0,BODY_CENTER_Y,0))
    chassis_skin.add(*sculpt_cockpit(potato))
    # Four visible axle stubs overlap the organic body and wheel hubs. The
    # mechanical frame still reads as mostly hidden inside Potato.
    for side in (-1,1):
        for z in (-1.05,1.05):
            chassis_hw.add(*transform(cylinder(.105,.72,DETAIL["axle"],axis="x",color=METAL),translation=(side*1.02,.48,z)))
    parts["Chassis"]=[(chassis_skin,0),(chassis_hw,3)]

    accent=Geo()
    # Shallow potato eyes are embedded in the skin instead of hovering above it.
    side_eyes=[(-1,.88,-.72),(-1,.68,.12),(-1,.98,.78),(1,.76,-.38),(1,1.02,.58)]
    for side,y,z in side_eyes:
        x=body_side_x(side,y,z)-side*.055
        accent.add(*transform(uv_ellipsoid(.080,.10,.075,*DETAIL["eye"],color=SOIL),translation=(x,y,z)))
    for x,z in [(.45,-1.0),(-.42,1.0)]:
        y=body_top_y(x,z)-.050
        accent.add(*transform(uv_ellipsoid(.09,.075,.075,*DETAIL["eye"],color=SOIL),translation=(x,y,z)))
    # Three short rear sprouts begin inside the potato surface.
    for x,z,ang,h in [(-.34,1.24,-.22,.42),(0.05,1.36,.08,.50),(.39,1.18,.28,.36)]:
        root_y=body_top_y(x,z)-.110
        center_y=root_y+.5*h*math.cos(ang)
        center_z=z+.5*h*math.sin(ang)
        tip_y=root_y+h*math.cos(ang)
        tip_z=z+h*math.sin(ang)
        stem=transform(cylinder(.058,h,DETAIL["stem"],axis="y",color=SPROUT),translation=(x,center_y,center_z),rotation=rot_x(ang))
        accent.add(*stem)
        accent.add(*transform(uv_ellipsoid(.14,.06,.08,*DETAIL["leaf"],color=SPROUT),translation=(x,tip_y,tip_z)))
    # Short scuffs are also sunk slightly into the flanks.
    for side,y,z in [(-1,.54,-.25),(1,.64,.82),(-1,.42,1.05)]:
        x=body_side_x(side,y,z)-side*.045
        accent.add(*transform(uv_ellipsoid(.065,.035,.15,*DETAIL["scuff"],color=SOIL),translation=(x,y,z),rotation=rot_x(.25)))
    parts["AccentMesh"]=[(accent,1)]

    steer_seg,steer_tube,steer_spoke=DETAIL["steer"]
    steer=Geo(); steer.add(*torus(.34,.34,.045,steer_seg,steer_tube,plane="xy",color=METAL))
    steer.add(*cylinder(.035,.62,steer_spoke,axis="x",color=METAL))
    parts["SteeringWheel"]=[(steer,3)]

    for name,x,z in [("Wheel_FL",-1.33,-1.05),("Wheel_FR",1.33,-1.05),("Wheel_RL",-1.33,1.05),("Wheel_RR",1.33,1.05)]:
        tire_seg,hub_seg,tread_count=DETAIL["wheel"]
        tire,hub=Geo(),Geo(); tire.add(*cylinder(.46,.32,tire_seg,axis="x",color=TIRE)); hub.add(*cylinder(.19,.35,hub_seg,axis="x",color=METAL))
        for k in range(tread_count):
            a=2*math.pi*k/tread_count; center=(0,.50*math.cos(a),.50*math.sin(a))
            tire.add(*transform(box((.38,.105,.22),TIRE),translation=center,rotation=rot_x(-a)))
        parts[name]=[(tire,2),(hub,3)]

    for name in ("Exhaust_L","Exhaust_R"):
        exhaust_seg,exhaust_ring,exhaust_tube=DETAIL["exhaust"]
        g=Geo(); g.add(*cylinder(.105,.62,exhaust_seg,axis="z",color=METAL)); g.add(*torus(.11,.11,.025,exhaust_ring,exhaust_tube,plane="xy",color=METAL))
        parts[name]=[(g,3)]
    return parts


MATERIALS=[
 {"name":"PotatoSkin","alphaMode":"OPAQUE","doubleSided":True,"pbrMetallicRoughness":{"baseColorFactor":[1,1,1,1],"metallicFactor":0.0,"roughnessFactor":0.92}},
 {"name":"PotatoAccent","alphaMode":"OPAQUE","doubleSided":True,"pbrMetallicRoughness":{"baseColorFactor":[1,1,1,1],"metallicFactor":0.0,"roughnessFactor":0.88}},
 {"name":"TireRubber","alphaMode":"OPAQUE","doubleSided":True,"pbrMetallicRoughness":{"baseColorFactor":TIRE.tolist(),"metallicFactor":0.0,"roughnessFactor":0.82}},
 {"name":"Hardware","alphaMode":"OPAQUE","doubleSided":True,"pbrMetallicRoughness":{"baseColorFactor":METAL.tolist(),"metallicFactor":0.62,"roughnessFactor":0.48}},
]


def export_glb(parts):
    doc={"asset":{"version":"2.0","generator":"Accurate Artistry procedural Potato builder"},"scene":0,"scenes":[{"nodes":[0]}],"nodes":[],"meshes":[],"materials":MATERIALS,"buffers":[{}],"bufferViews":[],"accessors":[],"extras":{"lod":LOD,"forward":"-Z","units":"meters","approvedName":"Potato"}}
    blob=bytearray()
    def add_array(arr,target=None):
        while len(blob)%4: blob.append(0)
        off=len(blob); raw=arr.tobytes(); blob.extend(raw)
        bv={"buffer":0,"byteOffset":off,"byteLength":len(raw)}
        if target: bv["target"]=target
        doc["bufferViews"].append(bv); return len(doc["bufferViews"])-1
    def accessor(arr,typ,component,target=None,minmax=False):
        bv=add_array(arr,target); a={"bufferView":bv,"componentType":component,"count":len(arr),"type":typ}
        if minmax: a.update(min=arr.min(axis=0).tolist(),max=arr.max(axis=0).tolist())
        doc["accessors"].append(a); return len(doc["accessors"])-1
    mesh_index={}; total_tris=0
    for name,prims in parts.items():
        out=[]
        for geo,mat in prims:
            p,n,c,i=geo.arrays(); total_tris += len(i)//3
            ind=i.astype(np.uint16 if len(p)<65536 else np.uint32)
            out.append({"attributes":{"POSITION":accessor(p,"VEC3",5126,34962,True),"NORMAL":accessor(n,"VEC3",5126,34962),"COLOR_0":accessor(c,"VEC4",5126,34962)},"indices":accessor(ind,"SCALAR",5123 if ind.dtype==np.uint16 else 5125,34963),"material":mat,"mode":4})
        doc["meshes"].append({"name":name,"primitives":out}); mesh_index[name]=len(doc["meshes"])-1
    names=["KartRoot","Chassis","AccentMesh","SteeringWheel","Wheel_FL","Wheel_FR","Wheel_RL","Wheel_RR","Exhaust_L","Exhaust_R","DriverMount","ItemMountRear","ItemMountForward"]
    doc["nodes"].append({"name":"KartRoot","children":list(range(1,len(names))),"extras":{"triangleCount":total_tris,"principalMaterials":4}})
    transforms={"Chassis":[0,0,0],"AccentMesh":[0,0,0],"SteeringWheel":[0,1.45,-.45],"Wheel_FL":[-1.33,.48,-1.05],"Wheel_FR":[1.33,.48,-1.05],"Wheel_RL":[-1.33,.48,1.05],"Wheel_RR":[1.33,.48,1.05],"Exhaust_L":[-.62,.63,1.64],"Exhaust_R":[.62,.63,1.64],"DriverMount":[0,1.5,.08],"ItemMountRear":[0,1.0,1.95],"ItemMountForward":[0,1.0,-1.95]}
    for name in names[1:]:
        node={"name":name,"translation":transforms[name]}
        if name in mesh_index: node["mesh"]=mesh_index[name]
        doc["nodes"].append(node)
    doc["buffers"][0]["byteLength"]=len(blob)
    js=json.dumps(doc,separators=(",",":")).encode(); js += b" "*((4-len(js)%4)%4)
    blob += b"\0"*((4-len(blob)%4)%4)
    total=12+8+len(js)+8+len(blob)
    OUT.write_bytes(struct.pack("<4sII",b"glTF",2,total)+struct.pack("<I4s",len(js),b"JSON")+js+struct.pack("<I4s",len(blob),b"BIN\0")+blob)
    return total_tris, doc


def preview(parts):
    translations={"Chassis":(0,0,0),"AccentMesh":(0,0,0),"SteeringWheel":(0,1.45,-.45),"Wheel_FL":(-1.33,.48,-1.05),"Wheel_FR":(1.33,.48,-1.05),"Wheel_RL":(-1.33,.48,1.05),"Wheel_RR":(1.33,.48,1.05),"Exhaust_L":(-.62,.63,1.64),"Exhaust_R":(.62,.63,1.64)}
    tris=[]; colors=[]
    light=np.array([-0.5,0.85,-0.35]); light/=np.linalg.norm(light)
    for name,prims in parts.items():
        t=np.array(translations[name])
        for geo,mat in prims:
            p,n,c,i=geo.arrays(); p=p+t
            for q in i.reshape(-1,3):
                tri=p[q]; nn=np.cross(tri[1]-tri[0],tri[2]-tri[0]); ln=np.linalg.norm(nn)
                if ln<1e-8: continue
                nn/=ln; shade=.70+.30*max(0,float(np.dot(nn,light)))
                col=c[q].mean(axis=0).copy(); col[:3]=np.clip(col[:3]*shade+.055,0,1)
                # glTF is Y-up. Matplotlib is Z-up, so remap only for the
                # contact sheet; the exported model coordinates stay intact.
                tris.append(tri[:, [0,2,1]]); colors.append(col)
    fig=plt.figure(figsize=(14,12),dpi=140,facecolor="#111720")
    views=[(23,-45,"Front three-quarter"),(21,135,"Rear three-quarter"),(62,-40,"Cockpit and sprouts"),(12,-90,"Side silhouette")]
    for k,(el,az,title) in enumerate(views,1):
        ax=fig.add_subplot(2,2,k,projection="3d",computed_zorder=False); ax.set_facecolor("#111720")
        pc=Poly3DCollection(tris,facecolors=colors,edgecolor=(0,0,0,.07),linewidth=.12); ax.add_collection3d(pc)
        ax.set_xlim(-2.15,2.15); ax.set_ylim(-2.25,2.25); ax.set_zlim(0,2.35)
        ax.set_box_aspect((4.3,4.5,2.35)); ax.view_init(el,az); ax.set_axis_off(); ax.set_title(title,color="#eef4ef",fontsize=15,pad=4)
    fig.suptitle(f"POTATO • {LOD} APPROVED GEOMETRY",color="#f2d7a4",fontsize=22,fontweight="bold",y=.98)
    fig.text(.5,.018,"Continuous upper body • sculpted matte-black cockpit • four connected wheel axles",ha="center",color="#b9c6bf",fontsize=12)
    plt.subplots_adjust(left=.01,right=.99,top=.94,bottom=.04,wspace=.01,hspace=.02); fig.savefig(PREVIEW,facecolor=fig.get_facecolor()); plt.close(fig)


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    parts=build_geometry(); tri,doc=export_glb(parts)
    if os.environ.get("POTATO_SKIP_PREVIEW") != "1":
        preview(parts)
    required={"KartRoot","Chassis","AccentMesh","SteeringWheel","Wheel_FL","Wheel_FR","Wheel_RL","Wheel_RR","Exhaust_L","Exhaust_R","DriverMount","ItemMountRear","ItemMountForward"}
    actual={n["name"] for n in doc["nodes"]}
    assert required<=actual and tri<=DETAIL["limit"] and len(doc["materials"])<=4
    print(json.dumps({"glb":str(OUT),"lod":LOD,"triangleLimit":DETAIL["limit"],"triangles":tri,"materials":len(doc["materials"]),"nodes":len(doc["nodes"]),"bytes":OUT.stat().st_size},indent=2))

if __name__=="__main__": main()
