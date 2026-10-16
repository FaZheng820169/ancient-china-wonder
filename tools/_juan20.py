# -*- coding: utf-8 -*-
"""Report which juan of Xieduo each batch-20 tale sits in."""
import glob
import os
import re

SRC = 'tools/_src/xieduo.md'
NUM = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7,
       '八': 8, '九': 9, '十': 10, '十一': 11, '十二': 12}

lines = open(SRC, encoding='utf-8').read().split('\n')
marks = []
for i, ln in enumerate(lines):
    m = re.match(r'\s*谐铎[。.]\s*卷([一二三四五六七八九十]+)\s*$', ln)
    if m:
        marks.append((i + 1, NUM[m.group(1)]))

files = sorted(glob.glob('tools/_src/batch20/tale_*.txt'))
for p in files:
    name = os.path.basename(p)[5:-4]
    body = open(p, encoding='utf-8').read().strip()
    head = body[:8]
    hit = None
    for i, ln in enumerate(lines):
        if head and head in ln:
            hit = i + 1
            break
    juan = None
    if hit:
        for ln_no, n in marks:
            if ln_no < hit:
                juan = n
    print('%-10s line=%-6s juan=%s' % (name, hit, juan))
