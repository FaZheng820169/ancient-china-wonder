# -*- coding: utf-8 -*-
"""Control: how much diff comes purely from a second q82 JPEG save (no erase)?"""
import os, sys
from PIL import Image, ImageChops, ImageStat

BAK = 'tools/_src/wm_before'
SLUGS = sys.argv[1:]


def grid(d):
    w, h = d.size
    out = []
    for r in range(6):
        row = []
        for c in range(8):
            box = (c * w // 8, r * h // 6, (c + 1) * w // 8, (r + 1) * h // 6)
            row.append('%5.1f' % ImageStat.Stat(d.crop(box)).mean[0])
        out.append('    ' + ' '.join(row))
    return '\n'.join(out)


for slug in SLUGS:
    a = Image.open(os.path.join(BAK, slug + '.jpg')).convert('RGB')
    tmp = '/tmp/_rt.jpg'
    a.save(tmp, 'JPEG', quality=82, progressive=True, optimize=True)
    a2 = Image.open(tmp).convert('RGB')
    d = ImageChops.difference(a, a2).convert('L')
    print('== %s  (pure re-save at q82)' % slug)
    print(grid(d))
