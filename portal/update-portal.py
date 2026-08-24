#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新道奇数据门户的文件索引。
扫描 D:\\baseball\\weekly 和 D:\\baseball\\roster 目录，
把最新的周报/日报文件列表写回 D:\\baseball\\index.html 的 FILE_INDEX 中。
"""
import json
import re
import os
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(r"D:\baseball")
INDEX_HTML = BASE_DIR / "index.html"


def extract_week_info(filename: str) -> dict:
    """从周报文件名提取信息，例如 2026-08-17-week20.md"""
    m = re.match(r"(\d{4}-\d{2}-\d{2})-week(\d+)\.md$", filename)
    if not m:
        return None
    date_str, week_num = m.groups()
    # 估算数据周期：周一 ~ 周日
    try:
        monday = datetime.strptime(date_str, "%Y-%m-%d")
        sunday = monday + timedelta(days=6)
    except ValueError:
        sunday = monday = None
    if monday:
        period = f"{monday.strftime('%m/%d')}-{sunday.strftime('%m/%d')}"
    else:
        period = f"Week {week_num}"
    return {
        "name": filename,
        "label": f"Week {int(week_num)} · {period}",
        "date": date_str,
        "sort": date_str,
    }


def extract_daily_info(filename: str) -> dict:
    """从日报文件名提取信息，例如 2026-08-20.md"""
    m = re.match(r"(\d{4}-\d{2}-\d{2})\.md$", filename)
    if not m:
        return None
    date_str = m.group(1)
    return {
        "name": filename,
        "label": f"{date_str[5:].replace('-', '/')} 阵容快照",
        "date": date_str,
        "sort": date_str,
    }


def scan_files(folder: Path, extractor) -> list:
    results = []
    if not folder.exists():
        return results
    for f in folder.iterdir():
        if not f.is_file() or f.suffix.lower() != ".md":
            continue
        info = extractor(f.name)
        if info:
            results.append(info)
    # 按日期倒序
    results.sort(key=lambda x: x["sort"], reverse=True)
    # 去掉 sort 字段
    for r in results:
        del r["sort"]
    return results


def update_index_html(index_data: dict) -> bool:
    if not INDEX_HTML.exists():
        print(f"[ERR] 门户文件不存在: {INDEX_HTML}")
        return False

    text = INDEX_HTML.read_text(encoding="utf-8")
    new_json = json.dumps(index_data, ensure_ascii=False, indent=12)

    pattern = r"const FILE_INDEX = \{[\s\S]*?\};"
    replacement = f"const FILE_INDEX = {new_json};"

    if not re.search(pattern, text):
        print("[ERR] 在 index.html 中找不到 FILE_INDEX 定义")
        return False

    new_text = re.sub(pattern, replacement, text, count=1)
    INDEX_HTML.write_text(new_text, encoding="utf-8")
    print(f"[OK] 已更新 {INDEX_HTML}")
    print(f"     周报: {len(index_data['weekly'])} 期")
    print(f"     日报: {len(index_data['daily'])} 天")
    return True


def main():
    weekly_dir = BASE_DIR / "weekly"
    daily_dir = BASE_DIR / "roster"

    weekly_files = scan_files(weekly_dir, extract_week_info)
    daily_files = scan_files(daily_dir, extract_daily_info)

    print(f"[INFO] 扫描到 {len(weekly_files)} 期周报，{len(daily_files)} 天日报")

    index_data = {
        "weekly": weekly_files,
        "daily": daily_files,
    }

    update_index_html(index_data)


if __name__ == "__main__":
    main()
