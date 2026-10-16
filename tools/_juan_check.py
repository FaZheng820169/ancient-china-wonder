# -*- coding: utf-8 -*-
"""Cross-check juan numbers of already-published Xieduo tales against the dump."""
import re

lines = open('tools/_src/xieduo.md', encoding='utf-8').read().split('\n')
NUM = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
       '七': 7, '八': 8, '九': 9, '十': 10, '十一': 11, '十二': 12}

marks = []
for i, ln in enumerate(lines, 1):
    if i <= 156:
        continue
    m = re.search(r'卷([一二三四五六七八九十]+)\s*$', ln)
    if m and len(ln.strip()) < 24:
        marks.append((i, NUM[m.group(1)]))

CASES = {
    '狐媚': 1, '一錢落職': 3, '孟婆莊': 8, '香粉地獄': 6,
    '森羅殿點鬼': 6, '窮士扶乩': 3, '蘸婦冰心': 10, '蟪蛄郡': 11,
    '身外身': 6, '換形乞丐': 7, '桃夭村': 4, '呂仙寶': 12,
}

for title, published in CASES.items():
    hit = None
    for i, ln in enumerate(lines, 1):
        if i > 156 and ln.strip() == title:
            hit = i
            break
    found = None
    if hit:
        for ln_no, n in marks:
            if ln_no < hit:
                found = n
    flag = 'OK ' if found == published else 'DIFF'
    print('%-14s line=%-6s dump=%-4s published=%-4s %s'
          % (title, hit, found, published, flag))
