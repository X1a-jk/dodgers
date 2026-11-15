# -*- coding: utf-8 -*-
"""去掉风琴面板 7 个条目里的 <em>时长</em> 标签"""
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
p = r'D:\baseball\index.html'
h = io.open(p, encoding='utf-8-sig').read()
# 只动 organ-item 行内的 <em>...</em>
pat = re.compile(r'(<div class="organ-item"[^>]*>.*?)<em>[^<]*</em>')
h2, n = pat.subn(r'\1', h)
assert n == 7, 'expected 7, got %d' % n
io.open(p, 'w', encoding='utf-8', newline='\n').write(h2)
print('removed', n, 'em labels, size', len(h2))
