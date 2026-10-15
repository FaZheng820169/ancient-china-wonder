# -*- coding: utf-8 -*-
"""Re-compress the batch-14 images after cloud watermark erase (cloud returns
uncompressed output, sometimes >1 MB)."""
import os
from PIL import Image

SLUGS = ['insect-writing', 'the-farewell-feast', 'the-mirror-that-showed-his-gall',
         'the-son-who-cost-a-fortune', 'the-wine-that-was-not-wine',
         'the-osmanthus-with-no-scent', 'the-turtle-who-taught-a-fortune-teller',
         'the-ants-patent-of-nobility', 'the-otters-offering', 'thorn-country',
         'the-tomb-called-gratitude', 'the-bride-who-cast-her-coat']

for s in SLUGS:
    p = 'public/images/stories/%s.jpg' % s
    if not os.path.exists(p):
        print('MISSING', s); continue
    before = os.path.getsize(p) // 1024
    im = Image.open(p)
    im = im.convert('RGB')
    if im.size != (1400, 933):
        im = im.resize((1400, 933), Image.LANCZOS)
    im.save(p, 'JPEG', quality=82, progressive=True, optimize=True)
    print('%-38s %6d KB -> %4d KB' % (s, before, os.path.getsize(p) // 1024))
