#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replace the postseason section of PLAYER-REPORTS-PLAN.md with final ticked state."""
import io
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

PLAN = r"D:\baseball\PLAYER-REPORTS-PLAN.md"
ps = json.load(io.open(r"D:\baseball\data\ps-postseason-final.json", encoding="utf-8"))

rows = []
for e in ps["participants"]:
    tags = []
    if e["bat"]["plateAppearances"] > 0:
        tags.append("打")
    if e["pit"]["outs"] > 0:
        tags.append("投")
    rows.append(f"| [x] | {e['name']} | {e['games']} | {'/'.join(tags)} |")

new_section = (
    "## 季后赛批（25 人，2026-10-17 定稿）\n\n"
    "> ✅ **已完成**：道奇 NLDS 3-1 晋级、NLCS 0-4 止步（共 8 场）。25 人出场名单从全部 8 场真实 boxscore\n"
    "> 重新汇总（`scripts\\fetch-ps-final.py`），报告已追加「2026 季后赛表现」章节（`scripts\\generate-ps-reports.py`），\n"
    "> 25/25 验证通过，已封存 `seasons\\2026\\players-postseason\\`，门户出现「2026 季后赛版」。\n\n"
    "| 完成 | 球员 | 出场 | 角色 |\n"
    "|---|---|---|---|\n"
    + "\n".join(rows) + "\n\n"
    "> 赛后核对项：\n"
    "> - [x] 道奇淘汰后重新跑出场名单汇总（全部季后赛场次）——25 人，与 NLCS G3 快照同名单，出场数有更新\n"
    "> - [x] 世界大赛出场名单——未晋级（NLCS 0-4），无需处理\n"
    "> - [x] 全部核对完 → 复制 report\\ → seasons\\2026\\players-postseason\\ → update-portal.py\n"
)

t = io.open(PLAN, encoding="utf-8").read()
start = t.index("## 季后赛批")
end = t.index("# 未来赛季（模板）")
# 保留 end 之前的分隔线
new = t[:start] + new_section + "\n---\n\n" + t[end:]
io.open(PLAN, "w", encoding="utf-8").write(new)

t2 = io.open(PLAN, encoding="utf-8").read()
print("[x] total:", t2.count("| [x] "), "| [ ] total:", t2.count("| [ ] "))
