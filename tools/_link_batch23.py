#!/usr/bin/env python3
"""Add batch-23 story slugs into worldview `related` lists (the 'hanging links').

Worldview.related is dual-use: it may hold worldview ids and story slugs, and a
story slug placed here renders as an inbound link on both pages and is counted
by audit_links.py. This is how new stories get attached to the encyclopedia.
"""
import re
import sys
from pathlib import Path

WV = Path('src/content/worldview')

ADD = {
    'the-ledger': [
        'lu-dongbin-tests-a-hermit',
        'axu-in-the-underworld',
    ],
    'small-gods': [
        'the-debt-the-temple-god-collected',
        'the-seven-ladies',
        'the-land-god-of-jianju-abbey',
        'the-goddess-who-bought-the-woods',
    ],
    'how-a-shrine-begins': [
        'the-land-god-of-jianju-abbey',
        'the-goddess-who-bought-the-woods',
    ],
    'divine-careers': [
        'the-land-god-of-jianju-abbey',
    ],
    'immortals-and-gods': [
        'the-thunder-god-answers-a-memo',
        'the-boys-who-chased-butterflies',
    ],
    'lu-dongbin': [
        'lu-dongbin-tests-a-hermit',
    ],
    'cultivation-system': [
        'lu-dongbin-tests-a-hermit',
    ],
    'the-underworld-exam': [
        'listening-for-the-omen',
    ],
    'reading-the-fate': [
        'listening-for-the-omen',
    ],
    'underworld': [
        'axu-in-the-underworld',
        'qiuding-in-the-underworld',
    ],
    'ghosts': [
        'qiuding-in-the-underworld',
    ],
    'kunlun': [
        'cai-zhengniang',
    ],
    'penglai': [
        'cai-zhengniang',
        'the-boys-who-chased-butterflies',
    ],
    'dragons': [
        'the-bronze-bell-of-fuzhou',
    ],
}

changed = 0
for stem, slugs in ADD.items():
    p = WV / (stem + '.md')
    txt = p.read_text(encoding='utf-8')
    if 'related:' not in txt:
        print('SKIP (no related block): %s' % stem)
        continue
    lines = txt.split('\n')
    start = lines.index('related:')
    # find the closing '---' of the frontmatter after `related:`
    end = None
    for i in range(start + 1, len(lines)):
        if lines[i].strip() == '---':
            end = i
            break
    if end is None:
        print('SKIP (unterminated frontmatter): %s' % stem)
        continue
    existing = set(re.findall(r'"([^"]+)"', '\n'.join(lines[start + 1:end])))
    fresh = [s for s in slugs if s not in existing]
    if not fresh:
        print('ok (already present): %s' % stem)
        continue
    insert = ['  - "%s"' % s for s in fresh]
    lines[end:end] = insert
    p.write_text('\n'.join(lines), encoding='utf-8')
    changed += 1
    print('added %d to %s: %s' % (len(fresh), stem, ', '.join(fresh)))

print('files changed:', changed)
sys.exit(0)
