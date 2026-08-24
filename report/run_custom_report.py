#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定制化球探报告运行器
用法：将当前球员的 PLAYER 字典写入 current_player.py，然后运行本脚本
"""
import sys
import os

# 确保可以导入当前目录的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from current_player import PLAYER
from custom_report_lib import generate_report

if __name__ == '__main__':
    generate_report(PLAYER)
