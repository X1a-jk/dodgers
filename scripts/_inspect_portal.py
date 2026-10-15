# -*- coding: utf-8 -*-
import io, re
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
print('len', len(t))
for m in re.finditer(r'''navItem\(['"](.+?)['"]\s*,\s*['"](.+?)['"]\s*,\s*['"](.+?)['"]\s*\)''', t):
    print('nav:', m.group(1), '|', m.group(2), '|', m.group(3))
print('---pages---')
for m in re.finditer(r'''data-page=['"](.+?)['"]''', t):
    print('page:', m.group(1))
