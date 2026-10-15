# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
print('==== renderPlayoffPage (190500 - 193500) ====')
print(t[190500:193600])
