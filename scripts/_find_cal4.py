# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
print('==== 154700 - 161300 (openGameModal) ====')
print(t[154700:161300])
