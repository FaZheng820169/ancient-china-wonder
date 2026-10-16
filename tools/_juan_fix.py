# -*- coding: utf-8 -*-
"""Correct wrong 'Xieduo juan N' citations in story frontmatter.

The authoritative juan comes from the table of contents at the head of
tools/_src/xieduo.md, cross-checked against the per-juan markers in the body.
"""
import glob
import os
import re

FIX = {
    'a-day-is-a-year': 10,
    'the-city-of-dung-beetles': 10,
    'the-bone-of-arrogance': 12,
    'the-dog-maid': 7,
    'the-face-wheel': 6,
    'the-man-who-caught-the-flies': 8,
    'the-painting-that-cured-jealousy': 2,
    'the-ten-aunts-temple': 8,
    'the-tortoise-under-the-stele': 5,
    'the-literate-dog': 6,
    'heart-of-ice': 9,
    'poor-scholar-planchette': 3,
    'the-beggar-who-was-rebuilt': 5,
    'the-dead-wife-keeps-house': 7,
    'the-official-with-no-qi': 7,
    'the-thief-who-judged-verse': 6,
}

for slug, juan in sorted(FIX.items()):
    p = os.path.join('src/content/stories', slug + '.md')
    if not os.path.exists(p):
        print('!! missing', slug)
        continue
    txt = open(p, encoding='utf-8').read()
    new, n = re.subn(r'Xieduo juan [0-9]+', 'Xieduo juan %d' % juan, txt, count=1)
    if n == 0:
        print('!! no match', slug)
        continue
    if new != txt:
        open(p, 'w', encoding='utf-8').write(new)
        print('%-40s -> juan %d' % (slug, juan))
    else:
        print('%-40s already juan %d' % (slug, juan))
