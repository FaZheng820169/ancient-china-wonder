"""Smoke-test the built site: verify every internal link/image resolves to a
file in dist/, and every page has a <title> and meta description."""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")

html_files = []
for dirpath, _, files in os.walk(DIST):
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(dirpath, f))

errors = []
missing_meta = []

def exists(url):
    url = url.split("#")[0].split("?")[0]
    if not url or url.startswith(("http://", "https://", "mailto:", "tel:", "//")):
        return True
    if url == "/":
        return os.path.exists(os.path.join(DIST, "index.html"))
    p = url.lstrip("/")
    return (
        os.path.exists(os.path.join(DIST, p))
        or os.path.exists(os.path.join(DIST, p, "index.html"))
        or os.path.exists(os.path.join(DIST, p + ".html"))
    )

for hf in html_files:
    rel = os.path.relpath(hf, DIST)
    with open(hf, encoding="utf-8") as fh:
        html = fh.read()
    if "<title>" not in html:
        missing_meta.append(f"{rel}: no <title>")
    if 'name="description"' not in html:
        missing_meta.append(f"{rel}: no meta description")
    for m in re.finditer(r'(?:href|src)="(/[^"]*)"', html):
        url = m.group(1)
        if url.startswith("/pagefind"):
            continue
        if not exists(url):
            errors.append(f"{rel}: broken -> {url}")

print(f"checked {len(html_files)} pages")
if missing_meta:
    print("\nMETA ISSUES:")
    print("\n".join(missing_meta[:30]))
if errors:
    print(f"\nBROKEN LINKS ({len(errors)}):")
    seen = set()
    for e in errors:
        target = e.split("-> ")[1]
        if target in seen:
            continue
        seen.add(target)
        print(" ", e)
    sys.exit(1)
print("all internal links resolve OK")
