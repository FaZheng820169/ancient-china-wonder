import re, glob, os, collections, json

slugs = set()
meta = {}
for p in glob.glob('src/content/stories/*.md'):
    slug = os.path.basename(p)[:-3]
    slugs.add(slug)
    s = open(p, encoding='utf-8').read()
    fm = s.split('---')[1]

    def g(k, d=''):
        m = re.search(r'^' + k + r':\s*(.*)$', fm, re.M)
        return m.group(1).strip().strip('"') if m else d

    rel = re.findall(r'^  - "([^"]+)"$', fm.split('related:')[1], re.M) if 'related:' in fm else []
    tags = re.findall(r'"([^"]+)"', g('tags', '[]'))
    meta[slug] = {'rel': rel, 'tags': tags, 'title': g('title'),
                  'source': g('sourceZh'), 'order': int(g('order', '0') or 0)}

wv_slugs = set(os.path.basename(p)[:-3] for p in glob.glob('src/content/worldview/*.md'))

print('=== 失效引用（story 的 related 指向了 worldview id）===')
for slug in sorted(meta):
    bad = [r for r in meta[slug]['rel'] if r in wv_slugs]
    if bad:
        print('  %-26s %s' % (slug, bad))

cited = collections.Counter()
for m in meta.values():
    for r in m['rel']:
        if r in slugs:
            cited[r] += 1
for p in glob.glob('src/content/worldview/*.md'):
    fm = open(p, encoding='utf-8').read().split('---')[1]
    for r in re.findall(r'^  - "([^"]+)"$', fm.split('related:')[1], re.M):
        if r in slugs:
            cited[r] += 1

orphans = sorted([s for s in slugs if cited[s] == 0])
print()
print('=== 孤岛页 %d 篇 ===' % len(orphans))
for s in orphans:
    m = meta[s]
    print('  %-28s | %-22s | %s' % (s, m['source'][:22], ','.join(m['tags'])))
