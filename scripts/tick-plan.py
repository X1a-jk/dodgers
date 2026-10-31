#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tick off all remaining regular-season players in PLAYER-REPORTS-PLAN.md."""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

PLAN = r"D:\baseball\PLAYER-REPORTS-PLAN.md"
t = io.open(PLAN, encoding="utf-8").read()

# 只在常规批范围内替换（季后赛批之前）
head, sep, tail = t.partition("## 季后赛批")
assert sep, "postseason section not found"

count = 0


def tick(m):
    global count
    count += 1
    return m.group(0).replace("| [ ] |", "| [x] |", 1).replace("| ✅ 有目录 |", "| ✅ 10-17 定稿 |", 1)


head = re.sub(r"\| \[ \] \| [^\n]*\| ✅ 有目录 \|", tick, head)

old_note = (
    "> 进度：8 / 53　|　**缺报告 8 人已补齐（2026-10-17）**：md + html + 图表齐全，已打勾。\n"
    ">\n"
    "> 剩余 45 人报告目录早已存在，但按规则 2 仍需按赛季最终数据核对/重新生成后才能打勾。"
)
new_note = (
    "> 进度：53 / 53　|　**常规赛批全部完成（2026-10-17 定稿）**：45 人按赛季最终数据重新生成\n"
    "> （数据驱动分析引擎：备注/优劣/评分全部由最终数据生成），8 人此前已补齐；53 人全部验证通过\n"
    "> （md + html + 图表 ≥3 + 数据抽查一致）。已封存 seasons\\2026\\players-regular\\。"
)
if old_note in head:
    head = head.replace(old_note, new_note)
    print("note updated")
else:
    assert new_note.splitlines()[0] in head, "neither old nor new note found"
    print("note already updated, skipping")

io.open(PLAN, "w", encoding="utf-8").write(head + sep + tail)
print("ticked:", count)
