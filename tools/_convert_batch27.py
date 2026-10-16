# -*- coding: utf-8 -*-
"""Convert batch-27 PNGs to 1400x933 progressive JPEGs. No watermark erase."""
import glob
import os
from PIL import Image

SRC = 'public/images/stories'
MAP = {
    'TraitorLackeyTempleScene': 'the-temple-of-the-traitors-lackey',
    'GodOfBooksRevengeScene': 'the-god-of-books-who-took-revenge',
    'VetTreatsDeadScene': 'the-vet-who-treated-the-dead',
    'GhostShrankSoldierScene': 'the-ghost-who-shrank-before-a-soldier',
    'GhostTutorBroomScene': 'the-ghost-tutor-of-broom-village',
    'LotusImmortalTestScene': 'the-lotus-immortal-who-tested-a-son',
    'PoetsThroughWallScene': 'the-poets-through-the-window',
    'OracleSlipsTempleScene': 'the-oracle-slips-of-general-bus-temple',
    'BlueStarGodScene': 'why-the-literary-star-god-is-blue',
    'LotusRootGirlScene': 'the-girl-with-the-lotus-root',
    'CrowOmenScene': 'the-crow-who-knew-a-man-before-his-rise',
    'MaidCatchesBulletsScene': 'the-maid-who-caught-the-bullets',
}

for prefix, slug in MAP.items():
    hits = sorted(glob.glob(os.path.join(SRC, prefix + '__*.png')))
    if not hits:
        print('!! MISSING PNG for', prefix)
        continue
    im = Image.open(hits[-1]).convert('RGB')
    im = im.resize((1400, 933), Image.LANCZOS)
    out = os.path.join(SRC, slug + '.jpg')
    im.save(out, 'JPEG', quality=82, progressive=True, optimize=True)
    print('%-46s %5d KB' % (slug, os.path.getsize(out) // 1024))
    for p in hits:
        os.remove(p)

print('remaining PNGs:', len(glob.glob(os.path.join(SRC, '*.png'))))
