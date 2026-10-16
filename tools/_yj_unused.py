"""List Yijian Zhi tales in cached volumes that are NOT yet published.

Compares extracted tale titles against tools/_src/_slugs.txt (titleZh column).

Usage: python tools/_yj_unused.py [ids...]   (default: all cached)
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
                # format: slug  titleZh  titleEn
                used.add(parts[1])
    return used


if __name__ == '__main__':
    used = load_used()
    d = pathlib.Path('tools/_src/yj')
    ids = sys.argv[1:] or sorted(p.stem for p in d.glob('*.txt'))
    total_unused = 0
    for vid in ids:
        p = d / f'{vid}.txt'
        if not p.exists():
            print('!! missing', vid)
            continue
        ts = tales(p.read_text(encoding='utf-8'))
        unused = [(t, b) for t, b in ts if t not in used]
        if unused:
            print('=' * 60)
            print(vid, len(ts), 'tales,', len(unused), 'UNUSED')
            for t, b in unused:
                print(f'  {t}\t{len(b)}')
            total_unused += len(unused)
    print('=' * 60)
    print('TOTAL UNUSED:', total_unused)
