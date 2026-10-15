# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
# find style blocks
for m in re.finditer(r'<style[^>]*>', t):
    end = t.find('</style>', m.start())
    print('style block', m.start(), '-', end, 'len', end-m.start())
# header area
hb = t.find('<header')
print('header at', hb)
print(t[hb:hb+1200])
