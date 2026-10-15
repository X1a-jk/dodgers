#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""De Paula 球探报告图表生成：封面 / 赛季对比雷达 / 综合评分雷达 / 近期趋势"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

FONT = font_manager.FontProperties(family="Microsoft YaHei")
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

OUT = Path(r"D:\baseball\report\josue-de-paula")
DATA = json.load(open(r"D:\baseball\data\de-paula-raw.json", encoding="utf-8"))

BLUE = "#005A9C"
LIGHT = "#4fc3f7"
DARK = "#16213e"
BG = "#0d1b2a"
GOLD = "#FFD700"

def get_season(year, team_key=None):
    for x in DATA["season_stats"]:
        if x["group"] == "hitting" and x["year"] == year and (team_key is None or team_key in x["team"]):
            return x["stat"]
    return {}

s26 = get_season(2026, "Tulsa")
s25 = get_season(2025, "Great Lakes")

def f(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default

pa26, pa25 = f(s26.get("plateAppearances")), f(s25.get("plateAppearances"))
stats26 = dict(
    g=s26.get("gamesPlayed"), pa=int(pa26), ab=s26.get("atBats"), r=s26.get("runs"),
    h=s26.get("hits"), dbl=s26.get("doubles"), tpl=s26.get("triples"), hr=s26.get("homeRuns"),
    rbi=s26.get("rbi"), bb=s26.get("baseOnBalls"), so=s26.get("strikeOuts"),
    sb=s26.get("stolenBases"), cs=s26.get("caughtStealing"),
    avg=s26.get("avg"), obp=s26.get("obp"), slg=s26.get("slg"), ops=s26.get("ops"),
    tb=s26.get("totalBases"),
    bb_pct=round(f(s26.get("baseOnBalls")) / pa26 * 100, 1),
    k_pct=round(f(s26.get("strikeOuts")) / pa26 * 100, 1),
)
stats25 = dict(
    g=s25.get("gamesPlayed"), pa=int(pa25),
    hr=s25.get("homeRuns"), sb=s25.get("stolenBases"), bb=s25.get("baseOnBalls"),
    so=s25.get("strikeOuts"),
    avg=s25.get("avg"), obp=s25.get("obp"), slg=s25.get("slg"), ops=s25.get("ops"),
    bb_pct=round(f(s25.get("baseOnBalls")) / pa25 * 100, 1),
    k_pct=round(f(s25.get("strikeOuts")) / pa25 * 100, 1),
)
print("2026:", stats26)
print("2025:", stats25)

# ---------- 1. 封面 ----------
fig, ax = plt.subplots(figsize=(12, 6.75), dpi=100)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.axis("off")
# 顶部渐变条
ax.add_patch(mpatches.Rectangle((0, 0.86), 1, 0.14, transform=ax.transAxes, color=BLUE))
ax.add_patch(mpatches.Rectangle((0, 0.84), 1, 0.02, transform=ax.transAxes, color=GOLD))
ax.text(0.04, 0.93, "JOSUE DE PAULA", transform=ax.transAxes, fontsize=34, fontweight="bold",
        color="white", fontproperties=FONT)
ax.text(0.04, 0.875, "道奇 #1 新秀 · MLB Pipeline 总榜 No.6 · 外野手", transform=ax.transAxes,
        fontsize=14, color=LIGHT, fontproperties=FONT)
ax.text(0.96, 0.93, "2026", transform=ax.transAxes, fontsize=30, fontweight="bold",
        color=GOLD, ha="right", fontproperties=FONT)
ax.text(0.96, 0.875, "2A Tulsa Drillers", transform=ax.transAxes, fontsize=13,
        color=LIGHT, ha="right", fontproperties=FONT)

# 头像
headshot = OUT / "headshot.jpg"
if headshot.exists():
    try:
        img = Image.open(headshot).convert("RGBA")
        # 圆形裁剪
        size = min(img.size)
        img = img.crop(((img.width - size) // 2, 0, (img.width + size) // 2, size))
        ax_img = fig.add_axes([0.40, 0.28, 0.20, 0.52])
        ax_img.imshow(img)
        ax_img.axis("off")
    except Exception as e:
        print("headshot skip:", e)

# 底部数据带
keys = [("AVG", stats26["avg"]), ("OBP", stats26["obp"]), ("SLG", stats26["slg"]),
        ("OPS", stats26["ops"]), ("HR", stats26["hr"]), ("SB", stats26["sb"]),
        ("BB%", f'{stats26["bb_pct"]}%'), ("K%", f'{stats26["k_pct"]}%')]
for i, (lab, val) in enumerate(keys):
    x = 0.02 + i * 0.1225
    ax.add_patch(mpatches.FancyBboxPatch((x, 0.06), 0.11, 0.13, transform=ax.transAxes,
                                         boxstyle="round,pad=0.008", facecolor="#1a2f45", edgecolor=BLUE, lw=1.2))
    ax.text(x + 0.055, 0.155, str(val), transform=ax.transAxes, fontsize=17, fontweight="bold",
            color="white", ha="center", fontproperties=FONT)
    ax.text(x + 0.055, 0.095, lab, transform=ax.transAxes, fontsize=11,
            color=LIGHT, ha="center", fontproperties=FONT)
ax.text(0.5, 0.015, "L/L · 6'3\" 185 lbs · 21岁 · 2026 未来之星赛 MVP · 25轰+25盗赛季",
        transform=ax.transAxes, fontsize=10, color="#90a4ae", ha="center", fontproperties=FONT)
fig.savefig(OUT / "josue-de-paula_report_cover.png", facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.close(fig)
print("[OK] cover")

# ---------- 2. 赛季对比雷达 ----------
cats = ["AVG", "OBP", "SLG", "OPS", "BB%", "K%"]
lo =   [0.15, 0.25, 0.25, 0.55, 5.0, 10.0]
hi =   [0.35, 0.45, 0.60, 1.05, 20.0, 30.0]
invert = [False, False, False, False, False, True]

def norm(v, l, h, inv):
    n = (v - l) / (h - l)
    return 1 - n if inv else n

vals26 = [f(stats26["avg"]), f(stats26["obp"]), f(stats26["slg"]), f(stats26["ops"]),
          stats26["bb_pct"], stats26["k_pct"]]
vals25 = [f(stats25["avg"]), f(stats25["obp"]), f(stats25["slg"]), f(stats25["ops"]),
          stats25["bb_pct"], stats25["k_pct"]]
v26 = [norm(v, l, h, i) for v, l, h, i in zip(vals26, lo, hi, invert)]
v25 = [norm(v, l, h, i) for v, l, h, i in zip(vals25, lo, hi, invert)]

angles = np.linspace(0, 2 * np.pi, len(cats), endpoint=False).tolist()
v26 += v26[:1]; v25 += v25[:1]; angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 7), dpi=100, subplot_kw=dict(polar=True))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.plot(angles, v25, color="#90a4ae", lw=2, label="2025 高阶1A (Great Lakes)")
ax.fill(angles, v25, color="#90a4ae", alpha=0.15)
ax.plot(angles, v26, color=LIGHT, lw=2.5, label="2026 2A (Tulsa)")
ax.fill(angles, v26, color=LIGHT, alpha=0.25)
ax.set_xticks(angles[:-1])
ax.set_xticklabels([f"{c}\n25: {a}\n26: {b}" for c, a, b in zip(
    cats,
    [f"{stats25['avg']}", f"{stats25['obp']}", f"{stats25['slg']}", f"{stats25['ops']}", f"{stats25['bb_pct']}%", f"{stats25['k_pct']}%"],
    [f"{stats26['avg']}", f"{stats26['obp']}", f"{stats26['slg']}", f"{stats26['ops']}", f"{stats26['bb_pct']}%", f"{stats26['k_pct']}%"])],
    fontproperties=FONT, fontsize=10, color="white")
ax.set_yticklabels([])
ax.set_ylim(0, 1)
ax.spines["polar"].set_color("#33475b")
ax.grid(color="#33475b", lw=0.8)
ax.set_title("2025 高阶1A vs 2026 2A 赛季对比（归一化雷达）", fontproperties=FONT,
             fontsize=14, color="white", pad=28)
leg = ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.14), ncol=2, prop=FONT, fontsize=11)
for t in leg.get_texts():
    t.set_color("white")
fig.savefig(OUT / "josue-de-paula_season_comparison.png", facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.close(fig)
print("[OK] season comparison")

# ---------- 3. 综合评分雷达（Pipeline 2026） ----------
grades = {"打击 Hit": 65, "力量 Power": 60, "跑速 Run": 40, "臂力 Arm": 50, "守备 Field": 40}
labels = list(grades.keys())
gvals = list(grades.values())
ang = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
gv = [v / 80 for v in gvals] + [gvals[0] / 80]
ang2 = ang + ang[:1]
fig, ax = plt.subplots(figsize=(8, 7), dpi=100, subplot_kw=dict(polar=True))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
colors = ["#4caf50" if v >= 60 else LIGHT if v >= 50 else "#ff9800" if v >= 40 else "#f44336" for v in gvals]
ax.plot(ang2, gv, color=LIGHT, lw=2.5)
ax.fill(ang2, gv, color=LIGHT, alpha=0.25)
ax.scatter(ang, [v / 80 for v in gvals], c=colors, s=90, zorder=5)
for a, v, c in zip(ang, gvals, colors):
    ax.annotate(str(v), xy=(a, v / 80), xytext=(a, v / 80 + 0.09),
                color=c, fontsize=15, fontweight="bold", ha="center", fontproperties=FONT)
ax.set_xticks(ang)
ax.set_xticklabels(labels, fontproperties=FONT, fontsize=12, color="white")
ax.set_yticks([0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["20", "40", "60", "80"], color="#90a4ae", fontsize=9)
ax.set_ylim(0, 1.15)
ax.spines["polar"].set_color("#33475b")
ax.grid(color="#33475b", lw=0.8)
ax.set_title("MLB Pipeline 2026 球探评分（20-80 分制）· Overall 60", fontproperties=FONT,
             fontsize=14, color="white", pad=24)
fig.savefig(OUT / "josue-de-paula_overall_grades.png", facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.close(fig)
print("[OK] grades radar")

# ---------- 4. 近47场趋势 ----------
gl = DATA["gamelog_2026"]
dates = [g["date"][5:] for g in gl]
hits = [g["h"] for g in gl]
ab = [g["ab"] for g in gl]
# 10场滚动打击率
roll, cum_h, cum_ab = [], 0, 0
h_cum, ab_cum = [], []
for i, (h, a) in enumerate(zip(hits, ab)):
    cum_h += h; cum_ab += a
    h_cum.append(cum_h); ab_cum.append(cum_ab)
    lo_i = max(0, i - 9)
    h10 = sum(hits[lo_i:i + 1]); a10 = sum(ab[lo_i:i + 1])
    roll.append(h10 / a10 if a10 else 0)
cum_avg = [h / a if a else 0 for h, a in zip(h_cum, ab_cum)]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7.5), dpi=100, sharex=True,
                               gridspec_kw={"height_ratios": [3, 2]})
fig.patch.set_facecolor(BG)
for a in (ax1, ax2):
    a.set_facecolor("#12233a")
    a.tick_params(colors="#90a4ae")
    for s in a.spines.values():
        s.set_color("#33475b")
x = np.arange(len(dates))
ax1.plot(x, roll, color=LIGHT, lw=2.2, marker="o", ms=3.5, label="10场滚动打击率")
ax1.plot(x, cum_avg, color=GOLD, lw=1.8, ls="--", label="累计打击率（47场窗口）")
ax1.axhline(0.300, color="#4caf50", lw=1, ls=":", alpha=0.7)
ax1.text(len(dates) - 1, 0.305, ".300", color="#4caf50", fontsize=9, ha="right", fontproperties=FONT)
ax1.set_ylim(0, 0.5)
ax1.legend(prop=FONT, labelcolor="white", facecolor="#12233a", edgecolor="#33475b")
ax1.set_title("近 47 场打击走势（2026-07-12 起，2A Tulsa）", fontproperties=FONT, fontsize=14, color="white")
ax1.grid(color="#22354a", lw=0.7, alpha=0.7)
ax1.set_ylabel("打击率", fontproperties=FONT, color="#90a4ae")

hr = [g["hr"] for g in gl]
sb = [g["sb"] for g in gl]
rbi = [g["rbi"] for g in gl]
w = 0.4
ax2.bar(x - w / 2, hr, width=w, color="#ef5350", label="本垒打")
ax2.bar(x + w / 2, sb, width=w, color="#66bb6a", label="盗垒")
for i, v in enumerate(rbi):
    if v >= 2:
        ax2.annotate(f"{v}RBI", xy=(i, max(hr[i], sb[i]) + 0.15), fontsize=7, color=GOLD,
                     ha="center", fontproperties=FONT)
ax2.legend(prop=FONT, labelcolor="white", facecolor="#12233a", edgecolor="#33475b", ncol=2)
ax2.set_ylabel("HR / SB", fontproperties=FONT, color="#90a4ae")
ax2.set_xticks(x[::4])
ax2.set_xticklabels([dates[i] for i in range(0, len(dates), 4)], rotation=45, fontsize=9)
ax2.grid(color="#22354a", lw=0.7, alpha=0.7, axis="y")
fig.tight_layout()
fig.savefig(OUT / "josue-de-paula_game_trends.png", facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.close(fig)
print("[OK] trends")

# 存一份统计摘要供写报告用
summary = {"stats26": stats26, "stats25": stats25}
(OUT / "stats_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print("[OK] stats_summary.json")
