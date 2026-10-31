#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tarik Skubal 定制化球探报告生成器
基于 D:\baseball\report\generate_custom_report.py 模板改编
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
TODAY = datetime.now().strftime('%Y-%m-%d')

PLAYER = {
    "name": "Tarik Skubal",
    "slug": "tarik-skubal",
    "last_name": "skubal",
    "number": "29",
    "position": "左投先发 (LHP)",
    "position_code": "P",
    "bats_throws": "右打 / 左投",
    "birth_date": "1996-11-20",
    "age": "29",
    "birthplace": "美国加州海沃德 (Hayward, CA)",
    "height_weight": "6'3\" / 240 lbs",
    "debut": "2020-08-18",
    "college": "Seattle University",
    "nickname": "Skubal",
    "status": "活跃",
    "type": "pitcher",
    "summary": """
        <p style="margin-bottom: 15px;">Tarik Skubal 是当今大联盟最顶尖的左投先发之一，连续两季（2024、2025）夺得美联赛扬奖，并在2024年包办<span class="highlight">胜投、ERA、三振三冠王</span>。2026年交易截止日前，道奇将他纳入阵中，立刻让轮值多了一名王牌级左投。</p>
        <p style="margin-bottom: 15px;">他的球风以<span class="success">高压快速球 + 犀利滑球</span>为核心，搭配优质的变速球与下沉快速球。2026年在老虎队仍缴出 7胜5败、2.79 ERA、0.91 WHIP 的顶尖数据，三振保送比超过 8:1，显示控球已是 elite 水准。</p>
        <p>加盟道奇后，Skubal 预计将成为季后赛轮值的 pillar。他的存在不仅能直接提升先发战力，也能让 Yamamoto、Sasaki 等年轻投手减少压力，是道奇冲刺冠军的最关键补强。</p>
    """,
    "career_highlights": """
        <div class="career-highlight">
            <h4>🎓 2018年 - 老虎第9轮选中</h4>
            <p>来自 Seattle University，2018年选秀第9轮（总第255顺位）被底特律老虎选中。大学时期创下校史胜投（21）、三振（224）与被打击率（.221）纪录。</p>
        </div>
        <div class="career-highlight">
            <h4>🌟 2020年 - 大联盟首秀</h4>
            <p>2020年8月18日登上大联盟，生涯初期起伏较大，但快速展现出三振潜力。2021年以164次三振刷新老虎新秀单季三振纪录。</p>
        </div>
        <div class="career-highlight">
            <h4>💪 2024年 - 赛扬 + 投手三冠王</h4>
            <p>31场先发、18胜4败、2.39 ERA、228 K，包办美联胜投、自责分率、三振三冠王。成为老虎队史继 Justin Verlander、Hal Newhouser 后第三位三冠王投手，并勇夺生涯首座赛扬奖。</p>
        </div>
        <div class="career-highlight">
            <h4>🏆 2025年 - 连庄赛扬</h4>
            <p>31场先发、13胜6败、2.21 ERA、241 K，0.89 WHIP 为大联盟最低。成为自1999-2000年 Pedro Martinez 以来首位连庄美联赛扬的投手，并连续入选全明星赛。</p>
        </div>
        <div class="career-highlight">
            <h4>🔵 2026年 - 加盟道奇</h4>
            <p>2026年交易截止日前被交易至洛杉矶道奇，背号 #29。道奇希望借助他的王牌身手稳住先发轮值，并在季后赛提供顶级左投战力。</p>
        </div>
    """,
    "stats_2026": {
        "G": 16, "GS": 16, "W": 7, "L": 5, "ERA": "2.79", "IP": "96.2", "K": 116, "BB": 14,
        "WHIP": "0.91", "K/9": "10.80", "BB/9": "1.30", "HR": 10
    },
    "stats_2025": {
        "G": 31, "GS": 31, "W": 13, "L": 6, "ERA": "2.21", "IP": "195.1", "K": 241, "BB": 33,
        "WHIP": "0.89", "K/9": "11.10", "BB/9": "1.52", "HR": 18
    },
    "stats_2024": {
        "G": 31, "GS": 31, "W": 18, "L": 4, "ERA": "2.39", "IP": "192.0", "K": 228, "BB": 35,
        "WHIP": "0.92", "K/9": "10.69", "BB/9": "1.64", "HR": 15
    },
    "cover_stats": [
        ("ERA", "2.79"), ("W-L", "7-5"), ("K", "116"), ("IP", "96.2"),
        ("WHIP", "0.91"), ("K/9", "10.80"), ("Age", "29"), ("Cy Young", "2x")
    ],
    "season_chart_data": [
        [2.39, 2.21, 2.79],   # ERA
        [0.92, 0.89, 0.91],   # WHIP
        [10.69, 11.10, 10.80], # K/9
        [1.64, 1.52, 1.30]     # BB/9
    ],
    "season_chart_years": ["2024", "2025", "2026"],
    "season_chart_stats": ["ERA", "WHIP", "K/9", "BB/9"],
    "pitch_arsenal": [
        {"name": "四缝快速球 (Four-Seam Fastball)", "velocity": "95-99 mph", "avg": "97.5", "desc": "Skubal 的压制核心。均速约 97 mph，最高可达 99 mph，具有优异的纵向位移。他善于用快速球抢 strike、制造追打，并能对抗左右打者。"},
        {"name": "滑球 (Slider)", "velocity": "86-89 mph", "avg": "87.5", "desc": "主要出局球，sharp break 且横向位移大。在两好球后用来制造挥空，对付右打者外角与左打者后脚特别有效。"},
        {"name": "变速球 (Changeup)", "velocity": "88-91 mph", "avg": "89.5", "desc": "优质第三球种，出手点与快速球相近，速度差约 8 mph。用来让打者重心前移、制造软弱滚地球或挥棒落空。"},
        {"name": "下沉快速球 (Sinker/Two-Seam)", "velocity": "94-97 mph", "avg": "95.5", "desc": "近年增加的球种，利用下沉位移制造滚地球，减少长打伤害。与四缝快速球搭配，让打者难以判定轨迹。"}
    ],
    "analysis": """
        <div style="margin-top: 20px;">
            <h3 style="color: #4fc3f7; margin-bottom: 15px;">投球机制与球风</h3>
            <p>Skubal 采用高四分之三（high-three-quarters）出手点，身体平衡良好，跨步方向稳定。他的快速球出手隐蔽，加上 slider 与 changeup 的释放点高度相似，让打者很难提前辨认球路。整体机制重复性高，是他能稳定维持低保送率的关键。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">近三年趋势（2024-2026）</h3>
            <p>2024 年是 Skubal 的爆发年：18 胜 4 败、2.39 ERA、228 K，首次突破 190 局并包办美联三冠王。2025 年他将 ERA 进一步压到 2.21，K/9 提升至 11.10，WHIP 0.89，连续两季投出赛扬等级内容。2026 年虽然 ERA 小幅回升至 2.79，但 WHIP 仍维持在 0.91 的 elite 水准，BB/9 从 1.64 → 1.52 → 1.30 持续进步，显示控球仍在进化。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">2026年数据解读</h3>
            <p>2026 年 2.79 ERA 相较于 2024-2025 的 2.21-2.39 略有上扬，主要与季中交易传闻、老虎队战绩压力以及小样本波动有关。值得注意的是他的三振保送比从 2024 年的 6.5:1 提升至 2026 年的 8.3:1，压制上垒能力并未下滑。加入道奇后，在更强的防守与牛棚支援下，ERA 有机会回到 2.40 以下。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">三振保送比与效率</h3>
            <p>2026 年 116 K / 14 BB，三振保送比约 8.3:1，属于 elite 等级。这意味着他很少因保送造成大局，也能在垒上有人时透过三振化解危机。加盟道奇后，在更强的防守与牛棚支援下，ERA 有机会进一步下探。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">长打伤害与球路分布</h3>
            <p>2026 年 96.2 局被敲 10 轰，HR/9 约 0.93，略高于 2025 年的 0.83。主要风险在于快速球偶尔进垒偏高时被强打者抓住。加入道奇后，需要更谨慎使用快速球比例，并善用 slider/changeup 在两好球后收尾。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">在道奇的角色定位</h3>
            <p>Skubal 将是道奇轮值中的王牌左投，很可能排在 Yamamoto 之后担任第 2 号先发。他的季后赛经验（2025 年季后赛 15.7 K/9）让他在短系列赛极具价值，是道奇争冠路上的 X-factor。</p>
        </div>
    """,
    "pros": [
        "连庄美联赛扬奖得主，2024年投手三冠王",
        "2025年 2.21 ERA、0.89 WHIP，压制力顶级",
        "快速球均速 97 mph，最高可达 99 mph",
        "Slider 与 Changeup 组成精英级三振武器库",
        "三振保送比超过 8:1，控球 elite",
        "季后赛经验丰富，2025 年季后赛 K/9 高达 15.7",
        "左投身份在轮值中具战略价值",
        "能吃局数，2024-2025 连续两季 31 场先发",
        "加盟道奇后ERA有望进一步下探"
    ],
    "cons": [
        "2026年数据较 2025 年略有下滑",
        "快速球偏高时偶尔被长打惩罚",
        "交易后需要适应国联打者与道奇配球体系",
        "季中转换球队可能短暂影响节奏",
        "过往有手肘伤病史（2022年左前臂肌肉伤势、2023年左肘拉伤）",
        "作为王牌，季后赛压力与期望值极高"
    ],
    "grades": [
        {"label": "Fastball", "value": 70, "grade": "A"},
        {"label": "Slider", "value": 65, "grade": "A-"},
        {"label": "Changeup", "value": 60, "grade": "B+"},
        {"label": "Sinker", "value": 60, "grade": "B+"},
        {"label": "Control", "value": 70, "grade": "A"},
        {"label": "Command", "value": 65, "grade": "A-"},
        {"label": "Stamina", "value": 60, "grade": "B+"},
        {"label": "Mental", "value": 65, "grade": "A-"}
    ],
    "overall_grade": 70,
    "overall_label": "A 级 / 王牌左投",
    "overall_desc": "当代最顶尖的左投先发之一，连续赛扬得主。加盟道奇后将成为轮值王牌与季后赛关键武器，预期能稳定贡献 elite 等级的先发内容。",
    "future_outlook": """
        <div style="margin-top: 20px;">
            <p>Tarik Skubal 正处于投手生涯的巅峰期。29岁的他拥有连续两季 190+ 局、ERA 低于 2.40、200+ 三振的履历，加入道奇这支冠军球队后，有望在更强的防守与牛棚支援下再创高峰。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
            <ol style="margin-left: 20px; line-height: 2;">
                <li><strong>快速球进垒点管理：</strong>减少偏高快速球比例，避免被强打者锁定。</li>
                <li><strong>增加 Sinker 使用：</strong>在垒上有人或两出局时多用下沉快速球制造滚地球，降低长打风险。</li>
                <li><strong>国联打者侦察报告：</strong>道奇投手教练团需快速建立对国联强打者的配球策略，尤其针对教士、勇士、费城人等争冠对手。</li>
                <li><strong>健康管理：</strong>过往左肘伤病史需要持续关注，避免在常规赛后期过度消耗。</li>
            </ol>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
            <p><strong>2026（下半季）：</strong>在道奇先发轮值中担任王牌左投，预估剩余先发 ERA 2.50-3.00，并在季后赛扛起第 2 战。</p>
            <p><strong>2027：</strong>若保持健康，仍是赛扬热门，预计 30+ 先发、ERA 2.20-2.70、220+ 三振。</p>
            <p><strong>2028+：</strong>进入 30 岁中后期，可能逐步从「绝对王牌」转为「经验王牌」，但控球与球路组合仍可维持数年的 elite 水准。</p>

            <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3>
            <ul style="margin-left: 20px; line-height: 2;">
                <li>左肘伤病史需要严格管理</li>
                <li>季中换队可能带来短暂适应期</li>
                <li>快速球被长打惩罚时，需要更快调整配球</li>
                <li>季后赛高强度调度下的疲劳累积</li>
            </ul>
        </div>
    """,
    "background": """
        <div style="margin-top: 20px;">
            <p>Tarik Daniel Skubal 出生于美国加州海沃德（Hayward, CA），在 Seattle University 度过辉煌的三年大学生涯。他创下校史胜投、三振与被打击率纪录，并在 2018 年选秀第 9 轮被底特律老虎选中。</p>
            <p>2020 年 8 月 18 日，Skubal 登上大联盟。生涯初期他展现惊人的三振能力，2021 年以 164 K 刷新老虎队史新秀三振纪录。2022 年他因左前臂肌肉伤势提前赛季报销，2023 年又因左肘拉伤缺席前半季，但复出后缴出 2.80 ERA 的强势表现。</p>
            <p>2024 年是 Skubal 的爆发年：18 胜 4 败、2.39 ERA、228 K，包办美联胜投、ERA、三振三冠王，并夺得生涯首座赛扬奖。2025 年他再以 2.21 ERA、241 K、0.89 WHIP 连庄赛扬，成为 Pedro Martinez 后首位连庄美联赛扬的投手。2025 年季后赛他更写下单场 14 K 的 AL 左投季后赛纪录。</p>
            <p>2026 年交易截止日前，道奇将 Skubal 交易来队，希望借助这位王牌左投的季后赛经验与顶级身手，再度冲击世界大赛冠军。</p>
        </div>
    """
}


def slugify(name):
    s = name.lower().replace(' ', '-')
    for a, b in [('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o'), ('ú', 'u'),
                 ('ñ', 'n'), ('ü', 'u'), ('ã', 'a'), ('õ', 'o'), ('ç', 'c'),
                 ('à', 'a'), ('è', 'e'), ('ì', 'i'), ('ò', 'o'), ('ù', 'u')]:
        s = s.replace(a, b)
    return s


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__TITLE__</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e0e0e0; line-height: 1.6; min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header {
            text-align: center; padding: 40px 0;
            background: linear-gradient(90deg, #005A9C 0%, #1a5490 50%, #005A9C 100%);
            border-radius: 15px; margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        .header h1 { font-size: 3em; color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); margin-bottom: 10px; }
        .header .subtitle { font-size: 1.2em; color: #e0e0e0; font-style: italic; }
        .player-card {
            background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 30px; margin-bottom: 30px;
            backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex; gap: 30px; flex-wrap: wrap;
        }
        .player-info { flex: 1; min-width: 250px; }
        .player-info h2 { color: #4fc3f7; margin-bottom: 15px; font-size: 1.8em; }
        .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .info-item { background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; }
        .info-item .label { font-size: 0.9em; color: #90a4ae; text-transform: uppercase; letter-spacing: 1px; }
        .info-item .value { font-size: 1.2em; color: #fff; font-weight: bold; }
        .section {
            background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 30px;
            margin-bottom: 30px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .section h2 {
            color: #4fc3f7; margin-bottom: 20px; font-size: 1.8em;
            border-bottom: 2px solid #4fc3f7; padding-bottom: 10px;
        }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px; }
        .stat-card {
            background: linear-gradient(135deg, rgba(0, 90, 156, 0.3) 0%, rgba(26, 84, 144, 0.3) 100%);
            border-radius: 10px; padding: 20px; text-align: center;
            border: 1px solid rgba(79, 195, 247, 0.3); transition: transform 0.3s ease;
        }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-card .stat-value { font-size: 2.5em; font-weight: bold; color: #4fc3f7; display: block; }
        .stat-card .stat-label { font-size: 0.9em; color: #90a4ae; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; }
        .comparison-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .comparison-table th, .comparison-table td { padding: 12px; text-align: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
        .comparison-table th { background: rgba(0, 90, 156, 0.3); color: #4fc3f7; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
        .comparison-table tr:hover { background: rgba(255, 255, 255, 0.05); }
        .pitch-arsenal { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
        .pitch-card {
            background: linear-gradient(135deg, rgba(0, 90, 156, 0.2) 0%, rgba(26, 84, 144, 0.2) 100%);
            border-radius: 10px; padding: 20px; border-left: 4px solid #4fc3f7;
        }
        .pitch-card h3 { color: #4fc3f7; margin-bottom: 10px; }
        .pitch-card .velocity { font-size: 1.5em; color: #fff; font-weight: bold; }
        .pros-cons { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
        .pros, .cons { background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 20px; }
        .pros h3 { color: #4caf50; margin-bottom: 15px; }
        .cons h3 { color: #f44336; margin-bottom: 15px; }
        .pros ul, .cons ul { list-style: none; }
        .pros li, .cons li { padding: 8px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
        .pros li::before { content: "✓ "; color: #4caf50; font-weight: bold; }
        .cons li::before { content: "✗ "; color: #f44336; font-weight: bold; }
        .grade { display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9em; }
        .grade-a { background: rgba(76, 175, 80, 0.3); color: #4caf50; }
        .grade-b { background: rgba(79, 195, 247, 0.3); color: #4fc3f7; }
        .grade-c { background: rgba(255, 152, 0, 0.3); color: #ff9800; }
        .grade-d { background: rgba(244, 67, 54, 0.3); color: #f44336; }
        .highlight { color: #4fc3f7; font-weight: bold; }
        .warning { color: #ff9800; font-weight: bold; }
        .success { color: #4caf50; font-weight: bold; }
        .danger { color: #f44336; font-weight: bold; }
        .career-highlight { background: rgba(255, 215, 0, 0.1); border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 10px; padding: 15px; margin: 15px 0; }
        .career-highlight h4 { color: #FFD700; margin-bottom: 10px; }
        .footer { text-align: center; padding: 20px; color: #90a4ae; font-size: 0.9em; }
        @media (max-width: 768px) { .header h1 { font-size: 2em; } .stats-grid { grid-template-columns: repeat(2, 1fr); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚾ __PLAYER_NAME__</h1>
            <p class="subtitle">__SUBTITLE__</p>
        </div>

        <div class="section" style="text-align: center; padding: 0; background: none; border: none; backdrop-filter: none; box-shadow: none;">
            <img src="__COVER_IMG__" alt="报告封面" style="width: 100%; max-width: 900px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        </div>

        <div class="player-card">
            <div class="player-info">
                <h2>基本信息</h2>
                <div class="info-grid">
__INFO_GRID__
                </div>
            </div>
            <div class="player-info">
                <h2>球探总评</h2>
__SCOUTING_SUMMARY__
            </div>
        </div>

        <div class="section">
            <h2>🏆 职业生涯亮点</h2>
__CAREER_HIGHLIGHTS__
        </div>

__2026_STATS_SECTION__

__SEASON_COMPARISON_SECTION__

__PITCH_ARSENAL_SECTION__

        <div class="section">
            <h2>🔍 球探分析</h2>
__ANALYSIS__
        </div>

        <div class="section">
            <h2>✅ 优势 vs ❌ 劣势</h2>
            <div class="pros-cons">
                <div class="pros">
                    <h3>优势 (Strengths)</h3>
                    <ul>
__PROS__
                    </ul>
                </div>
                <div class="cons">
                    <h3>劣势 (Weaknesses)</h3>
                    <ul>
__CONS__
                    </ul>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>📊 综合评分</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="__GRADES_RADAR__" alt="综合评分雷达图" style="width: 100%; max-width: 600px; border-radius: 10px;">
            </div>
            <div class="stats-grid">
__GRADES_GRID__
            </div>
            <div style="margin-top: 30px; text-align: center;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">总体潜力评分</h3>
                <div style="font-size: 4em; color: #4caf50; font-weight: bold;">__OVERALL_GRADE__</div>
                <p style="color: #90a4ae; margin-top: 10px;">__OVERALL_DESC__</p>
                <p style="margin-top: 15px;"><span class="grade grade-a" style="font-size: 1.2em;">__OVERALL_LABEL__</span></p>
            </div>
        </div>

        <div class="section">
            <h2>🔮 未来展望</h2>
__FUTURE_OUTLOOK__
        </div>

        <div class="section">
            <h2>📖 背景故事</h2>
__BACKGROUND__
        </div>

        <div class="footer">
            <p>数据来源：MLB.com | Baseball Savant (Statcast) | Fangraphs | MLB Stats API</p>
            <p>报告生成时间：__FOOTER_DATE__ | 数据截止日期：__DATA_DATE__</p>
            <p>⚾ 洛杉矶道奇队球探报告</p>
        </div>
    </div>
</body>
</html>
"""


def generate_cover(p, output_path):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    ax.text(0.5, 0.85, p['name'], fontsize=32, fontweight='bold', ha='center',
            color='white', transform=ax.transAxes)
    ax.text(0.5, 0.75, f"Los Angeles Dodgers #{p['number']} | {p['position']}", fontsize=18,
            ha='center', color='#4fc3f7', transform=ax.transAxes)
    ax.text(0.5, 0.65, 'SCOUTING REPORT 2026', fontsize=22, fontweight='bold', ha='center',
            color='#ff9800', transform=ax.transAxes)

    y_pos = 0.45
    for i, (label, value) in enumerate(p['cover_stats']):
        x_pos = 0.15 + (i % 4) * 0.23
        if i >= 4:
            y_pos = 0.25
        ax.text(x_pos, y_pos, value, fontsize=26, fontweight='bold', ha='center',
                color='#4fc3f7', transform=ax.transAxes)
        ax.text(x_pos, y_pos - 0.08, label, fontsize=12, ha='center',
                color='#90a4ae', transform=ax.transAxes)

    subtitle = f"{p['status']} | {p['college']} | MLB Debut {p['debut']}"
    ax.text(0.5, 0.08, subtitle, fontsize=14, ha='center',
            color='#90a4ae', transform=ax.transAxes, style='italic')
    ax.text(0.5, 0.02, f'Generated: {TODAY} | Data: MLB.com, MLB Stats API',
            fontsize=10, ha='center', color='#666', transform=ax.transAxes)

    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()


def generate_season_chart(p, output_path):
    stats = p['season_chart_stats']
    data = p['season_chart_data']
    years = p['season_chart_years']
    colors = ['#4fc3f7', '#4caf50', '#ff9800']

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for idx, stat in enumerate(stats):
        ax = axes[idx]
        vals = data[idx]
        x = np.arange(len(years))
        width = 0.5
        bars = ax.bar(x, vals, color=colors, edgecolor='white', alpha=0.9, width=width)
        ax.set_title(stat, fontsize=14, fontweight='bold', color='#1a1a2e')
        max_val = max(vals) * 1.25 if max(vals) != 0 else 1
        ax.set_ylim(0, max_val)
        ax.set_xticks(x)
        ax.set_xticklabels(years)
        ax.grid(axis='y', alpha=0.3)
        for bar, val in zip(bars, vals):
            height = bar.get_height()
            text = f'{val:.2f}' if stat in ['ERA', 'WHIP'] else f'{val:.1f}'
            ax.text(bar.get_x() + bar.get_width()/2., height + max_val*0.02,
                    text, ha='center', va='bottom', fontweight='bold', fontsize=11)

    fig.suptitle(f"{p['name']} - 2024-2026 Season Comparison", fontsize=16, fontweight='bold', color='#1a1a2e', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def generate_pitch_velocities(p, output_path):
    if not p.get('pitch_arsenal'):
        return
    arsenal = p['pitch_arsenal']
    fig, ax = plt.subplots(figsize=(12, 6))

    pitches = [a['name'] for a in arsenal]
    min_velo = []
    max_velo = []
    for a in arsenal:
        try:
            rng = a['velocity'].split('（')[0].strip()
            parts = rng.replace('mph', '').split('-')
            min_velo.append(float(parts[0].strip()))
            max_velo.append(float(parts[1].strip()))
        except Exception:
            min_velo.append(0)
            max_velo.append(0)
    avg_velo = [(min_v + max_v) / 2 for min_v, max_v in zip(min_velo, max_velo)]

    x = np.arange(len(pitches))
    width = 0.35
    ax.bar(x - width/2, min_velo, width, label='Min', color='#4fc3f7', alpha=0.8)
    ax.bar(x + width/2, max_velo, width, label='Max', color='#ff9800', alpha=0.8)

    for i, avg in enumerate(avg_velo):
        ax.plot([i - width/2, i + width/2], [avg, avg], 'r--', linewidth=2, alpha=0.7)
        ax.text(i, avg + 0.5, f'Avg {avg:.1f}', ha='center', va='bottom', fontweight='bold', color='red')

    ax.set_xlabel('Pitch Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Velocity (mph)', fontsize=12, fontweight='bold')
    ax.set_title(f"{p['name']} Pitch Arsenal Velocity Distribution", fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(pitches)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(80, 105)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def generate_grades_chart(p, output_path):
    categories = [g['label'] for g in p['grades']]
    values = [g['value'] for g in p['grades']]
    values += values[:1]
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    ax.plot(angles, values, 'o-', linewidth=2, color='#1E90FF', markersize=8)
    ax.fill(angles, values, alpha=0.25, color='#1E90FF')

    for angle, value in zip(angles[:-1], values[:-1]):
        ax.text(angle, value + 3, str(value), ha='center', va='center', fontweight='bold', fontsize=10, color='darkblue')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=10, fontweight='bold')
    ax.set_ylim(20, 80)
    ax.set_yticks([20, 30, 40, 50, 60, 70, 80])
    ax.set_yticklabels(['20', '30', '40', '50', '60', '70', '80'], color='grey', size=8)
    ax.set_title(f"{p['name']} - Scouting Grades\n(20-80 Scale)", size=16, fontweight='bold', pad=20)
    ax.grid(True)
    ax.axhspan(60, 80, alpha=0.05, color='green')
    ax.axhspan(50, 60, alpha=0.05, color='yellow')
    ax.axhspan(0, 50, alpha=0.05, color='red')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def grade_class(value):
    if value >= 60: return 'grade-a'
    if value >= 50: return 'grade-b'
    if value >= 40: return 'grade-c'
    return 'grade-d'


def build_info_grid(p):
    items = [
        ("全名", p['name']),
        ("出生日期", p['birth_date']),
        ("年龄", p['age'] + "岁"),
        ("出生地", p['birthplace']),
        ("身高/体重", p['height_weight']),
        ("击球/投球", p['bats_throws']),
        ("位置", p['position']),
        ("MLB首秀", p['debut']),
    ]
    if p.get('college'):
        items.append(("大学", p['college']))
    if p.get('nickname'):
        items.append(("绰号", p['nickname']))
    items.append(("背号", "#" + p['number']))
    items.append(("状态", p['status']))
    return "\n".join(
        f'                    <div class="info-item"><div class="label">{label}</div><div class="value">{value}</div></div>'
        for label, value in items
    )


def build_pitching_grid(stats):
    order = [('G', '出赛'), ('GS', '先发'), ('W', '胜'), ('L', '败'), ('ERA', 'ERA'),
             ('IP', 'IP'), ('K', 'K'), ('BB', 'BB'), ('WHIP', 'WHIP'), ('K/9', 'K/9'), ('BB/9', 'BB/9'), ('HR', '被全垒打')]
    html = ""
    for k, label in order:
        val = stats.get(k, '—')
        color = "#4fc3f7"
        if k == 'ERA' and val != '—':
            try:
                if float(val) > 4.5: color = "#ff9800"
                if float(val) > 5.5: color = "#f44336"
                if float(val) < 3.5: color = "#4caf50"
            except Exception:
                pass
        html += f'''
                <div class="stat-card">
                    <span class="stat-value" style="color: {color};">{val}</span>
                    <div class="stat-label">{label}</div>
                </div>'''
    return html


def build_pitching_table(s24, s25, s26):
    rows = ""
    for year, s in [("2024", s24), ("2025", s25), ("2026", s26)]:
        year_class = 'warning' if year == '2026' else 'highlight' if year == '2025' else 'success'
        rows += f'''                    <tr>
                        <td class="{year_class}">{year}</td>
                        <td>{s.get('G', '—')}</td>
                        <td>{s.get('GS', '—')}</td>
                        <td>{s.get('W', '—')}-{s.get('L', '—')}</td>
                        <td>{s.get('ERA', '—')}</td>
                        <td>{s.get('IP', '—')}</td>
                        <td>{s.get('K', '—')}</td>
                        <td>{s.get('BB', '—')}</td>
                        <td>{s.get('WHIP', '—')}</td>
                        <td>{s.get('K/9', '—')}</td>
                    </tr>'''
    return rows


def build_pitch_arsenal_html(p):
    if not p.get('pitch_arsenal'):
        return ""
    cards = "\n".join(
        f'''                <div class="pitch-card">
                    <h3>{a['name']}</h3>
                    <p><span class="velocity">{a['velocity']}</span></p>
                    <p>{a['desc']}</p>
                </div>'''
        for a in p['pitch_arsenal']
    )
    return f'''
        <div class="section">
            <h2>⚾ 投球武器库</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="{p['slug']}_pitch_velocities.png" alt="投球武器库速度" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
            <div class="pitch-arsenal">
{cards}
            </div>
        </div>
'''


def build_grades_grid(grades):
    return "\n".join(
        f'''                <div class="stat-card">
                    <span class="stat-value" style="color: {'#4caf50' if g['value'] >= 60 else '#4fc3f7' if g['value'] >= 50 else '#ff9800'};">{g['value']}</span>
                    <div class="stat-label">{g['label']}</div>
                    <span class="grade {grade_class(g['value'])}">{g['grade']}</span>
                </div>'''
        for g in grades
    )


def build_pros_cons(items):
    return "\n".join(f'                        <li>{item}</li>' for item in items)


def build_html(p):
    html = HTML_TEMPLATE
    html = html.replace('__TITLE__', f"{p['name']} 球探报告")
    html = html.replace('__PLAYER_NAME__', p['name'])
    html = html.replace('__SUBTITLE__', f"Los Angeles Dodgers #{p['number']} | {p['position']} | {p['status']}")
    html = html.replace('__COVER_IMG__', f"{p['slug']}_report_cover.png")
    html = html.replace('__INFO_GRID__', build_info_grid(p))
    html = html.replace('__SCOUTING_SUMMARY__', p['summary'])
    html = html.replace('__CAREER_HIGHLIGHTS__', p['career_highlights'])

    stats_section = f'''
        <div class="section">
            <h2>📊 2026赛季投球数据</h2>
            <div class="stats-grid">
{build_pitching_grid(p['stats_2026'])}
            </div>
        </div>
'''
    season_section = f'''
        <div class="section">
            <h2>📊 2024-2026 近三年赛季对比</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="{p['slug']}_season_comparison.png" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
            <h3 style="margin-top: 30px; color: #4fc3f7;">近三年投球数据对比</h3>
            <table class="comparison-table">
                <thead>
                    <tr><th>赛季</th><th>G</th><th>GS</th><th>W-L</th><th>ERA</th><th>IP</th><th>K</th><th>BB</th><th>WHIP</th><th>K/9</th></tr>
                </thead>
                <tbody>
{build_pitching_table(p['stats_2024'], p['stats_2025'], p['stats_2026'])}
                </tbody>
            </table>
        </div>
'''

    html = html.replace('__2026_STATS_SECTION__', stats_section)
    html = html.replace('__SEASON_COMPARISON_SECTION__', season_section)
    html = html.replace('__PITCH_ARSENAL_SECTION__', build_pitch_arsenal_html(p))
    html = html.replace('__ANALYSIS__', p['analysis'])
    html = html.replace('__PROS__', build_pros_cons(p['pros']))
    html = html.replace('__CONS__', build_pros_cons(p['cons']))
    html = html.replace('__GRADES_RADAR__', f"{p['slug']}_overall_grades.png")
    html = html.replace('__GRADES_GRID__', build_grades_grid(p['grades']))
    html = html.replace('__OVERALL_GRADE__', str(p['overall_grade']))
    html = html.replace('__OVERALL_DESC__', p['overall_desc'])
    html = html.replace('__OVERALL_LABEL__', p['overall_label'])
    html = html.replace('__FUTURE_OUTLOOK__', p['future_outlook'])
    html = html.replace('__BACKGROUND__', p['background'])
    html = html.replace('__FOOTER_DATE__', TODAY)
    html = html.replace('__DATA_DATE__', TODAY)
    return html


def build_md(p):
    s24, s25, s26 = p['stats_2024'], p['stats_2025'], p['stats_2026']
    lines = [
        f"# {p['name']} 球探报告",
        "",
        f"> **Los Angeles Dodgers #{p['number']} | {p['position']} | {p['status']}**",
        f"> ",
        f"> 报告生成时间：{TODAY}",
        "",
        "---",
        "",
        "## 📋 基本信息",
        "",
        f"- **姓名**：{p['name']}",
        f"- **背号**：#{p['number']}",
        f"- **位置**：{p['position']}",
        f"- **状态**：{p['status']}",
        f"- **击球/投球**：{p['bats_throws']}",
        f"- **出生日期**：{p['birth_date']}（{p['age']}岁）",
        f"- **MLB首秀**：{p['debut']}",
        "",
        "---",
        "",
        "## 📊 2026赛季数据",
        "",
        "| G | GS | W | L | ERA | IP | K | BB | WHIP | K/9 |",
        "|---|---|---|---|---|---|---|---|---|---|",
        f"| {s26.get('G','—')} | {s26.get('GS','—')} | {s26.get('W','—')} | {s26.get('L','—')} | {s26.get('ERA','—')} | {s26.get('IP','—')} | {s26.get('K','—')} | {s26.get('BB','—')} | {s26.get('WHIP','—')} | {s26.get('K/9','—')} |",
        "",
        "---",
        "",
        "## 📊 2024-2026 近三年数据对比",
        "",
        "| 赛季 | G | GS | W-L | ERA | IP | K | BB | WHIP | K/9 |",
        "|---|---|---|---|---|---|---|---|---|---|",
        f"| 2024 | {s24.get('G','—')} | {s24.get('GS','—')} | {s24.get('W','—')}-{s24.get('L','—')} | {s24.get('ERA','—')} | {s24.get('IP','—')} | {s24.get('K','—')} | {s24.get('BB','—')} | {s24.get('WHIP','—')} | {s24.get('K/9','—')} |",
        f"| 2025 | {s25.get('G','—')} | {s25.get('GS','—')} | {s25.get('W','—')}-{s25.get('L','—')} | {s25.get('ERA','—')} | {s25.get('IP','—')} | {s25.get('K','—')} | {s25.get('BB','—')} | {s25.get('WHIP','—')} | {s25.get('K/9','—')} |",
        f"| 2026 | {s26.get('G','—')} | {s26.get('GS','—')} | {s26.get('W','—')}-{s26.get('L','—')} | {s26.get('ERA','—')} | {s26.get('IP','—')} | {s26.get('K','—')} | {s26.get('BB','—')} | {s26.get('WHIP','—')} | {s26.get('K/9','—')} |",
        "",
        "**趋势简析**：2024 年包办美联投手三冠王并首夺赛扬；2025 年连庄赛扬，ERA 降至 2.21；2026 年 ERA 小幅回升至 2.79，但 BB/9 持续下降至 1.30，WHIP 仍维持在 elite 的 0.91。",
        "",
        "---",
        "",
        "## 📝 备注",
        "",
        "此报告为大谷/佐佐木级别的定制化详细球探报告。",
        "",
        f"*数据来源：MLB.com / MLB Stats API | 生成时间：{TODAY}*"
    ]
    return "\n".join(lines)


def main():
    p = PLAYER
    output_dir = os.path.join(r'D:\baseball\report', p['slug'])
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating custom report for {p['name']} -> {output_dir}")

    generate_cover(p, os.path.join(output_dir, f"{p['slug']}_report_cover.png"))
    generate_season_chart(p, os.path.join(output_dir, f"{p['slug']}_season_comparison.png"))
    if p['type'] == 'pitcher' and p.get('pitch_arsenal'):
        generate_pitch_velocities(p, os.path.join(output_dir, f"{p['slug']}_pitch_velocities.png"))
    generate_grades_chart(p, os.path.join(output_dir, f"{p['slug']}_overall_grades.png"))

    html = build_html(p)
    html_path = os.path.join(output_dir, f"{p['slug']}-scouting-report.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] HTML: {html_path}")

    md = build_md(p)
    md_path = os.path.join(output_dir, f"{p['slug']}-scouting-report.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"[OK] MD: {md_path}")
    print(f"\n{p['name']} custom detailed report completed!")


if __name__ == '__main__':
    main()
