# -*- coding: utf-8 -*-
"""Add inbound related-links from existing stories to the batch-15 newcomers."""
import io

PAIRS = [
    ('enrolment-of-ghosts', 'the-warrant-that-sank-the-boat'),
    ('the-litigation-writers', 'the-warrant-that-sank-the-boat'),
    ('xi-fangping', 'the-wife-who-died-every-afternoon'),
    ('peacock-sutra', 'the-wife-who-died-every-afternoon'),
    ('soul-jar', 'the-log-in-the-bed'),
    ('plague-god', 'the-log-in-the-bed'),
    ('zhang-furen', 'the-tomb-at-the-drill-ground'),
    ('one-cash', 'the-tomb-at-the-drill-ground'),
    ('dragon-girl-temple', 'the-bamboo-that-gathered-treasure'),
    ('kun-lun-nu', 'the-bamboo-that-gathered-treasure'),
    ('resentment-became-snake', 'the-red-snake-in-the-road'),
    ('the-exorcism-at-shangqing', 'the-red-snake-in-the-road'),
    ('shunji-king', 'the-crab-with-the-dipper'),
    ('three-drought-demons', 'the-crab-with-the-dipper'),
    ('three-hundred-cash', 'a-lifetimes-salary'),
    ('seizing-surplus-ghost', 'a-lifetimes-salary'),
    ('tang-xianzu', 'the-wizard-who-could-somersault'),
    ('monster-feared-reason', 'the-wizard-who-could-somersault'),
    ('city-god-drunk', 'the-ghost-seer'),
    ('thirteen-cats', 'the-ghost-seer'),
    ('the-man-who-bound-tigers', 'the-tiger-at-the-fireside'),
    ('ye-laotuo', 'the-tiger-at-the-fireside'),
    ('west-lake-girl', 'the-woman-who-followed-him-home'),
    ('loufan-woman', 'the-woman-who-followed-him-home'),
]

for host, new in PAIRS:
    p = 'src/content/stories/%s.md' % host
    lines = io.open(p, encoding='utf-8').read().split('\n')
    start = next(i for i, l in enumerate(lines) if l.startswith('related:'))
    last = start
    i = start + 1
    while i < len(lines) and lines[i].startswith('  - "'):
        last = i
        i += 1
    item = '  - "%s"' % new
    if item in lines:
        print('skip (already)', host, new)
        continue
    lines.insert(last + 1, item)
    io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print('%-34s <- %s' % (host, new))
