# -*- coding: utf-8 -*-
"""Convert batch-21 PNGs to 1400x933 progressive JPEGs. No watermark erase."""
import glob
import os
from PIL import Image

SRC = 'public/images/stories'
MAP = {
    'JudgeSwordsmanScene': 'the-swordsman-who-came-for-the-judge',
    'GhostPagodaScene': 'the-pagoda-of-ghosts',
    'CoffinLidScene': 'the-coffin-lid-that-flew',
    'OilJarGhostScene': 'boiling-the-ghost-in-oil',
    'DoorlessCountryScene': 'the-country-without-doors',
    'ThreeLivesGhostScene': 'the-ghost-who-followed-him-through-three-lives',
    'CraneStillnessScene': 'master-crane-stillness',
    'CorpseFragranceScene': 'two-tales-of-corpse-fragrance',
    'WaterGodScene': 'lord-qiu-becomes-a-water-god',
    'HeadCarryingScene': 'the-major-who-carried-his-head',
    'FoldingImmortalScene': 'the-folding-immortal',
    'IronPillScene': 'the-iron-pill-of-the-king-of-hell',
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
