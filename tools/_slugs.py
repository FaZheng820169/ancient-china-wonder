import glob
import os
import re

rows = []
for f in glob.glob('src/content/stories/*.md'):
    t = open(f, encoding='utf-8').read()
    slug = os.path.basename(f)[:-3]
    ti = re.search(r'^title:\s*(.+?)\s*$', t, re.M)
    zh = re.search(r'^titleZh:\s*(.+?)\s*$', t, re.M)
    rows.append((slug, (zh.group(1).strip('"') if zh else ''), (ti.group(1).strip('"') if ti else '')))
rows.sort()
for r in rows:
    print('%-42s %-14s %s' % r)
print(len(rows), 'stories')
