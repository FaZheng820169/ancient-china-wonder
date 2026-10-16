"""Find unused Yijian Zhi tales that could fill thin/orphaned worldview entries.

Prints unused tales whose title matches a gap keyword group, so batch-26
selection can target the worldview gaps instead of going by volume order.
"""
import pathlib
import re
import sys

NAV = ('首页', '四库全书', '明清实录', '二十四史', '国学书库', '添加收藏', '搜索引擎',
       '赞助本站', '译文', '全文检索', '古籍书目', '国学精选', '历史人物', '首页 >')
VOL = re.compile(r'^夷堅志[甲乙丙丁戊]卷')
CJK = re.compile(r'^[一-鿿]{2,8}$')


def tales(txt):
    lines = [ln for ln in txt.split('\n') if ln.strip()]
    start = 0
    for i, ln in enumerate(lines):
        if VOL.match(ln):
            start = i
            break
    lines = lines[start:]
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if CJK.match(ln) and not VOL.match(ln):
            body = []
            j = i + 1
            while j < len(lines) and (len(lines[j]) >= 40 or (body and len(lines[j]) >= 20 and not CJK.match(lines[j]))):
                if CJK.match(lines[j]) or VOL.match(lines[j]):
                    break
                body.append(lines[j])
                j += 1
            if body:
                out.append((ln, ''.join(body)))
            i = j
        else:
            i += 1
    return out


def load_used():
    used = set()
    p = pathlib.Path('tools/_src/_slugs.txt')
    if p.exists():
        for ln in p.read_text(encoding='utf-8').split('\n'):
            parts = ln.split()
            if len(parts) >= 2:
                used.add(parts[1])
    return used


GROUPS = {
    'dragon': ('龙', '蛟', '螭', '虬', '鼍'),
    'sacrifice': ('祀', '祭', '牢', '血食', '牺牲', '神牲'),
    'filing-heaven': ('天曹', '天庭', '上苍', '封神', '神籍', '天帝', '玉帝', '奏'),
    'wife-still': ('鬼妻', '亡妻', '妻', '寡', '节妇'),
    'fengdu': ('酆都', '丰都'),
    'lu-dongbin': ('吕洞宾', '吕仙', '吕翁', '纯阳', '吕公'),
    'meng-po': ('孟婆', '迷魂', '忘汤'),
    'corpse': ('僵尸', '枯骨', '尸', '冢'),
    'underworld-exam': ('冥官', '冥试', '阴司', '冥录'),
    'monsters': ('妖', '怪物', '魅', '魈', '精怪'),
    'queen-mother': ('西王母', '王母'),
    'small-gods': ('土地', '城隍', '社公', '庙神', '里社'),
}


def main():
    used = load_used()
    d = pathlib.Path('tools/_src/yj')
    ids = sys.argv[1:] or sorted(p.stem for p in d.glob('*.txt'))
    hits = {g: [] for g in GROUPS}
    for vid in ids:
        p = d / f'{vid}.txt'
        if not p.exists():
            continue
        for t, b in tales(p.read_text(encoding='utf-8')):
            if t in used:
                continue
            for g, kws in GROUPS.items():
                if any(k in t for k in kws):
                    hits[g].append((t, vid, len(b)))
                    break
    for g in GROUPS:
        lst = hits[g]
        print('=' * 60)
        print(f'{g}  ({len(lst)} candidates)')
        for t, vid, n in lst[:40]:
            print(f'  {t}\t[{vid}]\t{n}')


if __name__ == '__main__':
    main()
