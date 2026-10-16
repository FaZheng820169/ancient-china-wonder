# -*- coding: utf-8 -*-
"""Convert batch-24 PNGs to 1400x933 progressive JPEGs. No watermark erase."""
import glob
import os
from PIL import Image

SRC = 'public/images/stories'
MAP = {
    'GuiBuySonScene': 'the-ghost-who-bought-a-son',
    'LakeGuardScene': 'the-lake-god-who-guarded-a-corpse',
    'ThunderSwordScene': 'the-thunder-god-and-his-fire-sword',
    'DumplingGhostScene': 'the-ghost-who-brought-dumplings',
    'ChasteGirlScene': 'the-chaste-girl-who-cried-injustice',
    'NotVirtuousGodScene': 'not-every-god-was-virtuous',
    'FilingGhostScene': 'the-girl-ghost-who-filed-suits',
    'WaxieStonesScene': 'the-headless-stone-men-of-waxie',
    'WoodenDogScene': 'the-wooden-dog-that-barked',
    'BronzeActorsScene': 'the-bronze-actors-of-romance-of-the-west-chamber',
    'JealousGhostsScene': 'two-tales-of-jealous-ghosts',
    'TianfeiScene': 'the-goddess-of-the-favorable-winds',
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
    print('%-52s %5d KB' % (slug, os.path.getsize(out) // 1024))
    for p in hits:
        os.remove(p)

print('remaining PNGs:', len(glob.glob(os.path.join(SRC, '*.png'))))
