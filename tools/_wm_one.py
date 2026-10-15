# -*- coding: utf-8 -*-
import subprocess, re, os, sys
PY = r'C:/Users/33529/.workbuddy/binaries/python/versions/3.13.12/python.exe'
BUDDY = r'D:/workbuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/buddy-image-processing/scripts/buddy-image-processing.py'
img = 'public/images/stories/%s.jpg' % sys.argv[1]
token = sys.argv[2]
cmd = [PY, BUDDY, 'image-edit', '--operation', 'erase', '--image-file',
       os.path.abspath(img), '--prompt', 'Remove the AI watermark text in the bottom-right corner',
       '--token', token]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=170)
out = (r.stdout or '') + (r.stderr or '')
m = re.search(r'"path"\s*:\s*"(.*?)"', out)
p = m.group(1).replace('\\\\', '\\') if m else None
if p and os.path.exists(p):
    os.replace(p, img); print('OK', img, os.path.getsize(img)//1024, 'KB')
else:
    print('FAIL', out[:200].replace('\n', ' '))
