import glob
import re
import collections

mx = []
tags = collections.Counter()
order = 0
for f in glob.glob('src/content/stories/*.md'):
    t = open(f, encoding='utf-8').read()
    p = re.search(r'^published:\s*(\S+)', t, re.M)
    o = re.search(r'^order:\s*(\d+)', t, re.M)
    if p:
        mx.append(p.group(1))
    if o:
        order = max(order, int(o.group(1)))
    for tg in re.findall(r'^tags:\s*\[(.*?)\]', t, re.M):
        for x in re.findall(r'"(.*?)"', tg):
            tags[x] += 1
print('max published', max(mx) if mx else None)
print('max order', order)
for k, v in tags.most_common():
    print(v, k)
