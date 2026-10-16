# -*- coding: utf-8 -*-
"""Peek at candidate Xieduo tales: size + opening, using the same line-title logic
as _pick_batch12.py."""
import re, sys

t = open('tools/_src/xieduo.md', encoding='utf-8').read()
lines = t.split('\n')

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

body_titles = [(title_of(lines[i]), i) for i in range(body_start, len(lines)) if title_of(lines[i])]
order = {ti: n for n, (ti, i) in enumerate(body_titles)}
seg = {}
for n, (ti, i) in enumerate(body_titles):
    start = i + 1
    end = body_titles[n + 1][1] if n + 1 < len(body_titles) else len(lines)
    body = '\n'.join(lines[start:end])
    body = re.sub(r'^\u3000+', '', body, flags=re.M)
    body = re.sub(r'\s+', '', body)
    seg[ti] = body

WANT = sys.argv[1:] or ['虎痴', '屏角相郎', '吕仙宝', '卜将军庙灵签', '泥傀儡', '祥鸦',
                        '石赑屃', '术士驱蝇', '眼前杀报', '大士慈航']
for w in WANT:
    b = seg.get(w)
    if b is None:
        print('!! not found:', w)
        continue
    print('=' * 74)
    print('%s  (%d chars)' % (w, len(b)))
    print(b[:600])
    print()

print('TOTAL titles found:', len(body_titles))
