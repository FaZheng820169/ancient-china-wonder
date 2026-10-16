# -*- coding: utf-8 -*-
"""Fetch Yuan Mei's Zibuyu volumes from readonlylink/readonlylink-books via the
GitHub contents API (raw.githubusercontent is unreliable from this machine)."""
import base64
import io
import json
import os
import subprocess
import sys
import urllib.parse

OUT = 'tools/_src/zby'
API = 'https://api.github.com/repos/readonlylink/readonlylink-books/contents/'


def fetch(path):
    url = API + urllib.parse.quote(path, safe='/')
    r = subprocess.run(
        ['curl', '-s', '-H', 'Accept: application/vnd.github+json', url],
        capture_output=True)
    if r.returncode != 0:
        return None
    try:
        j = json.loads(r.stdout.decode('utf-8'))
    except Exception:
        return None
    if 'content' not in j:
        return None
    return base64.b64decode(j['content']).decode('utf-8')


os.makedirs(OUT, exist_ok=True)
for v in sys.argv[1:]:
    path = '袁枚/子不语/src/%s.md' % v
    txt = fetch(path)
    if txt is None:
        print('FAIL', v, flush=True)
        continue
    p = os.path.join(OUT, '%s.md' % v)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(txt)
    print('%s  %d chars' % (v, len(txt)), flush=True)
