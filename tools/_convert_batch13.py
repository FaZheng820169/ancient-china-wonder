# -*- coding: utf-8 -*-
"""Convert batch-13 ImageGen PNGs to web JPEGs (1400x933 q82 progressive)."""
import os, glob
from PIL import Image

OUT = 'public/images/stories'

MAP = [
    ("BrideDecoyScene", "the-bride-who-was-bait"),
    ("PheasantMatchScene", "the-pheasant-matchmaker"),
    ("DreamHouseholdScene", "the-household-in-a-dream"),
    ("HaloSevenLivesScene", "the-halo-of-seven-lives"),
    ("CoinHoleScene", "the-man-in-the-coin-hole"),
    ("GeomancerBonesScene", "the-geomancers-bones"),
    ("InventedDreamScene", "the-dream-he-invented"),
    ("CoverEyeGodScene", "the-god-who-covers-eyes"),
    ("LitigationWritersScene", "the-litigation-writers"),
    ("GhostBrothelScene", "the-ghost-brothel"),
    ("GodsGamblingScene", "the-gods-who-gambled"),
    ("TigerBinderScene", "the-man-who-bound-tigers"),
]

pngs = glob.glob(os.path.join(OUT, '*.png'))
print('PNG files found:', len(pngs))

ok = 0
for prefix, slug in MAP:
    hit = [p for p in pngs if os.path.basename(p).startswith(prefix)]
    if not hit:
        print('!! MISSING PNG for', prefix)
        continue
    src = hit[0]
    im = Image.open(src).convert('RGB')
    if im.size != (1400, 933):
        im = im.resize((1400, 933), Image.LANCZOS)
    dst = os.path.join(OUT, slug + '.jpg')
    im.save(dst, 'JPEG', quality=82, optimize=True, progressive=True)
    kb = os.path.getsize(dst) // 1024
    print('%-28s -> %-32s %4d KB' % (prefix, slug + '.jpg', kb))
    os.remove(src)
    ok += 1

print('\nconverted:', ok, '/', len(MAP))
left = glob.glob(os.path.join(OUT, '*.png'))
print('leftover PNGs:', len(left))
for p in left:
    print('   ', os.path.basename(p))
