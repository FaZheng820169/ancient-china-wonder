import re, collections, glob

c = collections.Counter()
for f in glob.glob('src/content/stories/*.md'):
    t = open(f, encoding='utf-8').read()
    m = re.search(r'^sourceZh:\s*(.+?)\s*$', t, re.M)
    c[m.group(1).strip('"\'') if m else '???'] += 1
for k, v in c.most_common():
    print(v, k)
print('total', sum(c.values()))
