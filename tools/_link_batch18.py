# -*- coding: utf-8 -*-
"""Batch 18 linking: strip worldview/feature slugs out of story `related`,
then hang the newcomers off the right worldview & feature entries instead."""
import io

DROP = {
    'the-collar-of-wood-and-iron': ['monsters-and-yaoguai'],
    'the-true-judge-bao-and-the-false': ['suing-heaven'],
    'summoned-as-a-witness': ['filing-with-heaven'],
    'the-judge-answers-questions': ['divine-careers', 'small-gods', 'the-underworld-exam'],
    'the-man-from-before-pangu': ['three-realms', 'penglai', 'how-souls-move-on', 'monsters-and-yaoguai'],
    'the-footbinding-case': ['suing-heaven', 'the-ledger'],
    'intercession-in-the-underworld': ['suing-heaven'],
    'the-god-nobody-could-name': ['how-a-shrine-begins', 'divine-careers', 'small-gods'],
    'the-register-of-the-unranked': ['the-underworld-exam', 'the-scholar-and-the-strange', 'the-ledger'],
    'the-ghost-who-sued-an-actor': ['suing-heaven', 'filing-with-heaven'],
    'the-eye-on-its-back': ['what-ghosts-can-do'],
    'when-the-stones-spoke': ['monsters-and-yaoguai', 'how-do-you-know'],
}

ADD_STORY = {
    'the-man-from-before-pangu': ['zhen-zhong', 'the-collar-of-wood-and-iron'],
    'summoned-as-a-witness': ['paper-and-brush-in-the-coffin'],
    'the-register-of-the-unranked': ['a-lifetimes-salary'],
    'the-eye-on-its-back': ['one-eyed-five'],
}

WV_PAIRS = [
    ('monsters-and-yaoguai', 'the-collar-of-wood-and-iron'),
    ('monsters-and-yaoguai', 'the-man-from-before-pangu'),
    ('monsters-and-yaoguai', 'when-the-stones-spoke'),
    ('monsters-and-yaoguai', 'the-eye-on-its-back'),
    ('divine-careers', 'the-judge-answers-questions'),
    ('divine-careers', 'the-god-nobody-could-name'),
    ('small-gods', 'the-judge-answers-questions'),
    ('small-gods', 'the-god-nobody-could-name'),
    ('the-underworld-exam', 'the-judge-answers-questions'),
    ('the-underworld-exam', 'the-register-of-the-unranked'),
    ('three-realms', 'the-man-from-before-pangu'),
    ('penglai', 'the-man-from-before-pangu'),
    ('how-souls-move-on', 'the-man-from-before-pangu'),
    ('the-ledger', 'the-footbinding-case'),
    ('the-ledger', 'the-register-of-the-unranked'),
    ('how-a-shrine-begins', 'the-god-nobody-could-name'),
    ('filing-with-heaven', 'summoned-as-a-witness'),
    ('filing-with-heaven', 'the-ghost-who-sued-an-actor'),
    ('underworld', 'intercession-in-the-underworld'),
    ('underworld', 'the-judge-answers-questions'),
    ('ghosts', 'the-eye-on-its-back'),
    ('ghosts', 'summoned-as-a-witness'),
    ('she-is-there-still', 'when-the-stones-spoke'),
]

FEATURE_PAIRS = [
    ('suing-heaven', 'the-true-judge-bao-and-the-false'),
    ('suing-heaven', 'the-footbinding-case'),
    ('suing-heaven', 'intercession-in-the-underworld'),
    ('suing-heaven', 'the-ghost-who-sued-an-actor'),
    ('the-scholar-and-the-strange', 'the-register-of-the-unranked'),
    ('what-ghosts-can-do', 'the-eye-on-its-back'),
    ('how-do-you-know', 'when-the-stones-spoke'),
    ('how-do-you-know', 'the-man-from-before-pangu'),
]

STORY_PAIRS = [
    ('xi-fangping', 'intercession-in-the-underworld'),
    ('paper-and-brush-in-the-coffin', 'summoned-as-a-witness'),
    ('the-warrant-that-sank-the-boat', 'summoned-as-a-witness'),
    ('a-lifetimes-salary', 'the-judge-answers-questions'),
    ('the-clerk-who-died-twice', 'the-judge-answers-questions'),
    ('the-ghost-seer', 'the-judge-answers-questions'),
    ('the-ten-aunts-temple', 'the-god-nobody-could-name'),
    ('ox-head-king', 'the-god-nobody-could-name'),
    ('zhen-zhong', 'the-man-from-before-pangu'),
    ('one-eyed-five', 'the-eye-on-its-back'),
    ('the-wizard-who-could-somersault', 'the-collar-of-wood-and-iron'),
    ('monster-feared-reason', 'the-eye-on-its-back'),
    ('the-litigation-writers', 'the-true-judge-bao-and-the-false'),
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
        keep = [l for l in lines[s + 1:e + 1]
                if l.strip().lstrip('- ').strip('"') not in drops]
        lines[s + 1:e + 1] = keep
    edit('stories', slug, work)

for slug, adds in ADD_STORY.items():
    def work(lines, adds=adds):
        s, e = related_block(lines)
        for a in adds:
            item = '  - "%s"' % a
            if item not in lines:
                lines.insert(e + 1, item)
                e += 1
    edit('stories', slug, work)


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
        return
    lines.insert(e + 1, item)
    io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))


for h, n in WV_PAIRS:
    add('worldview', h, n)
for h, n in FEATURE_PAIRS:
    add('features', h, n)
for h, n in STORY_PAIRS:
    add('stories', h, n)
print('linking done')
