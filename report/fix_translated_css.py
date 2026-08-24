#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 batch_translate_reports.py 误伤的 CSS 类名和代码类标识符。
"""
import os
import re

BASE_DIR = r'D:\baseball\report'

# 需要还原的替换
REVERTS = {
    '.球速': '.velocity',
    'class="球速"': 'class="velocity"',
    # 若 velocity 被替换成 球速 出现在文件名等场景需要还原，但文件路径中原来就是 _pitch_velocities.png 不受影响
    # 若有其他类名被误伤可继续添加
}


def fix_html(html):
    for bad, good in REVERTS.items():
        html = html.replace(bad, good)
    return html


def main():
    count = 0
    for slug in os.listdir(BASE_DIR):
        dir_path = os.path.join(BASE_DIR, slug)
        if not os.path.isdir(dir_path):
            continue
        for fname in os.listdir(dir_path):
            if fname.endswith('-scouting-report.html'):
                path = os.path.join(dir_path, fname)
                with open(path, 'r', encoding='utf-8') as f:
                    html = f.read()
                new_html = fix_html(html)
                if new_html != html:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_html)
                    count += 1
                    print(f'[fixed] {path}')
    print(f'\nFixed {count} reports.')


if __name__ == '__main__':
    main()
