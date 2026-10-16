"""Body-aware gap scan: find unused Yijian Zhi tales whose BODY mentions a
light/thin worldview concept, so batch-26 can target those entries.

Title-only matching misses concepts that live in the prose (dragons, Kunlun,
Fengdu, hun/po, Meng Po). This scans bodies too.
"""
import pathlib
import re
import sys

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


# group -> (worldview entry to feed, keyword tuple)
GROUPS = {
    'queen-mother': ('西王母', '王母'),
    'kunlun': ('崑崙', '昆仑'),
    'fengdu': ('酆都', '丰都', '冥府', '阴府', '地下'),
    'hun-po': ('魂', '魄'),
    'meng-po': ('孟婆',),
    'dragons': ('龙', '蛟', '螭'),
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
                if any(k in b for k in kws):
                    hits[g].append((t, vid, len(b)))
                    break
    for g in GROUPS:
        lst = hits[g]
        print('=' * 60)
        print(f'{g}  ({len(lst)} unused tales mention it)')
        for t, vid, n in lst[:18]:
            print(f'  {t}\t[{vid}]\t{n}')


if __name__ == '__main__':
    main()
