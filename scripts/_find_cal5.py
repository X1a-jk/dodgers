# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
print('==== 161260 - 163600 (loadGameLocal) ====')
print(t[161260:163700])
