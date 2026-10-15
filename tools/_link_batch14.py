# -*- coding: utf-8 -*-
"""Add inbound related-links from existing stories to the batch-14 newcomers."""
import io

PAIRS = [
    ('the-girl-who-parodied-the-classics', 'insect-writing'),
    ('the-man-who-bound-tigers', 'the-farewell-feast'),
    ('the-henpecked-magistrate', 'the-mirror-that-showed-his-gall'),
    ('one-cash', 'the-son-who-cost-a-fortune'),
    ('laoshan', 'the-wine-that-was-not-wine'),
    ('the-man-in-the-coin-hole', 'the-osmanthus-with-no-scent'),
    ('the-geomancers-bones', 'the-turtle-who-taught-a-fortune-teller'),
    ('nan-ke', 'the-ants-patent-of-nobility'),
    ('the-pheasant-matchmaker', 'the-otters-offering'),
    ('liu-chen-ruan-zhao', 'thorn-country'),
    ('guan-yu-false-verdict', 'the-tomb-called-gratitude'),
    ('tan-sheng', 'the-bride-who-cast-her-coat'),
]

for host, new in PAIRS:
    p = 'src/content/stories/%s.md' % host
    lines = io.open(p, encoding='utf-8').read().split('\n')
    # locate the related block
    start = next(i for i, l in enumerate(lines) if l.startswith('related:'))
    last = start
    i = start + 1
    while i < len(lines) and lines[i].startswith('  - "'):
        last = i; i += 1
    item = '  - "%s"' % new
    if item in lines:
        print('skip (already)', host, new); continue
    lines.insert(last + 1, item)
    io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print('%-34s <- %s' % (host, new))
