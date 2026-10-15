# -*- coding: utf-8 -*-
"""Re-compress batch-17 images after cloud erase returns them uncompressed."""
import os
from PIL import Image

SRC = 'public/images/stories'
SLUGS = ['the-woman-of-the-black-pine-valley', 'the-fifth-young-lord', 'the-house-in-the-cypress-wood', 'paper-and-brush-in-the-coffin', 'the-father-in-law-with-the-iron-ruler', 'the-wine-pressed-from-bone-marrow', 'seventy-days-of-thunder', 'the-nine-young-dragons', 'the-wildcat-wife', 'the-widow-who-came-to-file-suit', 'stabbing-the-spring', 'twelve-years-and-little-red']

for slug in SLUGS:
    p = os.path.join(SRC, slug + '.jpg')
    if not os.path.exists(p):
        print('MISSING', slug); continue
    before = os.path.getsize(p) // 1024
    im = Image.open(p).convert('RGB')
    if im.size != (1400, 933):
        im = im.resize((1400, 933), Image.LANCZOS)
    im.save(p, 'JPEG', quality=82, progressive=True, optimize=True)
    print('%-38s %5d -> %4d KB' % (slug, before, os.path.getsize(p) // 1024))
