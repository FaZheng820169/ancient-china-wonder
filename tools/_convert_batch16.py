# -*- coding: utf-8 -*-
"""Convert batch-16 PNGs to 1400x933 progressive JPEGs and stash pre-erase copies."""
import glob
import os
import shutil
from PIL import Image

SRC = 'public/images/stories'
BAK = 'tools/_src/wm_before'
MAP = {
    'YangtaiTigerWomanScene': 'the-woman-with-the-cat',
    'ShaggyHeadScene': 'shaggy-head',
    'OneLegGhostScene': 'the-one-legged-ghost',
    'TaoistSupperScene': 'the-taoist-who-came-to-supper',
    'HundredPiesScene': 'the-hundred-meat-pies',
    'OnePearScene': 'one-pear-a-day',
    'ThreeWarriorsScene': 'the-three-warriors',
    'LayBrotherPigScene': 'the-lay-brother-who-became-a-pig',
    'ClerkDiedTwiceScene': 'the-clerk-who-died-twice',
    'ZhangTenThousandScene': 'the-daughter-of-zhang-ten-thousand',
    'WetNurseRelicsScene': 'the-wet-nurses-relics',
    'CandleFlowersScene': 'the-candle-flowers',
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
