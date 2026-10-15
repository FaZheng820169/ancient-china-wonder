# -*- coding: utf-8 -*-
"""Control test: edge energy in the watermark band, erased vs never-erased images."""
import glob
import os
from PIL import Image, ImageFilter, ImageStat

ERASED = ['the-warrant-that-sank-the-boat', 'the-wife-who-died-every-afternoon',
          'the-log-in-the-bed', 'the-tomb-at-the-drill-ground',
          'the-bamboo-that-gathered-treasure', 'the-red-snake-in-the-road',
          'the-crab-with-the-dipper', 'a-lifetimes-salary',
          'the-wizard-who-could-somersault', 'the-ghost-seer',
          'the-tiger-at-the-fireside', 'the-woman-who-followed-him-home']


def band(im):
    w, h = im.size
    return im.crop((int(w * 0.70), int(h * 0.90), w, h))


def energy(p):
    im = Image.open(p).convert('RGB')
    return ImageStat.Stat(band(im).convert('L').filter(ImageFilter.FIND_EDGES)).mean[0]


def report(label, paths):
    vals = []
    for p in paths:
        try:
            vals.append((energy(p), os.path.basename(p)))
        except Exception as e:
            print('skip', p, e)
    vals.sort()
    n = len(vals)
    mean = sum(v for v, _ in vals) / n
    print('%-12s n=%2d  mean=%6.2f  median=%6.2f  min=%6.2f  max=%6.2f'
          % (label, n, mean, vals[n // 2][0], vals[0][0], vals[-1][0]))
    return vals


er = report('ERASED', ['public/images/stories/%s.jpg' % s for s in ERASED])
never = sorted(glob.glob('public/images/stories/*.jpg'))
never = [p for p in never if os.path.basename(p)[:-4] not in ERASED]
# sample 24 never-erased images spread across the alphabet
sample = never[:: max(1, len(never) // 24)][:24]
report('NEVER', sample)
print()
print('lowest erased :', ', '.join('%s %.1f' % (n, v) for v, n in er[:4]))
print('highest erased:', ', '.join('%s %.1f' % (n, v) for v, n in er[-4:]))
