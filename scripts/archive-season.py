#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
赛季封存（Season Archive）——在赛季完全结束后（季后赛打完）运行一次。

做的事：
1. 把现役目录的当年文件迁入 seasons\\YYYY\\：
   - weekly\\*.md                -> seasons\\YYYY\\regular\\weekly\\
   - roster\\YYYY-*.md           -> seasons\\YYYY\\regular\\daily\\
   - weekly\\postseason\\*.md    -> seasons\\YYYY\\postseason\\recaps\\
2. 快照当年数据：data\\*.json + 关键根目录 json -> seasons\\YYYY\\snapshots\\
   （保留 postseason.json 里已聚合的季后赛全程比分 + leaders，供总结引用）
3. 归档当年球员报告：report\\ -> seasons\\YYYY\\players\\
   ⚠️ 门户「球员报告」iframe 指向 report\\index.html，归档后该模块需指向新年份报告
4. 刷新门户索引（update-portal.py）

用法：
    python archive-season.py 2026            # 实际执行
    python archive-season.py 2026 --dry-run  # 只打印计划，不动文件

注意：只迁移「当年」文件（文件名以 YYYY- 开头或目录属于当年），
不碰其他年份和共享文件（dodgers-roster.md 等保留在现役目录）。
"""
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
BASE_DIR = Path(r"D:\baseball")


def log(msg):
    print(f"[archive] {msg}", flush=True)


def move_year_files(src: Path, dst: Path, year: str, dry: bool) -> int:
    """把 src 里 YYYY-*.md 文件迁入 dst，返回迁移数"""
    if not src.exists():
        return 0
    moved = 0
    for f in src.iterdir():
        if f.is_file() and f.name.startswith(year + "-") and f.suffix.lower() == ".md":
            if not dry:
                dst.mkdir(parents=True, exist_ok=True)
                shutil.move(str(f), str(dst / f.name))
            log(f"{'[dry] ' if dry else ''}move {f.name} -> {dst.relative_to(BASE_DIR)}")
            moved += 1
    return moved


def snapshot_data(year: str, dry: bool) -> int:
    """快照 data\\*.json 与根目录关键 json"""
    targets = []
    data_dir = BASE_DIR / "data"
    if data_dir.exists():
        targets += [f for f in data_dir.iterdir()
                    if f.is_file() and f.suffix == ".json" and not f.name.endswith(".bak")]
    for name in ("depth-chart.json", "dashboard-data.json", "file-index.json",
                 "dodgers-roster.md"):
        f = BASE_DIR / name
        if f.exists():
            targets.append(f)
    dst = BASE_DIR / "seasons" / year / "snapshots"
    n = 0
    for f in targets:
        if not dry:
            dst.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(f), str(dst / f.name))
        n += 1
    log(f"{'[dry] ' if dry else ''}snapshot {n} data files -> seasons/{year}/snapshots")
    return n


def archive_reports(year: str, dry: bool) -> None:
    """球员报告目录整体归档（report\\ -> seasons\\YYYY\\players\\）"""
    src = BASE_DIR / "report"
    dst = BASE_DIR / "seasons" / year / "players"
    if not src.exists():
        log("report/ 不存在，跳过球员报告归档")
        return
    if not dry:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            log(f"[warn] {dst} 已存在，跳过（避免覆盖）")
            return
        shutil.move(str(src), str(dst))
    log(f"{'[dry] ' if dry else ''}report/ -> seasons/{year}/players/"
        f"（门户球员报告 iframe 需改指新年度路径）")


def main():
    if len(sys.argv) < 2 or not sys.argv[1].isdigit():
        print("用法: python archive-season.py YYYY [--dry-run]")
        sys.exit(1)
    year = sys.argv[1]
    dry = "--dry-run" in sys.argv
    if len(year) != 4:
        print("年份格式: YYYY")
        sys.exit(1)

    log(f"开始封存 {year} 赛季{'（试运行）' if dry else ''} {datetime.now():%Y-%m-%d %H:%M}")
    n = 0
    n += move_year_files(BASE_DIR / "weekly",
                         BASE_DIR / "seasons" / year / "regular" / "weekly", year, dry)
    n += move_year_files(BASE_DIR / "roster",
                         BASE_DIR / "seasons" / year / "regular" / "daily", year, dry)
    # 季后赛战报（可能在 weekly\\postseason 或 seasons\\YYYY\\postseason\\recaps）
    n += move_year_files(BASE_DIR / "weekly" / "postseason",
                         BASE_DIR / "seasons" / year / "postseason" / "recaps", year, dry)
    snapshot_data(year, dry)
    archive_reports(year, dry)
    log(f"战报迁移 {n} 份")

    if not dry:
        import subprocess
        log("刷新门户索引...")
        subprocess.run([sys.executable, str(BASE_DIR / "portal" / "update-portal.py")],
                       check=False)
        # 清理空的 postseason 暂存目录
        leftover = BASE_DIR / "weekly" / "postseason"
        if leftover.exists() and not any(leftover.iterdir()):
            leftover.rmdir()
            log("清理空目录 weekly/postseason")
    log("封存完成" + ("（试运行，未动文件）" if dry else ""))


if __name__ == "__main__":
    main()
