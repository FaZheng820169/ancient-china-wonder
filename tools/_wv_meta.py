import glob
import os
import re

for f in sorted(glob.glob('src/content/worldview/*.md')):
    t = open(f, encoding='utf-8').read()
    b = re.search(r'^branch:\s*(\S+)', t, re.M)
    o = re.search(r'^order:\s*(\d+)', t, re.M)
    ti = re.search(r'^title:\s*(.+?)\s*$', t, re.M)
    print('%-28s %-12s %-4s %s' % (os.path.basename(f)[:-3],
                                   b.group(1) if b else '?',
                                   o.group(1) if o else '?',
                                   ti.group(1).strip('"') if ti else '?'))
