# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
for fn in ('function selectFile', 'function openRaw', 'function filterFiles', 'function renderModule'):
    i = t.find(fn)
    print('==', fn, i)
    print(t[i:i+1300])
    print()
