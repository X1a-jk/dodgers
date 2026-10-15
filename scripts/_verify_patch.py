# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
for k in ['模拟器', 'october-banner', 'renderRecapPage', 'applyOctoberTheme', 'data-page="recap"', '.ps-series', 'fetch-postseason.py']:
    print(k, '->', t.count(k))
