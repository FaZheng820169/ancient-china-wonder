"""Batch 26: add the 12 new story slugs to the related lists of the worldview
entries they are meant to thicken.

Mapping (gap-targeted):
  hun-and-po            +4   (the ox, the physician, the general, the girl)
  fengdu                +3   (the scholar, the brother, the sorcerer)
  dragons               +4   (four generals, water people, wife taken, flood)
  small-gods            +2   (the girl, the sorcerer)
  marriage-across-the-border +2 (wife taken, wife summoned)
"""
import pathlib
import re

WV = pathlib.Path('src/content/worldview')

ADD = {
    'hun-and-po': [
        'the-ox-that-bore-his-name',
        'the-physician-who-burned-with-aconite',
        'the-general-who-punched-a-ghost',
        'the-girl-claimed-by-the-neighbor-shrine',
    ],
    'fengdu': [
        'the-scholar-who-returned-from-the-court-of-death',
        'the-brother-who-traded-a-sickness',
        'the-sorcerer-and-the-seaside-shrine',
    ],
    'dragons': [
        'the-four-generals-and-the-river-dragon',
        'the-water-people-of-dingtao',
        'the-wife-taken-by-the-lake-dragon',
        'the-flood-that-rose-from-the-well',
    ],
    'small-gods': [
        'the-girl-claimed-by-the-neighbor-shrine',
        'the-sorcerer-and-the-seaside-shrine',
    ],
    'marriage-across-the-border': [
        'the-wife-taken-by-the-lake-dragon',
        'the-wife-summoned-from-the-other-side',
    ],
}


def add_to_related(text, new):
    # locate the related: block
    m = re.search(r'(related:\s*\n)((?:\s*-\s+.+\n)+)', text)
    if not m:
        # no related block: insert before closing ---
        block = 'related:\n' + ''.join(f'  - "{n}"\n' for n in new) + '---\n'
        text = text.replace('---\n', block, 1)
        return text, new
    existing = [ln.strip()[2:].strip().strip('"').strip("'")
                for ln in m.group(2).split('\n') if ln.strip().startswith('-')]
    to_add = [n for n in new if n not in existing]
    if not to_add:
        return text, []
    addition = ''.join(f'  - "{n}"\n' for n in to_add)
    new_block = m.group(1) + m.group(2) + addition
    text = text[:m.start()] + new_block + text[m.end():]
    return text, to_add


def main():
    files_changed = 0
    for wv, new in ADD.items():
        p = WV / f'{wv}.md'
        text = p.read_text(encoding='utf-8')
        text, added = add_to_related(text, new)
        if added:
            p.write_text(text, encoding='utf-8')
            files_changed += 1
            print(f'{wv}: +{len(added)} -> {added}')
        else:
            print(f'{wv}: (no change)')
    print('files changed:', files_changed)


if __name__ == '__main__':
    main()
