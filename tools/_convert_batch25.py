# -*- coding: utf-8 -*-
"""Convert batch-25 PNGs to 1400x933 progressive JPEGs. No watermark erase."""
import glob
import os
from PIL import Image

SRC = 'public/images/stories'
MAP = {
    'EarthGodBargainScene': 'the-earth-god-who-bargained',
    'ThunderVictimsScene': 'the-thunder-that-chose-its-victims',
    'GhostBattleScene': 'the-ghostly-battle-on-the-sandbar',
    'WestLakeJudgeScene': 'the-judge-of-the-west-lake',
    'TimberStormScene': 'the-timber-the-storm-delivered',
    'PerfectedFulingScene': 'the-perfected-man-of-fuling',
    'MonkGhostScene': 'the-monk-ghost-of-yunmen',
    'GreenTurtleScene': 'the-green-furred-turtle',
    'QinChessScene': 'the-qin-stand-and-the-chess-table',
    'TorturerGhostScene': 'the-torturer-and-the-life-taking-ghost',
    'GodHorsesScene': 'the-god-who-borrowed-two-horses',
    'GhostHomeScene': 'the-ghost-who-came-home',
}

for prefix, slug in MAP.items():
    hits = sorted(glob.glob(os.path.join(SRC, prefix + '__*.png')))
    if not hits:
        print('!! MISSING PNG for', prefix)
        continue
    im = Image.open(hits[-1]).convert('RGB')
    im = im.resize((1400, 933), Image.LANCZOS)
    out = os.path.join(SRC, slug + '.jpg')
    im.save(out, 'JPEG', quality=82, progressive=True, optimize=True)
    print('%-52s %5d KB' % (slug, os.path.getsize(out) // 1024))
    for p in hits:
        os.remove(p)

print('remaining PNGs:', len(glob.glob(os.path.join(SRC, '*.png'))))
