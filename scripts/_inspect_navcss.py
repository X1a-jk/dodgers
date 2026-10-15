# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
for cls in ('.nav-item {', '.nav-item.active', '.logo {', '.tag-green', '.callup-banner'):
    i = t.find(cls)
    if i >= 0:
        print('==', cls, i)
        print(t[i:i+400])
        print()
