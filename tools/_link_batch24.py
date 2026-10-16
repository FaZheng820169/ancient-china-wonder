#!/usr/bin/env python3
"""Add batch-24 story slugs into worldview `related` lists (the 'hanging links')."""
import re
import sys
from pathlib import Path

WV = Path('src/content/worldview')

ADD = {
    'the-ledger': [
        'the-ghost-who-bought-a-son',
    ],
    'small-gods': [
        'the-lake-god-who-guarded-a-corpse',
        'the-goddess-of-the-favorable-winds',
        'not-every-god-was-virtuous',
        'the-headless-stone-men-of-waxie',
    ],
    'divine-careers': [
        'not-every-god-was-virtuous',
    ],
    'filing-with-heaven': [
        'the-girl-ghost-who-filed-suits',
        'the-chaste-girl-who-cried-injustice',
    ],
    'the-canon-of-sacrifices': [
        'the-headless-stone-men-of-waxie',
    ],
    'dragons': [
        'the-goddess-of-the-favorable-winds',
    ],
    'immortals-and-gods': [
        'the-thunder-god-and-his-fire-sword',
    ],
    'underworld': [
        'the-girl-ghost-who-filed-suits',
        'the-ghost-who-bought-a-son',
    ],
    'ghosts': [
        'the-ghost-who-bought-a-son',
        'the-ghost-who-brought-dumplings',
        'the-chaste-girl-who-cried-injustice',
        'the-girl-ghost-who-filed-suits',
        'two-tales-of-jealous-ghosts',
        'not-every-god-was-virtuous',
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
