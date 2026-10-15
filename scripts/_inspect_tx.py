# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/scripts/fetch-transactions.py', encoding='utf-8').read()
print(t[:3500])
