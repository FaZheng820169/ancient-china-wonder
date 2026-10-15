# -*- coding: utf-8 -*-
"""Extract batch-12 Xieduo tales (12 unused) from cached xieduo.md."""
import re, os

t = open('tools/_src/xieduo.md', encoding='utf-8').read()
lines = t.split('\n')

WANT = ['虎痴', '隔牖谈诗', '妙画代良医', '上清官除妖', '奇女雪怨', '犬婢',
        '梦中梦', '死嫁', '贫儿学谄', '才士惩骄', '怕婆县令', '村姬毒舌']

TITLE = re.compile(r'^[\u4e00-\u9fff]{2,7}$')
def title_of(ln):
    s = ln.strip().strip('　').strip()
    return s if (s and len(s) <= 8 and TITLE.match(s)) else None

head = next(i for i, ln in enumerate(lines) if '谐铎' in ln and '沈起凤' in ln)
j = head + 1
while j < len(lines):
    if not lines[j].strip():
        j += 1; continue
    if title_of(lines[j]):
        j += 1
    else:
        break
body_start = j

body_titles = [(title_of(lines[i]), i) for i in range(body_start, len(lines)) if title_of(lines[i])]
order = {ti: n for n, (ti, i) in enumerate(body_titles)}

out = 'tools/_src/batch12'
os.makedirs(out, exist_ok=True)
for w in WANT:
    if w not in order:
        print('!! MISSING', w); continue
    n = order[w]
    start = body_titles[n][1] + 1
    end = body_titles[n + 1][1] if n + 1 < len(body_titles) else len(lines)
    seg = '\n'.join(lines[start:end])
    seg = re.sub(r'^　+', '', seg, flags=re.M)
    seg = re.sub(r'\n{2,}', '\n', seg).strip()
    open('%s/tale_%s.txt' % (out, w), 'w', encoding='utf-8').write(seg)
    print('%-8s %5d chars | %s' % (w, len(seg), seg[:40].replace('\n', ' ')))
