#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为所有报告中的赛季对比图和投球武器库速度图追加中文说明文字。"""
import os
import re

BASE_DIR = r'D:\baseball\report'

def add_captions(html, slug):
    # 赛季对比图
    old = f'<img src="{slug}_season_comparison.png" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">'
    caption = '<p style="text-align: center; color: #90a4ae; font-size: 0.95em; margin-top: 10px;">📈 上图为近三年核心数据趋势。柱状图高度代表该年度表现，便于快速比较球员状态的上升或下滑。</p>'
    if old in html and caption not in html:
        html = html.replace(old, old + '\n            ' + caption)

    # 投球武器库速度图
    old2 = f'<img src="{slug}_pitch_velocities.png" alt="投球武器库速度" style="width: 100%; max-width: 900px; border-radius: 10px;">'
    caption2 = '<p style="text-align: center; color: #90a4ae; font-size: 0.95em; margin-top: 10px;">⚾ 上图为各球种球速区间（蓝=最低球速，橙=最高球速，红线=平均值）。球速差与位移差越大，打者越难锁定单一球路。</p>'
    if old2 in html and caption2 not in html:
        html = html.replace(old2, old2 + '\n            ' + caption2)

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
                new_html = add_captions(html, slug)
                if new_html != html:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_html)
                    count += 1
                    print(f'[caption] {path}')
    print(f'\nAdded captions to {count} reports.')


if __name__ == '__main__':
    main()
