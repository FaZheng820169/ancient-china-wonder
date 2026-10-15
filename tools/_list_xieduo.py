# -*- coding: utf-8 -*-
"""List Xieduo tales not yet published, with length, to pick the next batch."""
import re, glob, io

used = set()
for f in glob.glob('src/content/stories/*.md'):
    t = io.open(f, encoding='utf-8').read()
    m = re.search(r'^sourceZh:\s*"(.*?)"', t, re.M)
    z = re.search(r'^titleZh:\s*"(.*?)"', t, re.M)
    if m and m.group(1) == '\u8c10\u94ce' and z:
        used.add(z.group(1))
print('USED (%d): %s\n' % (len(used), ' '.join(sorted(used))))

lines = open('tools/_src/xieduo.md', encoding='utf-8').read().split('\n')

TITLE = re.compile(r'^[\u4e00-\u9fff]{2,7}$')
def title_of(ln):
    s = ln.strip().strip('\u3000').strip()
    return s if (s and len(s) <= 8 and TITLE.match(s)) else None

# skip TOC: find where continuous title-run ends
head = next(i for i, ln in enumerate(lines) if '\u8c10\u94ce' in ln and '\u6c88\u8d77\u51e4' in ln)
j = head + 1
while j < len(lines):
    if not lines[j].strip():
        j += 1; continue
    if title_of(lines[j]):
        j += 1
    else:
        break
body_start = j

bt = [(title_of(lines[i]), i) for i in range(body_start, len(lines)) if title_of(lines[i])]
order = {ti: n for n, (ti, i) in enumerate(bt)}

print('%-10s %6s  %s' % ('TITLE', 'CHARS', 'OPENING'))
free = []
for n, (ti, i) in enumerate(bt):
    if ti in used:
        continue
    start = i + 1
    end = bt[n + 1][1] if n + 1 < len(bt) else len(lines)
    seg = '\n'.join(lines[start:end])
    seg = re.sub(r'^\u3000+', '', seg, flags=re.M)
    seg = re.sub(r'\n{2,}', '\n', seg).strip()
    free.append((ti, len(seg), seg[:34].replace('\n', ' ')))

free.sort(key=lambda x: -x[1])
for ti, ln_, op in free:
    print('%-10s %6d  %s' % (ti, ln_, op))
print('\nUNUSED TOTAL:', len(free))
