# -*- coding: utf-8 -*-
"""Batch 27: rewrite story.related to story-slug-only lists.

story.related may contain ONLY story slugs (never worldview ids or feature
slugs); the worldview backlinks are added separately on the worldview side.
Also designs an intra-batch interlink matrix so every story has >=1 inbound.
"""
import pathlib
import re

ST = pathlib.Path('src/content/stories')

RELATED = {
    'the-temple-of-the-traitors-lackey': [
        'the-god-of-books-who-took-revenge',
        'why-the-literary-star-god-is-blue',
        'the-crow-who-knew-a-man-before-his-rise',
    ],
    'the-god-of-books-who-took-revenge': [
        'the-temple-of-the-traitors-lackey',
        'the-ghost-tutor-of-broom-village',
        'the-god-who-borrowed-two-horses',
    ],
    'the-vet-who-treated-the-dead': [
        'the-scholar-who-returned-from-the-court-of-death',
        'the-ghost-tutor-of-broom-village',
        'the-poets-through-the-window',
    ],
    'the-ghost-who-shrank-before-a-soldier': [
        'the-ghost-tutor-of-broom-village',
        'the-lotus-immortal-who-tested-a-son',
        'the-poets-through-the-window',
    ],
    'the-ghost-tutor-of-broom-village': [
        'the-vet-who-treated-the-dead',
        'the-poets-through-the-window',
        'the-ghost-who-came-home',
    ],
    'the-lotus-immortal-who-tested-a-son': [
        'the-maid-who-caught-the-bullets',
        'the-girl-with-the-lotus-root',
        'the-perfected-man-of-fuling',
    ],
    'the-poets-through-the-window': [
        'the-vet-who-treated-the-dead',
        'the-ghost-tutor-of-broom-village',
        'the-ghost-who-followed-him-through-three-lives',
    ],
    'the-oracle-slips-of-general-bus-temple': [
        'why-the-literary-star-god-is-blue',
        'the-crow-who-knew-a-man-before-his-rise',
        'the-girl-who-read-faces',
    ],
    'why-the-literary-star-god-is-blue': [
        'the-temple-of-the-traitors-lackey',
        'the-oracle-slips-of-general-bus-temple',
        'the-thunder-god-answers-a-memo',
    ],
    'the-girl-with-the-lotus-root': [
        'the-lotus-immortal-who-tested-a-son',
        'the-maid-who-caught-the-bullets',
        'the-man-from-before-pangu',
    ],
    'the-crow-who-knew-a-man-before-his-rise': [
        'the-temple-of-the-traitors-lackey',
        'the-oracle-slips-of-general-bus-temple',
        'the-girl-who-read-faces',
    ],
    'the-maid-who-caught-the-bullets': [
        'the-lotus-immortal-who-tested-a-son',
        'the-girl-with-the-lotus-root',
        'the-perfected-man-of-fuling',
    ],
}


def rewrite(text, new):
    block = 'related:\n' + ''.join(f'  - "{n}"\n' for n in new)
    m = re.search(r'related:\s*\n(?:\s*-\s+.+\n)+', text)
    if not m:
        return text.replace('---\n', block + '---\n', 1)
    return text[:m.start()] + block + text[m.end():]


def main():
    changed = 0
    for slug, rel in RELATED.items():
        p = ST / f'{slug}.md'
        text = p.read_text(encoding='utf-8')
        new = rewrite(text, rel)
        if new != text:
            p.write_text(new, encoding='utf-8')
            changed += 1
            print(f'{slug}: related -> {len(rel)} story slugs')
        else:
            print(f'{slug}: NO CHANGE')
    print('files changed:', changed)


if __name__ == '__main__':
    main()
