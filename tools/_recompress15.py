# -*- coding: utf-8 -*-
"""Re-compress batch-15 images after cloud erase, and report the before/after
difference in the watermark corner so the erase can be verified without eyes."""
import os
from PIL import Image, ImageChops, ImageFilter, ImageStat

SRC = 'public/images/stories'
BAK = 'tools/_src/wm_before'

SLUGS = ['the-warrant-that-sank-the-boat', 'the-wife-who-died-every-afternoon',
         'the-log-in-the-bed', 'the-tomb-at-the-drill-ground',
         'the-bamboo-that-gathered-treasure', 'the-red-snake-in-the-road',
         'the-crab-with-the-dipper', 'a-lifetimes-salary',
         'the-wizard-who-could-somersault', 'the-ghost-seer',
         'the-tiger-at-the-fireside', 'the-woman-who-followed-him-home']


def corner(im):
    """bottom 14% x right 34% — where the platform watermark sits."""
    w, h = im.size
    return im.crop((int(w * 0.66), int(h * 0.86), w, h))


def edge_energy(im):
    return ImageStat.Stat(im.convert('L').filter(ImageFilter.FIND_EDGES)).mean[0]


print('%-36s %-9s %-9s %-9s %s' % ('slug', 'edge b4', 'edge aft', 'diff', 'size'))
for slug in SLUGS:
    after_p = os.path.join(SRC, slug + '.jpg')
    before_p = os.path.join(BAK, slug + '.jpg')
    before = Image.open(before_p).convert('RGB')
    after = Image.open(after_p).convert('RGB')
    eb = edge_energy(corner(before))
    ea = edge_energy(corner(after))
    d = ImageStat.Stat(ImageChops.difference(corner(before), corner(after))).mean[0]
    if after.size != (1400, 933):
        after = after.resize((1400, 933), Image.LANCZOS)
    after.save(after_p, 'JPEG', quality=82, progressive=True, optimize=True)
    print('%-36s %-9.2f %-9.2f %-9.2f %d KB' % (
        slug, eb, ea, d, os.path.getsize(after_p) // 1024))
