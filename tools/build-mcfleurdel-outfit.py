from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CHAR = ROOT / "public/assets/characters/aa-07"


def mask(size, polys, holes=None, blur=0.8, scale=4):
    w, h = size
    m = Image.new("L", (w * scale, h * scale), 0)
    d = ImageDraw.Draw(m)
    for poly in polys:
        d.polygon([(int(x * scale), int(y * scale)) for x, y in poly], fill=255)
    for kind, data in holes or []:
        if kind == "ellipse":
            d.ellipse(tuple(int(v * scale) for v in data), fill=0)
        else:
            d.polygon([(int(x * scale), int(y * scale)) for x, y in data], fill=0)
    m = m.resize((w, h), Image.Resampling.LANCZOS)
    return m.filter(ImageFilter.GaussianBlur(blur)) if blur else m


def checker(im, m, square=11, strength=0.88):
    arr = np.array(im.convert("RGBA")).astype(float)
    mm = np.array(m).astype(float) / 255.0
    h, w = mm.shape
    yy, xx = np.mgrid[:h, :w]
    chk = ((xx // square + yy // square) % 2) == 0
    target = np.empty((h, w, 3), float)
    target[chk] = [244, 244, 246]
    target[~chk] = [16, 15, 20]
    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    shade = np.clip(0.80 + (lum - 85) / 430, 0.66, 1.10)
    target *= shade[:, :, None]
    a = (mm * strength)[:, :, None]
    arr[:, :, :3] = arr[:, :, :3] * (1 - a) + target * a
    return Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGBA")


def tint(im, m, color, strength=0.65):
    arr = np.array(im.convert("RGBA")).astype(float)
    mm = np.array(m).astype(float) / 255.0
    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    shade = np.clip(0.82 + (lum - 95) / 520, 0.68, 1.08)
    target = np.ones_like(arr[:, :, :3]) * np.array(color, float)
    target *= shade[:, :, None]
    a = (mm * strength)[:, :, None]
    arr[:, :, :3] = arr[:, :, :3] * (1 - a) + target * a
    return Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGBA")


def formal_details(im, cx, cy, scale=1.0):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    s = scale
    d.polygon([(cx - 20*s, cy), (cx - 3*s, cy + 8*s), (cx - 10*s, cy + 21*s)], fill=(242,242,244,245))
    d.polygon([(cx + 20*s, cy), (cx + 3*s, cy + 8*s), (cx + 10*s, cy + 21*s)], fill=(242,242,244,245))
    by = cy + 14*s
    d.polygon([(cx - 2*s, by), (cx - 19*s, by - 8*s), (cx - 19*s, by + 8*s)], fill=(12,12,16,255))
    d.polygon([(cx + 2*s, by), (cx + 19*s, by - 8*s), (cx + 19*s, by + 8*s)], fill=(12,12,16,255))
    d.ellipse((cx - 4*s, by - 4*s, cx + 4*s, by + 4*s), fill=(38,34,45,255))
    return Image.alpha_composite(im, ov)


def belt(im, rect, spacing=8):
    ov = Image.new("RGBA", im.size, (0,0,0,0))
    d = ImageDraw.Draw(ov)
    x0,y0,x1,y1 = rect
    d.rounded_rectangle(rect, radius=3, fill=(14,13,18,235), outline=(70,65,78,230), width=1)
    for x in range(x0 + 5, x1 - 4, spacing):
        y = (y0 + y1) // 2
        d.ellipse((x-1.5,y-1.5,x+1.5,y+1.5), fill=(215,212,222,225))
    return Image.alpha_composite(im, ov)


def preserve_alpha(candidate, source):
    candidate.putalpha(source.getchannel("A"))
    return candidate


def portrait():
    path = CHAR / "portrait.png"
    src = Image.open(path).convert("RGBA")
    im = src.copy()
    checker_polys = [
        [(47,150),(66,136),(85,130),(96,153),(89,197),(76,238),(54,249),(43,204)],
        [(172,130),(194,137),(215,196),(208,245),(184,238),(166,202),(160,153)],
        [(80,151),(95,134),(104,150),(105,204),(91,231),(77,213)],
        [(153,148),(168,133),(180,151),(184,210),(169,233),(151,205)],
    ]
    im = checker(im, mask(im.size, checker_polys, [("ellipse", (95,147,161,220))], 0.6), 7, 0.88)
    im = tint(im, mask(im.size, [[(100,136),(156,136),(158,207),(128,235),(98,207)]], blur=0.5), (20,18,24), 0.50)
    im = tint(im, mask(im.size, [[(119,114),(137,114),(140,134),(136,154),(128,163),(120,154),(116,134)]], blur=0.5), (246,245,247), 0.92)
    im = formal_details(im, 128, 110, 0.56)
    im = belt(im, (104,213,152,221), 6)
    preserve_alpha(im, src).save(path)


def front_state(filename, variant):
    path = CHAR / "driver" / filename
    src = Image.open(path).convert("RGBA")
    im = src.copy()
    sets = {
        "front": [
            [(102,291),(151,263),(177,282),(171,327),(153,346),(144,391),(102,388),(84,334)],
            [(360,263),(410,291),(430,334),(411,389),(368,391),(360,346),(340,327),(335,282)],
        ],
        "steer-left": [
            [(96,282),(145,258),(177,278),(174,321),(150,347),(141,388),(95,382),(76,326)],
            [(359,257),(411,281),(439,323),(417,381),(370,389),(359,344),(334,327),(329,281)],
        ],
        "steer-right": [
            [(92,277),(143,257),(176,277),(173,319),(148,344),(139,388),(92,381),(74,323)],
            [(359,255),(414,279),(443,321),(419,381),(370,389),(358,344),(332,325),(328,280)],
        ],
        "hit": [
            [(92,280),(145,258),(176,278),(172,321),(148,347),(138,390),(91,384),(72,326)],
            [(360,258),(417,283),(446,324),(421,382),(371,391),(358,346),(331,328),(327,281)],
        ],
    }
    outer = sets[variant]
    outer += [
        [(162,268),(190,246),(205,265),(205,374),(181,402),(157,345)],
        [(307,264),(325,246),(352,271),(365,345),(338,401),(308,374)],
    ]
    holes = [("ellipse", (156,319,226,390)), ("ellipse", (286,319,356,390))]
    im = checker(im, mask(im.size, outer, holes, 1.0), 10, 0.86)
    im = tint(im, mask(im.size, [[(210,244),(302,244),(307,370),(256,411),(205,370)]], blur=0.7), (20,18,24), 0.45)
    im = tint(im, mask(im.size, [[(238,207),(274,207),(279,242),(272,278),(256,297),(240,278),(233,242)]], blur=0.7), (245,244,246), 0.90)
    im = formal_details(im, 256, 198, 1.0)
    im = belt(im, (215,384,297,398), 9)
    pants = [[(68,408),(84,409),(96,494),(80,497)], [(428,409),(444,408),(432,497),(416,494)]]
    im = checker(im, mask(im.size, pants, blur=0.8), 9, 0.76)
    preserve_alpha(im, src).save(path)


def validate(paths):
    for path, size in paths:
        im = Image.open(path).convert("RGBA")
        assert im.size == size, (path, im.size)
        a = np.array(im.getchannel("A"))
        assert a.min() == 0 and a.max() == 255
        assert all(im.getpixel(p)[3] == 0 for p in [(0,0),(size[0]-1,0),(0,size[1]-1),(size[0]-1,size[1]-1)])


portrait()
front_state("front.png", "front")
front_state("front-steer-left.png", "steer-left")
front_state("front-steer-right.png", "steer-right")
front_state("front-hit.png", "hit")
validate([
    (CHAR / "portrait.png", (256,256)),
    (CHAR / "driver/front.png", (512,512)),
    (CHAR / "driver/front-steer-left.png", (512,512)),
    (CHAR / "driver/front-steer-right.png", (512,512)),
    (CHAR / "driver/front-hit.png", (512,512)),
])
