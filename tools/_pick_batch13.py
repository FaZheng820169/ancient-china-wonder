# -*- coding: utf-8 -*-
"""Extract batch-13 candidate Xieduo tales (unused; variant duplicates excluded)."""
import re, os

t = open('tools/_src/xieduo.md', encoding='utf-8').read()
lines = t.split('\n')

# Variant duplicates of already-published tales are deliberately excluded
# (e.g. 十姨庙=十姨廟, 孟婆庄=孟婆莊, 鬼妇持家=鬼婦持家, 镜里人心=鏡裏人心 ...)
WANT = ['奇婚', '雉媒', '梦里家园', '顶上圆光', '草鞋四相公', '地师身后劫',
        '菜花三娘子', '况太守祠赝梦', '遮眼神', '讼师说讼', '鬼嫖', '神赌',
        '壮夫缚虎', '财戒']

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

out = 'tools/_src/batch13'
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
    print('%-10s %5d chars' % (w, len(seg)))
