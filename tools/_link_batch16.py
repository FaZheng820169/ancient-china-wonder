# -*- coding: utf-8 -*-
"""Add inbound related-links from existing stories/worldview to the batch-16 newcomers."""
import io

STORY_PAIRS = [
    ('the-tiger-at-the-fireside', 'the-woman-with-the-cat'),
    ('thirteen-cats', 'the-woman-with-the-cat'),
    ('loufan-woman', 'the-woman-with-the-cat'),
    ('ye-laotuo', 'shaggy-head'),
    ('gui-bi-jiang-san-mang', 'shaggy-head'),
    ('god-casual-unions', 'the-one-legged-ghost'),
    ('one-eyed-five', 'the-one-legged-ghost'),
    ('zhao-sanweng', 'the-taoist-who-came-to-supper'),
    ('the-son-who-cost-a-fortune', 'the-taoist-who-came-to-supper'),
    ('widow-tian', 'the-hundred-meat-pies'),
    ('the-woman-who-followed-him-home', 'the-hundred-meat-pies'),
    ('skin-field-surgeon', 'one-pear-a-day'),
    ('the-mirror-that-showed-his-gall', 'one-pear-a-day'),
    ('the-farewell-feast', 'the-three-warriors'),
    ('salt-rebel', 'the-daughter-of-zhang-ten-thousand'),
    ('three-hundred-cash', 'the-lay-brother-who-became-a-pig'),
    ('debt-of-silver', 'the-lay-brother-who-became-a-pig'),
    ('xi-fangping', 'the-clerk-who-died-twice'),
    ('a-lifetimes-salary', 'the-clerk-who-died-twice'),
    ('peacock-sutra', 'the-wet-nurses-relics'),
    ('the-literate-dog', 'the-wet-nurses-relics'),
    ('insect-writing', 'the-candle-flowers'),
    ('copyists-four-seals', 'the-candle-flowers'),
]

WV_PAIRS = [
    ('monsters-and-yaoguai', 'the-one-legged-ghost'),
    ('monsters-and-yaoguai', 'shaggy-head'),
    ('monsters-and-yaoguai', 'the-woman-with-the-cat'),
    ('small-gods', 'the-one-legged-ghost'),
    ('immortals-and-gods', 'the-taoist-who-came-to-supper'),
    ('the-ledger', 'the-lay-brother-who-became-a-pig'),
    ('underworld', 'the-clerk-who-died-twice'),
    ('divine-careers', 'the-clerk-who-died-twice'),
    ('filing-with-heaven', 'the-clerk-who-died-twice'),
    ('filing-with-heaven', 'the-hundred-meat-pies'),
    ('how-souls-move-on', 'the-wet-nurses-relics'),
    ('ghosts', 'the-daughter-of-zhang-ten-thousand'),
]


def add(kind, host, new):
    p = 'src/content/%s/%s.md' % (kind, host)
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
        return
    lines.insert(last + 1, item)
    io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print('%-34s <- %s' % (host, new))


for h, n in STORY_PAIRS:
    add('stories', h, n)
for h, n in WV_PAIRS:
    add('worldview', h, n)
