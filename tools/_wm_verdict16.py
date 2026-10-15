# -*- coding: utf-8 -*-
"""Is the erase confined to the watermark cell, or did it repaint the picture?
Metric: mean abs diff in bottom-right cell (expected) vs the worst other cell."""
import os
from PIL import Image, ImageChops, ImageStat

SRC = 'public/images/stories'
BAK = 'tools/_src/wm_before'
SLUGS = ['the-woman-with-the-cat', 'shaggy-head', 'the-one-legged-ghost', 'the-taoist-who-came-to-supper', 'the-hundred-meat-pies', 'one-pear-a-day', 'the-three-warriors', 'the-lay-brother-who-became-a-pig', 'the-clerk-who-died-twice', 'the-daughter-of-zhang-ten-thousand', 'the-wet-nurses-relics', 'the-candle-flowers']

print('%-38s %7s %7s  %s' % ('slug', 'wmcell', 'worst', 'verdict'))
bad = []
for slug in SLUGS:
    a = Image.open(os.path.join(SRC, slug + '.jpg')).convert('RGB')
    b = Image.open(os.path.join(BAK, slug + '.jpg')).convert('RGB')
    a = a.resize(b.size)
    d = ImageChops.difference(a, b).convert('L')
    w, h = d.size
    cells = {}
    for r in range(6):
        for c in range(8):
            box = (c * w // 8, r * h // 6, (c + 1) * w // 8, (r + 1) * h // 6)
            cells[(r, c)] = ImageStat.Stat(d.crop(box)).mean[0]
    wm = max(cells[(5, 7)], cells[(5, 6)], cells[(4, 7)])
    others = [v for k, v in cells.items() if k not in ((5, 7), (5, 6), (4, 7))]
    worst = max(others)
    ok = wm > worst * 1.5
    if not ok:
        bad.append(slug)
    print('%-38s %7.1f %7.1f  %s' % (slug, wm, worst, 'OK' if ok else 'REPAINTED'))
print()
print('repainted (%d): %s' % (len(bad), ', '.join(bad) if bad else 'none'))
