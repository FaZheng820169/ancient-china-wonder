# -*- coding: utf-8 -*-
"""Extract batch-14 candidate Xieduo tales (unused; variant duplicates excluded)."""
import re, os

t = open('tools/_src/xieduo.md', encoding='utf-8').read()
lines = t.split('\n')

WANT = ['老僧辨奸', '恶饯', '屏角相郎', '虫书', '捣鬼夫人', '荆棘里', '命中姻眷',
        '大士慈航', '獭祭', '臭桂', '蚁封', '龟鉴', '卜将军庙灵签', '道人神相',
        '镜戏', '酒戒', '烧录成名', '达士报恩']

TITLE = re.compile(r'^[\u4e00-\u9fff]{2,7}$')
def title_of(ln):
    s = ln.strip().strip('\u3000').strip()
    return s if (s and len(s) <= 8 and TITLE.match(s)) else None

head = next(i for i, ln in enumerate(lines) if '\u8c10\u94ce' in ln and '\u6c88\u8d77\u51e4' in ln)
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

out = 'tools/_src/batch14'
os.makedirs(out, exist_ok=True)
for w in WANT:
    if w not in order:
        print('!! MISSING', w); continue
    n = order[w]
    start = body_titles[n][1] + 1
    end = body_titles[n + 1][1] if n + 1 < len(body_titles) else len(lines)
    seg = '\n'.join(lines[start:end])
    seg = re.sub(r'^\u3000+', '', seg, flags=re.M)
    seg = re.sub(r'\n{2,}', '\n', seg).strip()
    open('%s/tale_%s.txt' % (out, w), 'w', encoding='utf-8').write(seg)
    print('%-12s %5d chars' % (w, len(seg)))
