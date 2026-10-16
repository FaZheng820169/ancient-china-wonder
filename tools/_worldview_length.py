"""Measure prose depth of each worldview entry (body chars after frontmatter).

Thickness (inbound story refs) and depth (prose quality) are different things:
an entry can be well-written but rarely referenced. This finds entries whose
PROSE is thin, which is the real candidate for expansion work.
"""
import pathlib
import re

WV = pathlib.Path('src/content/worldview')


def split_fm(text):
    if not text.startswith('---'):
        return '', text
    end = text.find('\n---', 3)
    if end == -1:
        return '', text
    return text[3:end], text[end + 4:]


def main():
    rows = []
    for p in sorted(WV.glob('*.md')):
        text = p.read_text(encoding='utf-8')
        fm, body = split_fm(text)
        body = re.sub(r'\s+', ' ', body).strip()
        # count markdown headings as a proxy for structure
        heads = len(re.findall(r'^## ', text, re.M))
        rows.append((p.stem, len(body), heads))

    rows.sort(key=lambda r: r[1])
    total = sum(r[1] for r in rows)
    avg = total // len(rows)
    print(f"{'entry':42} {'chars':>6} {'##':>3}")
    print('-' * 56)
    for stem, n, h in rows:
        flag = '  <-- THIN PROSE' if n < avg * 0.6 else ''
        print(f"{stem:42} {n:6} {h:3}{flag}")
    print('-' * 56)
    print(f"average {avg} chars across {len(rows)} entries")


if __name__ == '__main__':
    main()
