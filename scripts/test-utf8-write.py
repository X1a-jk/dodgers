import os
p = 'D:/baseball/report/test-utf8.txt'
with open(p, 'w', encoding='utf-8') as f:
    f.write('Jonathan Hernández 球探报告\n')
with open(p, 'rb') as f:
    print(f.read())
