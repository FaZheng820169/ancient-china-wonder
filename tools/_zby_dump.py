# -*- coding: utf-8 -*-
"""Dump the full text of named Zibuyu tales from the cached volumes."""
import glob
import io
import os
import re
import sys

WANT = sys.argv[1:]
for p in sorted(glob.glob('tools/_src/zby/*.md')):
    vol = os.path.basename(p)[:-3]
    txt = io.open(p, encoding='utf-8').read()
    for seg in re.split(r'^# ', txt, flags=re.M)[1:]:
        lines = seg.split('\n')
        title = lines[0].strip()
        if title not in WANT:
            continue
        body = '\n'.join(lines[1:]).strip()
        print('#' * 70)
        print('[%s] %s  (%d chars)' % (vol, title, len(body)))
        print(body)
        print()
