# -*- coding: utf-8 -*-
"""所有移动端单列 grid 的 1fr 改成 minmax(0, 1fr)，防止宽内容撑破轨道"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
p = r'D:\baseball\index.html'
h = io.open(p, encoding='utf-8-sig').read()
old = 'grid-template-columns: 1fr;'
n = h.count(old)
assert n >= 5, 'expect >=5 got %d' % n
h = h.replace(old, 'grid-template-columns: minmax(0, 1fr);')
io.open(p, 'w', encoding='utf-8', newline='\n').write(h)
print('replaced', n, 'occurrences')
