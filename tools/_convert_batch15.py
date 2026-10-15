# -*- coding: utf-8 -*-
"""Convert batch-15 PNGs (identified by prompt prefix) to 1400x933 progressive JPEGs,
and stash a pre-erase copy in tools/_src/wm_before/ so the erase can be diffed."""
import glob
import os
import shutil
from PIL import Image

SRC = 'public/images/stories'
BAK = 'tools/_src/wm_before'
MAP = {
    'BoatWarrantScene': 'the-warrant-that-sank-the-boat',
    'DailyExecutionScene': 'the-wife-who-died-every-afternoon',
    'BedLogScene': 'the-log-in-the-bed',
    'DrillGroundTombScene': 'the-tomb-at-the-drill-ground',
    'TreasureBambooScene': 'the-bamboo-that-gathered-treasure',
    'RedSnakeScene': 'the-red-snake-in-the-road',
    'DragonCrabScene': 'the-crab-with-the-dipper',
    'LifetimeSalaryScene': 'a-lifetimes-salary',
    'SomersaultWizardScene': 'the-wizard-who-could-somersault',
    'GhostSeerScene': 'the-ghost-seer',
    'FiresideTigerScene': 'the-tiger-at-the-fireside',
    'WomanOnTheRoadScene': 'the-woman-who-followed-him-home',
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
    print('%-36s %5d KB' % (slug, os.path.getsize(out) // 1024))
    for p in hits:
        os.remove(p)

print('remaining PNGs:', len(glob.glob(os.path.join(SRC, '*.png'))))
