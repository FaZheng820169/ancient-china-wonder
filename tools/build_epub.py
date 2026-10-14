"""Build EPUB ebooks from the Liaozhai translations in src/content/stories.

Produces:
  downloads/strange-tales-liaozhai.epub       -- the paid product (12 tales)
  public/downloads/liaozhai-sample.epub       -- free 3-tale sample
  public/images/books/cover.jpg               -- cover art (Pillow-drawn)

The EPUB is assembled by hand (zipfile + XML) so the project keeps zero
document-generation dependencies.
"""

import os
import re
import zipfile
from datetime import date
from html import escape

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORY_DIR = os.path.join(ROOT, "src", "content", "stories")
DOWNLOADS = os.path.join(ROOT, "downloads")
PUBLIC_DL = os.path.join(ROOT, "public", "downloads")
COVER_DIR = os.path.join(ROOT, "public", "images", "books")

PAPER = "#F7F5F0"
INK = "#1A1A1A"
BODY = "#3D3D3D"
MUTED = "#707070"
CINNABAR = "#A62C21"
PINE = "#2D5016"

FULL_SLUGS = [
    "nie-xiaoqian",
    "huapi",
    "laoshan",
    "yingning",
    "wang-liulang",
    "xiangyu",
    "cuizhi",
    "xi-fangping",
    "kao-chenghuang",
    "a-bao",
    "jiaona",
    "lu-pan",
]
SAMPLE_SLUGS = ["nie-xiaoqian", "huapi", "wang-liulang"]


# --------------------------------------------------------------------------
# frontmatter / markdown parsing
# --------------------------------------------------------------------------

def split_frontmatter(raw: str):
    if not raw.startswith("---"):
        return {}, raw
    parts = raw.split("\n---", 1)
    fm_text = parts[0].split("---", 1)[1]
    body = parts[1] if len(parts) > 1 else ""
    body = body.split("\n", 1)[1] if body.startswith("\n") else body
    return fm_text, body


def parse_frontmatter(fm_text: str):
    data = {"title": "", "titleZh": "", "author": "Unknown", "source": "", "era": "", "excerpt": ""}
    notes = []
    cur = None
    for line in fm_text.split("\n"):
        m = re.match(r'^(-?)\s*(term|text):\s*(.*)$', line)
        if m:
            if m.group(2) == "term":
                cur = {"term": unquote(m.group(3)), "text": ""}
                notes.append(cur)
            elif cur is not None:
                cur["text"] = unquote(m.group(3))
            continue
        m = re.match(r'^([a-zA-Z]+):\s*(.*)$', line)
        if m and m.group(1) in data:
            data[m.group(1)] = unquote(m.group(2))
    data["notes"] = notes
    return data


def unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    return s


def md_inline(s: str) -> str:
    s = escape(s)
    s = re.sub(r'\[([^\]]+)\]\((/[^)]+)\)', r'\1', s)  # drop internal links
    s = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', s)
    return s


def md_to_html(md: str) -> str:
    out = []
    for block in re.split(r'\n\s*\n', md.strip()):
        block = block.strip()
        if not block:
            continue
        if block.startswith("### "):
            out.append(f"<h3>{md_inline(block[4:])}</h3>")
        elif block.startswith("## "):
            out.append(f"<h2>{md_inline(block[3:])}</h2>")
        elif block.startswith("# "):
            out.append(f"<h2>{md_inline(block[2:])}</h2>")
        elif block.startswith("> "):
            out.append(f"<blockquote><p>{md_inline(block[2:])}</p></blockquote>")
        elif re.match(r'^[-*] ', block, re.M):
            items = "".join(f"<li>{md_inline(l[2:])}</li>" for l in block.split("\n") if re.match(r'^[-*] ', l))
            out.append(f"<ul>{items}</ul>")
        else:
            out.append(f"<p>{md_inline(block)}</p>")
    return "\n".join(out)


def load_story(slug: str):
    path = os.path.join(STORY_DIR, slug + ".md")
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    fm_text, body = split_frontmatter(raw)
    data = parse_frontmatter(fm_text)
    data["slug"] = slug
    data["html"] = md_to_html(body)
    return data


# --------------------------------------------------------------------------
# cover art
# --------------------------------------------------------------------------

def find_font(names, size):
    base = r"C:\Windows\Fonts"
    for n in names:
        p = os.path.join(base, n)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def make_cover(path: str):
    W, H = 1000, 1500
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # border rules
    d.rectangle([46, 46, W - 47, H - 47], outline=CINNABAR, width=3)
    d.rectangle([62, 62, W - 63, H - 63], outline="#E8E4DB", width=2)

    # ink mark: layered mountains, echoing the site seal
    d.polygon([(500, 660), (700, 1050), (300, 1050)], fill=CINNABAR)
    d.polygon([(500, 790), (640, 1020), (360, 1020)], fill=PINE)
    d.line([(150, 1090), (850, 1090)], fill="#E8E4DB", width=2)

    f_kicker = find_font(["seguisb.ttf", "segoeui.ttf", "arial.ttf"], 30)
    f_title = find_font(["georgiab.ttf", "georgia.ttf", "timesbd.ttf"], 78)
    f_sub = find_font(["georgia.ttf", "times.ttf", "arial.ttf"], 40)
    f_han = find_font(["msyh.ttc", "msyhbd.ttc", "simsun.ttc"], 44)
    f_small = find_font(["georgia.ttf", "times.ttf", "arial.ttf"], 32)

    def center(text, y, font, fill):
        w = d.textlength(text, font=font)
        d.text(((W - w) / 2, y), text, font=font, fill=fill)

    center("A N C I E N T   C H I N A   W O N D E R", 132, f_kicker, CINNABAR)
    center("STRANGE TALES", 260, f_title, INK)
    center("FROM A CHINESE", 352, f_title, INK)
    center("STUDIO", 444, f_title, INK)
    center("聊齋志異", 560, f_han, MUTED)
    center("Twelve translations from", 1180, f_sub, BODY)
    center("Liaozhai Zhiyi by Pu Songling", 1240, f_sub, BODY)
    center("with cultural notes", 1380, f_small, MUTED)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "JPEG", quality=88, optimize=True)
    return path


# --------------------------------------------------------------------------
# epub assembly
# --------------------------------------------------------------------------

STYLE = """
body { margin: 5% 7%; font-family: Georgia, 'Times New Roman', serif; color: #3D3D3D; line-height: 1.7; }
h1 { font-size: 1.7em; color: #1A1A1A; margin: 0 0 .1em; text-align: center; }
h2 { font-size: 1.25em; color: #1A1A1A; margin: 2em 0 .6em; }
h3 { font-size: 1.05em; color: #1A1A1A; margin: 1.6em 0 .4em; }
p { margin: 0 0 1em; text-align: justify; }
.title-zh { text-align: center; font-size: 1.1em; letter-spacing: .18em; color: #707070; margin: 0 0 1.6em; }
.kicker { text-align: center; font-size: .78em; letter-spacing: .18em; color: #A62C21; margin: 0 0 2em; }
.epigraph { font-style: italic; color: #707070; border-left: 2px solid #A62C21; padding-left: 1em; margin: 0 0 2em; }
blockquote { border-left: 2px solid #A62C21; padding-left: 1em; font-style: italic; color: #1A1A1A; }
.notes { border-top: 1px solid #E8E4DB; margin-top: 2.5em; padding-top: 1em; }
.notes h3 { color: #A62C21; margin: 1.2em 0 .2em; }
.notes p { font-size: .95em; }
.source { font-size: .85em; color: #707070; border-top: 1px solid #E8E4DB; margin-top: 2.5em; padding-top: 1em; }
.cover-title { text-align: center; }
"""


def chapter_html(story, include_notes=True):
    parts = [
        '<p class="kicker">LIAOZHAI ZHIYI · 聊齋志異</p>',
        f'<h1>{escape(story["title"])}</h1>',
        f'<p class="title-zh">{escape(story["titleZh"])}</p>',
        f'<p class="epigraph">{escape(story["excerpt"])}</p>',
        story["html"],
    ]
    if include_notes and story["notes"]:
        parts.append('<div class="notes"><h3>CULTURAL NOTES</h3>')
        for n in story["notes"]:
            parts.append(f'<h3>{escape(n["term"])}</h3><p>{escape(n["text"])}</p>')
        parts.append("</div>")
    parts.append(
        f'<p class="source">From <em>{escape(story["source"])}</em> ({escape(story["titleZh"])}), '
        f'by {escape(story["author"])}, {escape(story["era"])}. The original text is in the public '
        f'domain; this English rendering and the accompanying notes are original work.</p>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">'
        '<head><meta charset="utf-8" />'
        f"<title>{escape(story['title'])}</title>"
        f'<link rel="stylesheet" type="text/css" href="style.css" /></head>'
        f'<body>{"".join(parts)}</body></html>'
    )


def build_epub(out_path, stories, title, subtitle, cover_path, intro_html):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    uid = "urn:uuid:acw-liaozhai-" + ("full" if len(stories) > 4 else "sample")
    today = date.today().isoformat()

    manifest = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '<item id="css" href="style.css" media-type="text/css"/>',
        '<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>',
        '<item id="coverimg" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>',
        '<item id="intro" href="intro.xhtml" media-type="application/xhtml+xml"/>',
    ]
    spine = ['<itemref idref="cover"/>', '<itemref idref="intro"/>']
    for i, s in enumerate(stories, 1):
        cid = f"ch{i:02d}"
        manifest.append(f'<item id="{cid}" href="{cid}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{cid}"/>')

    nav_li = ['<li><a href="intro.xhtml">Introduction</a></li>']
    nav_li += [f'<li><a href="ch{i:02d}.xhtml">{escape(s["title"])}</a></li>' for i, s in enumerate(stories, 1)]

    ncx_points = ""
    for i, s in enumerate(stories, 1):
        ncx_points += (
            f'<navPoint id="np{i + 1}" playOrder="{i + 1}">'
            f'<navLabel><text>{escape(s["title"])}</text></navLabel>'
            f'<content src="ch{i:02d}.xhtml"/></navPoint>'
        )

    opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">{uid}</dc:identifier>
    <dc:title>{escape(title)}</dc:title>
    <dc:creator opf:role="aut">Pu Songling</dc:creator>
    <dc:creator opf:role="trl">Ancient China Wonder</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>Ancient China Wonder</dc:publisher>
    <dc:date>{today}</dc:date>
    <dc:rights>Source texts in the public domain. Translations and notes (c) Ancient China Wonder.</dc:rights>
    <dc:description>{escape(subtitle)}</dc:description>
    <meta property="dcterms:modified">{today}T00:00:00Z</meta>
  </metadata>
  <manifest>{"".join(manifest)}</manifest>
  <spine toc="ncx">{"".join(spine)}</spine>
</package>"""

    cover_xhtml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><meta charset="utf-8"/>
<title>Cover</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body class="cover-title"><div><img src="images/cover.jpg" alt="Cover" /></div></body></html>"""

    intro_xhtml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>'
        '<html xmlns="http://www.w3.org/1999/xhtml"><head><meta charset="utf-8"/>'
        f"<title>{escape(title)}</title>"
        '<link rel="stylesheet" type="text/css" href="style.css"/></head><body>'
        f'<h1>{escape(title)}</h1><p class="title-zh">聊齋志異</p>{intro_html}</body></html>'
    )

    nav_xhtml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><meta charset="utf-8"/><title>Contents</title></head>
<body><nav epub:type="toc" id="toc"><h1>Contents</h1><ol>{"".join(nav_li)}</ol></nav></body></html>"""

    ncx = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head><meta name="dtb:uid" content="{uid}"/></head>
  <docTitle><text>{escape(title)}</text></docTitle>
  <navMap>
    <navPoint id="np1" playOrder="1"><navLabel><text>Introduction</text></navLabel><content src="intro.xhtml"/></navPoint>
    {ncx_points}
  </navMap>
</ncx>"""

    container = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>"""

    with zipfile.ZipFile(out_path, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav_xhtml, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/toc.ncx", ncx, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", STYLE, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/cover.xhtml", cover_xhtml, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/intro.xhtml", intro_xhtml, compress_type=zipfile.ZIP_DEFLATED)
        z.write(cover_path, "OEBPS/images/cover.jpg", compress_type=zipfile.ZIP_STORED)
        for i, s in enumerate(stories, 1):
            z.writestr(f"OEBPS/ch{i:02d}.xhtml", chapter_html(s), compress_type=zipfile.ZIP_DEFLATED)

    return out_path


INTRO = """
<p class="kicker">A Reader's Note</p>
<p>Pu Songling (1640&ndash;1715) spent most of his life failing examinations in a small
Shandong town, and much of the rest of it collecting stories. The result,
<em>Liaozhai Zhiyi</em> &mdash; roughly four hundred and ninety tales &mdash; is the summit of the
Chinese zhiguai tradition: ghost stories, fox-wives, lawsuits in the underworld, satires of
the examination system, and a handful of love stories that have no equal anywhere in the
seventeenth century.</p>
<p>The twelve tales in this volume were translated directly from the classical Chinese.
They were not adapted from any existing English version; every rendering here is original
work, made from the public-domain text and from nothing else. Where a tale has been
condensed, the condensation is noted at the end of the chapter.</p>
<p>Each chapter also carries a short set of <em>cultural notes</em>. They are the reason this
volume exists in this form. A seventeenth-century Chinese reader brought a great deal to a
page like this &mdash; the examination system, the City God, the lantern festival, the shape of a
household &mdash; and a modern reader cannot be expected to supply it. The notes are there to
replace what the original assumed.</p>
<p>If you want more, the full library &mdash; forty tales, an encyclopedia of the shared
universe, and long essays on the fox spirit, the underworld and the swordsmen &mdash; is at
ancientchinawonder.com.</p>
"""

INTRO_SAMPLE = """
<p class="kicker">A Free Sample</p>
<p>Three tales from <em>Strange Tales from a Chinese Studio</em>: a ghost who refuses to kill,
a demon in a painted skin, and a drowned man promoted to be a god.</p>
<p>Each was translated directly from Pu Songling's classical Chinese, with notes on the
world the story assumes. The complete volume contains twelve tales and is available from
ancientchinawonder.com/books.</p>
"""


def main():
    cover = make_cover(os.path.join(COVER_DIR, "cover.jpg"))
    full = [load_story(s) for s in FULL_SLUGS]
    sample = [load_story(s) for s in SAMPLE_SLUGS]

    os.makedirs(DOWNLOADS, exist_ok=True)
    os.makedirs(PUBLIC_DL, exist_ok=True)

    p1 = build_epub(
        os.path.join(DOWNLOADS, "strange-tales-liaozhai.epub"),
        full,
        "Strange Tales from a Chinese Studio",
        "Twelve translations from Liaozhai Zhiyi by Pu Songling, with cultural notes.",
        cover,
        INTRO,
    )
    p2 = build_epub(
        os.path.join(PUBLIC_DL, "liaozhai-sample.epub"),
        sample,
        "Strange Tales from a Chinese Studio — Sample",
        "Three free tales from Pu Songling's Liaozhai Zhiyi.",
        cover,
        INTRO_SAMPLE,
    )
    for p in (p1, p2, cover):
        print(f"{p}  {os.path.getsize(p)//1024} KB")


if __name__ == "__main__":
    main()
