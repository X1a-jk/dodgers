#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量定制化球探报告运行器
用法：将一组球员配置写入 batch_players.py，然后运行本脚本
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from batch1_players import PLAYERS
from custom_report_lib import generate_report

if __name__ == '__main__':
    print(f"开始批量生成 {len(PLAYERS)} 名球员报告...")
    for idx, p in enumerate(PLAYERS, 1):
        print(f"\n[{idx}/{len(PLAYERS)}]", end=" ")
        generate_report(p)
    print(f"\n全部完成：{len(PLAYERS)} 名球员")
