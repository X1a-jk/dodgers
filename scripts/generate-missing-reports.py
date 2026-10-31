#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate scouting reports for Dodgers players (2026-10-17 定稿版).

- PLAYERS 从 data\\season-roster.json 加载（已完成 8 人在 DONE 中跳过）
- 数据驱动分析：备注/优势/劣势/评分全部按赛季最终数据生成
- 单人 try/except 生存 + API 重试 + 直连（绕过失效系统代理）
"""

import json
import os
import re
import textwrap
import urllib.request
from pathlib import Path
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

SEASON = datetime.now().year
REPORT_ROOT = Path("D:/baseball/report")
SEASON_ROSTER_JSON = Path("D:/baseball/data/season-roster.json")

# 2026-10-17 已完成的 8 人，跳过
DONE = {"Edwin Díaz", "Enrique Hernández", "Jonathan Hernández", "Teoscar Hernández",
        "Santiago Espinal", "Chuckie Robinson", "Cole Irvin", "Jake Eder"}

_PITCH_POS = {"P", "SP", "RP", "CL"}


def load_players_from_roster() -> list:
    data = json.loads(SEASON_ROSTER_JSON.read_text(encoding="utf-8"))
    out = []
    for r in data["players"]:
        if r["name"] in DONE:
            continue
        pos = (r.get("pos") or "").upper()
        has_pit = bool(r.get("pit"))
        has_bat = bool(r.get("bat"))
        if has_pit and not has_bat:
            ptype = "Pitcher"
        elif pos in _PITCH_POS and not has_bat:
            ptype = "Pitcher"
        elif has_pit and has_bat:
            ptype = "TwoWay"
        else:
            ptype = "Position"
        out.append({"id": r["id"], "name": r["name"], "position_type": ptype})
    return out


PLAYERS = load_players_from_roster()
if os.environ.get("MAXP"):
    PLAYERS = PLAYERS[: int(os.environ["MAXP"])]


def slugify(name: str) -> str:
    import unicodedata
    normalized = unicodedata.normalize('NFKD', name)
    ascii_name = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return re.sub(r"[^a-z0-9-]", "", ascii_name.lower().replace(" ", "-").replace("'", "").replace(".", ""))


_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # 直连，绕过本机注册表里的失效代理 (2026-10-17)


def fetch_json(url: str) -> dict:
    import time
    last_err = None
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
            with _OPENER.open(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            last_err = e
            wait = min(60, 5 * (2 ** attempt)) + attempt * 2
            print(f"  [retry {attempt + 1}/6] {type(e).__name__}: {e} — wait {wait:.0f}s", flush=True)
            time.sleep(wait)
    raise last_err


def fetch_team_season_stats(team_id: int, group: str, season: int) -> dict:
    """一次性拉整队赛季数据，返回 {player_id: stat}。比逐人查询温和得多（WAF 限速友好）。"""
    url = f"https://statsapi.mlb.com/api/v1/stats?stats=season&group={group}&playerPool=ALL&teamId={team_id}&season={season}"
    data = fetch_json(url)
    out = {}
    for st in data.get("stats", []):
        for split in st.get("splits", []):
            pid = (split.get("player") or {}).get("id")
            s = split.get("stat") or {}
            if pid and s:
                out[pid] = s
    return out


_TEAM_STATS_CACHE = {}


def get_team_stats(group: str, season: int) -> dict:
    key = (group, season)
    if key not in _TEAM_STATS_CACHE:
        _TEAM_STATS_CACHE[key] = fetch_team_season_stats(119, group, season)
        print(f"  [cache] {group} {season}: {len(_TEAM_STATS_CACHE[key])} players", flush=True)
    return _TEAM_STATS_CACHE[key]


def fetch_player(person_id: int) -> dict:
    url = f"https://statsapi.mlb.com/api/v1/people/{person_id}"
    return fetch_json(url)["people"][0]


def fetch_season_stats(person_id: int, season: int) -> dict:
    return {
        "hitting": get_team_stats("hitting", season).get(person_id, {}),
        "pitching": get_team_stats("pitching", season).get(person_id, {}),
    }


def fmt(value, default="-"):
    if value is None or value == "":
        return default
    return value


# ---------------------------------------------------------------------------
# 图表生成
# ---------------------------------------------------------------------------

def generate_cover(player_dir: Path, name: str, info: dict, stats: dict):
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    ax.axis('off')
    ax.text(0.05, 0.85, "⚾", fontsize=80, color='#ff9800', transform=ax.transAxes)
    ax.text(0.2, 0.75, name, fontsize=32, color='white', fontweight='bold', transform=ax.transAxes)
    subtitle = f"Los Angeles Dodgers #{fmt(info.get('primaryNumber',''))} | {fmt(info.get('primaryPosition',{}).get('abbreviation',''))}"
    ax.text(0.2, 0.62, subtitle, fontsize=16, color='#90a4ae', transform=ax.transAxes)
    ax.text(0.2, 0.52, f"{fmt(info.get('batSide',{}).get('description',''))} / {fmt(info.get('pitchHand',{}).get('description',''))}  |  Age {fmt(info.get('currentAge',''))}", fontsize=13, color='#e0e0e0', transform=ax.transAxes)
    if stats.get('pitching') and not stats.get('hitting'):
        s = stats['pitching']
        line = f"ERA {fmt(s.get('era'))}  |  WHIP {fmt(s.get('whip'))}  |  {fmt(s.get('wins'))}-{fmt(s.get('losses'))}  |  {fmt(s.get('strikeOuts'))} K"
    elif stats.get('pitching') and stats.get('hitting'):
        s = stats['pitching']
        h = stats['hitting']
        line = f"{fmt(h.get('avg'))}/{fmt(h.get('obp'))}/{fmt(h.get('slg'))}  |  {fmt(h.get('homeRuns'))} HR  |  投球 ERA {fmt(s.get('era'))}"
    else:
        s = stats.get('hitting', {})
        line = f"{fmt(s.get('avg'))}/{fmt(s.get('obp'))}/{fmt(s.get('slg'))}  |  {fmt(s.get('homeRuns'))} HR  |  {fmt(s.get('rbi'))} RBI"
    ax.text(0.2, 0.42, line, fontsize=14, color='#ff9800', fontweight='bold', transform=ax.transAxes)
    fig.savefig(player_dir / f"{slugify(name)}_report_cover.png", dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close(fig)


def generate_radar(name: str, labels: list, values: list, out_path: Path, title: str):
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values_plot = values + values[:1]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True), facecolor='#1a1a2e')
    ax.set_facecolor('#16213e')
    ax.plot(angles, values_plot, color='#ff9800', linewidth=2)
    ax.fill(angles, values_plot, color='#ff9800', alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='white', size=10)
    ax.set_ylim(20, 80)
    ax.set_yticks([30, 50, 70])
    ax.set_yticklabels(['30', '50', '70'], color='#90a4ae', size=8)
    ax.set_title(title, color='white', fontsize=14, fontweight='bold', pad=20)
    fig.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close(fig)


def generate_season_comparison(player_dir: Path, name: str, stats_2025: dict, stats_2026: dict, is_pitcher: bool):
    labels = []
    v2025 = []
    v2026 = []
    if is_pitcher:
        labels = ['ERA', 'WHIP', 'K/9', 'BB/9']
        s25 = stats_2025.get('pitching', {})
        s26 = stats_2026.get('pitching', {})
        # For ERA/WHIP lower is better; invert for radar display
        def inv(x, default=5.0):
            try:
                return max(20, 80 - float(x) * 10)
            except Exception:
                return 40
        v2025 = [inv(s25.get('era')), inv(s25.get('whip')), min(80, float(s25.get('strikeOutsPer9Inn', 0) or 0) * 4 + 20), max(20, 80 - float(s25.get('basesOnBallsPer9Inn', 0) or 0) * 8)]
        v2026 = [inv(s26.get('era')), inv(s26.get('whip')), min(80, float(s26.get('strikeOutsPer9Inn', 0) or 0) * 4 + 20), max(20, 80 - float(s26.get('basesOnBallsPer9Inn', 0) or 0) * 8)]
    else:
        labels = ['AVG', 'OBP', 'SLG', 'OPS']
        def scale(x):
            try:
                return float(x) * 100
            except Exception:
                return 40
        s25 = stats_2025.get('hitting', {})
        s26 = stats_2026.get('hitting', {})
        v2025 = [scale(s25.get('avg')), scale(s25.get('obp')), scale(s25.get('slg')), scale(s25.get('ops'))]
        v2026 = [scale(s26.get('avg')), scale(s26.get('obp')), scale(s26.get('slg')), scale(s26.get('ops'))]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    v2025 += v2025[:1]; v2026 += v2026[:1]; angles += angles[:1]
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True), facecolor='#1a1a2e')
    ax.set_facecolor('#16213e')
    ax.plot(angles, v2025, color='#4fc3f7', linewidth=2, label='2025')
    ax.fill(angles, v2025, color='#4fc3f7', alpha=0.15)
    ax.plot(angles, v2026, color='#ff9800', linewidth=2, label='2026')
    ax.fill(angles, v2026, color='#ff9800', alpha=0.15)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='white', size=11)
    ax.set_ylim(20, 100)
    ax.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
    ax.set_title('2025 vs 2026 Season Comparison', color='white', fontsize=14, fontweight='bold', pad=20)
    out = player_dir / f"{slugify(name)}_season_comparison.png"
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close(fig)


# ---------------------------------------------------------------------------
# 数据驱动分析引擎
# ---------------------------------------------------------------------------

def _f(x, default=None):
    try:
        if x in (None, "", "-"):
            return default
        return float(x)
    except (TypeError, ValueError):
        return default


def _i(x, default=0):
    v = _f(x)
    return int(v) if v is not None else default


def _tier(value, table, default):
    """value 从大到小匹配 table: [(阈值, 分数)...]，返回对应分数"""
    if value is None:
        return default
    for threshold, score in table:
        if value >= threshold:
            return score
    return default


def _cmp(new, old, good_when_high=True, fmt="{:.3f}"):
    """返回 (差值文案, 方向词)"""
    if new is None or old is None:
        return "", ""
    diff = new - old
    if good_when_high:
        word = "提升" if diff > 0.005 else ("下滑" if diff < -0.005 else "持平")
    else:
        word = "下滑" if diff > 0.005 else ("提升" if diff < -0.005 else "持平")
    try:
        return f"{fmt.format(new)} vs 去年 {fmt.format(old)}（{word} {abs(diff):.3f}）", word
    except Exception:
        return "", ""


def _hitter_grades(s, pos):
    avg = _f(s.get("avg")); slg = _f(s.get("slg"))
    ab = _i(s.get("atBats")); bb = _i(s.get("baseOnBalls"))
    sb = _i(s.get("stolenBases"))
    pa = ab + bb
    bbrate = (bb / pa * 100) if pa else None
    contact = _tier(avg, [(0.320, 70), (0.300, 65), (0.280, 60), (0.260, 55), (0.240, 50), (0.220, 45)], 40)
    power = _tier(slg, [(0.550, 70), (0.500, 65), (0.450, 60), (0.400, 55), (0.350, 50), (0.300, 45)], 40)
    discipline = _tier(bbrate, [(16, 70), (13, 65), (11, 60), (9, 55), (7, 50), (5, 45)], 40)
    speed = _tier(sb, [(30, 70), (20, 65), (12, 60), (7, 55), (3, 50), (1, 45)], 40)
    defense = 55 if pos in ("C", "SS", "2B", "CF") else (50 if pos in ("1B", "3B", "LF", "RF") else 45)
    arm = 60 if pos in ("C", "RF", "3B", "SS") else (55 if pos in ("LF", "CF") else 50)
    return {"Contact": contact, "Power": power, "Discipline": discipline,
            "Speed": speed, "Defense": defense, "Arm": arm}


def _pitcher_grades(s):
    era = _f(s.get("era")); whip = _f(s.get("whip"))
    k9 = _f(s.get("strikeOutsPer9Inn")) or _f(s.get("strikeOutsPer9Innings"))
    bb9 = _f(s.get("basesOnBallsPer9Inn")) or _f(s.get("basesOnBallsPer9Innings"))
    ip = _f(s.get("inningsPitched"))
    fb = _tier(k9, [(11, 70), (10, 65), (9, 60), (8, 55), (7, 50), (6, 45)], 40)
    ctl = _tier(bb9, [(0, 70), (1.8, 65), (2.4, 60), (3.0, 55), (3.6, 50), (4.2, 45)], 40) if bb9 is not None else 50
    if bb9 is not None and bb9 > 6:
        ctl = 35
    cmd = _tier(whip, [(0, 70), (1.00, 65), (1.15, 60), (1.25, 55), (1.40, 50), (1.55, 45)], 40)
    stam = _tier(ip, [(180, 70), (150, 65), (120, 60), (90, 55), (60, 50), (30, 45)], 40)
    return {"Fastball": fb, "Offspeed": 55, "Control": ctl, "Command": cmd,
            "Stamina": stam, "Mental": 55}


def _role_pitcher(s):
    g = _i(s.get("gamesPlayed")); gs = _i(s.get("gamesStarted")); ip = _f(s.get("inningsPitched")) or 0
    if gs == 0 and g > 0:
        return "长中继/多局后援" if ip / g >= 1.5 else "一局型后援"
    if gs > 0 and gs < g:
        return "swingman（先发/后援两用）"
    if gs > 0:
        return "先发投手"
    return "投手"


def _hitter_bundle(name, s26, s25, pos):
    g = _i(s26.get("gamesPlayed")); ab = _i(s26.get("atBats"))
    avg = _f(s26.get("avg")); obp = _f(s26.get("obp")); slg = _f(s26.get("slg")); ops = _f(s26.get("ops"))
    hr = _i(s26.get("homeRuns")); rbi = _i(s26.get("rbi")); sb = _i(s26.get("stolenBases"))
    bb = _i(s26.get("baseOnBalls")); so = _i(s26.get("strikeOuts"))
    small = g < 40
    pts, strengths, weaknesses = [], [], []

    if avg is not None:
        tier = "elite" if avg >= .300 else ("优秀" if avg >= .280 else ("稳定" if avg >= .250 else ("偏低" if avg >= .220 else "挣扎")))
        cmp_txt, _ = _cmp(avg, _f(s25.get("avg")))
        pts.append(f"**打击率 {avg:.3f}**（{tier}）{cmp_txt} — " + (
            "击球品质出色，contact 能力可靠" if avg >= .280 else
            "具备一定 contact 能力" if avg >= .250 else
            "击球稳定性不足，需调整打击机制与选球"))
        (strengths if avg >= .270 else weaknesses).append(f"打击率 {avg:.3f}" + ("，高水准 contact" if avg >= .300 else ""))
    if obp is not None and avg is not None:
        gap = obp - avg
        word = "选球眼极佳，保送贡献大" if gap >= .085 else ("上垒能力合格" if gap >= .055 else "上垒主要依赖打击率，保送偏少")
        pts.append(f"**上垒率 {obp:.3f}**（OBP-AVG 差 {gap:.3f}）— {word}，{bb} 次保送")
        if gap >= .085:
            strengths.append(f"选球眼出色（{bb} BB）")
        if gap < .045 and avg is not None and avg < .260:
            weaknesses.append("保送偏少，上垒效率低")
    if slg is not None:
        iso = slg - (avg or 0)
        cmp_txt, _ = _cmp(slg, _f(s25.get("slg")))
        pts.append(f"**长打率 {slg:.3f}**（ISO {iso:.3f}）{cmp_txt} — " + (
            "重炮级长打火力" if slg >= .500 else
            "长打火力扎实" if slg >= .430 else
            "长打产出一般，以 gap power 为主" if slg >= .380 else
            "长打威胁有限"))
        if slg >= .470:
            strengths.append(f"长打火力（{slg:.3f} SLG）")
        if slg < .350 and g >= 60:
            weaknesses.append("长打威胁有限")
    if hr or rbi:
        pts.append(f"**全垒打 {hr} 支 / 打点 {rbi} 分** — " + (
            f"约每 {max(g,1)/max(hr,1):.0f} 场 1 轰，run production 可观" if hr >= 20 else
            f"有一定 run production，但产量与先发角色相比偏少" if hr >= 10 and g >= 100 else
            "run production 有限，多为角色球员产量"))
        if hr >= 25:
            strengths.append(f"{hr} 轰的火力输出")
        if g >= 120 and hr < 12:
            weaknesses.append(f"全垒打产量偏低（{hr} 轰 / {g} 场）")
    if so and g:
        rate = so / g
        if rate >= 1.3:
            pts.append(f"**三振 {so} 次（场均 {rate:.1f} 次）** — 挥空率偏高，contact 与 power 的 trade-off 明显")
            weaknesses.append("三振率偏高")
        elif rate <= 0.55 and ab:
            pts.append(f"**三振 {so} 次（场均 {rate:.1f} 次）** — 控棒能力出色，三振率低")
            strengths.append("低三振率")
    if sb:
        pts.append(f"**盗垒 {sb} 次** — 具备跑垒威胁")
    if g:
        pts.append(f"**出赛 {g} 场** — " + (
            "全勤级别的耐久度，球队倚重的日常战力" if g >= 150 else
            "出赛稳定" if g >= 100 else
            "出勤中规中矩" if g >= 60 else
            "出赛样本小，多为轮换/伤停影响"))
    if small:
        pts.append("⚠️ **小样本警告**：出赛不足 40 场，以上数据仅供参考，不宜过度解读")

    ops_cmp, trend = _cmp(ops, _f(s25.get("ops")))
    if ops_cmp:
        pts.append(f"**OPS {ops:.3f}** {ops_cmp}")

    grades = _hitter_grades(s26, pos)
    if not strengths:
        strengths = ["多位置弹性与阵容深度价值"]
    if not weaknesses:
        weaknesses = ["整体工具平均，缺乏精英级单一项"] if not small else ["样本过小，真实水平待观察"]
    return pts, strengths[:3], weaknesses[:3], grades, trend or "持平", small


def _pitcher_bundle(name, s26, s25):
    g = _i(s26.get("gamesPlayed")); gs = _i(s26.get("gamesStarted"))
    era = _f(s26.get("era")); whip = _f(s26.get("whip"))
    ip = _f(s26.get("inningsPitched")) or 0
    w = _i(s26.get("wins")); l = _i(s26.get("losses")); so = _i(s26.get("strikeOuts"))
    k9 = _f(s26.get("strikeOutsPer9Inn")) or _f(s26.get("strikeOutsPer9Innings"))
    bb9 = _f(s26.get("basesOnBallsPer9Inn")) or _f(s26.get("basesOnBallsPer9Innings"))
    sv = _i(s26.get("saves")); role = _role_pitcher(s26)
    small = ip < 25
    pts, strengths, weaknesses = [], [], []

    cmp_era, trend = _cmp(era, _f(s25.get("era")), good_when_high=False)
    if era is not None:
        tier = "联盟顶级" if era < 2.50 else ("优秀" if era < 3.50 else ("合格" if era < 4.50 else "偏高"))
        pts.append(f"**ERA {era:.2f}**（{tier}）{cmp_era} — " + (
            "压制力出色，值得高杠杆信任" if era < 3.00 else
            "压制力可靠" if era < 4.00 else
            "压制力平平，需依靠球团支援" if era < 5.00 else
            "失分偏高，有被对手重创的风险"))
        (strengths if era < 3.20 else weaknesses if era > 4.50 else []).append(f"ERA {era:.2f}")
    if whip is not None:
        pts.append(f"**WHIP {whip:.2f}** — " + (
            "上垒压制极佳" if whip < 1.10 else
            "上垒压制合格" if whip < 1.30 else
            "允许过多上垒，局数压力大"))
        if whip >= 1.50:
            weaknesses.append(f"WHIP {whip:.2f}，上垒过多")
        elif whip < 1.05:
            strengths.append(f"WHIP {whip:.2f} 的低上垒率")
    if k9 is not None:
        word = "三振武器顶级" if k9 >= 11 else "三振能力强" if k9 >= 9 else "三振能力平均" if k9 >= 7.5 else "三振能力偏弱，靠制造击球出局"
        pts.append(f"**K/9 {k9:.1f}**（{so}K）— {word}")
        if k9 >= 10:
            strengths.append(f"K/9 {k9:.1f} 的三振火力")
        if k9 < 6.5 and ip > 40:
            weaknesses.append("三振能力偏弱")
    if bb9 is not None:
        word = "控球精英" if bb9 < 2.0 else "控球稳定" if bb9 < 3.0 else "控球不稳，保送偏多" if bb9 < 4.5 else "控球失控，急需修正"
        pts.append(f"**BB/9 {bb9:.1f}** — {word}")
        if bb9 >= 4.5:
            weaknesses.append(f"BB/9 {bb9:.1f} 控球需修正")
        elif bb9 < 2.2 and ip > 30:
            strengths.append("控球稳定")
    if ip:
        pts.append(f"**{ip:.1f} 局 / {g} 场**（角色：{role}）— " + (
            "负担量大，是轮值/牛棚骨干" if ip >= 150 else
            "出赛局数稳定" if ip >= 60 else
            "吃局数有限"))
    if sv:
        pts.append(f"**救援成功 {sv} 次** — 终结者经验")
        strengths.append(f"{sv} 次救援成功")
    if small:
        pts.append("⚠️ **小样本警告**：投球局数不足 25 局，数据波动大，仅供参考")
    if w or l:
        pts.append(f"**战绩 {w}-{l}**")

    grades = _pitcher_grades(s26)
    if not strengths:
        strengths = ["可信赖的阵容深度 arms"]
    if not weaknesses:
        weaknesses = ["无明显短板，但缺乏 elite 级武器"] if not small else ["样本过小，真实水平待观察"]
    return pts, strengths[:3], weaknesses[:3], grades, trend or "持平", small, role


def _grade_label(v):
    if v >= 70: return "A+ (精英)"
    if v >= 65: return "A (优秀)"
    if v >= 60: return "A- / B+ (良好)"
    if v >= 55: return "B+ (高于平均)"
    if v >= 50: return "B (平均)"
    if v >= 45: return "B- (略低于平均)"
    if v >= 40: return "C+ (边缘)"
    return "C (偏弱)"


def _hitting_table(s25, s26):
    return f"""| 赛季 | G | AB | R | H | 2B | 3B | HR | RBI | SB | BB | SO | AVG | OBP | SLG | OPS |
|------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025 | {fmt(s25.get('gamesPlayed'))} | {fmt(s25.get('atBats'))} | {fmt(s25.get('runs'))} | {fmt(s25.get('hits'))} | {fmt(s25.get('doubles'))} | {fmt(s25.get('triples'))} | {fmt(s25.get('homeRuns'))} | {fmt(s25.get('rbi'))} | {fmt(s25.get('stolenBases'))} | {fmt(s25.get('baseOnBalls'))} | {fmt(s25.get('strikeOuts'))} | {fmt(s25.get('avg'))} | {fmt(s25.get('obp'))} | {fmt(s25.get('slg'))} | {fmt(s25.get('ops'))} |
| 2026 | {fmt(s26.get('gamesPlayed'))} | {fmt(s26.get('atBats'))} | {fmt(s26.get('runs'))} | {fmt(s26.get('hits'))} | {fmt(s26.get('doubles'))} | {fmt(s26.get('triples'))} | {fmt(s26.get('homeRuns'))} | {fmt(s26.get('rbi'))} | {fmt(s26.get('stolenBases'))} | {fmt(s26.get('baseOnBalls'))} | {fmt(s26.get('strikeOuts'))} | {fmt(s26.get('avg'))} | {fmt(s26.get('obp'))} | {fmt(s26.get('slg'))} | {fmt(s26.get('ops'))} |"""


def _pitching_table(s25, s26):
    return f"""| 赛季 | G | GS | W-L | ERA | IP | H | R | ER | HR | BB | SO | WHIP | K/9 | BB/9 |
|------|---|---|-----|------|------|---|---|---|---|---|---|------|------|------|
| 2025 | {fmt(s25.get('gamesPlayed'))} | {fmt(s25.get('gamesStarted'))} | {fmt(s25.get('wins'))}-{fmt(s25.get('losses'))} | {fmt(s25.get('era'))} | {fmt(s25.get('inningsPitched'))} | {fmt(s25.get('hits'))} | {fmt(s25.get('runs'))} | {fmt(s25.get('earnedRuns'))} | {fmt(s25.get('homeRuns'))} | {fmt(s25.get('baseOnBalls'))} | {fmt(s25.get('strikeOuts'))} | {fmt(s25.get('whip'))} | {fmt(s25.get('strikeOutsPer9Inn'))} | {fmt(s25.get('basesOnBallsPer9Inn'))} |
| 2026 | {fmt(s26.get('gamesPlayed'))} | {fmt(s26.get('gamesStarted'))} | {fmt(s26.get('wins'))}-{fmt(s26.get('losses'))} | {fmt(s26.get('era'))} | {fmt(s26.get('inningsPitched'))} | {fmt(s26.get('hits'))} | {fmt(s26.get('runs'))} | {fmt(s26.get('earnedRuns'))} | {fmt(s26.get('homeRuns'))} | {fmt(s26.get('baseOnBalls'))} | {fmt(s26.get('strikeOuts'))} | {fmt(s26.get('whip'))} | {fmt(s26.get('strikeOutsPer9Inn'))} | {fmt(s26.get('basesOnBallsPer9Inn'))} |"""


def build_analysis(name, info, stats_2025, stats_2026, pos_type):
    pos = (info.get("primaryPosition") or {}).get("abbreviation", "")
    s26h, s26p = stats_2026.get("hitting", {}), stats_2026.get("pitching", {})
    s25h, s25p = stats_2025.get("hitting", {}), stats_2025.get("pitching", {})
    two_way = pos_type == "TwoWay" or (bool(s26h) and bool(s26p))

    if pos_type == "Pitcher" or (bool(s26p) and not bool(s26h)):
        is_pitcher = True
        pts, strengths, weaknesses, grades, trend, small, role = _pitcher_bundle(name, s26p, s25p)
        g = _i(s26p.get("gamesPlayed"))
        era_v = _f(s26p.get("era"))
        summary = (f"{name} 2026 赛季担任{role}，出赛 {g} 场，ERA {f'{era_v:.2f}' if era_v is not None else '-'}、"
                   f"WHIP {_f(s26p.get('whip')) or '-'}、{_f(s26p.get('inningsPitched')) or 0:.1f} 局。")
        if era_v is not None:
            summary += (" 其压制力在联盟属上乘，是牛棚/轮值可倚重的人选。" if era_v < 3.20 else
                        " 整体表现符合角色预期，稳定性是其价值所在。" if era_v < 4.50 else
                        " 本季失分偏高，需在控球与配球策略上做出调整。")
        if small:
            summary += " 样本较小，评级仅供参考。"
        radar_labels = list(grades.keys())
        radar_values = list(grades.values())
        table = _pitching_table(s25p, s26p)
        extra = ""
    else:
        is_pitcher = False
        pts, strengths, weaknesses, grades, trend, small = _hitter_bundle(name, s26h, s25h, pos)
        g = _i(s26h.get("gamesPlayed"))
        ops_v = _f(s26h.get("ops"))
        summary = (f"{name} 2026 赛季出赛 {g} 场，缴出 {s26h.get('avg', '-')}/{s26h.get('obp', '-')}/"
                   f"{s26h.get('slg', '-')}、{s26h.get('homeRuns', '-')} 轰 {s26h.get('rbi', '-')} 打点的成绩。")
        if ops_v is not None:
            summary += (" 其进攻产出高居联盟前列，是打线核心。" if ops_v >= .900 else
                        " 进攻贡献稳定，是打线中坚。" if ops_v >= .780 else
                        " 进攻贡献一般，更多价值体现在其他方面。" if ops_v >= .680 else
                        " 本季打击表现低于预期，需要调整。")
        if small:
            summary += " 样本较小，评级仅供参考。"
        radar_labels = list(grades.keys())
        radar_values = list(grades.values())
        table = _hitting_table(s25h, s26h)
        extra = ""
        if two_way and s26p:
            extra = (
                "\n\n### 🥎 投球成绩（二刀流）\n\n"
                f"{_f(s26p.get('era')) or '-'} ERA / {_f(s26p.get('whip')) or '-'} WHIP / "
                f"{s26p.get('wins', '-')}-{s26p.get('losses', '-')} / "
                f"{_f(s26p.get('inningsPitched')) or 0:.1f} IP / {s26p.get('strikeOuts', '-')} K"
                " — 二刀流出赛，投球端同样贡献价值。"
            )

    analysis_md = "\n".join(f"- {p}" for p in pts)
    strengths_md = "\n".join(f"- ✅ {s}" for s in strengths)
    weaknesses_md = "\n".join(f"- ❌ {w}" for w in weaknesses)
    grades_rows = "\n".join(f"| {k} | {v} | {_grade_label(v)} |" for k, v in grades.items())
    overall = sum(grades.values()) / len(grades)
    grades_md = (
        "| 项目 | 评分 (20-80) | 等级 |\n"
        "|------|-------------|------|\n"
        f"{grades_rows}\n\n"
        f"### 总体评分：{overall:.0f} ({_grade_label(overall)})"
    )

    return {
        "is_pitcher": is_pitcher, "summary": summary, "table": table,
        "analysis": analysis_md + extra, "strengths": strengths_md,
        "weaknesses": weaknesses_md, "grades": grades_md,
        "radar_labels": radar_labels, "radar_values": radar_values,
        "trend": trend, "two_way": two_way,
    }


# ---------------------------------------------------------------------------
# 报告文本与 HTML
# ---------------------------------------------------------------------------

def build_markdown(name: str, info: dict, bundle: dict) -> str:
    pos = info.get('primaryPosition', {}).get('abbreviation', '')
    number = info.get('primaryNumber', '')
    bt = f"{fmt(info.get('batSide',{}).get('code',''))}/{fmt(info.get('pitchHand',{}).get('code',''))}"
    trend_word = {"提升": "上升", "下滑": "下滑"}.get(bundle["trend"], "持平")

    return f"""# {name} 球探报告

> **Los Angeles Dodgers #{number} | {pos} | {bt}**
> 
> 报告生成时间：{datetime.now().strftime('%Y-%m-%d')}（2026 赛季最终数据）

---

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| **全名** | {fmt(info.get('fullName'))} |
| **出生日期** | {fmt(info.get('birthDate'))} |
| **年龄** | {fmt(info.get('currentAge'))}岁 |
| **出生地** | {fmt(info.get('birthCity'))}, {fmt(info.get('birthCountry'))} |
| **身高/体重** | {fmt(info.get('height'))} / {fmt(info.get('weight'))} lbs |
| **击球/投球** | {fmt(info.get('batSide',{}).get('description'))} / {fmt(info.get('pitchHand',{}).get('description'))} |
| **MLB首秀** | {fmt(info.get('mlbDebutDate'))} |
| **背号** | #{number} |

---

## 🎯 球探总评

{bundle["summary"]}

---

## 📊 2025 vs 2026 赛季数据

{bundle["table"]}

---

## 🔍 球探分析

{bundle["analysis"]}

---

## ✅ 优势 vs ❌ 劣势

### 优势
{bundle["strengths"]}

### 劣势
{bundle["weaknesses"]}

---

## 📊 综合评分

{bundle["grades"]}

---

## 🔮 未来展望

{name} 2026 赛季整体呈{trend_word}趋势。以现有工具组合与年龄结构评估，预期仍可维持当前角色贡献；后续重点观察健康状态与关键数据指标的延续性。

---

*数据来源：MLB.com | MLB Stats API*
*报告生成：{datetime.now().strftime('%Y-%m-%d')}*
"""


def build_html(name: str, md: str, slug: str) -> str:
    # Convert simple markdown tables and headings to HTML
    html_body = md
    html_body = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_body, flags=re.M)
    html_body = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_body, flags=re.M)
    html_body = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_body, flags=re.M)
    html_body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_body)
    html_body = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_body)
    # Blockquotes
    html_body = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html_body, flags=re.M)
    # Lists
    lines = html_body.split('\n')
    out = []
    in_ul = False
    for line in lines:
        m = re.match(r'^(\s*)-\s+(.+)$', line)
        if m:
            if not in_ul:
                out.append('<ul>')
                in_ul = True
            out.append(f'<li>{m.group(2)}</li>')
        else:
            if in_ul:
                out.append('</ul>')
                in_ul = False
            out.append(line)
    if in_ul:
        out.append('</ul>')
    html_body = '\n'.join(out)
    # Tables: crude conversion
    def convert_table(match):
        rows = match.group(0).strip().split('\n')
        thead = '<thead><tr>' + ''.join(f'<th>{c}</th>' for c in rows[0].split('|') if c.strip()) + '</tr></thead>'
        tbody = '<tbody>'
        for row in rows[2:]:
            tbody += '<tr>' + ''.join(f'<td>{c}</td>' for c in row.split('|') if c.strip()) + '</tr>'
        tbody += '</tbody>'
        return f'<table class="comparison-table">{thead}{tbody}</table>'
    html_body = re.sub(r'\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n?)+', convert_table, html_body)
    # Insert images at sections
    html_body = html_body.replace('<h2>📋 基本信息</h2>', f'<div style="text-align:center;padding:0;"><img src="{slug}_report_cover.png" alt="报告封面" style="width:100%;max-width:800px;border-radius:10px;"></div>\n<h2>📋 基本信息</h2>')
    html_body = html_body.replace('<h2>📊 2025 vs 2026 赛季数据</h2>', f'<h2>📊 2025 vs 2026 赛季数据</h2>\n<div style="text-align:center;margin:20px 0;"><img src="{slug}_season_comparison.png" alt="赛季对比" style="width:100%;max-width:900px;border-radius:10px;"></div>')
    html_body = html_body.replace('<h2>📊 综合评分</h2>', f'<h2>📊 综合评分</h2>\n<div style="text-align:center;margin:20px 0;"><img src="{slug}_overall_grades.png" alt="综合评分" style="width:100%;max-width:600px;border-radius:10px;"></div>')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} 球探报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: #e0e0e0; line-height: 1.6; min-height: 100vh; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; padding: 40px 0; background: linear-gradient(90deg, #005A9C 0%, #1a5490 50%, #005A9C 100%); border-radius: 15px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
        .header h1 {{ font-size: 3em; color: #fff; margin-bottom: 10px; }}
        .section {{ background: rgba(255,255,255,0.05); border-radius: 15px; padding: 30px; margin-bottom: 30px; border: 1px solid rgba(255,255,255,0.1); }}
        .section h2 {{ color: #4fc3f7; margin-bottom: 20px; font-size: 1.8em; border-bottom: 2px solid #4fc3f7; padding-bottom: 10px; }}
        .section h3 {{ color: #ff9800; margin: 20px 0 15px; }}
        .comparison-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .comparison-table th, .comparison-table td {{ padding: 12px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .comparison-table th {{ background: rgba(0,90,156,0.3); color: #4fc3f7; }}
        blockquote {{ border-left: 4px solid #ff9800; padding-left: 15px; margin: 15px 0; color: #90a4ae; font-style: italic; }}
        ul {{ margin-left: 20px; line-height: 2; }}
        .footer {{ text-align: center; padding: 20px; color: #90a4ae; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚾ {name}</h1>
        </div>
        {html_body}
        <div class="footer">
            <p>数据来源：MLB.com | MLB Stats API</p>
            <p>报告生成时间：{datetime.now().strftime('%Y-%m-%d')}</p>
            <p>⚾ 洛杉矶道奇队球探报告</p>
        </div>
    </div>
</body>
</html>
"""


def _generate_one(p: dict):
    pid = p["id"]
    name = p["name"]
    slug = slugify(name)
    player_dir = REPORT_ROOT / slug
    player_dir.mkdir(parents=True, exist_ok=True)

    info = fetch_player(pid)
    stats_2025 = fetch_season_stats(pid, 2025)
    stats_2026 = fetch_season_stats(pid, 2026)

    bundle = build_analysis(name, info, stats_2025, stats_2026, p["position_type"])

    generate_cover(player_dir, name, info, stats_2026)
    generate_season_comparison(player_dir, name, stats_2025, stats_2026, bundle["is_pitcher"])
    generate_radar(name, bundle["radar_labels"], bundle["radar_values"],
                   player_dir / f"{slug}_overall_grades.png", 'Overall Grades')

    md = build_markdown(name, info, bundle)
    html = build_html(name, md, slug)

    (player_dir / f"{slug}-scouting-report.md").write_text(md, encoding='utf-8')
    (player_dir / f"{slug}-scouting-report.html").write_text(html, encoding='utf-8')
    print(f"Generated: {name}", flush=True)


def main():
    failed = []
    for p in PLAYERS:
        try:
            _generate_one(p)
        except Exception as e:
            failed.append((p["name"], repr(e)))
            print(f"FAILED: {p['name']} -> {e!r}", flush=True)
    print()
    if failed:
        print(f"{len(failed)} player(s) failed:")
        for name, err in failed:
            print(f"  - {name}: {err}")
    else:
        print("All players generated OK.")
    print("Done. Run build-dodgers-dashboard.py to refresh index.html")


if __name__ == "__main__":
    main()
