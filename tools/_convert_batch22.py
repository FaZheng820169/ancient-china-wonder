# -*- coding: utf-8 -*-
"""Convert batch-22 PNGs to 1400x933 progressive JPEGs. No watermark erase."""
import glob
import os
from PIL import Image

SRC = 'public/images/stories'
MAP = {
    'GuangxiGhostMasterScene': 'the-ghost-masters-of-guangxi',
    'DivineScaleScene': 'the-scale-of-merit',
    'YanHuiJudgeScene': 'yan-hui-judges-for-his-master',
    'TextualCriticismScene': 'the-gods-know-no-textual-criticism',
    'TurtlePavilionScene': 'the-pavilion-of-the-great-turtle',
    'WenchangTigerScene': 'the-tiger-who-carried-wenchangs-head',
    'ChickenFeetScene': 'the-chicken-footed-people',
    'WholeBonesScene': 'the-rite-of-the-whole-bones',
    'MistakenGhostScene': 'the-wronged-ghosts-mistook-their-man',
    'ExamQuestionScene': 'the-planchette-showed-the-questions',
    'FoxElixirScene': 'the-foxs-elixir',
    'ThunderPickpocketScene': 'thunder-strikes-the-pickpockets',
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
    print('%-46s %5d KB' % (slug, os.path.getsize(out) // 1024))
    for p in hits:
        os.remove(p)

print('remaining PNGs:', len(glob.glob(os.path.join(SRC, '*.png'))))
