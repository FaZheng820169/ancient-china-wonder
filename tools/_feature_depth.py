"""Audit features (long-form essays): prose depth, section count, frontmatter completeness.

Mirrors _worldview_length.py for the features collection. Flags entries whose
prose is well below the collection average, or missing required frontmatter.
"""
import pathlib
import re

FT = pathlib.Path('src/content/features')


def split_fm(text):
    if not text.startswith('---'):
        return '', text
    end = text.find('\n---', 3)
    if end == -1:
        return '', text
    return text[3:end], text[end + 4:]


def main():
    rows = []
    for p in sorted(FT.glob('*.md')):
        text = p.read_text(encoding='utf-8')
        fm, body = split_fm(text)
        body = re.sub(r'\s+', ' ', body).strip()
        heads = len(re.findall(r'^## ', text, re.M))
        has_excerpt = 'excerpt:' in fm
        has_image = 'image:' in fm
        rows.append((p.stem, len(body), heads, has_excerpt, has_image))

    rows.sort(key=lambda r: r[1])
    total = sum(r[1] for r in rows)
    avg = total // len(rows) if rows else 0
    print(f"{'feature':38} {'chars':>6} {'##':>3} {'exc':>4} {'img':>4}")
    print('-' * 60)
    for stem, n, h, ex, im in rows:
        flag = '  <-- THIN' if n < avg * 0.6 else ''
        print(f"{stem:38} {n:6} {h:3} {str(ex):>4} {str(im):>4}{flag}")
    print('-' * 60)
    print(f"average {avg} chars across {len(rows)} features")
    print("missing excerpt:", [s for s, _, _, e, _ in rows if not e])
    print("missing image  :", [s for s, _, _, _, i in rows if not i])


if __name__ == '__main__':
    main()
