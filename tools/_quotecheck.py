# -*- coding: utf-8 -*-
"""Flag frontmatter lines whose double quotes do not balance."""
import glob
import sys

bad = 0
for p in sorted(glob.glob('src/content/stories/*.md')) + sorted(glob.glob('src/content/worldview/*.md')):
    txt = open(p, encoding='utf-8').read()
    parts = txt.split('---')
    if len(parts) < 3:
        print('NO FRONTMATTER', p)
        bad += 1
        continue
    fm = parts[1]
    for i, ln in enumerate(fm.split('\n'), 2):
        if ln.count('"') % 2:
            print('%s:%d  %s' % (p, i, ln[:110]))
            bad += 1
print('unbalanced lines:', bad)
sys.exit(1 if bad else 0)
