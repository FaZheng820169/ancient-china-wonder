"""List candidate tales in cached Yijian Zhi volumes.

Usage: python tools/_yj_pick.py [ids...]   (default: all cached)
"""
import pathlib
import re
import sys

NAV = ('首页', '四库全书', '明清实录', '二十四史', '国学书库', '添加收藏', '搜索引擎',
       '赞助本站', '译文', '全文检索', '古籍书目', '国学精选', '历史人物', '首页 >')

VOL = re.compile(r'^夷堅志[甲乙丙丁戊]卷')
CJK = re.compile(r'^[一-鿿]{2,8}$')


def tales(txt: str):
    lines = [ln for ln in txt.split('\n') if ln.strip()]
    # drop navigation header: start at the first volume header line
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


if __name__ == '__main__':
    d = pathlib.Path('tools/_src/yj')
    ids = sys.argv[1:] or sorted(p.stem for p in d.glob('*.txt'))
    for vid in ids:
        p = d / f'{vid}.txt'
        if not p.exists():
            print('!! missing', vid)
            continue
        ts = tales(p.read_text(encoding='utf-8'))
        print('=' * 60)
        print(vid, len(ts), 'tales')
        for t, b in ts:
            print(f'  {t}\t{len(b)}')
