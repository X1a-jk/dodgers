# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open(r'D:\baseball\portal\design-roadmap.md', encoding='utf-8').read()
i = t.find('| 23.')
print('--- roadmap row23 ---')
print(repr(t[i:i+340]))
m = io.open(r'C:\Users\Junkai XIA\.openclaw\workspace\memory\2026-09-28.md', encoding='utf-8').read()
print('--- memory tail ---')
print(repr(m[-450:]))
