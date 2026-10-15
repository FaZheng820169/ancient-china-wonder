# -*- coding: utf-8 -*-
"""Batch-remove the 'AI生成/WORKBUDDY' watermark from all site images via the
cloud erase tool. Resumable: completed files are recorded in tools/_wm_done.txt.

Usage: python tools/_erase_watermarks.py <token> <start> <count>
"""
import sys, subprocess, re, os, glob, shutil

PY = r'C:/Users/33529/.workbuddy/binaries/python/versions/3.13.12/python.exe'
BUDDY = r'D:/workbuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/buddy-image-processing/scripts/buddy-image-processing.py'
PROMPT = 'Remove the AI watermark text in the bottom-right corner'
MANIFEST = 'tools/_wm_done.txt'

def main():
    token, start, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    imgs = sorted(glob.glob('public/images/stories/*.jpg'))
    if os.path.isdir('public/images/worldview'):
        imgs += sorted(glob.glob('public/images/worldview/*.jpg'))
    done = set()
    if os.path.exists(MANIFEST):
        done = set(x.strip() for x in open(MANIFEST, encoding='utf-8') if x.strip())
    todo = [i for i in range(start, min(start + count, len(imgs))) if os.path.basename(imgs[i]) not in done]
    print('TOTAL %d | done %d | this batch %d' % (len(imgs), len(done), len(todo)), flush=True)
    logf = open(MANIFEST, 'a', encoding='utf-8')
    n_ok = 0
    for i in todo:
        img = imgs[i]; base = os.path.basename(img)
        cmd = [PY, BUDDY, 'image-edit', '--operation', 'erase', '--image-file',
               os.path.abspath(img), '--prompt', PROMPT, '--token', token]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=150)
        except subprocess.TimeoutExpired:
            print('TIMEOUT %d %s' % (i, base), flush=True); continue
        out = (r.stdout or '') + (r.stderr or '')
        low = out.lower()
        if 'auth_invalid' in low or 'auth_missing' in low or 'not authenticated' in low or 'invalid' in low and 'token' in low:
            print('NEED_TOKEN_AT %d %s' % (i, base), flush=True)
            logf.close(); sys.exit(2)
        m = re.search(r'"path"\s*:\s*"(.*?)"', out)
        path = m.group(1).replace('\\\\', '\\') if m else None
        if path and os.path.exists(path):
            shutil.copy(path, img)   # overwrite original in place
            os.remove(path)
            done.add(base); logf.write(base + '\n'); logf.flush()
            n_ok += 1
            print('OK %d/%d %s' % (i, len(imgs), base), flush=True)
        else:
            print('FAIL %d %s :: %s' % (i, base, out[-160:].replace('\n', ' ')), flush=True)
    logf.close()
    print('BATCH DONE ok=%d' % n_ok, flush=True)

if __name__ == '__main__':
    main()
