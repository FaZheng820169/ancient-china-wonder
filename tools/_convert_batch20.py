# -*- coding: utf-8 -*-
"""Convert batch-20 PNGs to 1400x933 progressive JPEGs. No watermark erase."""
import glob
import os
from PIL import Image

SRC = 'public/images/stories'
MAP = {
    'LuBoneScene': 'the-bone-of-arrogance',
    'ClayPuppetScene': 'the-clay-puppet',
    'SteleTortoiseScene': 'the-tortoise-under-the-stele',
    'FlyCatcherScene': 'the-man-who-caught-the-flies',
    'SlaughterDreamScene': 'the-slaughter-she-dreamed-through',
    'FishBasketScene': 'the-boat-of-the-fish-basket',
    'FaceReaderScene': 'the-girl-who-read-faces',
    'BookwormsScene': 'a-funeral-oration-for-the-bookworms',
    'LeopardOxScene': 'the-ox-who-bought-a-leopards-spots',
    'BodySwapScene': 'the-monk-who-lent-him-a-body',
    'FlatulenceScholarScene': 'top-of-the-list-by-accident',
    'FaithfulSoldierScene': 'the-soldier-who-kept-his-word',
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
