#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按赛季最终数据批量重生成 53 人道奇球员报告（2026 常规赛最终版）。

数据源：data\\season-roster.json（名单）+ data\\_player-raw\\{id}_{season}.json（web_fetch 预抓的原始数据）。
产出：D:\\baseball\\report\\{slug}\\ 下 md + html + 3 张图表（封面/赛季对比/综合评分）。
图表标签一律用英文，规避 matplotlib 缺中文字体的问题。
"""

import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

SEASON = 2026
DATA = Path("D:/baseball/data")
RAW = DATA / "_player-raw"
REPORT_ROOT = Path("D:/baseball/report")
ROSTER = json.loads((DATA / "season-roster.json").read_text(encoding="utf-8"))


def slugify(name: str) -> str:
    normalized = unicodedata.normalize('NFKD', name)
    ascii_name = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return re.sub(r"[^a-z0-9-]", "", ascii_name.lower().replace(" ", "-").replace("'", "").replace(".", ""))


def load_raw(person_id):
    """返回 (info, stats26, stats25)"""
    info, s26, s25 = {}, {"hitting": {}, "pitching": {}}, {"hitting": {}, "pitching": {}}
    for season, bucket in ((2026, s26), (2025, s25)):
        f = RAW / f"{person_id}_{season}.json"
        if not f.exists():
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        people = d.get("people", [])
        if not people:
            continue
        p = people[0]
        if season == 2026:
            info = p
        for g in p.get("stats", []):
            gname = g.get("group", {}).get("displayName", "").lower()
            splits = g.get("splits", [])
            if gname in ("hitting", "pitching") and splits:
                st = splits[0].get("stat", {})
                if st and st.get("gamesPlayed"):
                    bucket[gname] = st
    return info, s26, s25


def f2(x, nd=2):
    try:
        return round(float(x), nd)
    except (TypeError, ValueError):
        return None


def has_bat(s):
    return bool(s.get("hitting", {}).get("gamesPlayed"))


def has_pit(s):
    return bool(s.get("pitching", {}).get("gamesPlayed"))


def fmt(x, d="-"):
    return d if x in (None, "") else x


# ---------- 评分计算（20-80 scale） ----------

def hitting_grades(h):
    avg = f2(h.get("avg")); obp = f2(h.get("obp")); slg = f2(h.get("slg"))
    ops = f2(h.get("ops"))
    so, bb = float(h.get("strikeOuts") or 0), float(h.get("baseOnBalls") or 0)
    pa = float(h.get("plateAppearances") or 1) or 1
    hr = float(h.get("homeRuns") or 0); sb = float(h.get("stolenBases") or 0)
    g = float(h.get("gamesPlayed") or 1)

    def clamp(v): return max(25, min(80, v))
    contact = clamp(50 + ((avg or 0) - .250) * 220)
    power = clamp(50 + ((slg or 0) - .420) * 130 + (hr / g) * 6)
    discipline = clamp(50 + ((obp or 0) - .320) * 200 - (so / pa) * 40 + (bb / pa) * 80)
    speed = clamp(50 + sb * 1.2 - (float(h.get("caughtStealing") or 0)) * 2)
    return {
        "Contact": round(contact), "Power": round(power), "Discipline": round(discipline),
        "Speed": round(speed), "Defense": 55, "Arm": 55,
    }, (ops or 0)


def pitching_grades(p):
    era = f2(p.get("era")); whip = f2(p.get("whip"))
    k9 = f2(p.get("strikeoutsPer9Inn")); bb9 = f2(p.get("walksPer9Inn"))
    sv = float(p.get("saves") or 0); hld = float(p.get("holds") or 0)
    ip = float(p.get("inningsPitched".replace("inningsPitched", "inningsPitched")) or 0)

    def ip_float(s):
        if not s: return 0.0
        s = str(s)
        if "." in s:
            whole, frac = s.split(".")
            return int(whole) + (int(frac) * 1 / 3 if len(frac) == 1 else 0)
        return float(s)

    def clamp(v): return max(25, min(80, v))
    stuff = clamp(50 + ((k9 or 0) - 8.5) * 3.5)
    control = clamp(50 - ((bb9 or 0) - 3.0) * 10)
    command = clamp(50 - ((whip or 1.30) - 1.20) * 45)
    durability = clamp(50 + ip_float(p.get("inningsPitched")) / 4)
    return {
        "Fastball": round(stuff), "Offspeed": round((stuff + control) / 2),
        "Control": round(control), "Command": round(command),
        "Stamina": round(durability), "Mental": 55,
    }, (era if era is not None else 9.99)


def grade_label(score):
    if score >= 70: return "A+"
    if score >= 65: return "A"
    if score >= 60: return "A-"
    if score >= 55: return "B+"
    if score >= 50: return "B"
    if score >= 45: return "B-"
    if score >= 40: return "C+"
    return "C"


# ---------- 数据驱动文案 ----------

def trend_word(d, lower_better=False):
    if d is None: return "样本不足以下结论"
    if lower_better: d = -d
    if d > 0.02: return "较 2025 明显提升"
    if d < -0.02: return "较 2025 明显下滑"
    return "与 2025 基本持平"


def hitter_note(h26, h25):
    avg = f2(h26.get("avg")); obp = f2(h26.get("obp")); slg = f2(h26.get("slg"))
    ops = f2(h26.get("ops"))
    hr, rbi, sb = h26.get("homeRuns"), h26.get("rbi"), h26.get("stolenBases")
    g = h26.get("gamesPlayed")
    pa = float(h26.get("plateAppearances") or 0)
    k_rate = (float(h26.get("strikeOuts") or 0) / pa) if pa else None
    obp_gap = (obp - avg) if (obp and avg) else None
    ops25 = f2(h25.get("ops")) if h25 else None
    d_ops = (ops - ops25) if (ops is not None and ops25 is not None) else None

    parts = [f"2026 赛季出赛 {g} 场，缴出 {fmt(h26.get('avg'))}/{fmt(h26.get('obp'))}/{fmt(h26.get('slg'))}、OPS {fmt(h26.get('ops'))}，{hr} 轰 {rbi} 打点" + (f"、{sb} 次盗垒成功" if sb and int(sb) > 0 else "") + "。"]
    if obp_gap is not None:
        parts.append(f"上垒率与打击率差距 {obp_gap:.3f}——" + ("选球耐心带来的额外上垒贡献明显。" if obp_gap >= .06 else ("上垒几乎全靠安打，保送贡献有限。" if obp_gap <= .03 else "上垒结构中规中矩。")))
    if k_rate is not None:
        parts.append(f"三振率约 {k_rate*100:.1f}%" + ("，属于高挥空型打者。" if k_rate > .25 else "，控球球能力尚在联盟平均水准之上。" if k_rate < .15 else "，处于联盟常态区间。"))
    iso = (slg - avg) if (slg and avg) else None
    if iso is not None:
        parts.append(f"纯长打率 ISO {iso:.3f}，" + ("长打是其主要价值来源。" if iso >= .180 else "长打产出一般。"))
    if d_ops is not None:
        parts.append(f"OPS {trend_word(d_ops)}（{(d_ops):+.3f}）。")
    elif not h25:
        parts.append("2025 年无大联盟数据，本季为新样本起点。")
    return "".join(parts)


def pitcher_note(p26, p25):
    era, whip = fmt(p26.get("era")), fmt(p26.get("whip"))
    k9, bb9 = fmt(p26.get("strikeoutsPer9Inn")), fmt(p26.get("walksPer9Inn"))
    w, l = p26.get("wins"), p26.get("losses")
    g, gs = p26.get("gamesPlayed"), p26.get("gamesStarted")
    sv, hld, bs = p26.get("saves"), p26.get("holds"), p26.get("blownSaves")
    ip = p26.get("inningsPitched")
    role = "先发" if gs and int(gs) >= int(g) * 0.5 else "后援"
    era25 = f2(p25.get("era")) if p25 else None
    era26 = f2(p26.get("era"))
    d_era = (era26 - era25) if (era26 is not None and era25 is not None) else None

    parts = [f"2026 赛季以{role}身份出赛 {g} 场（{gs or 0} 场先发），战绩 {w}-{l}，ERA {era}、WHIP {whip}，共投 {ip} 局，K/9 {k9}、BB/9 {bb9}。"]
    if sv and int(sv) > 0:
        parts.append(f"终结者角色：{sv} 次救援成功 / {p26.get('saveOpportunities') or '?'} 次机会，另有 {bs or 0} 次救援失败。")
    elif hld and int(hld) > 0:
        parts.append(f"中继 setup 角色：{hld} 次 hold。")
    k9f = f2(p26.get("strikeoutsPer9Inn")); bb9f = f2(p26.get("walksPer9Inn"))
    if k9f is not None:
        parts.append(f"三振能力（K/9 {k9}）" + ("是其压制打者的核心武器。" if k9f >= 10 else "处于联盟平均水准。" if k9f >= 7.5 else "偏弱，更依赖制造软弱击球。"))
    if bb9f is not None and bb9f > 4.0:
        parts.append(f"但 BB/9 {bb9} 偏高，控球是其最大隐患。")
    if era26 is not None and era26 >= 6:
        parts.append(f"ERA {era} 远高于联盟平均，本季整体表现令人失望。")
    elif era26 is not None and era26 <= 2.5:
        parts.append(f"ERA {era} 属于联盟顶尖水准。")
    if d_era is not None:
        parts.append(f"ERA {trend_word(d_era, lower_better=True)}（{(d_era):+.2f}）。")
    elif not p25:
        parts.append("2025 年无大联盟数据，本季为新样本起点。")
    return "".join(parts)


# ---------- 图表 ----------

def generate_cover(player_dir, slug, name, info, s26):
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e'); ax.axis('off')
    ax.text(0.05, 0.82, "LA", fontsize=72, color='#ff9800', fontweight='bold', transform=ax.transAxes)
    ax.text(0.28, 0.78, name, fontsize=28, color='white', fontweight='bold', transform=ax.transAxes)
    pos = (info.get("primaryPosition") or {}).get("abbreviation", "")
    subtitle = f"Los Angeles Dodgers #{fmt(info.get('primaryNumber',''))} | {pos} | {SEASON} Final"
    ax.text(0.28, 0.64, subtitle, fontsize=14, color='#90a4ae', transform=ax.transAxes)
    age = fmt(info.get('currentAge', ''))
    bh = f"{(info.get('batSide') or {}).get('code','?')} / {(info.get('pitchHand') or {}).get('code','?')}"
    ax.text(0.28, 0.54, f"Bats/Throws {bh} | Age {age}", fontsize=12, color='#e0e0e0', transform=ax.transAxes)
    if has_pit(s26) and not has_bat(s26):
        st = s26['pitching']
        line = f"ERA {fmt(st.get('era'))} | WHIP {fmt(st.get('whip'))} | {fmt(st.get('wins'))}-{fmt(st.get('losses'))} | {fmt(st.get('strikeOuts'))} K"
    elif has_bat(s26) and not has_pit(s26):
        st = s26['hitting']
        line = f"{fmt(st.get('avg'))}/{fmt(st.get('obp'))}/{fmt(st.get('slg'))} | {fmt(st.get('homeRuns'))} HR | {fmt(st.get('rbi'))} RBI"
    else:
        hb, pt = s26.get('hitting', {}), s26.get('pitching', {})
        line = f"{fmt(hb.get('avg'))}/{fmt(hb.get('obp'))}/{fmt(hb.get('slg'))} + ERA {fmt(pt.get('era'))}"
    ax.text(0.28, 0.42, line, fontsize=14, color='#ff9800', fontweight='bold', transform=ax.transAxes)
    ax.text(0.28, 0.30, f"Final Season Report - {datetime.now().strftime('%Y-%m-%d')}", fontsize=10, color='#78909c', transform=ax.transAxes)
    fig.savefig(player_dir / f"{slug}_report_cover.png", dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close(fig)


def generate_season_comparison(player_dir, slug, s25, s26, is_pitcher, is_two_way):
    if is_two_way:
        labels = ['AVG', 'OBP', 'SLG', 'OPS']
        h25, h26 = s25.get('hitting', {}), s26.get('hitting', {})
        scale = lambda x: (float(x) * 100) if x not in (None, "", "-") else None
        v25 = [scale(h25.get(k)) for k in ('avg', 'obp', 'slg', 'ops')]
        v26 = [scale(h26.get(k)) for k in ('avg', 'obp', 'slg', 'ops')]
    elif is_pitcher:
        labels = ['ERA', 'WHIP', 'K/9', 'BB/9']
        p25, p26 = s25.get('pitching', {}), s26.get('pitching', {})
        def pit_vals(p):
            era = f2(p.get('era')); whip = f2(p.get('whip')); k9 = f2(p.get('strikeoutsPer9Inn')); bb9 = f2(p.get('walksPer9Inn'))
            return [max(20, 80 - era * 10) if era is not None else None,
                    max(20, 80 - whip * 30) if whip is not None else None,
                    min(80, k9 * 4 + 20) if k9 is not None else None,
                    max(20, 80 - bb9 * 8) if bb9 is not None else None]
        v25, v26 = pit_vals(p25), pit_vals(p26)
    else:
        labels = ['AVG', 'OBP', 'SLG', 'OPS']
        h25, h26 = s25.get('hitting', {}), s26.get('hitting', {})
        scale = lambda x: (float(x) * 100) if x not in (None, "", "-") else None
        v25 = [scale(h25.get(k)) for k in ('avg', 'obp', 'slg', 'ops')]
        v26 = [scale(h26.get(k)) for k in ('avg', 'obp', 'slg', 'ops')]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True), facecolor='#1a1a2e')
    ax.set_facecolor('#16213e')
    for values, color, label in ((v25, '#4fc3f7', '2025'), (v26, '#ff9800', f'{SEASON}')):
        if any(v is None for v in values):
            continue
        v = values + values[:1]
        ax.plot(angles, v, color=color, linewidth=2, label=label)
        ax.fill(angles, v, color=color, alpha=0.15)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels, color='white', size=11)
    ax.set_ylim(20, 100)
    ax.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
    ax.set_title(f'2025 vs {SEASON} Season Comparison', color='white', fontsize=14, fontweight='bold', pad=20)
    fig.savefig(player_dir / f"{slug}_season_comparison.png", dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close(fig)


def generate_grades_radar(player_dir, slug, grades, title):
    labels = list(grades.keys())
    values = [grades[k] for k in labels]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values_plot = values + values[:1]; angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True), facecolor='#1a1a2e')
    ax.set_facecolor('#16213e')
    ax.plot(angles, values_plot, color='#ff9800', linewidth=2)
    ax.fill(angles, values_plot, color='#ff9800', alpha=0.25)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels, color='white', size=10)
    ax.set_ylim(20, 80); ax.set_yticks([30, 50, 70]); ax.set_yticklabels(['30', '50', '70'], color='#90a4ae', size=8)
    ax.set_title(title, color='white', fontsize=14, fontweight='bold', pad=20)
    fig.savefig(player_dir / f"{slug}_overall_grades.png", dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close(fig)


# ---------- 报告文档 ----------

def hitting_table(h, season_label):
    cols = ["gamesPlayed", "atBats", "runs", "hits", "doubles", "homeRuns", "rbi", "stolenBases", "baseOnBalls", "strikeOuts", "avg", "obp", "slg", "ops"]
    header = "| 赛季 | G | AB | R | H | 2B | HR | RBI | SB | BB | SO | AVG | OBP | SLG | OPS |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
    row = f"| {season_label} |" + "".join(f" {fmt(h.get(c))} |" for c in cols)
    return header + row


def pitching_table(p, season_label):
    cols = [("gamesPlayed",), ("gamesStarted",), ("wins", "losses", "-"), ("era",), ("inningsPitched",), ("hits",), ("runs",), ("earnedRuns",), ("homeRuns",), ("baseOnBalls",), ("strikeOuts",), ("whip",), ("strikeoutsPer9Inn",), ("walksPer9Inn",)]
    header = "| 赛季 | G | GS | W-L | ERA | IP | H | R | ER | HR | BB | SO | WHIP | K/9 | BB/9 |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
    cells = []
    for c in cols:
        if len(c) == 3:
            cells.append(f"{fmt(p.get('wins'))}-{fmt(p.get('losses'))}")
        else:
            cells.append(fmt(p.get(c[0])))
    row = f"| {season_label} | " + " | ".join(cells) + " |"
    return header + row


def build_report(player, info, s26, s25):
    name = player["name"]
    slug = slugify(name)
    pos = player.get("pos", "")
    roster_status = player.get("statusCn", "")
    departed = player.get("departed")
    two_way = has_bat(s26) and has_pit(s26)
    is_p = (pos == "P" and not has_bat(s26)) or (not has_bat(s26) and has_pit(s26))

    h26, h25 = s26.get("hitting", {}), s25.get("hitting", {})
    p26, p25 = s26.get("pitching", {}), s25.get("pitching", {})

    if two_way:
        grades, key_val = hitting_grades(h26)
        pgrades, _ = pitching_grades(p26)
        grades_line = f"综合评分 {round(sum(grades.values())/len(grades))}（打击）/ {round(sum(pgrades.values())/len(pgrades))}（投球）"
    elif is_p:
        grades, key_val = pitching_grades(p26)
        grades_line = f"综合评分 {round(sum(grades.values())/len(grades))}（{grade_label(sum(grades.values())/len(grades))} 级）"
    else:
        grades, key_val = hitting_grades(h26)
        grades_line = f"综合评分 {round(sum(grades.values())/len(grades))}（{grade_label(sum(grades.values())/len(grades))} 级）"

    # 数据驱动总评
    if two_way:
        summary = hitter_note(h26, h25) + " 投球端：" + pitcher_note(p26, p25)
    elif is_p:
        summary = pitcher_note(p26, p25)
    else:
        summary = hitter_note(h26, h25)
    if departed:
        summary += f" 该球员已离队（{departed}），本报告为道奇时期最终数据存档。"
    g26 = int(h26.get("gamesPlayed") or p26.get("gamesPlayed") or 0)
    if g26 and g26 < 40:
        summary += f" 注意：本赛季仅 {g26} 场出赛，属小样本，数据波动大，评价需谨慎。"

    # 优势/劣势
    strengths, weaknesses = [], []
    if not is_p and h26:
        obp_gap = (f2(h26.get("obp")) or 0) - (f2(h26.get("avg")) or 0)
        if obp_gap >= .06: strengths.append(f"选球耐心好（OBP-AVG 差距 {obp_gap:.3f}，保送贡献稳定）")
        if f2(h26.get("ops")) and f2(h26.get("ops")) >= .800: strengths.append(f"攻击指数 OPS {h26.get('ops')} 高于联盟平均")
        if int(h26.get("homeRuns") or 0) >= 20: strengths.append(f"单季 {h26.get('homeRuns')} 轰的长打火力")
        if obp_gap <= .025: weaknesses.append("上垒过度依赖安打，保送产出偏低")
        if f2(h26.get("ops")) and f2(h26.get("ops")) < .700: weaknesses.append(f"OPS {h26.get('ops')} 低于联盟平均，进攻效率不足")
        pa = float(h26.get("plateAppearances") or 0)
        if pa and float(h26.get("strikeOuts") or 0) / pa > .27: weaknesses.append("三振率偏高，接触稳定性待提升")
    if (is_p or two_way) and p26:
        if f2(p26.get("strikeoutsPer9Inn")) and f2(p26.get("strikeoutsPer9Inn")) >= 10: strengths.append(f"三振能力出色（K/9 {p26.get('strikeoutsPer9Inn')}）")
        if f2(p26.get("era")) and f2(p26.get("era")) <= 3.00: strengths.append(f"ERA {p26.get('era')} 属于联盟上乘")
        if f2(p26.get("whip")) and f2(p26.get("whip")) <= 1.10: strengths.append(f"WHIP {p26.get('whip')}，压制造打者能力佳")
        if int(p26.get("saves") or 0) > 0: strengths.append(f"{p26.get('saves')} 次救援成功，可担任终结者")
        if f2(p26.get("era")) and f2(p26.get("era")) >= 5.00: weaknesses.append(f"ERA {p26.get('era')} 过高，压制力明显不足")
        if f2(p26.get("walksPer9Inn")) and f2(p26.get("walksPer9Inn")) >= 4.0: weaknesses.append(f"BB/9 {p26.get('walksPer9Inn')} 控球失稳")
        if f2(p26.get("whip")) and f2(p26.get("whip")) >= 1.45: weaknesses.append(f"WHIP {p26.get('whip')}，每局上垒人数过多")
    if not strengths: strengths.append("具备大联盟级别身手与稳定角色")
    if not weaknesses: weaknesses.append("需在更长样本中证明稳定性")

    grade_rows = "\n".join(f"| {k} | {v} | {grade_label(v)} |" for k, v in grades.items())

    # 数据表
    tables = []
    if h26 or h25:
        blocks = []
        if h25: blocks.append(hitting_table(h25, "2025"))
        if h26: blocks.append(hitting_table(h26, str(SEASON)))
        tables.append(("📊 打击数据（2025 vs 2026）", "\n\n".join(blocks)))
    if p26 or p25:
        blocks = []
        if p25: blocks.append(pitching_table(p25, "2025"))
        if p26: blocks.append(pitching_table(p26, str(SEASON)))
        tables.append(("⚾ 投球数据（2025 vs 2026）", "\n\n".join(blocks)))
    tables_md = "\n\n---\n\n".join(f"## {t}\n\n{b}" for t, b in tables)

    role_line = roster_status + (f"（{departed}）" if departed else "")
    two_way_line = "\n> ⚡ **二刀流球员**：本季同时贡献打击与投球。\n" if two_way else ""

    md = f"""# {name} 球探报告（{SEASON} 赛季最终版）

> **Los Angeles Dodgers #{fmt(info.get('primaryNumber',''))} | {pos} | 名单状态：{role_line}**
{two_way_line}> 
> 报告生成时间：{datetime.now().strftime('%Y-%m-%d')} ｜ 数据：MLB Stats API 官方赛季数据

---

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| **全名** | {fmt(info.get('fullName', name))} |
| **出生日期** | {fmt(info.get('birthDate'))}（{fmt(info.get('currentAge'))}岁） |
| **出生地** | {fmt(info.get('birthCity'))}, {fmt(info.get('birthCountry'))} |
| **身高/体重** | {fmt(info.get('height'))} / {fmt(info.get('weight'))} lbs |
| **击球/投球** | {fmt((info.get('batSide') or {{}}).get('description'))} / {fmt((info.get('pitchHand') or {{}}).get('description'))} |
| **MLB首秀** | {fmt(info.get('mlbDebutDate'))} |
| **守备位置** | {fmt((info.get('primaryPosition') or {{}}).get('name', pos))} |

---

## 🔍 球探总评

{summary}

---

{tables_md}

---

## ✅ 优势

{chr(10).join('- ✅ ' + s for s in strengths)}

## ⚠️ 劣势

{chr(10).join('- ⚠️ ' + w for w in weaknesses)}

---

## 📊 综合评分（20-80 分制）

| 项目 | 评分 | 等级 |
|------|------|------|
{grade_rows}

### {grades_line}

---

## 🔮 未来展望

{name} {SEASON} 赛季的最终数据已定格。{"其攻防两端的双向价值若能延续，将是联盟稀缺的顶级资产。" if two_way else "其未来走向取决于健康、角色定位与关键数据的稳定性。"}{f" 球员已离开道奇（{departed}），祝其职业生涯下一阶段顺利。" if departed else ""}

---

*数据来源：MLB.com | MLB Stats API（stats=season）*
*报告生成：{datetime.now().strftime('%Y-%m-%d')} ｜ 道奇 {SEASON} 赛季球员报告最终版*
"""
    return md


def build_html(name, md, slug):
    body = md
    body = re.sub(r'^# (.+)$', r'<h1>\1</h1>', body, flags=re.M)
    body = re.sub(r'^## (.+)$', r'<h2>\1</h2>', body, flags=re.M)
    body = re.sub(r'^### (.+)$', r'<h3>\1</h3>', body, flags=re.M)
    body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', body)
    body = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', body, flags=re.M)
    lines = body.split('\n'); out = []; in_ul = False; in_table = False
    for line in lines:
        m = re.match(r'^(\s*)-\s+(.+)$', line)
        if m:
            if not in_ul: out.append('<ul>'); in_ul = True
            out.append(f'<li>{m.group(2)}</li>'); continue
        if in_ul: out.append('</ul>'); in_ul = False
        if line.strip().startswith('|') and line.strip().endswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if set(''.join(cells)) <= set('-: '):
                continue
            if not in_table:
                out.append('<table class="comparison-table">'); in_table = True; is_header = True
            if cells and cells[0] in ('赛季', '项目'):
                out.append('<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>')
            else:
                out.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
            continue
        if in_table: out.append('</table>'); in_table = False
        out.append(line)
    if in_ul: out.append('</ul>')
    if in_table: out.append('</table>')
    body = '\n'.join(out)
    body = body.replace('<h2>📋 基本信息</h2>', f'<div style="text-align:center;"><img src="{slug}_report_cover.png" style="width:100%;max-width:800px;border-radius:10px;"></div>\n<h2>📋 基本信息</h2>')
    body = re.sub(r'<h2>📊 打击数据.*?</h2>', f'<h2>📊 打击数据（2025 vs 2026）</h2>\n<div style="text-align:center;margin:20px 0;"><img src="{slug}_season_comparison.png" style="width:100%;max-width:700px;border-radius:10px;"></div>', body)
    body = re.sub(r'<h2>⚾ 投球数据.*?</h2>', f'<h2>⚾ 投球数据（2025 vs 2026）</h2>\n<div style="text-align:center;margin:20px 0;"><img src="{slug}_season_comparison.png" style="width:100%;max-width:700px;border-radius:10px;"></div>', body)
    body = body.replace('<h2>📊 综合评分（20-80 分制）</h2>', f'<h2>📊 综合评分（20-80 分制）</h2>\n<div style="text-align:center;margin:20px 0;"><img src="{slug}_overall_grades.png" style="width:100%;max-width:600px;border-radius:10px;"></div>')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} 球探报告（{SEASON} 最终版）</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif; background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%); color:#e0e0e0; line-height:1.6; min-height:100vh; }}
.container {{ max-width:1100px; margin:0 auto; padding:20px; }}
h1 {{ text-align:center; padding:30px 0; color:#fff; background:linear-gradient(90deg,#005A9C,#1a5490,#005A9C); border-radius:15px; margin-bottom:25px; }}
h2 {{ color:#4fc3f7; margin:25px 0 15px; border-bottom:2px solid #4fc3f7; padding-bottom:8px; }}
h3 {{ color:#ff9800; margin:18px 0 12px; }}
.comparison-table {{ width:100%; border-collapse:collapse; margin:15px 0; font-size:.95em; }}
.comparison-table th,.comparison-table td {{ padding:10px; text-align:center; border-bottom:1px solid rgba(255,255,255,.1); }}
.comparison-table th {{ background:rgba(0,90,156,.3); color:#4fc3f7; }}
blockquote {{ border-left:4px solid #ff9800; padding-left:15px; margin:12px 0; color:#90a4ae; font-style:italic; }}
ul {{ margin-left:20px; line-height:2; }}
</style>
</head>
<body><div class="container">
{body}
<div style="text-align:center;padding:20px;color:#90a4ae;font-size:.9em;">数据来源：MLB.com | MLB Stats API ｜ 道奇 {SEASON} 赛季球员报告最终版</div>
</div></body></html>"""


def main():
    ok, fail = [], []
    for player in ROSTER["players"]:
        name = player["name"]
        slug = slugify(name)
        try:
            info, s26, s25 = load_raw(player["id"])
            if not info:
                raise RuntimeError(f"no raw data ({player['id']})")
            player_dir = REPORT_ROOT / slug
            player_dir.mkdir(parents=True, exist_ok=True)
            two_way = has_bat(s26) and has_pit(s26)
            is_p = not has_bat(s26) and has_pit(s26)
            generate_cover(player_dir, slug, name, info, s26)
            generate_season_comparison(player_dir, slug, s25, s26, is_p, two_way)
            if two_way:
                grades, _ = hitting_grades(s26["hitting"])
            elif is_p:
                grades, _ = pitching_grades(s26["pitching"])
            else:
                grades, _ = hitting_grades(s26["hitting"])
            generate_grades_radar(player_dir, slug, grades, f"{name} - Overall Grades")
            md = build_report(player, info, s26, s25)
            html = build_html(name, md, slug)
            (player_dir / f"{slug}-scouting-report.md").write_text(md, encoding="utf-8")
            (player_dir / f"{slug}-scouting-report.html").write_text(html, encoding="utf-8")
            ok.append(name)
            print(f"OK {name}", flush=True)
        except Exception as e:
            fail.append((name, repr(e)))
            print(f"FAIL {name}: {e!r}", flush=True)
    print(f"\nDone: {len(ok)} ok, {len(fail)} failed", flush=True)
    for n, e in fail:
        print(f"  FAILED: {n}: {e}", flush=True)


if __name__ == "__main__":
    main()
