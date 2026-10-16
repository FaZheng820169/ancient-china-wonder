# -*- coding: utf-8 -*-
"""List Zibuyu tale titles from cached volumes, flagging any already published."""
import glob
import io
import os
import re

PUB = {}
for f in glob.glob('src/content/stories/*.md'):
    t = io.open(f, encoding='utf-8').read()
    slug = os.path.basename(f)[:-3]
    m = re.search(r'^titleZh:\s*(.+?)\s*$', t, re.M)
    if m:
        PUB[m.group(1).strip('"')] = slug

for p in sorted(glob.glob('tools/_src/zby/*.md')):
    vol = os.path.basename(p)[:-3]
    txt = io.open(p, encoding='utf-8').read()
    parts = re.split(r'^# ', txt, flags=re.M)[1:]
    print('=' * 62)
    print('volume %s  %d tales' % (vol, len(parts)))
    for seg in parts:
        lines = seg.split('\n')
        title = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()
        if len(body) < 80:
            continue
        mark = 'USED' if title in PUB else '    '
        print('  %-16s %-5s %5d' % (title, mark, len(body)))
