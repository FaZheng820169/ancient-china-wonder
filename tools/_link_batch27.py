# -*- coding: utf-8 -*-
"""Batch 27: add the 12 Xieduo story slugs to the worldview entries they feed.

Feeds: how-a-shrine-begins / small-gods / divine-careers / underworld / ghosts /
cultivation-system / immortals-and-gods / lu-dongbin / reading-the-fate /
monsters-and-yaoguai / hun-and-po.
"""
import pathlib
import re

WV = pathlib.Path('src/content/worldview')

ADD = {
    'how-a-shrine-begins': [
        'the-temple-of-the-traitors-lackey',
        'the-god-of-books-who-took-revenge',
        'the-crow-who-knew-a-man-before-his-rise',
    ],
    'small-gods': [
        'the-temple-of-the-traitors-lackey',
        'the-god-of-books-who-took-revenge',
        'the-oracle-slips-of-general-bus-temple',
    ],
    'divine-careers': [
        'the-temple-of-the-traitors-lackey',
        'the-god-of-books-who-took-revenge',
    ],
    'underworld': [
        'the-vet-who-treated-the-dead',
    ],
    'ghosts': [
        'the-vet-who-treated-the-dead',
        'the-ghost-who-shrank-before-a-soldier',
        'the-ghost-tutor-of-broom-village',
        'the-poets-through-the-window',
    ],
    'cultivation-system': [
        'the-ghost-who-shrank-before-a-soldier',
        'the-lotus-immortal-who-tested-a-son',
    ],
    'immortals-and-gods': [
        'the-lotus-immortal-who-tested-a-son',
        'why-the-literary-star-god-is-blue',
    ],
    'lu-dongbin': [
        'the-lotus-immortal-who-tested-a-son',
    ],
    'reading-the-fate': [
        'the-oracle-slips-of-general-bus-temple',
        'why-the-literary-star-god-is-blue',
        'the-crow-who-knew-a-man-before-his-rise',
    ],
    'monsters-and-yaoguai': [
        'the-girl-with-the-lotus-root',
    ],
    'hun-and-po': [
        'the-girl-with-the-lotus-root',
    ],
}


def add_to_related(text, new):
    m = re.search(r'(related:\s*\n)((?:\s*-\s+.+\n)+)', text)
    if not m:
        block = 'related:\n' + ''.join(f'  - "{n}"\n' for n in new) + '---\n'
        return text.replace('---\n', block, 1), new
    existing = [ln.strip()[2:].strip().strip('"').strip("'")
                for ln in m.group(2).split('\n') if ln.strip().startswith('-')]
    to_add = [n for n in new if n not in existing]
    if not to_add:
        return text, []
    addition = ''.join(f'  - "{n}"\n' for n in to_add)
    return text[:m.start()] + m.group(1) + m.group(2) + addition + text[m.end():], to_add


def main():
    changed = 0
    for wv, new in ADD.items():
        p = WV / f'{wv}.md'
        text = p.read_text(encoding='utf-8')
        text, added = add_to_related(text, new)
        if added:
            p.write_text(text, encoding='utf-8')
            changed += 1
            print(f'{wv}: +{len(added)}')
        else:
            print(f'{wv}: (no change)')
    print('files changed:', changed)


if __name__ == '__main__':
    main()
