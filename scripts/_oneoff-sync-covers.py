# -*- coding: utf-8 -*-
# 一次性：把 report\ 下全部封面（含短名残留）同步到 seasons\2026\players-regular 与 players-postseason
import io
import json
import os
import re
import shutil
import unicodedata

BASE = r'D:\baseball'
roster = json.load(io.open(r'D:\baseball\data\season-roster.json', encoding='utf-8'))['players']

def slugify(name):
    s = unicodedata.normalize('NFKD', name)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower().replace(' ', '-')

targets = {
    'players-regular': [slugify(p['name']) for p in roster],
    'players-postseason': ['will-smith','kyle-tucker','max-muncy','freddie-freeman','shohei-ohtani','teoscar-hernandez','andy-pages','mookie-betts','tommy-edman','tanner-scott','alex-vesia','evan-phillips','enrique-hernandez','edwin-diaz','miguel-rojas','brock-stewart','edgardo-henriquez','josue-de-paula','roki-sasaki','tarik-skubal','kris-bubic','blake-snell','yoshinobu-yamamoto','tyler-glasnow','justin-wrobleski'],
}
copied, problems = 0, []
for batch, slugs in targets.items():
    dst_root = os.path.join(BASE, 'seasons', '2026', batch)
    for slug in slugs:
        src = os.path.join(BASE, 'report', slug)
        dst = os.path.join(dst_root, slug)
        if not os.path.isdir(dst):
            problems.append((batch, slug, 'no sealed dir'))
            continue
        covers = [f for f in os.listdir(src) if f.endswith('_report_cover.png')]
        for c in covers:
            shutil.copy2(os.path.join(src, c), os.path.join(dst, c))
            copied += 1
        htmls = [f for f in os.listdir(dst) if f.endswith('.html')]
        if htmls:
            t = io.open(os.path.join(dst, htmls[0]), encoding='utf-8').read()
            for ref in set(re.findall(r'([\w-]+_report_cover\.png)', t)):
                if not os.path.exists(os.path.join(dst, ref)):
                    problems.append((batch, slug, f'ref missing: {ref}'))
print('copied:', copied)
print('problems:', problems if problems else 'none')
