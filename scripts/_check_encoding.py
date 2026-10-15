# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. update-portal.py 源文件编码探测
raw = open(r'D:\baseball\portal\update-portal.py', 'rb').read()
i = raw.find('当前'.encode('utf-8'))
print('py contains UTF-8 当前:', i >= 0)
i2 = raw.find('当前'.encode('gbk'))
print('py contains GBK 当前:', i2 >= 0)

# 2. file-index.json 里的 reportEditions 原始字节
rawj = open(r'D:\baseball\portal\file-index.json', 'rb').read()
i3 = rawj.find('当前'.encode('utf-8'))
print('json contains UTF-8 当前:', i3 >= 0)
i4 = rawj.find('褰撳墠'.encode('utf-8'))
print('json contains mojibake 褰撳墠:', i4 >= 0)
