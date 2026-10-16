# -*- coding: utf-8 -*-
"""Convert batch-23 PNGs to 1400x933 progressive JPEGs. No watermark erase."""
import glob
import os
from PIL import Image

SRC = 'public/images/stories'
MAP = {
    'ThunderMemoScene': 'the-thunder-god-answers-a-memo',
    'TempleDebtScene': 'the-debt-the-temple-god-collected',
    'SevenLadiesScene': 'the-seven-ladies',
    'LandGodScene': 'the-land-god-of-jianju-abbey',
    'DongbinTestScene': 'lu-dongbin-tests-a-hermit',
    'GoddessWoodsScene': 'the-goddess-who-bought-the-woods',
    'OmenBridgeScene': 'listening-for-the-omen',
    'ButterflyBoysScene': 'the-boys-who-chased-butterflies',
    'AxuCourtScene': 'axu-in-the-underworld',
    'CaiZhengScene': 'cai-zhengniang',
    'BronzeBellScene': 'the-bronze-bell-of-fuzhou',
    'QiuCourtScene': 'qiuding-in-the-underworld',
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
