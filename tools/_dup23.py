import pathlib, sys
cands = [
 ('the-thunder-god-answers-a-memo','雷州雷神'),
 ('the-debt-the-temple-god-collected','資聖土地'),
 ('the-seven-ladies','七姑子'),
 ('the-land-god-of-jianju-abbey','簡寂觀土地'),
 ('lu-dongbin-tests-a-hermit','陳待制'),
 ('the-goddess-who-bought-the-woods','林夫人廟'),
 ('listening-for-the-omen','婆惜響卜'),
 ('the-boys-who-chased-butterflies','李氏二童'),
 ('axu-in-the-underworld','阿徐入冥'),
 ('cai-zhengniang','蔡箏娘'),
 ('the-bronze-bell-of-fuzhou','復州銅磬'),
 ('qiuding-in-the-underworld','丘鼎入冥'),
]
zh = {}
for p in pathlib.Path('src/content/stories').glob('*.md'):
    fm = p.read_text(encoding='utf-8').split('---')[1]
    t = z = ''
    for line in fm.split('\n'):
        if line.startswith('title:'): t = line.split(':',1)[1].strip().strip('"')
        if line.startswith('titleZh:'): z = line.split(':',1)[1].strip().strip('"')
    zh[z] = p.stem
dup = 0
for slug, z in cands:
    if pathlib.Path(f'src/content/stories/{slug}.md').exists():
        print('DUP SLUG', slug); dup += 1
    if z in zh:
        print('DUP ZH  ', z, '->', zh[z]); dup += 1
print('candidates:', len(cands), 'duplicates:', dup)
sys.exit(0)
