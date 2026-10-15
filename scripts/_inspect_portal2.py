# -*- coding: utf-8 -*-
import io, re
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
i = t.find("data-page=\"dashboard\"")
seg = t[i-200:i+2600]
import sys
sys.stdout.reconfigure(encoding='utf-8')
print(seg)
