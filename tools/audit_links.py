"""Audit the internal link graph of the story collection.

Run after adding a batch of stories:

    python tools/audit_links.py

Reports:
  - related references that point at worldview ids (never rendered on story pages)
  - related references that point at non-existent slugs
  - orphan pages: stories no other story links to
  - stories missing an illustration or with fewer than 4 cultural notes
  - source distribution
"""

import collections
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

STORY_DIR = 'src/content/stories'
WV_DIR = 'src/content/worldview'


def frontmatter(path):
    return open(path, encoding='utf-8').read().split('---')[1]


def field(fm, key, default=''):
    m = re.search(r'^' + key + r':\s*(.*)$', fm, re.M)
    return m.group(1).strip().strip('"') if m else default


def rel_list(fm):
    if 'related:' not in fm:
        return []
    m = re.search(r'^related:\n((?:  - ".*"\n)*)', fm, re.M)
    if m:
        return re.findall(r'^  - "(.*)"$', m.group(1), re.M)
    m = re.search(r'^related:\s*\[(.*)\]\s*$', fm, re.M)
    if m and m.group(1).strip():
        return [x.strip().strip('"') for x in m.group(1).split(',')]
    return []


story_slugs = set()
meta = {}
for p in glob.glob(os.path.join(STORY_DIR, '*.md')):
    slug = os.path.basename(p)[:-3]
    fm = frontmatter(p)
    story_slugs.add(slug)
    meta[slug] = {
        'rel': rel_list(fm),
        'notes': len(re.findall(r'^  - term:', fm, re.M)),
        'image': bool(field(fm, 'image')),
        'source': field(fm, 'sourceZh'),
        'tags': re.findall(r'"([^"]+)"', field(fm, 'tags', '[]')),
    }

wv_slugs = set(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(WV_DIR, '*.md')))

problems = 0

print('Stories: %d   Worldview: %d' % (len(story_slugs), len(wv_slugs)))
print()

print('-- Dead related references --')
dead = {}
for slug, m in meta.items():
    bad = [r for r in m['rel'] if r in wv_slugs or r not in story_slugs]
    if bad:
        dead[slug] = bad
if dead:
    for slug in sorted(dead):
        print('  %-30s %s' % (slug, dead[slug]))
    problems += sum(len(v) for v in dead.values())
else:
    print('  none')
print()

inbound = collections.Counter()
for m in meta.values():
    for r in m['rel']:
        if r in story_slugs:
            inbound[r] += 1
for p in glob.glob(os.path.join(WV_DIR, '*.md')):
    for r in rel_list(frontmatter(p)):
        if r in story_slugs:
            inbound[r] += 1

orphans = sorted(s for s in story_slugs if inbound[s] == 0)
print('-- Orphan pages (no inbound related link) --')
print('  %d %s' % (len(orphans), orphans[:15] if orphans else ''))
problems += len(orphans)
print()

print('-- Quality --')
no_img = [s for s in meta if not meta[s]['image']]
few_notes = [s for s in meta if meta[s]['notes'] < 4]
print('  missing illustration : %d %s' % (len(no_img), no_img[:8]))
print('  fewer than 4 notes   : %d %s' % (len(few_notes), few_notes[:8]))
problems += len(no_img) + len(few_notes)
print()

print('-- Sources --')
for src, n in collections.Counter(m['source'] for m in meta.values()).most_common(8):
    print('  %-34s %d' % (src[:34], n))
print()

vals = sorted(inbound.values())
if vals:
    print('Inbound links per story: min %d / median %d / max %d'
          % (vals[0], vals[len(vals) // 2], vals[-1]))
print()
print('PROBLEMS: %d' % problems)
sys.exit(1 if problems else 0)
