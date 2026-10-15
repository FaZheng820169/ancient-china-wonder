import re, glob, os, collections

slugs = set()
meta = {}
for p in glob.glob('src/content/stories/*.md'):
    s = open(p, encoding='utf-8').read()
    fm = s.split('---')[1]
    slug = os.path.basename(p)[:-3]
    slugs.add(slug)

    def g(k, d=''):
        m = re.search(r'^' + k + r':\s*(.*)$', fm, re.M)
        return m.group(1).strip().strip('"') if m else d

    rel = re.findall(r'^  - "([^"]+)"$', fm.split('related:')[1], re.M) if 'related:' in fm else []
    notes = len(re.findall(r'^  - term:', fm, re.M))
    img = g('image')
    meta[slug] = {
        'rel': rel,
        'notes': notes,
        'img': bool(img and img != '""'),
        'source': g('sourceZh'),
        'featured': g('featured') == 'true',
        'order': int(g('order', '0') or 0),
    }

bad_rel = collections.defaultdict(list)
for slug, m in meta.items():
    for r in m['rel']:
        if r not in slugs:
            bad_rel[slug].append(r)

cited = collections.Counter()
for m in meta.values():
    for r in m['rel']:
        if r in slugs:
            cited[r] += 1

wv = {}
for p in glob.glob('src/content/worldview/*.md'):
    s = open(p, encoding='utf-8').read()
    fm = s.split('---')[1]
    slug = os.path.basename(p)[:-3]
    rel = re.findall(r'^  - "([^"]+)"$', fm.split('related:')[1], re.M) if 'related:' in fm else []
    wv[slug] = rel
    for r in rel:
        if r in slugs:
            cited[r] += 1

print('stories:', len(slugs))
print('notes<4 :', sum(1 for m in meta.values() if m['notes'] < 4))
print('no image:', sum(1 for m in meta.values() if not m['img']))
print('bad related refs:', sum(len(v) for v in bad_rel.values()), dict(list(bad_rel.items())[:8]))
print('featured:', sum(1 for m in meta.values() if m['featured']))
print()
orphans = sorted([s for s in slugs if cited[s] == 0])
print('orphan stories (never linked):', len(orphans))
print('  ', orphans[:25])
print()
src = collections.Counter(m['source'] for m in meta.values())
for k, v in src.most_common():
    print('  %-24s %d' % (k, v))
