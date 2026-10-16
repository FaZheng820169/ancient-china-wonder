# -*- coding: utf-8 -*-
"""Extract batch-20 Xieduo tales from cached xieduo.md (same title logic as batch 12)."""
import re, os

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

WANT = ['吕仙宝', '泥傀儡', '石赑屃', '术士驱蝇', '眼前杀报', '大士慈航',
        '屏角相郎', '祭蠹文', '兽谱', '和尚婆心', '泄气生员', '营卒守义']

out = 'tools/_src/batch20'
os.makedirs(out, exist_ok=True)
for w in WANT:
    if w not in order:
        print('!! MISSING', w)
        continue
    n = order[w]
    start = body_titles[n][1] + 1
    end = body_titles[n + 1][1] if n + 1 < len(body_titles) else len(lines)
    seg = '\n'.join(lines[start:end])
    seg = re.sub(r'^\u3000+', '', seg, flags=re.M)
    seg = re.sub(r'\n{2,}', '\n', seg).strip()
    open('%s/tale_%s.txt' % (out, w), 'w', encoding='utf-8').write(seg)
    print('%s' % w)
