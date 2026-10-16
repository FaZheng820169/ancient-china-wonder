# -*- coding: utf-8 -*-
"""Audit the 'Xieduo juan N' claims in story frontmatter against the table of contents."""
import glob
import os
import re

# Juan -> titles, transcribed from the table of contents in tools/_src/xieduo.md
TOC = {
    1: ['狐媚', '虎痴', '鸡谈', '獭祭', '蚁封', '龟鉴', '兔孕', '雉煤'],
    2: ['屏角相郎', '笔头减寿', '讨猫檄', '祭蠹文', '隔牖谈诗', '垂帘论曲', '考牌逐腐鬼', '妙画代良医'],
    3: ['娇娃皈佛', '穷士扶乩', '老面鬼', '遮眼神', '烧录成名', '读书贻笑', '镜戏', '帖嘲', '一钱落职', '两指题旌'],
    4: ['酒戒', '色戒', '财戒', '气戒', '侠妓教忠', '雏伶尽孝', '丐妇殉节', '营卒守义', '桃夭村', '荆棘里'],
    5: ['恶饯', '奇婚', '泄气生员', '换形乞丐', '菜花三娘子', '草鞋四相公', '讼师说讼', '名妓沽名', '泥傀儡', '石赑屃'],
    6: ['上清宫除妖', '森罗殿点鬼', '苏三', '葛九', '奇女雪怨', '达士报恩', '梦中梦', '身外身', '香粉地狱', '面目轮回', '能诗贼', '识字犬'],
    7: ['有根女', '无气官', '鬼妇持家', '鄙夫训世', '虫书', '兽谱', '黑衣太仆', '巾帼幕宾', '鲛奴', '犬婢'],
    8: ['棺中鬼手', '镜里人心', '孟婆庄', '十姨庙', '车前数典', '骡后谈书', '死嫁', '生吊', '术士驱蝇', '壮夫缚虎'],
    9: ['嘲吴蒙', '赛齐妇', '村姬毒舌', '醮妇冰心', '地师身后劫', '节母死时箴', '顶上圆光', '掌中秘戏', '眼前杀报', '脑后淫魔'],
    10: ['道人神相', '和尚婆心', '蟪蛄郡', '蜣螂城', '鬼嫖', '神赌', '梦里家园', '命中姻眷', '臭桂', '祥鸦'],
    11: ['老僧辨奸', '青衣捕盗', '正士驱邪', '恶客除淫', '芙蓉城香姑子', '扫帚村钝秀才', '三杖惩奴', '片言保赤', '盗师', '鬼婿', '书神作祟', '病鬼延医'],
    12: ['南部', '北里', '贫儿学馅', '才士惩骄', '卜将军庙灵签', '况太守祠赝梦', '怕婆县令', '捣鬼夫人', '吕仙宝筏', '大士慈航', '奎垣真像'],
}
BY_TITLE = {}
for j, ts in TOC.items():
    for t in ts:
        BY_TITLE[t] = j

CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7,
      '八': 8, '九': 9, '十': 10, '十一': 11, '十二': 12}

for p in sorted(glob.glob('src/content/stories/*.md')):
    txt = open(p, encoding='utf-8').read()
    fm = txt.split('---')[1]
    note = re.search(r'^originalNote: "(.*)"$', fm, re.M)
    tz = re.search(r'^titleZh: "(.*)"$', fm, re.M)
    if not note or 'Xieduo' not in note.group(1):
        continue
    if not tz:
        continue
    title = tz.group(1)
    claim = re.search(r'juan ([0-9]+|[一二三四五六七八九十]+)', note.group(1))
    claim_n = None
    if claim:
        c = claim.group(1)
        claim_n = int(c) if c.isdigit() else CN.get(c)
    true_n = BY_TITLE.get(title)
    if true_n is None:
        # try the first two characters
        for t, j in BY_TITLE.items():
            if t[:2] == title[:2]:
                true_n = j
                break
    flag = 'OK' if claim_n == true_n else 'CHECK'
    print('%-42s %-8s claim=%-4s toc=%-4s %s'
          % (os.path.basename(p)[:-3], title, claim_n, true_n, flag))
