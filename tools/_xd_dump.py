# -*- coding: utf-8 -*-
"""Dump full text of named Xieduo tales.

Usage: python tools/_xd_dump.py 卜将军庙灵签 奎垣真像 ...
Mirrors _yj_dump.py for the Xieduo source at tools/_src/xieduo.md.
"""
import re
import sys

lines = open('tools/_src/xieduo.md', encoding='utf-8').read().split('\n')

TITLE = re.compile(r'^[\u4e00-\u9fff]{2,7}$')


def title_of(ln):
    s = ln.strip().strip('\u3000').strip()
    return s if (s and len(s) <= 8 and TITLE.match(s)) else None


head = next(i for i, ln in enumerate(lines) if '谐铎' in ln and '沈起凤' in ln)
j = head + 1
while j < len(lines):
    if not lines[j].strip():
        j += 1
        continue
    if title_of(lines[j]):
        j += 1
    else:
        break
body_start = j

bt = [(title_of(lines[i]), i) for i in range(body_start, len(lines)) if title_of(lines[i])]

want = sys.argv[1:]
for n, (ti, i) in enumerate(bt):
    if ti in want:
        start = i + 1
        end = bt[n + 1][1] if n + 1 < len(bt) else len(lines)
        seg = '\n'.join(lines[start:end])
        seg = re.sub(r'^\u3000+', '', seg, flags=re.M)
        seg = re.sub(r'\n{2,}', '\n', seg).strip()
        print('#' * 70)
        print(f'{ti}  ({len(seg)} chars)')
        print(seg)
        print()
