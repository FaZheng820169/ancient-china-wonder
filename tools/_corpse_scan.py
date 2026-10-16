import re, glob, os

KEYS = ['僵尸', '僵屍', '尸', '屍', '骸', '棺', '肉块', '肉塊', '魃', '腐', '冢', '墳']

rows = []
for p in sorted(glob.glob('src/content/stories/*.md')):
    t = open(p, encoding='utf-8').read()
    parts = t.split('---')
    fm = parts[1] if len(parts) > 1 else ''
    o = re.search(r'^order:\s*(\d+)', fm, re.M)
    o = int(o.group(1)) if o else 0
    tz = re.search(r'^titleZh:\s*(.+)$', fm, re.M)
    tz = tz.group(1).strip().strip('"') if tz else ''
    ti = re.search(r'^title:\s*(.+)$', fm, re.M)
    ti = ti.group(1).strip().strip('"') if ti else ''
    hits = {k: fm.count(k) for k in KEYS if fm.count(k)}
    score = (fm.count('僵尸') + fm.count('僵屍')) * 5 + (fm.count('魃') * 4) \
        + fm.count('尸') + fm.count('屍') + fm.count('骸') * 2 \
        + fm.count('棺') + fm.count('腐')
    if score >= 3:
        rows.append((score, o, os.path.basename(p)[:-3], tz, ti, hits))

rows.sort(reverse=True)
for score, o, slug, tz, ti, hits in rows:
    print('%3d  o%-4d %-42s %-12s %s' % (score, o, slug, tz, ti))
    print('      %s' % hits)
print('total candidates', len(rows))
