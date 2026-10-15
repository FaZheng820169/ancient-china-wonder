# -*- coding: utf-8 -*-
"""Second pass on the 5 repainted images, with a much stricter prompt.
Originals stay safe in tools/_src/wm_before, so a bad result is revertible."""
import subprocess, re, os, sys

PY = r'C:/Users/33529/.workbuddy/binaries/python/versions/3.13.12/python.exe'
BUDDY = r'D:/workbuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/buddy-image-processing/scripts/buddy-image-processing.py'
PROMPT = ('Erase only the small semi-transparent watermark text in the extreme bottom-right '
          'corner. Do not touch any other part of the image. Keep every other pixel, colour, '
          'figure and brush stroke exactly as it is.')
TOKEN = sys.argv[1]

SLUGS = ['the-father-in-law-with-the-iron-ruler', 'the-nine-young-dragons',
         'the-wildcat-wife', 'stabbing-the-spring']

ok = 0
for slug in SLUGS:
    img = 'public/images/stories/%s.jpg' % slug
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
