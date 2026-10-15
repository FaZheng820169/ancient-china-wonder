# -*- coding: utf-8 -*-
"""Split Xieduo (谐铎) into individual tales.

Structure: YAML frontmatter -> "谐铎　清　沈起凤" -> TOC block (contiguous run of
title lines) -> body.  We skip the TOC, then for each title take its FIRST
standalone occurrence in the body and slice to the next title line."""
import re

t = open('tools/_src/xieduo.md', encoding='utf-8').read()
lines = t.split('\n')

WANT = ['狐媚', '香粉地狱', '穷士扶乩', '森罗殿点鬼', '能诗贼', '识字犬',
        '无气官', '鬼妇持家', '十姨庙', '蘸妇冰心', '蟪蛄郡', '蜣螂城']

TITLE = re.compile(r'^[\u4e00-\u9fff]{2,7}$')


def title_of(ln):
    s = ln.strip().strip('　').strip()
    return s if (s and len(s) <= 8 and TITLE.match(s)) else None


# 1. locate the start of the TOC block
head = None
for i, ln in enumerate(lines):
    if '谐铎' in ln and '沈起凤' in ln:
        head = i
        break
print('header line:', head, repr(lines[head]) if head is not None else None)

# 2. TOC = contiguous run of title lines after the header (blank lines allowed)
j = head + 1
toc = []
while j < len(lines):
    if not lines[j].strip():
        j += 1
        continue
    ti = title_of(lines[j])
    if ti:
        toc.append(ti)
        j += 1
    else:
        break
body_start = j
print('TOC entries:', len(toc), ' body starts at line', body_start)

# 3. first occurrence of each WANT title inside the body
first = {}
for i in range(body_start, len(lines)):
    ti = title_of(lines[i])
    if ti and ti in WANT and ti not in first:
        first[ti] = i

# 4. all title lines in the body, in order, to find slice ends
body_titles = []
for i in range(body_start, len(lines)):
    ti = title_of(lines[i])
    if ti:
        body_titles.append((ti, i))
order = {ti: n for n, (ti, i) in enumerate(body_titles)}

for w in WANT:
    if w not in first:
        print('!! missing', w)
        continue
    n = order[w]
    start = body_titles[n][1] + 1
    end = body_titles[n + 1][1] if n + 1 < len(body_titles) else len(lines)
    seg = '\n'.join(lines[start:end])
    seg = re.sub(r'^　+', '', seg, flags=re.M)
    seg = re.sub(r'\n{2,}', '\n', seg).strip()
    open('tools/_src/tale_%s.txt' % w, 'w', encoding='utf-8').write(seg)
    print('%-8s %5d chars  %s' % (w, len(seg), seg[:30].replace('\n', ' ')))
