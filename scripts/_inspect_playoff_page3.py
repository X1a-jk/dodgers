# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
print('==== 193600 - 196600 ====')
print(t[193600:196600])
print('==== router contexts ====')
for pos in (95519, 97439, 104504, 147229):
    print('----', pos, '----')
    print(t[pos-400:pos+200])
