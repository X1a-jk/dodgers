# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
# locate playoff page section
m = re.search(r'<div class="page[^"]*" id="page-playoff"', t)
print('page section at', m.start() if m else None)
if m:
    seg = t[m.start():m.start()+1500]
    print(seg)
# locate render function for playoff
for mm in re.finditer(r'function\s+(render\w*[Pp]layoff\w*|load\w*[Pp]layoff\w*)\s*\(', t):
    print('FUNC', mm.group(1), 'at', mm.start())
for mm in re.finditer(r'playoff', t):
    pass
print('count playoff occurrences:', len(re.findall('playoff', t)))
# show context of each occurrence of 'renderPlayoff' or 'playoff' in JS
idxs = [mm.start() for mm in re.finditer(r'playoff', t)]
for i in idxs:
    line_start = t.rfind('\n', 0, i)
    line = t[line_start+1:t.find('\n', i)]
    if 'nav' not in line and 'data-page' not in line and 'href' not in line.lower():
        print(i, '|', line.strip()[:120])
