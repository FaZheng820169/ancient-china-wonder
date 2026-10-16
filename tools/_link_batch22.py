#!/usr/bin/env python3
"""Add batch-22 story slugs into worldview `related` lists (the 'hanging links').

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
        'the-ghost-masters-of-guangxi',
        'the-wronged-ghosts-mistook-their-man',
    ],
    'the-ledger': [
        'the-scale-of-merit',
        'thunder-strikes-the-pickpockets',
    ],
    'the-underworld-exam': [
        'yan-hui-judges-for-his-master',
        'the-planchette-showed-the-questions',
    ],
    'reading-the-fate': [
        'the-planchette-showed-the-questions',
        'the-foxs-elixir',
    ],
    'fox-spirits': [
        'the-foxs-elixir',
    ],
    'cultivation-system': [
        'the-rite-of-the-whole-bones',
    ],
    'immortals-and-gods': [
        'the-gods-know-no-textual-criticism',
    ],
    'dragons': [
        'the-pavilion-of-the-great-turtle',
    ],
    'monsters-and-yaoguai': [
        'the-chicken-footed-people',
        'the-tiger-who-carried-wenchangs-head',
    ],
    'small-gods': [
        'the-tiger-who-carried-wenchangs-head',
    ],
    'how-souls-move-on': [
        'the-wronged-ghosts-mistook-their-man',
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
