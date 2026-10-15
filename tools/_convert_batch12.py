# -*- coding: utf-8 -*-
"""Convert the 12 batch-12 Xieduo illustrations from PNG to web-ready JPEGs."""
import os, glob
from PIL import Image

IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "images", "stories")
MAP = [
    ("TigerFoolScene", "tiger-fool"),
    ("AdvanceMourningScene", "the-advance-mourning"),
    ("PaintingJealousyScene", "the-painting-that-cured-jealousy"),
    ("ExorcismShangqingScene", "the-exorcism-at-shangqing"),
    ("GirlAvengerScene", "the-girl-who-avenged-herself"),
    ("DogMaidScene", "the-dog-maid"),
    ("DreamWithinDreamScene", "dream-within-a-dream"),
    ("ActressDeathScene", "the-actress-who-married-in-death"),
    ("BeggarFlatteryScene", "the-beggar-who-learned-to-flatter"),
    ("TalentPrideScene", "the-talented-man-chastened"),
    ("HenpeckedMagistrateScene", "the-henpecked-magistrate"),
    ("VillageGirlTongueScene", "the-village-girl-with-the-sharp-tongue"),
]

for prefix, slug in MAP:
    pngs = sorted(glob.glob(os.path.join(IMG, prefix + "*.png")))
    if not pngs:
        print("!! NO PNG for", prefix); continue
    src = pngs[0]
    dst = os.path.join(IMG, slug + ".jpg")
    im = Image.open(src).convert("RGB")
    if im.width > 1400:
        im = im.resize((1400, 933), Image.LANCZOS)
    im.save(dst, "JPEG", quality=82, optimize=True, progressive=True)
    os.remove(src)
    print("%-44s %5d KB" % (slug + ".jpg", os.path.getsize(dst)//1024))
print("done")
