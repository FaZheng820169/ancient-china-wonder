# -*- coding: utf-8 -*-
"""Convert batch-26 PNGs to 1400x933 progressive JPEGs. No watermark erase."""
import glob
import os
from PIL import Image

SRC = 'public/images/stories'
MAP = {
    'OxBorneNameScene': 'the-ox-that-bore-his-name',
    'AconitePhysicianScene': 'the-physician-who-burned-with-aconite',
    'GhostPunchGeneralScene': 'the-general-who-punched-a-ghost',
    'NeighborShrineGirlScene': 'the-girl-claimed-by-the-neighbor-shrine',
    'CourtOfDeathScholarScene': 'the-scholar-who-returned-from-the-court-of-death',
    'TradedSicknessBrotherScene': 'the-brother-who-traded-a-sickness',
    'RiverDragonFourGeneralsScene': 'the-four-generals-and-the-river-dragon',
    'DingtaoWaterPeopleScene': 'the-water-people-of-dingtao',
    'LakeDragonWifeScene': 'the-wife-taken-by-the-lake-dragon',
    'FloodFromWellScene': 'the-flood-that-rose-from-the-well',
    'SeasideShrineSorcererScene': 'the-sorcerer-and-the-seaside-shrine',
    'OtherSideWifeScene': 'the-wife-summoned-from-the-other-side',
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
