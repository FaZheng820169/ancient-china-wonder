"""Resize + rename the raw AI illustrations into web-ready JPEGs, then the raw
PNGs and staging folders can be removed."""

import os
import shutil
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEND = os.path.join(ROOT, "public", "gen", "d")
IMG = os.path.join(ROOT, "public", "images")

# (source, destination-relative, max-width)
MAP = [
    (os.path.join(GEND, "Traditional_Chinese_ink_wash_p_2026-10-14T13-50-23.png"), "hero.jpg", 1800),
    (os.path.join(GEND, "Traditional_Chinese_ink_wash_p_2026-10-14T13-50-27.png"), "worldview/fox-spirit.jpg", 1400),
    (os.path.join(GEND, "Traditional_Chinese_ink_wash_p_2026-10-14T13-50-31.png"), "stories/liu-yi.jpg", 1400),
    (os.path.join(IMG, "Traditional_Chinese_ink_wash_p_2026-10-14T13-49-30.png"), "stories/nie-xiaoqian.jpg", 1400),
    (os.path.join(IMG, "Traditional_Chinese_ink_wash_p_2026-10-14T13-49-31.png"), "stories/nie-yinniang.jpg", 1400),
    (os.path.join(IMG, "Traditional_Chinese_ink_wash_p_2026-10-14T13-49-33.png"), "stories/li-ji.jpg", 1400),
    (os.path.join(IMG, "Traditional_Chinese_ink_wash_p_2026-10-14T13-49-34.png"), "og-default.jpg", 1400),
    (os.path.join(IMG, "Traditional_Chinese_ink_wash_p_2026-10-14T13-49-35.png"), "worldview/kunlun.jpg", 1400),
    (os.path.join(IMG, "Traditional_Chinese_ink_wash_p_2026-10-14T13-49-38.png"), "worldview/underworld.jpg", 1400),
]

for src, rel, maxw in MAP:
    dst = os.path.join(IMG, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im = Image.open(src).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(dst, "JPEG", quality=80, optimize=True, progressive=True)
    print(f"{rel}: {im.width}x{im.height}  {os.path.getsize(dst)//1024} KB")

# cleanup raw staging
shutil.rmtree(os.path.join(ROOT, "public", "gen"), ignore_errors=True)
for f in os.listdir(IMG):
    if f.endswith(".png"):
        os.remove(os.path.join(IMG, f))
print("cleaned staging")
