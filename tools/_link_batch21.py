#!/usr/bin/env python3
"""Add batch-21 story slugs into worldview `related` lists (the 'hanging links').

Worldview.related is dual-use: it may hold worldview ids and story slugs, and a
story slug placed here renders as an inbound link on both pages and is counted
by audit_links.py. This is how new stories get attached to the encyclopedia.
"""
import re
import sys
from pathlib import Path

WV = Path('src/content/worldview')

ADD = {
    'ghosts': [
        'the-pagoda-of-ghosts',
        'boiling-the-ghost-in-oil',
        'the-coffin-lid-that-flew',
        'the-major-who-carried-his-head',
    ],
    'three-realms': [
        'the-country-without-doors',
    ],
    'how-souls-move-on': [
        'the-major-who-carried-his-head',
        'the-ghost-who-followed-him-through-three-lives',
    ],
    'the-ledger': [
        'two-tales-of-corpse-fragrance',
        'the-ghost-who-followed-him-through-three-lives',
    ],
    'divine-careers': [
        'lord-qiu-becomes-a-water-god',
    ],
    'how-a-shrine-begins': [
        'lord-qiu-becomes-a-water-god',
    ],
    'the-underworld-exam': [
        'the-iron-pill-of-the-king-of-hell',
    ],
    'fengdu': [
        'the-iron-pill-of-the-king-of-hell',
    ],
    'cultivation-system': [
        'the-folding-immortal',
    ],
    'immortals-and-gods': [
        'the-folding-immortal',
    ],
    'lu-dongbin': [
        'the-swordsman-who-came-for-the-judge',
    ],
    'the-corpse-that-does-not-become-a-ghost': [
        'two-tales-of-corpse-fragrance',
    ],
    'reading-the-fate': [
        'master-crane-stillness',
    ],
    'marriage-across-the-border': [
        'the-ghost-who-followed-him-through-three-lives',
    ],
    'small-gods': [
        'lord-qiu-becomes-a-water-god',
    ],
    'the-canon-of-sacrifices': [
        'lord-qiu-becomes-a-water-god',
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
