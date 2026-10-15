# -*- coding: utf-8 -*-
"""Batch 17 linking:
1. strip worldview / feature slugs out of story `related` lists (they are dead refs there)
2. hang the newcomers off the right worldview & feature entries instead (bidirectional)"""
import io

DROP = {
    'the-woman-of-the-black-pine-valley': ['filing-with-heaven'],
    'the-fifth-young-lord': ['filing-with-heaven'],
    'the-house-in-the-cypress-wood': ['how-souls-move-on'],
    'paper-and-brush-in-the-coffin': ['filing-with-heaven'],
    'the-father-in-law-with-the-iron-ruler': ['filing-with-heaven', 'small-gods'],
    'the-wine-pressed-from-bone-marrow': ['how-do-you-know'],
    'seventy-days-of-thunder': ['filing-with-heaven', 'how-souls-move-on'],
    'the-nine-young-dragons': ['divine-careers', 'small-gods'],
    'the-widow-who-came-to-file-suit': ['filing-with-heaven', 'fox-spirits'],
    'stabbing-the-spring': ['filing-with-heaven', 'divine-careers'],
    'twelve-years-and-little-red': ['how-do-you-know'],
}

RENAME = {
    'the-wine-pressed-from-bone-marrow': ('the-world-inside-a-pillow', 'zhen-zhong'),
}

WV_PAIRS = [
    ('filing-with-heaven', 'paper-and-brush-in-the-coffin'),
    ('filing-with-heaven', 'the-father-in-law-with-the-iron-ruler'),
    ('filing-with-heaven', 'the-fifth-young-lord'),
    ('filing-with-heaven', 'seventy-days-of-thunder'),
    ('filing-with-heaven', 'stabbing-the-spring'),
    ('filing-with-heaven', 'the-widow-who-came-to-file-suit'),
    ('filing-with-heaven', 'the-woman-of-the-black-pine-valley'),
    ('how-souls-move-on', 'seventy-days-of-thunder'),
    ('how-souls-move-on', 'the-house-in-the-cypress-wood'),
    ('small-gods', 'the-father-in-law-with-the-iron-ruler'),
    ('small-gods', 'the-nine-young-dragons'),
    ('divine-careers', 'the-nine-young-dragons'),
    ('divine-careers', 'stabbing-the-spring'),
    ('fox-spirits', 'the-widow-who-came-to-file-suit'),
    ('monsters-and-yaoguai', 'the-wildcat-wife'),
    ('marriage-across-the-border', 'the-woman-of-the-black-pine-valley'),
    ('marriage-across-the-border', 'the-house-in-the-cypress-wood'),
    ('ghosts', 'the-house-in-the-cypress-wood'),
    ('dragons', 'the-nine-young-dragons'),
    ('the-ledger', 'twelve-years-and-little-red'),
]

FEATURE_PAIRS = [
    ('how-do-you-know', 'the-wine-pressed-from-bone-marrow'),
    ('how-do-you-know', 'twelve-years-and-little-red'),
    ('the-dream-is-a-country', 'the-wine-pressed-from-bone-marrow'),
]

STORY_PAIRS = [
    ('zhen-zhong', 'the-wine-pressed-from-bone-marrow'),
    ('the-wine-that-was-not-wine', 'the-wine-pressed-from-bone-marrow'),
    ('the-clerk-who-died-twice', 'the-wine-pressed-from-bone-marrow'),
    ('the-wine-that-was-not-wine', 'twelve-years-and-little-red'),
    ('the-crab-with-the-dipper', 'stabbing-the-spring'),
    ('the-crab-with-the-dipper', 'the-nine-young-dragons'),
    ('the-warrant-that-sank-the-boat', 'the-father-in-law-with-the-iron-ruler'),
    ('thirteen-cats', 'the-wildcat-wife'),
    ('the-woman-with-the-cat', 'the-wildcat-wife'),
    ('xi-fangping', 'paper-and-brush-in-the-coffin'),
    ('a-lifetimes-salary', 'twelve-years-and-little-red'),
]


def related_block(lines):
    start = next(i for i, l in enumerate(lines) if l.startswith('related:'))
    last = start
    i = start + 1
    while i < len(lines) and lines[i].startswith('  - "'):
        last = i
        i += 1
    return start, last


def edit(kind, host, fn):
    p = 'src/content/%s/%s.md' % (kind, host)
    lines = io.open(p, encoding='utf-8').read().split('\n')
    fn(lines)
    io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))


for slug, drops in DROP.items():
    def work(lines, drops=drops):
        s, e = related_block(lines)
        keep = []
        for l in lines[s + 1:e + 1]:
            ref = l.strip().lstrip('- ').strip('"')
            if ref in drops:
                continue
            keep.append(l)
        lines[s + 1:e + 1] = keep
    edit('stories', slug, work)
    print('dropped from %-38s %s' % (slug, ', '.join(drops)))

for slug, (old, new) in RENAME.items():
    def work(lines, old=old, new=new):
        for i, l in enumerate(lines):
            if l.strip() == '- "%s"' % old:
                lines[i] = '  - "%s"' % new
    edit('stories', slug, work)
    print('renamed in %-38s %s -> %s' % (slug, old, new))


def add(kind, host, new):
    p = 'src/content/%s/%s.md' % (kind, host)
    lines = io.open(p, encoding='utf-8').read().split('\n')
    try:
        s, e = related_block(lines)
    except StopIteration:
        print('!! no related block in', host)
        return
    item = '  - "%s"' % new
    if item in lines:
        print('skip (already)', host, new)
        return
    lines.insert(e + 1, item)
    io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print('%-34s <- %s' % (host, new))


for h, n in WV_PAIRS:
    add('worldview', h, n)
for h, n in FEATURE_PAIRS:
    add('features', h, n)
for h, n in STORY_PAIRS:
    add('stories', h, n)
