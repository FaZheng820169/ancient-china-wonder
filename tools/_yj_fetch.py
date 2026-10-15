"""Fetch Yijian Zhi (夷坚志) volumes from guoxuedashi and cache plain text.

Usage: python tools/_yj_fetch.py 5587 5588 5589
Caches to tools/_src/yj/<id>.txt
"""
import re
import subprocess
import sys
import pathlib

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"


def fetch(vid: str) -> str:
    url = f"https://www.guoxuedashi.com/sikuquanshu/fanti/510p/{vid}.html"
    out = pathlib.Path(f"_yj_{vid}.html")
    subprocess.run(
        ["curl", "-s", "-m", "40", "-A", UA, url, "-o", str(out)],
        check=True,
    )
    raw = out.read_text("utf-8", errors="ignore")
    # keep only the body area
    m = re.search(r'(<div[^>]*class="[^"]*book-content[^"]*"[^>]*>)(.*?)(</div>)', raw, re.S)
    body = m.group(2) if m else raw
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.S)
    lines = [re.sub(r"<[^>]+>", "", ln).strip() for ln in body.split("\n")]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines)


if __name__ == "__main__":
    d = pathlib.Path("tools/_src/yj")
    d.mkdir(parents=True, exist_ok=True)
    for vid in sys.argv[1:]:
        txt = fetch(vid)
        (d / f"{vid}.txt").write_text(txt, encoding="utf-8")
        print(vid, len(txt), "chars")
