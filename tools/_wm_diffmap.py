# -*- coding: utf-8 -*-
"""Where did the erase actually change the image? 8x6 grid of mean abs diff."""
import os
from PIL import Image, ImageChops, ImageStat

SRC = 'public/images/stories'
BAK = 'tools/_src/wm_before'

import sys
SLUGS = sys.argv[1:] or ['the-warrant-that-sank-the-boat', 'the-tiger-at-the-fireside',
         'the-ghost-seer', 'the-wife-who-died-every-afternoon',
         'the-log-in-the-bed', 'the-red-snake-in-the-road']

for slug in SLUGS:
    a = Image.open(os.path.join(SRC, slug + '.jpg')).convert('RGB')
    b = Image.open(os.path.join(BAK, slug + '.jpg')).convert('RGB')
    a = a.resize(b.size)
    d = ImageChops.difference(a, b).convert('L')
    w, h = d.size
    print('==', slug)
    for r in range(6):
        row = []
        for c in range(8):
            box = (c * w // 8, r * h // 6, (c + 1) * w // 8, (r + 1) * h // 6)
            row.append('%5.1f' % ImageStat.Stat(d.crop(box)).mean[0])
        print('   ', ' '.join(row))
