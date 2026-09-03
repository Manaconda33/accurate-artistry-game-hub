from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "public/assets/characters/aa-07/driver"


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


def checker(im, m, square=10, strength=0.86):
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


def tint(im, m, color, strength=0.5):
    arr = np.array(im.convert("RGBA")).astype(float)
    mm = np.array(m).astype(float) / 255.0
    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    shade = np.clip(0.82 + (lum - 95) / 520, 0.68, 1.08)
    target = np.ones_like(arr[:, :, :3]) * np.array(color, float)
    target *= shade[:, :, None]
    a = (mm * strength)[:, :, None]
    arr[:, :, :3] = arr[:, :, :3] * (1 - a) + target * a
    return Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGBA")


def formal_details(im, cx=256, cy=198, scale=1.0):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    s = scale
    d.polygon([(cx-20*s,cy),(cx-3*s,cy+8*s),(cx-10*s,cy+21*s)], fill=(242,242,244,245))
    d.polygon([(cx+20*s,cy),(cx+3*s,cy+8*s),(cx+10*s,cy+21*s)], fill=(242,242,244,245))
    by = cy + 14*s
    d.polygon([(cx-2*s,by),(cx-19*s,by-8*s),(cx-19*s,by+8*s)], fill=(12,12,16,255))
    d.polygon([(cx+2*s,by),(cx+19*s,by-8*s),(cx+19*s,by+8*s)], fill=(12,12,16,255))
    d.ellipse((cx-4*s,by-4*s,cx+4*s,by+4*s), fill=(38,34,45,255))
    return Image.alpha_composite(im, ov)


def belt(im, rect, spacing=9):
    ov = Image.new("RGBA", im.size, (0,0,0,0))
    d = ImageDraw.Draw(ov)
    x0,y0,x1,y1 = rect
    d.rounded_rectangle(rect, radius=3, fill=(14,13,18,235), outline=(70,65,78,230), width=1)
    for x in range(x0+5, x1-4, spacing):
        y = (y0+y1)//2
        d.ellipse((x-1.5,y-1.5,x+1.5,y+1.5), fill=(215,212,222,225))
    return Image.alpha_composite(im, ov)


def preserve_alpha(candidate, source):
    candidate.putalpha(source.getchannel("A"))
    return candidate


def front_victory():
    path = DRIVER / "front-victory.png"
    src = Image.open(path).convert("RGBA")
    im = src.copy()
    polys = [
        [(90,185),(129,180),(151,205),(149,274),(132,319),(104,318),(84,280)],
        [(359,260),(409,284),(432,329),(412,387),(368,390),(359,345),(340,326),(335,281)],
        [(162,267),(190,244),(205,263),(204,376),(180,402),(156,345)],
        [(307,264),(325,244),(351,269),(365,345),(338,402),(308,376)],
    ]
    holes = [("ellipse", (64,158,130,240)), ("ellipse", (286,318,356,390))]
    im = checker(im, mask(im.size, polys, holes, 1.0), 10, 0.86)
    im = tint(im, mask(im.size, [[(210,244),(302,244),(307,370),(256,411),(205,370)]], blur=0.7), (20,18,24), 0.45)
    im = tint(im, mask(im.size, [[(238,207),(274,207),(279,242),(272,278),(256,297),(240,278),(233,242)]], blur=0.7), (245,244,246), 0.90)
    im = formal_details(im, 256, 198, 1.0)
    im = belt(im, (215,384,297,398), 9)
    pants = [[(68,408),(84,409),(96,494),(80,497)], [(428,409),(444,408),(432,497),(416,494)]]
    im = checker(im, mask(im.size, pants, blur=0.8), 9, 0.76)
    preserve_alpha(im, src).save(path)


def rear_state(filename, variant):
    path = DRIVER / filename
    src = Image.open(path).convert("RGBA")
    im = src.copy()
    left = [(73,247),(116,230),(150,253),(146,315),(128,364),(92,363),(70,322)]
    right = [(360,252),(401,231),(440,246),(454,318),(431,363),(393,364),(367,315)]
    if variant == "steer-left":
        left = [(69,245),(112,226),(150,250),(148,309),(128,363),(90,364),(65,317)]
        right = [(358,229),(408,212),(447,241),(461,300),(439,350),(396,354),(365,307)]
    elif variant == "steer-right":
        left = [(61,251),(104,233),(143,255),(148,310),(128,365),(88,366),(59,319)]
        right = [(365,242),(409,222),(449,246),(463,305),(441,353),(399,356),(369,310)]
    elif variant == "hit":
        left = [(59,245),(101,226),(142,249),(146,309),(126,365),(86,367),(56,317)]
        right = [(370,245),(413,226),(454,251),(466,313),(443,362),(402,363),(372,316)]
    elif variant == "victory":
        left = [(61,252),(102,235),(142,257),(146,313),(126,367),(86,369),(57,321)]
        right = [(374,222),(410,190),(445,206),(458,266),(445,321),(411,348),(380,309)]
    coat = [
        [(126,320),(180,294),(203,316),(197,430),(169,461),(127,441)],
        [(309,316),(333,294),(387,320),(386,441),(343,461),(315,430)],
        [(188,344),(226,334),(232,431),(206,457),(179,439)],
        [(280,334),(324,344),(333,439),(306,457),(280,431)],
    ]
    holes = [("ellipse", (72,220,150,300)), ("ellipse", (360,220,448,300))]
    im = checker(im, mask(im.size, [left,right] + coat, holes, 1.0), 10, 0.86)
    im = tint(im, mask(im.size, [[(208,286),(304,286),(320,424),(256,462),(192,424)]], blur=0.8), (19,17,23), 0.38)
    pants = [[(60,353),(78,354),(83,470),(65,472)], [(434,354),(452,353),(447,472),(429,470)]]
    im = checker(im, mask(im.size, pants, blur=0.8), 9, 0.70)
    preserve_alpha(im, src).save(path)


def validate(paths):
    for path in paths:
        im = Image.open(path).convert("RGBA")
        assert im.size == (512,512), (path, im.size)
        a = np.array(im.getchannel("A"))
        assert a.min() == 0 and a.max() == 255
        assert all(im.getpixel(p)[3] == 0 for p in [(0,0),(511,0),(0,511),(511,511)])


front_victory()
rear_state("rear.png", "rear")
rear_state("steer-left.png", "steer-left")
rear_state("steer-right.png", "steer-right")
rear_state("hit.png", "hit")
rear_state("victory.png", "victory")
validate([
    DRIVER / "front-victory.png",
    DRIVER / "rear.png",
    DRIVER / "steer-left.png",
    DRIVER / "steer-right.png",
    DRIVER / "hit.png",
    DRIVER / "victory.png",
])
