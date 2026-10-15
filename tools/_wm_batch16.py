# -*- coding: utf-8 -*-
"""Erase the platform watermark from the 12 batch-15 images only."""
import subprocess, re, os, sys

PY = r'C:/Users/33529/.workbuddy/binaries/python/versions/3.13.12/python.exe'
BUDDY = r'D:/workbuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/buddy-image-processing/scripts/buddy-image-processing.py'
PROMPT = 'Remove the AI watermark text in the bottom-right corner'
TOKEN = sys.argv[1]

SLUGS = ['the-woman-with-the-cat', 'shaggy-head', 'the-one-legged-ghost', 'the-taoist-who-came-to-supper', 'the-hundred-meat-pies', 'one-pear-a-day', 'the-three-warriors', 'the-lay-brother-who-became-a-pig', 'the-clerk-who-died-twice', 'the-daughter-of-zhang-ten-thousand', 'the-wet-nurses-relics', 'the-candle-flowers']

ok = 0
for slug in SLUGS:
    img = 'public/images/stories/%s.jpg' % slug
    if not os.path.exists(img):
        print('MISSING', slug, flush=True); continue
    cmd = [PY, BUDDY, 'image-edit', '--operation', 'erase', '--image-file',
           os.path.abspath(img), '--prompt', PROMPT, '--token', TOKEN]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=170)
    except subprocess.TimeoutExpired:
        print('TIMEOUT', slug, flush=True); continue
    out = (r.stdout or '') + (r.stderr or '')
    m = re.search(r'"path"\s*:\s*"(.*?)"', out)
    path = m.group(1).replace('\\\\', '\\') if m else None
    if path and os.path.exists(path):
        os.replace(path, img)
        print('OK %-38s %d KB' % (slug, os.path.getsize(img) // 1024), flush=True)
        ok += 1
    else:
        print('FAIL %-36s %s' % (slug, (out[:160].replace('\n', ' ') or 'rc=%s' % r.returncode)), flush=True)
print('DONE %d/%d' % (ok, len(SLUGS)))
