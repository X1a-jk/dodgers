# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
# 日历弹窗：找日历点击处理函数。看 40668 附近 CSS 后的 JS，和 76213（周战报第一次出现）
print('==== around 75500-77200 (nav area?) ====')
print(t[75400:77260])
