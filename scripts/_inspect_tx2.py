# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/scripts/fetch-transactions.py', encoding='utf-8').read()
print(t[3500:4632])
d = io.open('D:/baseball/data/depth-chart.json', encoding='utf-8').read()
print(d[:900])
