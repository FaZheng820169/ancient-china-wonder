"""Stage raw AI illustrations: build an indexed contact sheet so they can be
identified, and keep a stable ordered list of source files."""

import glob
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "images")
SHEET = os.path.join(ROOT, "tools", "_contact_sheet.png")

files = sorted(glob.glob(os.path.join(ROOT, "public", "**", "*.png"), recursive=True))
files = [f for f in files if "_contact_sheet" not in f and not f.endswith(("favicon.png", "og-default.jpg"))]

COLS, CELL = 3, 380
rows = (len(files) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * CELL, rows * (CELL + 24)), "white")
draw = ImageDraw.Draw(sheet)

for i, f in enumerate(files):
    im = Image.open(f).convert("RGB")
    im.thumbnail((CELL, CELL))
    x = (i % COLS) * CELL
    y = (i // COLS) * (CELL + 24)
    sheet.paste(im, (x + (CELL - im.width) // 2, y))
    draw.text((x + 6, y + CELL + 4), f"{i:02d}  {os.path.basename(f)[-24:-4]}", fill="black")

sheet.save(SHEET)
print(f"{len(files)} images -> {SHEET}")
for i, f in enumerate(files):
    print(f"{i:02d}\t{f}")
