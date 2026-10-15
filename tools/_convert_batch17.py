# -*- coding: utf-8 -*-
"""Convert batch-17 PNGs to 1400x933 progressive JPEGs and stash pre-erase copies."""
import glob
import os
import shutil
from PIL import Image

SRC = 'public/images/stories'
BAK = 'tools/_src/wm_before'
MAP = {
    'PineValleyWoman': 'the-woman-of-the-black-pine-valley',
    'FifthLordScene': 'the-fifth-young-lord',
    'CypressHouseScene': 'the-house-in-the-cypress-wood',
    'CoffinBrushScene': 'paper-and-brush-in-the-coffin',
    'IronRulerScene': 'the-father-in-law-with-the-iron-ruler',
    'MarrowWineScene': 'the-wine-pressed-from-bone-marrow',
    'SeventyDaysScene': 'seventy-days-of-thunder',
    'NineDragonsScene': 'the-nine-young-dragons',
    'WildcatWifeScene': 'the-wildcat-wife',
    'WidowSuitScene': 'the-widow-who-came-to-file-suit',
    'StabbingSpringScene': 'stabbing-the-spring',
    'LittleRedQinScene': 'twelve-years-and-little-red',
}

os.makedirs(BAK, exist_ok=True)

for prefix, slug in MAP.items():
    hits = sorted(glob.glob(os.path.join(SRC, prefix + '__*.png')))
    if not hits:
        print('!! MISSING PNG for', prefix)
        continue
    im = Image.open(hits[-1]).convert('RGB')
    im = im.resize((1400, 933), Image.LANCZOS)
    out = os.path.join(SRC, slug + '.jpg')
    im.save(out, 'JPEG', quality=82, progressive=True, optimize=True)
    shutil.copy2(out, os.path.join(BAK, slug + '.jpg'))
    print('%-38s %5d KB' % (slug, os.path.getsize(out) // 1024))
    for p in hits:
        os.remove(p)

print('remaining PNGs:', len(glob.glob(os.path.join(SRC, '*.png'))))
