import re, glob, os

stories = set(os.path.basename(p)[:-3] for p in glob.glob('src/content/stories/*.md'))
counts = {}
for p in glob.glob('src/content/worldview/*.md'):
    fm = open(p, encoding='utf-8').read().split('---')[1]
    m = re.search(r'^related:\n((?:  - ".*"\n)*)', fm, re.M)
    if not m:
        continue
    for r in re.findall(r'^  - "(.*)"$', m.group(1), re.M):
        if r in stories:
            counts.setdefault(r, []).append(os.path.basename(p)[:-3])

hit = len(counts)
print('stories that will show a "Where this fits" block: %d / %d' % (hit, len(stories)))
twice = {k: v for k, v in counts.items() if len(v) > 1}
print('linked from more than one entry: %d' % len(twice))
top = sorted(counts.items(), key=lambda kv: -len(kv[1]))[:8]
for k, v in top:
    print('  %-46s %d  %s' % (k, len(v), ', '.join(v)))
