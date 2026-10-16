import re, glob, sys

WANT = ['zombie-drank-blood', 'three-drought-demons', 'the-geomancers-bones',
        'loufan-woman', 'the-hand-in-the-coffin', 'soul-jar', 'borrowed-body',
        'nanchang-scholar', 'the-collar-of-wood-and-iron', 'skull-breath',
        'the-man-from-before-pangu', 'the-wet-nurses-relics']

for slug in WANT:
    p = 'src/content/stories/%s.md' % slug
    t = open(p, encoding='utf-8').read()
    fm = t.split('---')[1]
    m = re.search(r'^original:\s*\|?\n((?:  .*\n|\n)*)', fm, re.M)
    block = m.group(1) if m else ''
    zh = '\n'.join(l.strip() for l in block.splitlines() if l.strip())
    tz = re.search(r'^titleZh:\s*(.+)$', fm, re.M)
    print('#' * 70)
    print(slug, '|', tz.group(1).strip().strip('"') if tz else '')
    print(zh[:1600])
    print()
