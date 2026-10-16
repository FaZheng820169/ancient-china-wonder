#!/usr/bin/env python3
"""Dedupe batch-22 candidates against every published story (titleZh + slug)."""
import re, glob

CAND = [
    ('the-ghost-masters-of-guangxi', '广西鬼师'),
    ('the-scale-of-merit', '神秤'),
    ('yan-hui-judges-for-his-master', '颜渊为先师判狱'),
    ('the-gods-know-no-textual-criticism', '神仙不解考据'),
    ('the-pavilion-of-the-great-turtle', '鼋壳亭'),
    ('the-tiger-who-carried-wenchangs-head', '虎衔文昌头'),
    ('the-chicken-footed-people', '鸡脚人'),
    ('the-rite-of-the-whole-bones', '道家有全骨法'),
    ('the-wronged-ghosts-mistook-their-man', '冤鬼错认'),
    ('the-planchette-showed-the-questions', '乩仙示题'),
    ('the-foxs-elixir', '狐丹'),
    ('thunder-strikes-the-pickpockets', '雷打扒手'),
]

slugs = set()
zh = set()
for p in glob.glob('src/content/stories/*.md'):
    slugs.add(p.split('\\')[-1][:-3])
    txt = open(p, encoding='utf-8').read()
    m = re.search(r'^titleZh:\s*"?([^"\n]+)"?', txt, re.M)
    if m:
        zh.add(m.group(1).strip())

bad = 0
for slug, t in CAND:
    s_ok = slug not in slugs
    z_ok = t not in zh
    print('%-40s slug=%s zh=%s' % (slug, 'ok' if s_ok else 'COLLIDE', 'ok' if z_ok else 'COLLIDE'))
    if not (s_ok and z_ok):
        bad += 1
print('collisions:', bad)
