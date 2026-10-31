#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用定制化球员球探报告生成器
为大谷/佐佐木级别的深度报告提供统一模板
每次运行前修改 PLAYER 字典即可生成单一球员报告
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
TODAY = datetime.now().strftime('%Y-%m-%d')

# ---------------------------------------------------------------------------
# 当前球员配置（每次修改此字典生成不同球员）
# ---------------------------------------------------------------------------
PLAYER = {
    "name": "Eric Lauer",
    "slug": "eric-lauer",
    "last_name": "lauer",
    "number": "33",
    "position": "左投先发 (LHP)",
    "position_code": "P",
    "bats_throws": "右打 / 左投",
    "birth_date": "1995-06-03",
    "age": "31",
    "birthplace": "美国俄亥俄州伊利里亚 (Elyria, OH)",
    "height_weight": "6'3\" / 209 lbs",
    "debut": "2018-04-24",
    "college": "Kent State",
    "nickname": "Gomer",
    "status": "活跃",
    "type": "pitcher",  # 'pitcher' or 'batter'
    "summary": """
        <p style="margin-bottom: 15px;">Eric Lauer 是一名<span class="highlight">经验丰富的左投先发</span>，以稳定的控球、变化的球速和顽强的竞赛态度著称。他在大学时期就是全国顶级投手，2016年以首轮第25顺位被圣地亚哥教士选中。</p>
        <p style="margin-bottom: 15px;">2025年，他在蓝鸟队缴出 9胜2败、3.18 ERA、104.2局的优质赛季，并在季后赛中多次挺身而出，包括世界大赛第3战对道奇的4.2局无失分救援。2026年他转战道奇队，但赛季初期数据有所波动，目前仍在适应新环境和竞争激烈的国联西区。</p>
        <p>Lauer 的球风不以球速见长，而是依靠<span class="success">控球、节奏变化和击球软弱度</span>。他的 ceiling 可能不是赛扬级别，但作为轮值后端或长中继/左派角色，他依然具备稳定贡献价值。</p>
    """,
    "career_highlights": """
        <div class="career-highlight">
            <h4>🎓 2016年 - 大学传奇 + 首轮新秀</h4>
            <p>在 Kent State 大学三年生涯 23-10、1.86 ERA、292 K，大三赛季更缴出0.62 ERA、125 K 的历史级数据。荣获 Collegiate Baseball National Player of the Year 和 College Baseball Hall of Fame Pitcher of the Year。2016年选秀首轮第25顺位被教士选中。</p>
        </div>
        <div class="career-highlight">
            <h4>🌟 2018年 - 大联盟首秀</h4>
            <p>2018年4月24日登上大联盟，成为教士轮值的一员。生涯早期以左投控球型投手定位，逐步积累大联盟经验。</p>
        </div>
        <div class="career-highlight">
            <h4>💪 2025年 - 蓝鸟赛季高峰 + 世界大赛英雄</h4>
            <p>15场先发、9-2、3.77 ERA（74.0 IP）；牛棚13场、1.76 ERA、0.75 WHIP。世界大赛第3战对道奇投出4.2局无失分救援，是自2014年 Madison Bumgarner 以来世界大赛最长无失分救援之一。</p>
        </div>
        <div class="career-highlight">
            <h4>🔵 2026年 - 加盟道奇</h4>
            <p>2026年加盟洛杉矶道奇，背号33。目前处于适应期，数据虽有起伏，但丰富的左投经验和季后赛履历使他成为道奇轮值/牛棚中值得信赖的老将。</p>
        </div>
    """,
    "stats_2026": {
        "G": 8, "GS": 6, "W": 1, "L": 5, "ERA": "6.69", "IP": "36.1", "K": 26, "BB": 16,
        "WHIP": "1.49", "K/9": "6.44", "BB/9": "3.96", "HR": 11
    },
    "stats_2025": {
        "G": 28, "GS": 15, "W": 9, "L": 2, "ERA": "3.18", "IP": "104.2", "K": 102, "BB": 26,
        "WHIP": "1.11", "K/9": "8.77", "BB/9": "2.24", "HR": 15
    },
    "cover_stats": [
        ("ERA", "6.69"), ("W-L", "1-5"), ("K", "26"), ("IP", "36.1"),
        ("WHIP", "1.49"), ("K/9", "6.44"), ("Age", "31"), ("2025 ERA", "3.18")
    ],
    "season_chart_2025": [3.18, 1.11, 8.77, 2.24],  # ERA, WHIP, K/9, BB/9
    "season_chart_2026": [6.69, 1.49, 6.44, 3.96],
    "season_chart_stats": ["ERA", "WHIP", "K/9", "BB/9"],
    "pitch_arsenal": [
        {"name": "四缝快速球 (Four-Seam Fastball)", "velocity": "90-93 mph", "avg": "91.5", "desc": "Lauer 的控球主轴，不以球速见长，但进垒点精准。他经常利用上角快速球来抢好球数，或让打者敲出软弱飞球。"},
        {"name": "切球 (Cutter)", "velocity": "86-89 mph", "avg": "87.5", "desc": "主要用来对付右打者，制造横向位移和 weak contact。是他在2025年成功的主要变化球之一。"},
        {"name": "变速球 (Changeup)", "velocity": "82-85 mph", "avg": "83.5", "desc": "对付左打者的关键武器，速度差约8 mph，出手点与快速球相似，能制造挥棒时间差。"},
        {"name": "滑球 (Slider)", "velocity": "79-83 mph", "avg": "81.0", "desc": "作为第四球种，用来在两好球后制造追打。使用频率较低，但能增加球路变化。"}
    ],
    "analysis": """
        <div style="margin-top: 20px;">
            <h3 style="color: #4fc3f7; margin-bottom: 15px;">投球机制与球风</h3>
            <p>Lauer 是一名典型的左投控球型投手。他的快速球均速约91-92 mph，在大联盟先发中并不突出，但他依靠 release point 的一致性、球路组合和节奏变化来压制打者。他的投球机制简洁，重复性高，这使他能够稳定地进入好球带。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">2026年数据下滑原因</h3>
            <p>2026年ERA从2025年的3.18飙升至6.69，WHIP从1.11升至1.49，K/9从8.77降至6.44。这显示他的快速球压制力下降，打者更容易将球打进场内。同时保送率上升，反映他在新球队体系中尚未找到最佳节奏。此外，36.1局的小样本也意味着数据波动较大，不能据此判定他已大幅下滑。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">控球与球路组合</h3>
            <p>控球一直是 Lauer 的核心竞争力。2025年BB/9仅2.24，2026年上升至3.96，需要重新找回好球带边缘的 precision。他的切球和变速球在2025年表现优异，但2026年变化球被击球率偏高，说明打者对他的配球研究更深，需要增加变化幅度或调整使用顺序。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">左投价值与角色定位</h3>
            <p>作为左投，Lauer 在道奇队中具备独特的战术价值。他可以在轮值后端稳定吃局数，也可以在牛棚中担任 long relief 或 lefty specialist。2025年他在蓝鸟队已经证明，只要身体健康、节奏稳定，他依然能缴出接近3.20 ERA 的水准。</p>
        </div>
    """,
    "pros": [
        "左投身份，在轮值和牛棚中具战术价值",
        "大学时代证明过顶级控球能力",
        "2025年 104.2局、3.18 ERA，显示仍有稳定先发能力",
        "2025年世界大赛关键救援，展现季后赛抗压能力",
        "切球/变速球组合在状态好时是有效武器",
        "经验丰富，能在道奇教练团体系下快速调整",
        "BB/9 在稳定状态下低于2.5，控球精确",
        "能够吃下局数，适合长中继/轮换角色"
    ],
    "cons": [
        "2026年ERA 6.69，数据大幅下滑",
        "快速球球速不突出，压制力有限",
        "K/9 从8.77降至6.44，三振能力明显衰退",
        "保送率上升至3.96，控球节奏不稳",
        "被击球率偏高，容易让打者上垒",
        "在新球队/新体系适应期较长",
        "2026年数据为小样本，仍待观察是否真正衰退"
    ],
    "grades": [
        {"label": "Fastball", "value": 50, "grade": "B-"},
        {"label": "Cutter", "value": 55, "grade": "B"},
        {"label": "Changeup", "value": 55, "grade": "B"},
        {"label": "Slider", "value": 50, "grade": "B-"},
        {"label": "Control", "value": 55, "grade": "B"},
        {"label": "Command", "value": 50, "grade": "B-"},
        {"label": "Stamina", "value": 60, "grade": "B+"},
        {"label": "Mental", "value": 65, "grade": "A-"}
    ],
    "overall_grade": 55,
    "overall_label": "B 级 / 控球型左投",
    "overall_desc": "经验丰富的左投，2025年仍具3.20 ERA 水准。2026年处于适应期，若找回控球和变化球节奏，仍是稳定轮值/牛棚贡献者。",
    "future_outlook": """
        <div style="margin-top: 20px;">
            <p>Eric Lauer 的2026年开局不理想，但他的履历显示他具备快速反弹的能力。31岁的他仍处于投手生涯的黄金后期，经验是他的最大资产。在道奇这样的争冠球队中，他可能不需要担任王牌，而是作为稳定左投和长局数提供者。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
            <ol style="margin-left: 20px; line-height: 2;">
                <li><strong>找回控球节奏：</strong>将BB/9压回3.0以下，重新建立 first-pitch strike 优势。</li>
                <li><strong>提升变化球被击球率：</strong>调整切球和变速球的使用比例，避免打者坐等着打。</li>
                <li><strong>增加球速/仰角变化：</strong>利用快速球上角和变速球下坠的对比，提升挥空率。</li>
                <li><strong>定位弹性角色：</strong>在轮值和牛棚之间灵活切换，为道奇提供最大价值。</li>
            </ol>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
            <p><strong>2026（下半季）：</strong>若适应顺利，ERA有望回到4.50-5.00区间，主要作为轮值后端或长中继。</p>
            <p><strong>2027：</strong>若保持健康，可能恢复至3.80-4.20 ERA 水准，担任150局左右的左投轮值。</p>
            <p><strong>2028+：</strong>随着年龄增长，逐渐转向牛棚/长中继角色，以经验和控球帮助球队。</p>

            <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3>
            <ul style="margin-left: 20px; line-height: 2;">
                <li>若2026年持续低迷，可能在交易截止日前被移出轮值</li>
                <li>球速不足导致面对强打阵容时压制力有限</li>
                <li>控球状态未恢复时，容易陷入高保送+高被击球的恶性循环</li>
            </ul>
        </div>
    """,
    "background": """
        <div style="margin-top: 20px;">
            <p>Eric Lance Lauer 出生于美国俄亥俄州伊利里亚（Elyria），绰号 "Gomer"。他在 Midview High School 度过辉煌的四年，不仅是棒球队队长和州最佳投手，也是橄榄球队的二队全州球员。2013年，他在第17轮被多伦多蓝鸟选中，但选择进入 Kent State 大学继续磨练。</p>
            <p>在 Kent State，Lauer 成为校史传奇之一。三年生涯 23胜10败、1.86 ERA，送出292次三振。大三赛季他缴出0.62 ERA 的全国最佳数据，并荣获 Collegiate Baseball National Player of the Year 和 College Baseball Hall of Fame Pitcher of the Year。2024年，他入选 Kent State 大学体育名人堂。</p>
            <p>2016年，圣地亚哥教士在首轮第25顺位选中 Lauer。他在2018年登上大联盟，随后历经教士、酿酒人和蓝鸟等队。2025年在蓝鸟队，他达到职业生涯又一个高峰，常规赛表现出色，更在世界大赛中留下经典救援。2026年，他加盟洛杉矶道奇，希望在这座冠军之城重振旗鼓。</p>
            <p>场外，Lauer 是 Cleveland Cavaliers、Browns 和 New England Patriots 的球迷。他喜欢高尔夫、电子游戏和弹吉他。他以沉稳的职业态度和善于调整著称，是更衣室中深受信赖的老将。</p>
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


# ---------------------------------------------------------------------------
# HTML 模板
# ---------------------------------------------------------------------------
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
        .decline-note { background: rgba(255, 152, 0, 0.1); border: 1px solid rgba(255, 152, 0, 0.3); border-radius: 10px; padding: 15px; margin: 15px 0; }
        .decline-note h4 { color: #ff9800; margin-bottom: 10px; }
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


# ---------------------------------------------------------------------------
# Chart generation
# ---------------------------------------------------------------------------

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

    subtitle = p.get('cover_subtitle', '')
    if not subtitle:
        subtitle = f"{p['status']} | {p['college']} | MLB Debut {p['debut']}"
    ax.text(0.5, 0.08, subtitle, fontsize=14, ha='center',
            color='#90a4ae', transform=ax.transAxes, style='italic')
    ax.text(0.5, 0.02, f'Generated: {TODAY} | Data: MLB.com, MLB Stats API',
            fontsize=10, ha='center', color='#666', transform=ax.transAxes)

    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()


def generate_season_chart(p, output_path):
    stats = p['season_chart_stats']
    vals_2025 = p['season_chart_2025']
    vals_2026 = p['season_chart_2026']

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    colors = ['#4fc3f7', '#ff9800']

    for idx, stat in enumerate(stats):
        ax = axes[idx]
        vals = [vals_2025[idx], vals_2026[idx]]
        bars = ax.bar(['2025', '2026'], vals, color=colors, edgecolor='white', alpha=0.9, width=0.5)
        ax.set_title(stat, fontsize=14, fontweight='bold', color='#1a1a2e')
        max_val = max(vals) * 1.25 if max(vals) != 0 else 1
        ax.set_ylim(0, max_val)
        ax.grid(axis='y', alpha=0.3)
        for bar, val in zip(bars, vals):
            height = bar.get_height()
            if p['type'] == 'pitcher':
                text = f'{val:.2f}' if stat in ['ERA', 'WHIP'] else f'{val:.1f}'
            else:
                text = f'{val:.3f}'
            ax.text(bar.get_x() + bar.get_width()/2., height + max_val*0.02,
                    text, ha='center', va='bottom', fontweight='bold', fontsize=11)

    fig.suptitle(f"{p['name']} - 2025 vs 2026 Season Comparison", fontsize=16, fontweight='bold', color='#1a1a2e', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def generate_pitch_velocities(p, output_path):
    print(f"[DEBUG] generate_pitch_velocities for {p.get('name')}, arsenal len={len(p.get('pitch_arsenal', []))}")
    if not p.get('pitch_arsenal'):
        return
    arsenal = p['pitch_arsenal']
    fig, ax = plt.subplots(figsize=(12, 6))

    pitches = [a['name'] for a in arsenal]
    min_velo = []
    max_velo = []
    for i, a in enumerate(arsenal):
        print(f"[DEBUG] pitch {i}: {a.get('velocity')}")
        # parse "90-93 mph" to min/max
        try:
            rng = a['velocity'].split('（')[0].strip()
            parts = rng.replace('mph', '').split('-')
            min_velo.append(float(parts[0].strip()))
            max_velo.append(float(parts[1].strip()))
        except Exception as e:
            print(f"[DEBUG] parse exception: {e}")
            min_velo.append(0)
            max_velo.append(0)
    avg_velo = [(min_v + max_v) / 2 for min_v, max_v in zip(min_velo, max_velo)]
    print(f"[DEBUG] len pitches={len(pitches)} min={len(min_velo)} max={len(max_velo)} avg={len(avg_velo)}")
    print(f"[DEBUG] min_velo={min_velo}")
    print(f"[DEBUG] max_velo={max_velo}")
    print(f"[DEBUG] avg_velo={avg_velo}")

    x = np.arange(len(pitches))
    width = 0.35
    bars1 = ax.bar(x - width/2, min_velo, width, label='Min', color='#4fc3f7', alpha=0.8)
    bars2 = ax.bar(x + width/2, max_velo, width, label='Max', color='#ff9800', alpha=0.8)

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
    ax.set_ylim(70, 105)

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


# ---------------------------------------------------------------------------
# HTML builders
# ---------------------------------------------------------------------------

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


def build_batting_grid(stats):
    order = [('G', '出赛'), ('AVG', '打击率'), ('OBP', '上垒率'), ('SLG', '长打率'), ('OPS', 'OPS'),
             ('HR', '本垒打'), ('RBI', '打点'), ('SB', '盗垒')]
    html = ""
    for k, label in order:
        val = stats.get(k, '—')
        html += f'''
                <div class="stat-card">
                    <span class="stat-value">{val}</span>
                    <div class="stat-label">{label}</div>
                </div>'''
    return html


def build_pitching_table(s25, s26):
    rows = ""
    for year, s in [("2025", s25), ("2026", s26)]:
        rows += f'''                    <tr>
                        <td class="{'warning' if year == '2026' else 'highlight'}">{year}</td>
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


def build_batting_table(s25, s26):
    rows = ""
    for year, s in [("2025", s25), ("2026", s26)]:
        rows += f'''                    <tr>
                        <td class="{'warning' if year == '2026' else 'highlight'}">{year}</td>
                        <td>{s.get('G', '—')}</td>
                        <td>{s.get('AVG', '—')}</td>
                        <td>{s.get('OBP', '—')}</td>
                        <td>{s.get('SLG', '—')}</td>
                        <td>{s.get('OPS', '—')}</td>
                        <td>{s.get('HR', '—')}</td>
                        <td>{s.get('RBI', '—')}</td>
                        <td>{s.get('BB', '—')}</td>
                        <td>{s.get('SO', '—')}</td>
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


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------

def build_html(p):
    html = HTML_TEMPLATE
    html = html.replace('__TITLE__', f"{p['name']} 球探报告")
    html = html.replace('__PLAYER_NAME__', p['name'])
    html = html.replace('__SUBTITLE__', f"Los Angeles Dodgers #{p['number']} | {p['position']} | {p['status']}")
    html = html.replace('__COVER_IMG__', f"{p['slug']}_report_cover.png")
    html = html.replace('__INFO_GRID__', build_info_grid(p))
    html = html.replace('__SCOUTING_SUMMARY__', p['summary'])
    html = html.replace('__CAREER_HIGHLIGHTS__', p['career_highlights'])

    # 2026 stats section
    if p['type'] == 'pitcher':
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
            <h2>📊 2025 vs 2026 赛季对比</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="{p['slug']}_season_comparison.png" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
            <h3 style="margin-top: 30px; color: #4fc3f7;">投球数据对比</h3>
            <table class="comparison-table">
                <thead>
                    <tr><th>赛季</th><th>G</th><th>GS</th><th>W-L</th><th>ERA</th><th>IP</th><th>K</th><th>BB</th><th>WHIP</th><th>K/9</th></tr>
                </thead>
                <tbody>
{build_pitching_table(p['stats_2025'], p['stats_2026'])}
                </tbody>
            </table>
        </div>
'''
    else:
        stats_section = f'''
        <div class="section">
            <h2>📊 2026赛季打击数据</h2>
            <div class="stats-grid">
{build_batting_grid(p['stats_2026'])}
            </div>
        </div>
'''
        season_section = f'''
        <div class="section">
            <h2>📊 2025 vs 2026 赛季对比</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="{p['slug']}_season_comparison.png" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
            <h3 style="margin-top: 30px; color: #4fc3f7;">打击数据对比</h3>
            <table class="comparison-table">
                <thead>
                    <tr><th>赛季</th><th>G</th><th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th><th>HR</th><th>RBI</th><th>BB</th><th>SO</th></tr>
                </thead>
                <tbody>
{build_batting_table(p['stats_2025'], p['stats_2026'])}
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
    s26 = p['stats_2026']
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
    ]
    if p['type'] == 'pitcher':
        lines.append(f"| G | GS | W | L | ERA | IP | K | BB | WHIP | K/9 |")
        lines.append(f"|---|---|---|---|---|---|---|---|---|---|")
        lines.append(f"| {s26.get('G','—')} | {s26.get('GS','—')} | {s26.get('W','—')} | {s26.get('L','—')} | {s26.get('ERA','—')} | {s26.get('IP','—')} | {s26.get('K','—')} | {s26.get('BB','—')} | {s26.get('WHIP','—')} | {s26.get('K/9','—')} |")
    else:
        lines.append(f"| G | AVG | OBP | SLG | OPS | HR | RBI | SB | BB | SO |")
        lines.append(f"|---|---|---|---|---|---|---|---|---|---|")
        lines.append(f"| {s26.get('G','—')} | {s26.get('AVG','—')} | {s26.get('OBP','—')} | {s26.get('SLG','—')} | {s26.get('OPS','—')} | {s26.get('HR','—')} | {s26.get('RBI','—')} | {s26.get('SB','—')} | {s26.get('BB','—')} | {s26.get('SO','—')} |")
    lines.extend(["", "---", "", "## 📝 备注", "", "此报告为大谷/佐佐木级别的定制化详细球探报告。", "", f"*数据来源：MLB.com / MLB Stats API | 生成时间：{TODAY}*"])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

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
