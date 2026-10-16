# -*- coding: utf-8 -*-
"""Convert batch-19 PNGs straight to 1400x933 progressive JPEGs.
No watermark erase (user decision 2026-10-16)."""
import glob
import os
from PIL import Image

SRC = 'public/images/stories'
MAP = {
    'CorpseSilverScene': 'the-corpse-who-rose-for-silver',
    'EarthGodScene': 'the-earth-god-who-told',
    'PoisonTempleScene': 'the-temple-that-ran-on-poison',
    'ColdGhostsScene': 'where-ghosts-do-not-call',
    'FalseFatherScene': 'the-spirit-who-played-the-father',
    'CoffinCartScene': 'the-coffin-he-rode-home',
    'TaisuiScene': 'four-meetings-with-the-year-god',
    'BambooTubeScene': 'the-voice-in-the-bamboo-tube',
    'SouthernDipperScene': 'the-falling-star-in-the-southern-dipper',
    'FormerWifeScene': 'the-man-who-remembered-his-first-wife',
    'SoapberryScene': 'under-the-soapberry-trees',
    'SealedGhostScene': 'the-ghost-sealed-in-the-prison',
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
    print('%-40s %5d KB' % (slug, os.path.getsize(out) // 1024))
    for p in hits:
        os.remove(p)

print('remaining PNGs:', len(glob.glob(os.path.join(SRC, '*.png'))))
