# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
for mm in re.finditer(r'DOMContentLoaded|window\.onload|showPage\(|initPalette|paletteItems', t):
    i = mm.start()
    line_start = t.rfind('\n', 0, i)
    print(i, '|', t[line_start+1:t.find('\n', i)].strip()[:140])
print('---- end of script ----')
print(t[-1500:])
