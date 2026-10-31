# -*- coding: utf-8 -*-
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
for slug in sys.argv[1:]:
    html = open(rf'D:\baseball\report\{slug}\{slug}-scouting-report.html', encoding='utf-8').read()
    print('='*25, slug)
    for sec in ['投球武器库', '球探分析', '优势', '综合评分', '未来展望', '职业生涯亮点']:
        m = re.search(r'<h2>[^<]*?' + sec + r'.*?</h2>(.*?)(?=<div class="section">|<div class="footer">)', html, re.S)
        if not m:
            continue
        txt = re.sub(r'<[^>]+>', '|', m.group(1))
        txt = re.sub(r'\|+', ' | ', txt)
        txt = ' '.join(txt.split())
        print(f'--- {sec}:', txt[:900])
