#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate postseason-edition reports for the 25 Dodgers playoff participants.

在常规赛定稿报告的基础上追加「2026 季后赛表现」章节（真实 boxscore 聚合数据）。
输出到 report\\<slug>\\（覆盖），由 archive 步骤复制到 seasons\\2026\\players-postseason\\。
"""
import importlib.util
import io
import json
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

_spec = importlib.util.spec_from_file_location(
    "gm", r"D:\baseball\scripts\generate-missing-reports.py")
gm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gm)

PS = json.load(io.open(r"D:\baseball\data\ps-postseason-final.json", encoding="utf-8"))
GAMES = PS["games"]
PARTICIPANTS = PS["participants"]


def team_result():
    rounds = {}
    for g in GAMES:
        r = g["desc"]
        rounds.setdefault(r, {"w": 0, "l": 0})
        away_s, home_s = (int(x) for x in g["score"].split(" - "))
        dodgers_is_home = g["home"] == "Los Angeles Dodgers"
        d_score = home_s if dodgers_is_home else away_s
        o_score = away_s if dodgers_is_home else home_s
        if d_score > o_score:
            rounds[r]["w"] += 1
        else:
            rounds[r]["l"] += 1
    parts = []
    cn = {"NL Division Series": "NLDS", "NL Championship Series": "NLCS", "World Series": "世界大赛"}
    for r, rec in rounds.items():
        parts.append(f"{cn.get(r, r)} {rec['w']}-{rec['l']}")
    return "、".join(parts)


RESULT_LINE = team_result()


def ps_section(e: dict) -> str:
    b, p = e["bat"], e["pit"]
    lines = ["## 🏆 2026 季后赛表现", "",
             f"> 道奇 2026 季后赛战绩：{RESULT_LINE}", ""]
    hl = []
    if b["plateAppearances"] > 0:
        lines += [
            f"| G | PA | AVG | OBP | SLG | OPS | HR | RBI | BB | SO |",
            f"|---|---|-----|-----|-----|-----|----|----|----|----|",
            f"| {e['games']} | {b['plateAppearances']} | {b['avg']} | {b['obp']} | {b['slg']} | {b['ops']} "
            f"| {b['homeRuns']} | {b['rbi']} | {b['baseOnBalls']} | {b['strikeOuts']} |",
            "",
        ]
        if b["homeRuns"] > 0:
            hl.append(f"季后赛轰出 {b['homeRuns']} 支全垒打")
        if b["rbi"] >= 6:
            hl.append(f"贡献 {b['rbi']} 分打点，是球队季后赛 run production 主力")
        if b["plateAppearances"] >= 25 and b["avg"] != "-":
            avg = float(b["avg"])
            hl.append(f"打击率 {b['avg']}，季后赛" + ("手感火热" if avg >= .300 else "输出稳定" if avg >= .250 else "表现低于常规赛水平"))
        if not hl:
            hl.append("季后赛主要承担轮换/代打角色，产量有限")
    if p["outs"] > 0:
        lines += [
            f"| G | GS | W-L | ERA | WHIP | IP | SO | BB |",
            f"|---|---|-----|-----|------|----|----|----|",
            f"| {e['games']} | {e['gs']} | {p['wins']}-{p['losses']} | {p['era']} | {p['whip']} | {p['ip']} "
            f"| {p['strikeOuts']} | {p['baseOnBalls']} |",
            "",
        ]
        era = float(p["era"]) if p["era"] != "-" else None
        if era is not None:
            hl.append(f"季后赛 ERA {p['era']}（{p['ip']} 局）" +
                      ("，压制力出色" if era < 3.00 else "，表现稳健" if era < 4.50 else "，失分偏多"))
        if p["saves"] > 0:
            hl.append(f"拿下 {p['saves']} 次救援成功")
        if e["gs"] >= 2:
            hl.append(f"季后赛 {e['gs']} 场先发")
    hl.append("⚠️ 季后赛样本小，数据波动大，宜结合常规赛综合评估")
    lines += [f"- {h}" for h in hl]
    return "\n".join(lines)


def generate_ps_one(e: dict):
    name = e["name"]
    slug = gm.slugify(name)
    player_dir = gm.REPORT_ROOT / slug
    player_dir.mkdir(parents=True, exist_ok=True)

    pos_type = ("Pitcher" if (e["pit"]["outs"] > 0 and e["bat"]["plateAppearances"] == 0)
                else "TwoWay" if (e["pit"]["outs"] > 0 and e["bat"]["plateAppearances"] > 0)
                else "Position")
    info = gm.fetch_player(e["id"])
    stats_2025 = gm.fetch_season_stats(e["id"], 2025)
    stats_2026 = gm.fetch_season_stats(e["id"], 2026)
    bundle = gm.build_analysis(name, info, stats_2025, stats_2026, pos_type)

    gm.generate_cover(player_dir, name, info, stats_2026)
    gm.generate_season_comparison(player_dir, name, stats_2025, stats_2026, bundle["is_pitcher"])
    gm.generate_radar(name, bundle["radar_labels"], bundle["radar_values"],
                      player_dir / f"{slug}_overall_grades.png", 'Overall Grades')

    md = gm.build_markdown(name, info, bundle)
    # 在未来展望前插入季后赛章节
    anchor = "\n---\n\n## 🔮 未来展望"
    assert anchor in md, f"anchor missing for {name}"
    md = md.replace(anchor, f"\n---\n\n{ps_section(e)}\n\n---\n\n## 🔮 未来展望", 1)
    # 封面副标题注明季后赛版
    md = md.replace("（2026 赛季最终数据）", "（2026 赛季最终数据 · 季后赛版）", 1)

    html = gm.build_html(name, md, slug)
    (player_dir / f"{slug}-scouting-report.md").write_text(md, encoding="utf-8")
    (player_dir / f"{slug}-scouting-report.html").write_text(html, encoding="utf-8")
    print(f"Generated PS: {name}", flush=True)


def main():
    failed = []
    for e in PARTICIPANTS:
        try:
            generate_ps_one(e)
        except Exception as ex:
            failed.append((e["name"], repr(ex)))
            print(f"FAILED: {e['name']} -> {ex!r}", flush=True)
    print()
    if failed:
        print(f"{len(failed)} failed:")
        for n, err in failed:
            print(f"  - {n}: {err}")
    else:
        print("All postseason reports generated OK.")


if __name__ == "__main__":
    main()
