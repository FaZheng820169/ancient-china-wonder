# -*- coding: utf-8 -*-
"""Convert batch-18 PNGs straight to 1400x933 progressive JPEGs.
No watermark erase any more (user decision 2026-10-16), so no backup/verdict step."""
import glob
import os
from PIL import Image

SRC = 'public/images/stories'
MAP = {
    'WoodCollarScene': 'the-collar-of-wood-and-iron',
    'FalseJudgeBaoScene': 'the-true-judge-bao-and-the-false',
    'SummonedWitnessScene': 'summoned-as-a-witness',
    'NightJudgeScene': 'the-judge-answers-questions',
    'BeforePanguScene': 'the-man-from-before-pangu',
    'FootbindingCaseScene': 'the-footbinding-case',
    'IntercessionScene': 'intercession-in-the-underworld',
    'NamelessGodScene': 'the-god-nobody-could-name',
    'UnrankedRegisterScene': 'the-register-of-the-unranked',
    'GhostSuesActorScene': 'the-ghost-who-sued-an-actor',
    'EyeOnBackScene': 'the-eye-on-its-back',
    'StonesSpokeScene': 'when-the-stones-spoke',
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
    print('%-38s %5d KB' % (slug, os.path.getsize(out) // 1024))
    for p in hits:
        os.remove(p)

print('remaining PNGs:', len(glob.glob(os.path.join(SRC, '*.png'))))
