# -*- coding: utf-8 -*-
"""Revert images where the erase repainted the picture instead of just the watermark."""
import os
import shutil

BAK = 'tools/_src/wm_before'
SRC = 'public/images/stories'
SLUGS = ['the-house-in-the-cypress-wood', 'the-father-in-law-with-the-iron-ruler',
         'the-nine-young-dragons', 'the-wildcat-wife', 'stabbing-the-spring']

for slug in SLUGS:
    src = os.path.join(BAK, slug + '.jpg')
    dst = os.path.join(SRC, slug + '.jpg')
    if not os.path.exists(src):
        print('NO BACKUP', slug); continue
    shutil.copy2(src, dst)
    print('reverted %-38s %d KB' % (slug, os.path.getsize(dst) // 1024))
