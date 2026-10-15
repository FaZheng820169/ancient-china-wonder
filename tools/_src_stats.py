import glob, os, re, collections
rows=[]
for p in glob.glob('src/content/stories/*.md'):
    slug=os.path.basename(p)[:-3]
    txt=open(p,encoding='utf-8').read()
    fm=txt.split('---')[1]
    def f(k):
        m=re.search(r'^'+k+r':\s*(.*)$',fm,re.M)
        return m.group(1).strip().strip('"') if m else ''
    rows.append((slug,f('title'),f('titleZh'),f('sourceZh'),f('source'),f('author'),f('era'),f('featured')=='true',f('order')))
g=collections.defaultdict(list)
for r in rows: g[r[3]].append(r)
for src,items in sorted(g.items(),key=lambda x:-len(x[1])):
    print('='*60)
    print(src,'|',items[0][4],'|',items[0][5],'|',items[0][6],'| n=',len(items))
    for it in sorted(items,key=lambda x:int(x[8] or 99)):
        print('   %-34s %-30s %s %s'%(it[0],it[1][:28],it[2],'FEAT' if it[7] else ''))
