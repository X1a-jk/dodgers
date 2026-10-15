# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
m = re.search(r':root\s*\{', t)
print('root at', m.start())
print(t[m.start():m.start()+1200])
print('==== body / theme class ====')
for mm in re.finditer(r'<body[^>]*>', t):
    print(mm.group(0), mm.start())
print('==== sidebar style ====')
m2 = re.search(r'\.sidebar\s*\{', t)
print(t[m2.start():m2.start()+600])
