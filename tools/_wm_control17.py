# -*- coding: utf-8 -*-
"""Control test for batch 17: edge energy in the watermark band, before vs after erase."""
import os
from PIL import Image, ImageFilter, ImageStat

BAK = 'tools/_src/wm_before'
SRC = 'public/images/stories'
SLUGS = ['the-woman-of-the-black-pine-valley', 'the-fifth-young-lord', 'the-house-in-the-cypress-wood', 'paper-and-brush-in-the-coffin', 'the-father-in-law-with-the-iron-ruler', 'the-wine-pressed-from-bone-marrow', 'seventy-days-of-thunder', 'the-nine-young-dragons', 'the-wildcat-wife', 'the-widow-who-came-to-file-suit', 'stabbing-the-spring', 'twelve-years-and-little-red']


def band(im):
    w, h = im.size
    return im.crop((int(w * 0.70), int(h * 0.90), w, h))


def energy(p):
    im = Image.open(p).convert('RGB')
    return ImageStat.Stat(band(im).convert('L').filter(ImageFilter.FIND_EDGES)).mean[0]


tot_b = tot_a = 0.0
print('%-38s %7s %7s' % ('slug', 'before', 'after'))
for s in SLUGS:
    b = os.path.join(BAK, s + '.jpg')
    a = os.path.join(SRC, s + '.jpg')
    eb = energy(b) if os.path.exists(b) else float('nan')
    ea = energy(a) if os.path.exists(a) else float('nan')
    tot_b += eb
    tot_a += ea
    print('%-38s %7.2f %7.2f' % (s, eb, ea))
print('%-38s %7.2f %7.2f' % ('MEAN', tot_b / len(SLUGS), tot_a / len(SLUGS)))
