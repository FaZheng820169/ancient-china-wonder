import io

txt = open('tools/_src/_slugs.txt', encoding='utf-8').read()
CAND = ['呂仙寶', '吕仙宝', '泥傀儡', '石贔屓', '石赑屃', '術士驅蠅', '术士驱蝇',
        '眼前殺報', '眼前杀报', '大士慈航', '屏角相郎', '祭蠹文', '獸譜', '兽谱',
        '和尚婆心', '洩氣生員', '泄气生员', '營卒守義', '营卒守义']
for c in CAND:
    print(('DUP!!  ' if c in txt else 'ok     ') + c)
