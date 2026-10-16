import re, glob

d = []
for f in glob.glob('src/content/*/*.md'):
    t = open(f, encoding='utf-8').read()
    m = re.search(r'^published:\s*([0-9-]+)', t, re.M)
    if m:
        d.append((m.group(1), f))
d.sort()
for a, b in d[-10:]:
    print(a, b)
