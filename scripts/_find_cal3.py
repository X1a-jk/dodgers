# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
# 找日历弹窗函数：日历相关 JS（cal-day 点击、弹窗 DOM）
import re
for m in re.finditer(r'function\s+(\w*[Cc]al\w*|\w*[Mm]odal\w*|\w*[Gg]ame[Dd]etail\w*)\s*\(', t):
    print('FUNC', m.group(1), m.start())
# 搜 onclick 里的日历处理
for m in re.finditer(r'onclick="[^"]*[Cc]al[^"]*"', t):
    print('onclick:', m.group(0)[:100], m.start())
