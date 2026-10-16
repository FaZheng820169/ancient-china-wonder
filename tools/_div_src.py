# -*- coding: utf-8 -*-
"""Dump the original Chinese block of the divination-related stories."""
import os

SLUGS = [
    'the-turtle-who-taught-a-fortune-teller',
    'the-son-who-cost-a-fortune',
    'the-geomancers-bones',
    'ding-hun-dian',
    'goddess-zigu',
    'poor-scholar-planchette',
    'the-falling-star-in-the-southern-dipper',
    'kao-chenghuang',
    'the-bride-who-cast-her-coat',
    'the-voice-in-the-bamboo-tube',
]

for s in SLUGS:
    p = os.path.join('src/content/stories', s + '.md')
    txt = open(p, encoding='utf-8').read()
    fm = txt.split('---')[1]
    print('=' * 20, s)
    grab = False
    for ln in fm.split('\n'):
        if ln.startswith('original: |'):
            grab = True
            continue
        if grab:
            if ln and not ln.startswith(' ') and not ln.startswith('\t'):
                break
            print(ln[2:] if ln.startswith('  ') else ln)
    print()
