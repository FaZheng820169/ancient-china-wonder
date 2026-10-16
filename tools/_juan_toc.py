# -*- coding: utf-8 -*-
"""Resolve the juan of a Xieduo title from the table of contents block."""
import glob
import os
import re

lines = open('tools/_src/xieduo.md', encoding='utf-8').read().split('\n')
NUM = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7,
       '八': 8, '九': 9, '十': 10, '十一': 11, '十二': 12}

# TOC runs from line 24 up to the line starting the body (157).
marks = []
for i, ln in enumerate(lines, 1):
    m = re.match(r'\s*卷([一二三四五六七八九十]+)\s*$', ln)
    if m and 20 <= i <= 156:
        marks.append((i, NUM[m.group(1)]))

titles = {}
for p in sorted(glob.glob('tools/_src/batch20/tale_*.txt')):
    name = os.path.basename(p)[5:-4]
    body = open(p, encoding='utf-8').read().strip()[:8]
    for i, ln in enumerate(lines, 1):
        if 20 <= i <= 156 and body and body in ln:
            j = None
            for ln_no, n in marks:
                if ln_no < i:
                    j = n
            titles[name] = (i, j, ln.strip())

# Also report where each title appears in the body, per the body markers.
bodymarks = []
for i, ln in enumerate(lines, 1):
    m = re.search(r'卷([一二三四五六七八九十]+)\s*$', ln)
    if m and i > 156 and len(ln.strip()) < 24:
        bodymarks.append((i, NUM[m.group(1)]))

print('TOC resolution:')
for name in sorted(titles):
    print('  %-10s toc_line=%-5s juan=%s' % (name, titles[name][0], titles[name][1]))

print()
print('Body resolution:')
for p in sorted(glob.glob('tools/_src/batch20/tale_*.txt')):
    name = os.path.basename(p)[5:-4]
    head = open(p, encoding='utf-8').read().strip()[:8]
    hit = None
    for i, ln in enumerate(lines, 1):
        if i > 156 and head and head in ln:
            hit = i
            break
    j = None
    for ln_no, n in bodymarks:
        if hit and ln_no < hit:
            j = n
    print('  %-10s body_line=%-6s juan=%s' % (name, hit, j))
