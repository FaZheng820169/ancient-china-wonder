"""Attach batch-25 story slugs to relevant worldview entries.

Each worldview's `related:` list gains the new story slugs (deduped).
Usage: python tools/_link_batch25.py
"""
import pathlib

BASE = pathlib.Path('src/content/worldview')

ADD = {
    'small-gods': [
        'the-earth-god-who-bargained',
        'the-god-who-borrowed-two-horses',
        'the-timber-the-storm-delivered',
        'the-ghostly-battle-on-the-sandbar',
    ],
    'the-canon-of-sacrifices': [
        'the-god-who-borrowed-two-horses',
        'the-timber-the-storm-delivered',
    ],
    'immortals-and-gods': [
        'the-perfected-man-of-fuling',
    ],
    'reading-the-fate': [
        'the-perfected-man-of-fuling',
    ],
    'ghosts': [
        'the-judge-of-the-west-lake',
        'the-monk-ghost-of-yunmen',
        'the-torturer-and-the-life-taking-ghost',
        'the-ghost-who-came-home',
        'the-ghostly-battle-on-the-sandbar',
    ],
    'underworld': [
        'the-judge-of-the-west-lake',
        'the-ghost-who-came-home',
    ],
    'the-ledger': [
        'the-torturer-and-the-life-taking-ghost',
        'the-thunder-that-chose-its-victims',
    ],
    'how-a-shrine-begins': [
        'the-timber-the-storm-delivered',
        'the-god-who-borrowed-two-horses',
    ],
}


def patch(name, new_slugs):
    p = BASE / f'{name}.md'
    lines = p.read_text(encoding='utf-8').split('\n')
    out = []
    i = 0
    added = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if line.strip() == 'related:' and i + 1 < len(lines) and lines[i + 1].lstrip().startswith('- '):
            # collect existing related entries
            existing = []
            j = i + 1
            while j < len(lines) and lines[j].lstrip().startswith('- '):
                existing.append(lines[j].strip().strip('- "').strip('"'))
                out.append(lines[j])
                j += 1
            # append missing new slugs
            for s in new_slugs:
                if s not in existing:
                    out.append(f'  - "{s}"')
                    existing.append(s)
                    added += 1
            i = j
            continue
        i += 1
    p.write_text('\n'.join(out), encoding='utf-8')
    print(f'{name}: +{added} related')


for name, slugs in ADD.items():
    patch(name, slugs)
print('done')
