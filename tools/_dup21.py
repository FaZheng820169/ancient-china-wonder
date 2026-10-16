# -*- coding: utf-8 -*-
"""Check batch-21 candidate titles against everything already published."""
import glob
import io
import os
import re

CAND = ['姚端恪公遇剑仙', '鬼宝塔', '棺盖飞', '油瓶烹鬼', '无门国', '吴髯',
        '鹤静先生', '尸香二则', '裘文达公为水神', '捧头司马', '折叠仙',
        '阎王升殿先吞铁丸']
TITLES = {
    '姚端恪公遇剑仙': 'The Swordsman Who Came for the Judge',
    '鬼宝塔': 'The Pagoda of Ghosts',
    '棺盖飞': 'The Coffin Lid That Flew',
    '油瓶烹鬼': 'Boiling the Ghost in Oil',
    '无门国': 'The Country Without Doors',
    '吴髯': 'The Ghost Who Followed Him Through Three Lives',
    '鹤静先生': 'Master Crane Stillness',
    '尸香二则': 'Two Tales of Corpse Fragrance',
    '裘文达公为水神': 'Lord Qiu Becomes a Water God',
    '捧头司马': 'The Major Who Carried His Head',
    '折叠仙': 'The Folding Immortal',
    '阎王升殿先吞铁丸': 'The Iron Pill of the King of Hell',
}

pub_zh, pub_en = {}, {}
for f in glob.glob('src/content/stories/*.md'):
    t = io.open(f, encoding='utf-8').read()
    m = re.search(r'^titleZh:\s*(.+?)\s*$', t, re.M)
    if m:
        pub_zh[m.group(1).strip('"')] = os.path.basename(f)[:-3]
    m = re.search(r'^title:\s*(.+?)\s*$', t, re.M)
    if m:
        pub_en[m.group(1).strip('"').lower()] = os.path.basename(f)[:-3]

for zh in CAND:
    a = pub_zh.get(zh, 'ok')
    b = pub_en.get(TITLES[zh].lower(), 'ok')
    print('%-16s zh=%-28s en=%s' % (zh, a, b))
