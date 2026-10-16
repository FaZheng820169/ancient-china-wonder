import re, glob, collections

c = collections.Counter()
for f in glob.glob('src/content/stories/*.md'):
    fm = open(f, encoding='utf-8').read().split('---')[1]
    m = re.search(r'^tags:\s*\[(.*)\]', fm, re.M)
    if m:
        for t in re.findall(r'"([^"]+)"', m.group(1)):
            c[t] += 1
for t, n in c.most_common(80):
    print(n, t)
