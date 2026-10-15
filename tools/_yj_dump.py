"""Dump full text of named Yijian Zhi tales.

Usage: python tools/_yj_dump.py 建康太和古墓 三趙失舟 ...
"""
import sys

sys.path.insert(0, 'tools')
from _yj_pick import tales  # noqa: E402
import pathlib  # noqa: E402

want = sys.argv[1:]
d = pathlib.Path('tools/_src/yj')
for p in sorted(d.glob('*.txt')):
    for t, b in tales(p.read_text(encoding='utf-8')):
        if t in want:
            print('#' * 70)
            print(f'[{p.stem}] {t}  ({len(b)} chars)')
            print(b)
            print()
