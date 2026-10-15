# -*- coding: utf-8 -*-
"""Convert batch-14 PNGs (identified by prompt prefix) to 1400x933 progressive JPEGs."""
import glob, os
from PIL import Image

SRC = 'public/images/stories'
MAP = {
    'InsectWritingScene': 'insect-writing',
    'FarewellFeastScene': 'the-farewell-feast',
    'GallMirrorScene': 'the-mirror-that-showed-his-gall',
    'FortunateSonScene': 'the-son-who-cost-a-fortune',
    'NotWineScene': 'the-wine-that-was-not-wine',
    'ScentlessOsmanthusScene': 'the-osmanthus-with-no-scent',
    'TurtleTeacherScene': 'the-turtle-who-taught-a-fortune-teller',
    'AntPatentScene': 'the-ants-patent-of-nobility',
    'OtterOfferingScene': 'the-otters-offering',
    'ThornCountryScene': 'thorn-country',
    'GratitudeTombScene': 'the-tomb-called-gratitude',
    'CastCoatScene': 'the-bride-who-cast-her-coat',
}

for prefix, slug in MAP.items():
    hits = glob.glob(os.path.join(SRC, prefix + '__*.png'))
    if not hits:
        print('!! MISSING PNG for', prefix); continue
    hits.sort()
    p = hits[-1]
    im = Image.open(p).convert('RGB')
    if im.size != (1536, 1024):
        im = im.resize((1400, 933), Image.LANCZOS)
    else:
        im = im.resize((1400, 933), Image.LANCZOS)
    out = os.path.join(SRC, slug + '.jpg')
    im.save(out, 'JPEG', quality=82, progressive=True, optimize=True)
    kb = os.path.getsize(out) // 1024
    print('%-34s %5d KB' % (slug, kb))
    os.remove(p)

left = glob.glob(os.path.join(SRC, '*.png'))
print('remaining PNGs:', len(left))
