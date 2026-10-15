#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新道奇数据门户的文件索引。

扫描内容（按年分档）：
- 现役目录：weekly\（当前常规赛周报）、roster\（当前日报快照）
- 赛季存档：seasons\\YYYY\\regular\\weekly、seasons\\YYYY\\regular\\daily、
  seasons\\YYYY\\postseason\\recaps（由 archive-season.py 在赛季末迁入）

每个条目带 folder 字段（相对门户服务器根目录），门户阅读器据此取文件。
输出：
- portal\file-index.json（门户运行时优先实时读取）
- index.html 内嵌的 FILE_INDEX 常量（兼容兜底）
"""
import json
import re
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(r"D:\baseball")
INDEX_HTML = BASE_DIR / "index.html"
INDEX_JSON = BASE_DIR / "portal" / "file-index.json"
SEASONS_DIR = BASE_DIR / "seasons"


def extract_week_info(filename: str) -> dict:
    """从周报文件名提取信息，例如 2026-08-17-week20.md"""
    m = re.match(r"(\d{4}-\d{2}-\d{2})-week(\d+)\.md$", filename)
    if not m:
        return None
    date_str, week_num = m.groups()
    try:
        monday = datetime.strptime(date_str, "%Y-%m-%d")
        sunday = monday + timedelta(days=6)
        period = f"{monday.strftime('%m/%d')}-{sunday.strftime('%m/%d')}"
    except ValueError:
        period = f"Week {week_num}"
    return {
        "name": filename,
        "label": f"Week {int(week_num)} · {period}",
        "date": date_str,
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
    }


def extract_postseason_info(filename: str) -> dict:
    """季后赛战报文件名，例如 2026-10-05-ps-nlds-g1-g3.md"""
    m = re.match(r"(\d{4}-\d{2}-\d{2})-ps-([a-z0-9\-]+)\.md$", filename)
    if not m:
        return None
    date_str, slug = m.groups()
    label = slug.replace("-", " ").upper()
    return {
        "name": filename,
        "label": f"🍂 {label} · {date_str[5:]}",
        "date": date_str,
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
    return results


def scan_seasons() -> dict:
    r"""扫描 seasons\YYYY\... 存档目录，条目带 folder 和赛季标签"""
    entries = {"weekly": [], "daily": [], "postseason": []}
    if not SEASONS_DIR.exists():
        return entries
    for season_dir in sorted(SEASONS_DIR.iterdir()):
        if not season_dir.is_dir() or not season_dir.name.isdigit():
            continue
        year = season_dir.name
        for info in scan_files(season_dir / "regular" / "weekly", extract_week_info):
            info["folder"] = f"seasons/{year}/regular/weekly"
            info["label"] = f"{year} · {info['label']}"
            info["season"] = year
            entries["weekly"].append(info)
        for info in scan_files(season_dir / "regular" / "daily", extract_daily_info):
            info["folder"] = f"seasons/{year}/regular/daily"
            info["label"] = f"{year} · {info['label']}"
            info["season"] = year
            entries["daily"].append(info)
        for info in scan_files(season_dir / "postseason" / "recaps", extract_postseason_info):
            info["folder"] = f"seasons/{year}/postseason/recaps"
            info["season"] = year
            entries["postseason"].append(info)
    return entries


def scan_report_editions() -> list:
    r"""球员报告版本清单（年度/批次切换接口）。

    约定：
    - report\index.html                      → 当前赛季进行中版（实时更新）
    - seasons\YYYY\players\index.html        → 该年赛季总结版（archive-season.py 迁入）
    - seasons\YYYY\players-<edition>\index.html → 批次版：asg 全明星 / regular 常规赛 /
      postseason 季后赛 / mid 季中（手动复制 report\ 后改名即可被扫描到）
    """
    cn = {"asg": "全明星版", "regular": "常规赛版", "postseason": "季后赛版",
          "mid": "季中版", "final": "赛季总结版"}
    editions = []
    current_year = str(datetime.now().year)
    if (BASE_DIR / "report" / "index.html").exists():
        editions.append({"label": f"{current_year} 当前（实时更新）",
                         "path": "report/index.html", "current": True})
    if SEASONS_DIR.exists():
        for season_dir in sorted(SEASONS_DIR.iterdir(), reverse=True):
            if not season_dir.is_dir() or not season_dir.name.isdigit():
                continue
            year = season_dir.name
            if (season_dir / "players" / "index.html").exists():
                editions.append({"label": f"{year} 赛季总结版",
                                 "path": f"seasons/{year}/players/index.html"})
            for sub in sorted(season_dir.glob("players-*")):
                idx = sub / "index.html"
                if not idx.exists():
                    continue
                tag = sub.name[len("players-"):]
                editions.append({"label": f"{year} {cn.get(tag, tag)}",
                                 "path": f"seasons/{year}/{sub.name}/index.html"})
    return editions


def build_index() -> dict:
    index_data = scan_seasons()

    # 现役目录（当前赛季进行中的新文件；赛季末由 archive-season.py 迁入 seasons\）
    # 赛季字段取文件名日期前缀（YYYY-MM-DD → YYYY），与存档条目口径一致
    for info in scan_files(BASE_DIR / "weekly", extract_week_info):
        info["folder"] = "weekly"
        info["season"] = info["date"][:4]
        index_data["weekly"].append(info)
    # 现役日报：统一命名为「YYYY · MM/DD 阵容快照」（与存档条目同口径）
    # 并按日期去重——同一日期若已存在存档条目（seasons\YYYY\regular\daily），
    # 跳过现役目录里的副本（已知坑：封存后 daily-report.py 又写了同一天，造成 9/28 重复）
    archived_dates = {i["date"] for i in index_data["daily"]}
    for info in scan_files(BASE_DIR / "roster", extract_daily_info):
        if info["date"] in archived_dates:
            continue
        info["folder"] = "roster"
        info["label"] = f"{info['date'][:4]} · {info['label']}"
        info["season"] = info["date"][:4]
        index_data["daily"].append(info)
    for info in scan_files(BASE_DIR / "weekly" / "postseason", extract_postseason_info):
        info["folder"] = "weekly/postseason"
        info["season"] = info["date"][:4]
        index_data["postseason"].append(info)

    # 统一按日期倒序（新→旧）
    for key in ("weekly", "daily", "postseason"):
        index_data[key].sort(key=lambda x: x["date"], reverse=True)

    # 可用年份清单（新→旧），供门户年份选择器使用；新赛季归档后自动出现
    years = sorted({i["season"] for k in ("weekly", "daily", "postseason")
                    for i in index_data[k]}, reverse=True)
    index_data["years"] = years
    index_data["currentSeason"] = years[0] if years else str(datetime.now().year)
    index_data["reportEditions"] = scan_report_editions()

    index_data["generatedAt"] = datetime.now().isoformat()
    return index_data


def update_index_html(index_data: dict) -> bool:
    if not INDEX_HTML.exists():
        print(f"[ERR] 门户文件不存在: {INDEX_HTML}")
        return False

    text = INDEX_HTML.read_text(encoding="utf-8")
    new_json = json.dumps(index_data, ensure_ascii=False, indent=12)

    pattern = r"(?:const|let) FILE_INDEX = \{[\s\S]*?\};"
    replacement = f"let FILE_INDEX = {new_json};"

    if not re.search(pattern, text):
        print("[ERR] 在 index.html 中找不到 FILE_INDEX 定义")
        return False

    new_text = re.sub(pattern, replacement, text, count=1)
    INDEX_HTML.write_text(new_text, encoding="utf-8")
    print(f"[OK] 已更新 {INDEX_HTML}")
    print(f"     周报: {len(index_data['weekly'])} 期")
    print(f"     日报: {len(index_data['daily'])} 天")
    print(f"     季后赛战报: {len(index_data.get('postseason', []))} 期")
    return True


def main():
    index_data = build_index()
    print(f"[INFO] 扫描到 {len(index_data['weekly'])} 期周报，"
          f"{len(index_data['daily'])} 天日报，"
          f"{len(index_data.get('postseason', []))} 期季后赛战报")

    INDEX_JSON.parent.mkdir(parents=True, exist_ok=True)
    INDEX_JSON.write_text(
        json.dumps(index_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[OK] 已写出 {INDEX_JSON}")

    update_index_html(index_data)


if __name__ == "__main__":
    main()
