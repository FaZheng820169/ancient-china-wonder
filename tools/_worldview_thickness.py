"""Worldview thickness: how many stories (and worldview cross-links) support each entry.

For each worldview entry, counts:
  - story refs: items in its `related` that are NOT other worldview ids
  - wv refs:    items in its `related` that ARE other worldview ids
Also prints orphaned (0 story refs) and thin (<3) entries.
"""
import pathlib
import re

WV_DIR = pathlib.Path('src/content/worldview')
ST_DIR = pathlib.Path('src/content/stories')

# collect all worldview ids
wv_ids = {p.stem for p in WV_DIR.glob('*.md')}


def parse_related(text):
    """Extract the `related:` YAML list from frontmatter."""
    m = re.search(r'related:\s*\n((?:\s*-\s+.+\n)+)', text)
    if not m:
        return []
    return [ln.strip()[2:].strip().strip('"').strip("'")
            for ln in m.group(1).split('\n') if ln.strip().startswith('-')]


def main():
    rows = []
    for p in sorted(WV_DIR.glob('*.md')):
        text = p.read_text(encoding='utf-8')
        rel = parse_related(text)
        story_refs = [r for r in rel if r not in wv_ids]
        wv_refs = [r for r in rel if r in wv_ids]
        rows.append((p.stem, len(story_refs), len(wv_refs), story_refs))

    rows.sort(key=lambda r: (r[1], r[2]))
    print(f"{'entry':42} story  wv")
    print('-' * 56)
    for stem, s, w, _ in rows:
        print(f"{stem:42} {s:5}  {w:3}")

    print('\nORPHANED (0 story refs):')
    for stem, s, w, _ in rows:
        if s == 0:
            print('  -', stem)

    print('\nTHIN (1-2 story refs):')
    for stem, s, w, _ in rows:
        if 1 <= s <= 2:
            print('  -', stem, f'({s})')

    print('\nTHICKEST (>=8):')
    for stem, s, w, _ in rows:
        if s >= 8:
            print('  -', stem, f'({s})')


if __name__ == '__main__':
    main()
