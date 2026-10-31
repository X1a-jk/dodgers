# -*- coding: utf-8 -*-
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
for slug in sys.argv[1:]:
    html = open(rf'D:\baseball\report\{slug}\{slug}-scouting-report.html', encoding='utf-8').read()
    pairs = re.findall(r'<div class="label">([^<]+)</div><div class="value">([^<]+)</div>', html)
    print('='*20, slug)
    for k, v in pairs:
        print(' ', k, '=', v)
    m = re.search(r'<h2>[^<]*背景故事</h2>(.*?)</div>\s*</div>', html, re.S)
    if m:
        txt = re.sub(r'<[^>]+>', '', m.group(1))
        print('  BG:', ' '.join(txt.split())[:700])
    t = re.search(r'<title>(.*?)</title>', html)
    print('  title:', t.group(1) if t else None)
    print('  cover refs:', sorted(set(re.findall(r'src="([^"]*report_cover[^"]*)"', html))))
    s = re.search(r'class="subtitle">(.*?)</p>', html)
    print('  subtitle:', s.group(1) if s else None)
