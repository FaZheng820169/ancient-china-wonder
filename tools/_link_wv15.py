# -*- coding: utf-8 -*-
"""Point worldview entries at the batch-15 stories that illustrate them."""
import io

PAIRS = [
    ('small-gods', 'the-warrant-that-sank-the-boat'),
    ('small-gods', 'the-crab-with-the-dipper'),
    ('the-ledger', 'a-lifetimes-salary'),
    ('the-ledger', 'the-warrant-that-sank-the-boat'),
    ('underworld', 'the-wife-who-died-every-afternoon'),
    ('how-souls-move-on', 'the-wife-who-died-every-afternoon'),
    ('marriage-across-the-border', 'the-woman-who-followed-him-home'),
    ('monsters-and-yaoguai', 'the-red-snake-in-the-road'),
    ('divine-careers', 'the-ghost-seer'),
    ('dragons', 'the-crab-with-the-dipper'),
]

for host, new in PAIRS:
    p = 'src/content/worldview/%s.md' % host
    txt = io.open(p, encoding='utf-8').read()
    lines = txt.split('\n')
    if 'related:' not in txt:
        print('!! no related block in', host)
        continue
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
    print('%-26s <- %s' % (host, new))
