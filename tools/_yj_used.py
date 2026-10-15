import glob
import re

out = []
for f in sorted(glob.glob('src/content/stories/*.md')):
    t = open(f, encoding='utf-8').read()
    head = t[:900]
    if '夷坚志' in head or 'Yijian' in head:
        zh = re.search(r'^titleZh:\s*(.+?)\s*$', t, re.M)
        ti = re.search(r'^title:\s*(.+?)\s*$', t, re.M)
        out.append('%s | %s' % ((zh.group(1).strip('"\'') if zh else '?'),
                                (ti.group(1).strip('"\'') if ti else '?')))
print(len(out), 'Yijian Zhi stories already published')
for o in out:
    print(o)
