# -*- coding: utf-8 -*-
import re
lines = open('tools/_src/xieduo.md', encoding='utf-8').read().split('\n')
for i, ln in enumerate(lines, 1):
    if re.search(r'卷[一二三四五六七八九十]', ln) and len(ln.strip()) < 20:
        print(i, repr(ln.strip()))
