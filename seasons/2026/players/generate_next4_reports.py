#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 Kyle Tucker、Max Muncy、Andy Pages、Teoscar Hernández
生成佐佐木朗希级别的详细球探报告（HTML + 图表 + Markdown）
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from datetime import datetime

BASE_DIR = r'D:\baseball\report'
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

TODAY = datetime.now().strftime('%Y-%m-%d')
DATA_DATE = (datetime.now().strftime('%Y-%m-%d'))


def slugify(name):
    """生成文件夹/文件名使用的 slug（去除重音等）"""
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
        .comparison-table th, .comparison-table td { padding: 15px; text-align: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
        .comparison-table th { background: rgba(0, 90, 156, 0.3); color: #4fc3f7; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
        .comparison-table tr:hover { background: rgba(255, 255, 255, 0.05); }
        .pitch-arsenal { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
        .pitch-card {
            background: linear-gradient(135deg, rgba(0, 90, 156, 0.2) 0%, rgba(26, 84, 144, 0.2) 100%);
            border-radius: 10px; padding: 20px; border-left: 4px solid #4fc3f7;
        }
        .pitch-card h3 { color: #4fc3f7; margin-bottom: 10px; }
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
        .mvp { color: #FFD700; font-weight: bold; }
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

        <div class="section">
            <h2>📊 2026赛季统计</h2>
            <div class="stats-grid">
__STATS_2026_GRID__
            </div>
        </div>

        <div class="section">
            <h2>📊 2025 vs 2026 赛季对比</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="__SEASON_CHART__" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
            <h3 style="margin-top: 30px; color: #4fc3f7;">打击数据对比</h3>
            <table class="comparison-table">
                <thead>
                    <tr><th>赛季</th><th>G</th><th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th><th>HR</th><th>RBI</th><th>BB</th><th>SO</th></tr>
                </thead>
                <tbody>
__SEASON_TABLE__
                </tbody>
            </table>
        </div>

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


PLAYERS = [
    {
        "name": "Kyle Tucker",
        "slug": "kyle-tucker",
        "last_name": "tucker",
        "number": "23",
        "position": "右外野手 (RF)",
        "bats_throws": "左打 / 右投",
        "birth_date": "1997-01-17",
        "age": "29",
        "birthplace": "美国佛罗里达州坦帕",
        "height_weight": "6'3\" / 212 lbs",
        "debut": "2018-07-07",
        "nickname": "Tuck",
        "subtitle": "Los Angeles Dodgers #23 | 右外野手 | 左打 | 强力外野",
        "summary": """
            <p style="margin-bottom: 15px;">Kyle Tucker 是当今大联盟最具天赋的右外野手之一，<span class="highlight">以卓越的力量-速度组合、顶级选球能力和金手套级别的防守著称</span>。</p>
            <p style="margin-bottom: 15px;">他在2025年于小熊队打出.266/.377/.464、22轰、25盗的精英赛季，证明自己是联盟前五的右外野手。2026年加盟道奇后，虽然长打数据有所下滑，但.341的上垒率仍显示其出色的plate discipline。</p>
            <p>Tucker 的挥棒平顺、防守范围大、臂力优秀，是道奇外野防线的核心人物。下半季有望找回长打节奏，成为球队季后赛的关键武器。</p>
        """,
        "career_highlights": """
            <div class="career-highlight">
                <h4>🏆 2022年 - 世界大赛冠军（休斯顿太空人）</h4>
                <p>生涯早期即随太空人夺冠，积累丰富季后赛经验。</p>
            </div>
            <div class="career-highlight">
                <h4>🥇 2023年 - 全明星 + 金手套提名</h4>
                <p>攻守俱佳的赛季，确立联盟顶级右外野手地位。</p>
            </div>
            <div class="career-highlight">
                <h4>💪 2025年 - 30-30级别的完整赛季（芝加哥小熊）</h4>
                <p>.266 AVG | .377 OBP | .464 SLG | 22 HR | 73 RBI | 25 SB</p>
                <p>精英级别的全能表现，自由市场最炙手可热的强打好手。</p>
            </div>
        """,
        "stats_2026": {"G": 91, "AVG": ".244", "OBP": ".341", "SLG": ".375", "OPS": ".716",
                       "HR": 7, "RBI": 47, "SB": 6, "2B": 18, "3B": 2, "BB": 48, "SO": 76},
        "stats_2025": {"G": 136, "AVG": ".266", "OBP": ".377", "SLG": ".464", "OPS": ".841",
                       "HR": 22, "RBI": 73, "SB": 25, "2B": 25, "3B": 4, "BB": 87, "SO": 88},
        "cover_stats": [("AVG", ".244"), ("OPS", ".716"), ("HR", "7"), ("RBI", "47"),
                        ("SB", "6"), ("OBP", ".341"), ("Age", "29"), ("2025 OPS", ".841")],
        "analysis": """
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">打击机制</h3>
                <p>Tucker 的挥棒路径长而流畅，出手点低，能够产生强劲的拉打力量。他的左打挥棒很适合道奇体育场的右外野短墙，但2026年 his launch angle 似乎偏低，导致长打率从.464降至.375。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">选球能力</h3>
                <p>选球是 Tucker 最核心的竞争力。2026年保送率仍维持12.6%，上垒率.341，高于联盟平均。他不会被坏球诱惑，经常能迫使投手进入有利count。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">防守能力</h3>
                <p>Tucker 的右外野防守达到金手套级别。6'3"的身材加上出色的第一步反应，使他能覆盖大量范围。臂力准确且有力，能够有效阻止跑者推进。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">2026年调整空间</h3>
                <p>2026年的打击数据下滑主要源于力量输出不足（7轰 vs 2025年22轰）。打击率.244也低于生涯平均，可能与新环境、新球探报告以及略微增加的上旋球有关。下半季若提升击球仰角，仍有20+轰潜力。</p>
            </div>
        """,
        "pros": [
            "精英级别的选球能力，保送率位居联盟前列",
            "力量-速度兼具，曾有25盗记录",
            "金手套级别的右外野防守",
            "臂力优秀，能够有效阻止跑垒",
            "关键时刻具备长打能力",
            "丰富的季后赛经验（2022年世界大赛冠军）",
            "上垒能力稳定，能担任第一棒或第二棒",
            "身体健康，出勤率较高"
        ],
        "cons": [
            "2026年力量输出明显下滑（仅7轰）",
            "打击率.244低于生涯平均",
            "面对高球速快速球时偶尔出棒较慢",
            "道奇主场的右外野短墙尚未充分利用",
            "对左投的压制力略逊于右投",
            "高期望值下的薪资压力"
        ],
        "grades": [
            {"label": "Contact", "value": 60, "grade": "A-"},
            {"label": "Power", "value": 60, "grade": "A-"},
            {"label": "Discipline", "value": 70, "grade": "A"},
            {"label": "Speed", "value": 60, "grade": "A-"},
            {"label": "Defense", "value": 70, "grade": "A"},
            {"label": "Arm", "value": 65, "grade": "A-"},
            {"label": "Clutch", "value": 60, "grade": "A-"},
            {"label": "Leadership", "value": 55, "grade": "B"}
        ],
        "overall_grade": 62,
        "overall_label": "A- 级 / 全明星外野",
        "overall_desc": "攻守兼备的右外野手，只要找回长打节奏，仍是联盟顶级外野",
        "future_outlook": """
            <div style="margin-top: 20px;">
                <p>Kyle Tucker 仍处于29岁的黄金年龄，2026年的数据下滑更像是环境适应期而非能力衰退。他的核心技能（选球、防守、速度）都保持在高水准，下半季最可能看到长打复苏。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>提升击球仰角：</strong>将更多滚地球转化为长打， especially 利用右外野短墙</li>
                    <li><strong>保持选球节奏：</strong>不要因成绩压力而扩大好球带</li>
                    <li><strong>增加盗垒尝试：</strong>在6 SB基础上，恢复至15-20盗水准</li>
                    <li><strong>面对左投加强：</strong>针对性研究左投配球模式</li>
                </ol>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
                <p><strong>2026（下半季）：</strong>OPS有望回升至.800+，全季约20轰、15盗</p>
                <p><strong>2027-2028：</strong>进入生涯巅峰，维持.270/.360/.480，25轰+20盗</p>
                <p><strong>2029+：</strong>随着年龄增长速度下降，但凭借选球和防守仍具高价值</p>

                <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3>
                <ul style="margin-left: 20px; line-height: 2;">
                    <li>力量输出持续低迷可能影响打序位置</li>
                    <li>道奇外野竞争激烈，需保持高产出</li>
                    <li>高价合约带来的期望值压力</li>
                </ul>
            </div>
        """,
        "background": """
            <div style="margin-top: 20px;">
                <p>Kyle Tucker 出生于佛罗里达州坦帕，棒球基因深厚：他的父亲 Fred Tucker 和哥哥 Preston Tucker 都曾在职业棒球体系打拼。Kyle 在高中时期就是全美瞩目的强打少年，2015年MLB选秀中，他在首轮第5顺位被休斯顿太空人选中。</p>
                <p>在太空人农场系统，Tucker 迅速展现出顶级天赋，2018年登上大联盟。他在2022年帮助球队夺得世界大赛冠军，并在2023年入选全明星。2025年，他在芝加哥小熊队打出职业生涯最完整的一个赛季，成为自由市场最大牌的强打外野手之一。</p>
                <p>2026年，Tucker 加盟洛杉矶道奇队，与外野搭档 Andy Pages、Teoscar Hernández 组成强力外野防线。他的防守和选球使他成为道奇打线中不可或缺的一员。</p>
                <p>场外，Tucker 以低调和职业态度著称。他喜欢钓鱼和高尔夫，是球队更衣室中稳定的存在。</p>
            </div>
        """
    },
    {
        "name": "Max Muncy",
        "slug": "max-muncy",
        "last_name": "muncy",
        "number": "13",
        "position": "三垒手 (3B)",
        "bats_throws": "左打 / 右投",
        "birth_date": "1990-08-25",
        "age": "35",
        "birthplace": "美国德克萨斯州米德兰",
        "height_weight": "5'10\" / 215 lbs",
        "debut": "2015-04-25",
        "nickname": "Maximus",
        "subtitle": "Los Angeles Dodgers #13 | 三垒手 | 左打 | 强力左打",
        "summary": """
            <p style="margin-bottom: 15px;">Max Muncy 是道奇队近年来最具代表性的力量型左打者之一，<span class="highlight">以高保送率、强劲拉打力量和大赛经验闻名</span>。</p>
            <p style="margin-bottom: 15px;">2026年，35岁的 Muncy 仍维持.259/.354/.488、.842 OPS 的高效产出，其中长打率.488显示他的power tool并未衰退。他是道奇打线中重要的middle-of-the-order bat。</p>
            <p>Muncy 的防守虽然不以范围见长，但在三垒位置基本功扎实，失误率低。他的领导力和冠军经验对道奇年轻球员的成长极具价值。</p>
        """,
        "career_highlights": """
            <div class="career-highlight">
                <h4>🏆 2018年 - 道奇生涯 breakout</h4>
                <p>从A's minor league deal加入道奇后，轰出35支全垒打，.973 OPS，成为球队惊喜。</p>
            </div>
            <div class="career-highlight">
                <h4>🥇 2019年 - 首次全明星</h4>
                <p>35轰，98打点，确立联盟顶级力量型左打者地位。</p>
            </div>
            <div class="career-highlight">
                <h4>🏆 2020年 - 世界大赛冠军</h4>
                <p>在泡泡赛季中贡献关键长打，帮助道奇时隔32年再夺世界大赛冠军。</p>
            </div>
            <div class="career-highlight">
                <h4>💪 2021年 - 36轰赛季</h4>
                <p>36支全垒打、94打点，连续第二年展现 elite power。</p>
            </div>
        """,
        "stats_2026": {"G": 89, "AVG": ".259", "OBP": ".354", "SLG": ".488", "OPS": ".842",
                       "HR": 17, "RBI": 40, "SB": 1, "2B": 14, "3B": 1, "BB": 40, "SO": 79},
        "stats_2025": {"G": 100, "AVG": ".243", "OBP": ".376", "SLG": ".470", "OPS": ".846",
                       "HR": 19, "RBI": 67, "SB": 4, "2B": 10, "3B": 2, "BB": 64, "SO": 83},
        "cover_stats": [("AVG", ".259"), ("OPS", ".842"), ("HR", "17"), ("RBI", "40"),
                        ("OBP", ".354"), ("SLG", ".488"), ("Age", "35"), ("All-Star", "2019")],
        "analysis": """
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">打击机制</h3>
                <p>Muncy 采用典型的左打拉打姿势，上挥角度大，擅长将球拉起。他的击球结果高度偏向飞球和滚地球两极，是典型的「三真」打者：高保送、高三振、高长打。2026年他的打击率提升至.259，显示他正在做出更稳定的contact调整。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">选球能力</h3>
                <p>Muncy 的选球能力极为出色。2026年保送率11.9%，上垒率.354，能够持续为打线制造机会。他不会被边缘坏球诱惑，迫使投手必须进入好球带。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">防守能力</h3>
                <p>虽然 Muncy 的身材（5'10"）在三垒不具优势，但他的基本功扎实，手臂足够应付内野传球。守备范围属于平均以下，但靠站位和预判弥补。随着年龄增长，他可能逐渐向一垒/DH过渡。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">年龄与伤病</h3>
                <p>35岁的 Muncy 已度过体能巅峰，但2025年100场和2026年89场的出勤率显示他仍可靠。道奇可能会让他在赛季末段更多休息，以保持季后赛状态。</p>
            </div>
        """,
        "pros": [
            "精英级别的力量输出，17轰展现持续power",
            "出色的选球能力，保送率稳定",
            "高OPS和长打率，middle-of-the-order威胁",
            "丰富的季后赛和冠军经验",
            "更衣室领袖，年轻球员导师",
            "左打平衡道奇打线",
            "关键时刻长打能力",
            "三垒/一垒/DH多功能性"
        ],
        "cons": [
            "三振率偏高，容易吞下关键K",
            "打击率偏低，非高average类型",
            "速度极差，盗垒贡献几乎为零",
            "三垒防守范围有限",
            "对左投有时表现挣扎",
            "年龄35岁，衰退风险增加"
        ],
        "grades": [
            {"label": "Contact", "value": 50, "grade": "B"},
            {"label": "Power", "value": 70, "grade": "A"},
            {"label": "Discipline", "value": 70, "grade": "A"},
            {"label": "Speed", "value": 35, "grade": "C+"},
            {"label": "Defense", "value": 50, "grade": "B"},
            {"label": "Arm", "value": 55, "grade": "B"},
            {"label": "Clutch", "value": 60, "grade": "A-"},
            {"label": "Leadership", "value": 65, "grade": "A-"}
        ],
        "overall_grade": 60,
        "overall_label": "B+ 级 / 强打三垒手",
        "overall_desc": "力量与选球兼具的左打者，是道奇打线的核心火力点",
        "future_outlook": """
            <div style="margin-top: 20px;">
                <p>Max Muncy 已进入职业生涯后期，但他的力量输出和选球能力仍使他具备高价值。道奇可能会逐步降低他的三垒守备负担，让他在一垒和DH之间轮换，延长职业生涯。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>减少三垒守备：</strong>更多轮换至一垒/DH，保护身体</li>
                    <li><strong>维持选球：</strong>继续以高保送率贡献上垒</li>
                    <li><strong>打击率优化：</strong>将更多滚地球转化为平飞球，提升BABIP</li>
                    <li><strong>经验传承：</strong>指导年轻力量型左打者如 Andy Pages</li>
                </ol>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
                <p><strong>2026（下半季）：</strong>维持.250/.350/.480，全季约25-28轰</p>
                <p><strong>2027：</strong>可能转为1B/DH为主，OPS仍保持.800+</p>
                <p><strong>2028+：</strong>以老将身份贡献，重点在power off the bench</p>

                <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3>
                <ul style="margin-left: 20px; line-height: 2;">
                    <li>年龄增长导致守备范围进一步下降</li>
                    <li>三振率偏高，面对 elite 投手容易被压制</li>
                    <li>伤病风险随年龄增加</li>
                </ul>
            </div>
        """,
        "background": """
            <div style="margin-top: 20px;">
                <p>Max Muncy 出生于德克萨斯州米德兰，父亲曾是职业球员。他在高中时展现出 strong plate discipline 和力量潜质，2012年选秀中在第5轮被奥克兰运动家选中。</p>
                <p>Muncy 在A's体系中上升，2015年完成大联盟首秀，但表现平平。2017年他曾短暂离开棒球，经过训练调整后，2018年与道奇签下小联盟合约。这次签约成为他生涯转折点——他在道奇打出35轰，震惊联盟。</p>
                <p>2019年，Muncy 首次入选全明星，并帮助球队在2020年夺得世界大赛冠军。2021年他再次轰出36支全垒打，巩固了自己作为道奇核心打者的地位。</p>
                <p>场外，Muncy 以幽默和领导力著称。他经常在社交媒体上自嘲自己的「三真」打法，并积极参与青少年棒球活动。他的妻子 Kellie 和孩子们经常出现在道奇球场。</p>
            </div>
        """
    },
    {
        "name": "Andy Pages",
        "slug": "andy-pages",
        "last_name": "pages",
        "number": "44",
        "position": "中外野手 (CF)",
        "bats_throws": "右打 / 右投",
        "birth_date": "2000-12-08",
        "age": "25",
        "birthplace": "古巴",
        "height_weight": "6'1\" / 212 lbs",
        "debut": "2024-04-16",
        "nickname": "Pages",
        "subtitle": "Los Angeles Dodgers #44 | 中外野手 | 右打 | 新秀全明星",
        "summary": """
            <p style="margin-bottom: 15px;">Andy Pages 是道奇队最具潜力的年轻球员之一，<span class="highlight">以中外野的 premium position、右打力量和持续进步的选球能力崭露头角</span>。</p>
            <p style="margin-bottom: 15px;">2025年，他在完整赛季中击出27轰、86打点，首次入选全明星，展现成为球队长期中外野手的潜力。2026年，他的OPS进一步提升至.807，上垒率从.313提升至.336，显示plate discipline持续进步。</p>
            <p>Pages 的速度、臂力和防守范围使他成为道奇外野的未来核心。25岁的他仍有巨大成长空间，是道奇农场体系最成功的培养案例之一。</p>
        """,
        "career_highlights": """
            <div class="career-highlight">
                <h4>🌟 2024年 - MLB 首秀</h4>
                <p>2024年4月16日完成大联盟首秀，迅速展现 power-speed 潜力。</p>
            </div>
            <div class="career-highlight">
                <h4>⭐ 2025年 - 首次全明星 + 27轰赛季</h4>
                <p>.272 AVG | .461 SLG | 27 HR | 86 RBI | 14 SB</p>
                <p>在完整赛季中证明自己是道奇外野的未来核心，首次入选全明星。</p>
            </div>
            <div class="career-highlight">
                <h4>📈 2026年 - 持续进步</h4>
                <p>.270 AVG | .336 OBP | .471 SLG | .807 OPS | 17 HR | 66 RBI</p>
                <p>上垒率和OPS双双提升，展现 maturity 与 adjustability。</p>
            </div>
        """,
        "stats_2026": {"G": 96, "AVG": ".270", "OBP": ".336", "SLG": ".471", "OPS": ".807",
                       "HR": 17, "RBI": 66, "SB": 8, "2B": 21, "3B": 1, "BB": 34, "SO": 80},
        "stats_2025": {"G": 156, "AVG": ".272", "OBP": ".313", "SLG": ".461", "OPS": ".774",
                       "HR": 27, "RBI": 86, "SB": 14, "2B": 27, "3B": 1, "BB": 29, "SO": 135},
        "cover_stats": [("AVG", ".270"), ("OPS", ".807"), ("HR", "17"), ("RBI", "66"),
                        ("SB", "8"), ("OBP", ".336"), ("Age", "25"), ("All-Star", "2025")],
        "analysis": """
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">打击机制</h3>
                <p>Pages 的挥棒充满爆发力，出手速度快，能够将球打到所有方向。他的力量主要来自下半身和髋部旋转， his bat speed 使他能够处理高球速。2026年他在选球上的进步尤其明显，保送率从4.6%提升至8.3%。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">选球能力</h3>
                <p>选球是 Pages 最大的进步点。2025年他仅有29次保送，但2026年已经34次，且出赛场次还更少。如果他继续改善击球区纪律，上垒率有望突破.350。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">防守能力</h3>
                <p>Pages 是道奇中外野的首选。他的速度、判断力和第一步反应使他能够覆盖大量中外野范围。臂力足以阻止跑者推进，是 premium position 的 elite defender。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">成长空间</h3>
                <p>25岁的 Pages 仍在学习大联盟投手。他的三振率仍偏高（19.5%），面对变化球时偶尔出棒过大。如果能够提升两好球后的contact能力，他将成为.280/.350/.500级别的全明星。</p>
            </div>
        """,
        "pros": [
            "年轻（25岁），成长空间巨大",
            "中外野 premium position 的 elite defender",
            "力量-速度兼具，20-20潜力",
            "选球能力持续进步",
            "臂力优秀，防守价值高",
            "已经展现全明星水准（2025）",
            "打球态度积极，学习能力强",
            "道奇重点培养的未来核心"
        ],
        "cons": [
            "三振率仍偏高，contact稳定性待提升",
            "对变化球识别仍在进步中",
            "2026年盗垒次数较2025年下降",
            "面对 elite 左投有时被压制",
            "比赛经验相对较少",
            "高强度赛季下体能管理需加强"
        ],
        "grades": [
            {"label": "Contact", "value": 55, "grade": "B+"},
            {"label": "Power", "value": 60, "grade": "A-"},
            {"label": "Discipline", "value": 55, "grade": "B+"},
            {"label": "Speed", "value": 60, "grade": "A-"},
            {"label": "Defense", "value": 65, "grade": "A-"},
            {"label": "Arm", "value": 60, "grade": "A-"},
            {"label": "Clutch", "value": 55, "grade": "B+"},
            {"label": "Leadership", "value": 50, "grade": "B"}
        ],
        "overall_grade": 58,
        "overall_label": "B+ 级 / 潜力全明星",
        "overall_desc": "年轻且全面，是道奇未来5-10年的中外野答案",
        "future_outlook": """
            <div style="margin-top: 20px;">
                <p>Andy Pages 是道奇队未来最光明的资产之一。他在25岁就已经是联盟平均以上的中外野手，并且每年都有明显进步。如果他的选球和contact能力继续发展，他有望成为年度全明星甚至MVP候选人。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>继续提升选球：</strong>目标保送率10%+，上垒率.350</li>
                    <li><strong>降低三振率：</strong>在两好球后采用更短挥棒路径</li>
                    <li><strong>提升盗垒效率：</strong>恢复15-20盗水准</li>
                    <li><strong>保持防守：</strong>继续巩固金手套级别中外野防守</li>
                </ol>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
                <p><strong>2026（下半季）：</strong>OPS有望维持在.800+，全季约25轰、12盗</p>
                <p><strong>2027-2028：</strong>进入全明星常客，.280/.350/.500，30轰+20盗</p>
                <p><strong>2029+：</strong>道奇外野核心，可能获得金手套并进入MVP讨论</p>

                <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3>
                <ul style="margin-left: 20px; line-height: 2;">
                    <li>高 strikeout rate 可能导致成绩波动</li>
                    <li>中外野防守对身体负担大，需管理健康</li>
                    <li>外界期望值过高可能带来心理压力</li>
                </ul>
            </div>
        """,
        "background": """
            <div style="margin-top: 20px;">
                <p>Andy Pages 出生于古巴，是近年来道奇从古巴签下最成功的年轻球员之一。他在2017年离开古巴，2018年以自由球员身份与洛杉矶道奇签约，签约金达到当年国际自由球员市场的顶额。</p>
                <p>Pages 在道奇农场系统中迅速上升，以出色的中外野防守和 raw power 著称。2024年4月16日，他完成大联盟首秀。尽管首个赛季有起伏，但他在2025年就打出27轰、86打点的完整赛季，并首次入选全明星。</p>
                <p>Pages 的成长速度超出预期，他被视为道奇继 Cody Bellinger 之后最重要的中外野培养成果。他的古巴背景也使他成为拉丁美洲年轻球员在道奇体系的榜样。</p>
                <p>场外，Pages 以谦逊和努力工作闻名。他的英语进步迅速，与队友关系融洽。他喜欢音乐和家庭聚会，是道奇更衣室中受欢迎的成员。</p>
            </div>
        """
    },
    {
        "name": "Teoscar Hernández",
        "slug": "teoscar-hernandez",
        "last_name": "hernandez",
        "number": "37",
        "position": "左外野手 (LF)",
        "bats_throws": "右打 / 右投",
        "birth_date": "1992-10-15",
        "age": "33",
        "birthplace": "多米尼加共和国",
        "height_weight": "6'0\" / 215 lbs",
        "debut": "2016-08-12",
        "nickname": "电风扇",
        "subtitle": "Los Angeles Dodgers #37 | 左外野手 | 右打 | 电风扇",
        "summary": """
            <p style="margin-bottom: 15px;">Teoscar Hernández 是一位<span class="highlight">以 raw power 和强劲臂力著称的 veteran 外野手</span>，在中国球迷圈有「电风扇」的绰号，形容他挥棒时的大幅度动作和高三振率。</p>
            <p style="margin-bottom: 15px;">2025年，他轰出25支全垒打、89打点，是道奇外野的重要火力点。然而2026年受限于伤病和状态起伏，仅出战63场，OPS下滑至.706。</p>
            <p>Hernández 仍然拥有改变比赛的一击能力，但随着年龄增长，他需要更精准地管理体能和击球选择，以延长职业生涯。</p>
        """,
        "career_highlights": """
            <div class="career-highlight">
                <h4>🥇 2020年 - 美联银棒奖</h4>
                <p>在多伦多蓝鸟打出.289/.340/.579，16轰，展现 elite power。</p>
            </div>
            <div class="career-highlight">
                <h4>🥇 2021年 - 再次银棒奖 + 32轰</h4>
                <p>.296 AVG | .524 SLG | 32 HR | 116 RBI，生涯最佳赛季。</p>
            </div>
            <div class="career-highlight">
                <h4>💪 2025年 - 道奇25轰赛季</h4>
                <p>.247 AVG | .454 SLG | 25 HR | 89 RBI | 5 SB</p>
                <p>加盟道奇后仍是外野重要火力点，贡献大量关键长打。</p>
            </div>
        """,
        "stats_2026": {"G": 63, "AVG": ".243", "OBP": ".319", "SLG": ".387", "OPS": ".706",
                       "HR": 8, "RBI": 36, "SB": 2, "2B": 8, "3B": 0, "BB": 24, "SO": 70},
        "stats_2025": {"G": 134, "AVG": ".247", "OBP": ".284", "SLG": ".454", "OPS": ".738",
                       "HR": 25, "RBI": 89, "SB": 5, "2B": 29, "3B": 1, "BB": 26, "SO": 134},
        "cover_stats": [("AVG", ".243"), ("OPS", ".706"), ("HR", "8"), ("RBI", "36"),
                        ("SB", "2"), ("OBP", ".319"), ("Age", "33"), ("Silver Slugger", "2x")],
        "analysis": """
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">打击机制</h3>
                <p>Hernández 的挥棒动作大、力量强，能够击出极远距离的全垒打。他喜欢追打高位快速球和低位滑球，但也因此容易被边缘球诱导。2026年 his launch angle 和击球点似乎不够稳定，导致长打率大幅下滑。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">选球能力</h3>
                <p>选球是 Hernández 长期以来的弱点。2025年OBP仅.284，2026年提升至.319，已经是进步。但他仍需减少对坏球的追逐，尤其是在两好球后。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">防守能力</h3>
                <p>Hernández 在左外野的防守属于平均水准。他的臂力是他的最大优势，曾多次送出精彩助杀。但 range 和脚步速度随着年龄增长有所下滑。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">2026年低迷原因</h3>
                <p>2026年仅出赛63场，显示他可能受到伤病困扰。即使健康，他的打击数据也全面下滑，力量不再像2025年那样稳定。这可能意味着他需要转型为 platoon/DH 角色。</p>
            </div>
        """,
        "pros": [
            " raw power 出色，能击出深远全垒打",
            "两次银棒奖得主，power tool 经过验证",
            "左外野臂力强劲，助杀能力优秀",
            " postseason 经验丰富",
            "右打可平衡打线面对左投",
            "更衣室气氛活跃，团队化学反应好",
            "面对 fastball 时极具威胁"
        ],
        "cons": [
            "三振率极高，「电风扇」绰号不虚",
            "上垒能力偏弱，OBP长期偏低",
            "2026年力量和数据全面下滑",
            "防守 range 随着年龄下降",
            "状态起伏大，容易出现长打荒",
            "33岁，未来体能和产出存疑"
        ],
        "grades": [
            {"label": "Contact", "value": 50, "grade": "B"},
            {"label": "Power", "value": 65, "grade": "A-"},
            {"label": "Discipline", "value": 45, "grade": "C+"},
            {"label": "Speed", "value": 45, "grade": "C+"},
            {"label": "Defense", "value": 50, "grade": "B"},
            {"label": "Arm", "value": 60, "grade": "A-"},
            {"label": "Clutch", "value": 55, "grade": "B"},
            {"label": "Leadership", "value": 55, "grade": "B"}
        ],
        "overall_grade": 55,
        "overall_label": "B 级 / 力量型外野",
        "overall_desc": "具备一击改变比赛的能力，但稳定性和上垒能力限制了他的上限",
        "future_outlook": """
            <div style="margin-top: 20px;">
                <p>Teoscar Hernández 的未来取决于他能否重振2025年的力量水准。33岁的他不再处于上升期，但如果能恢复健康并改善选球，仍可作为 platoon 左外野或 DH 贡献20轰左右的火力。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>改善选球：</strong>减少追打坏球，提升OBP至.320+</li>
                    <li><strong>恢复力量：</strong>通过打击训练找回 launch angle</li>
                    <li><strong>管理健康：</strong>减少外野守备负担，考虑更多DH</li>
                    <li><strong>定位 platoon：</strong>面对左投时发挥最大优势</li>
                </ol>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
                <p><strong>2026（下半季）：</strong>若健康，有望恢复至.250/.300/.450，全季约15轰</p>
                <p><strong>2027：</strong>可能转为 platoon/DH 角色，20轰左右</p>
                <p><strong>2028+：</strong>以 veteran bat off the bench 身份结束生涯</p>

                <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3>
                <ul style="margin-left: 20px; line-height: 2;">
                    <li>年龄和伤病导致产出持续下滑</li>
                    <li>高三振率容易被 elite 后援压制</li>
                    <li>防守价值下降可能使他失去首发位置</li>
                </ul>
            </div>
        """,
        "background": """
            <div style="margin-top: 20px;">
                <p>Teoscar Hernández 出生于多米尼加共和国，2011年以国际自由球员身份与休斯顿太空人签约。他在太空人农场体系中逐渐成长，2016年8月12日完成大联盟首秀。</p>
                <p>在休斯顿未能获得稳定位置后，Hernández 于2017年被交易到多伦多蓝鸟。在多伦多，他打出职业生涯最佳表现，连续在2020年和2021年获得美联银棒奖，2021年更轰出32支全垒打、116打点。</p>
                <p>随后他曾效力于西雅图水手，2025年加盟洛杉矶道奇。在道奇，他以强劲的臂力和不时改变比赛的 long ball 成为外野轮换的重要成员。中国球迷因他大幅挥棒和高三振率而称他为「电风扇」。</p>
                <p>场外，Hernández 性格开朗，是更衣室中的活跃分子。他热衷于回馈多米尼加社区，经常在家乡举办棒球训练营。</p>
            </div>
        """
    }
]


def build_info_grid(p):
    items = [
        ("出生日期", p["birth_date"]),
        ("年龄", p["age"] + "岁"),
        ("出生地", p["birthplace"]),
        ("身高/体重", p["height_weight"]),
        ("投球/击球", p["bats_throws"]),
        ("MLB首秀", p["debut"]),
        ("背号", "#" + p["number"]),
        ("绰号", p["nickname"]),
    ]
    return "\n".join(
        f'                        <div class="info-item"><div class="label">{label}</div><div class="value">{value}</div></div>'
        for label, value in items
    )


def build_stats_2026_grid(p):
    s = p["stats_2026"]
    order = [("G", "出赛"), ("AVG", "打击率"), ("OBP", "上垒率"), ("SLG", "长打率"),
             ("OPS", "OPS"), ("HR", "全垒打"), ("RBI", "打点"), ("SB", "盗垒")]
    html = ""
    for key, label in order:
        val = s[key]
        color = "#4fc3f7"
        if key == "AVG":
            try:
                if float(val.strip(".")) / 1000 < 0.250:
                    color = "#ff9800"
            except Exception:
                pass
        html += f'''
                <div class="stat-card">
                    <span class="stat-value" style="color: {color};">{val}</span>
                    <div class="stat-label">{label}</div>
                </div>'''
    return html


def build_season_table(p):
    s25 = p["stats_2025"]
    s26 = p["stats_2026"]
    rows = []
    for year, s in [("2025", s25), ("2026", s26)]:
        rows.append(
            f'''                    <tr>
                        <td class="{'warning' if year == '2026' else 'highlight'}">{year}</td>
                        <td>{s['G']}</td>
                        <td>{s['AVG']}</td>
                        <td>{s['OBP']}</td>
                        <td>{s['SLG']}</td>
                        <td>{s['OPS']}</td>
                        <td>{s['HR']}</td>
                        <td>{s['RBI']}</td>
                        <td>{s['BB']}</td>
                        <td>{s['SO']}</td>
                    </tr>'''
        )
    return "\n".join(rows)


def build_pros_cons(items):
    return "\n".join(f'                        <li>{item}</li>' for item in items)


def grade_class(value):
    if value >= 60:
        return "grade-a"
    elif value >= 50:
        return "grade-b"
    elif value >= 40:
        return "grade-c"
    else:
        return "grade-d"


def build_grades_grid(p):
    html = ""
    for g in p["grades"]:
        cls = grade_class(g["value"])
        html += f'''
                <div class="stat-card">
                    <span class="stat-value" style="color: {'#4caf50' if g['value'] >= 60 else '#4fc3f7' if g['value'] >= 50 else '#ff9800'};">{g['value']}</span>
                    <div class="stat-label">{g['label']}</div>
                    <span class="grade {cls}">{g['grade']}</span>
                </div>'''
    return html


def generate_cover(p, path):
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

    ax.text(0.5, 0.08, p['subtitle'].split('|')[-1].strip(), fontsize=14, ha='center',
            color='#90a4ae', transform=ax.transAxes, style='italic')
    ax.text(0.5, 0.02, f'Generated: {TODAY} | Data: MLB.com, MLB Stats API',
            fontsize=10, ha='center', color='#666', transform=ax.transAxes)

    plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()


def generate_season_chart(p, path):
    s25 = p['stats_2025']
    s26 = p['stats_2026']
    stats = ['AVG', 'OBP', 'SLG', 'OPS']
    vals_2025 = [float(s25[k]) for k in stats]
    vals_2026 = [float(s26[k]) for k in stats]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    colors = ['#4fc3f7', '#ff9800']
    x_labels = ['2025', '2026']

    for idx, stat in enumerate(stats):
        ax = axes[idx]
        vals = [vals_2025[idx], vals_2026[idx]]
        bars = ax.bar(x_labels, vals, color=colors, edgecolor='white', alpha=0.9, width=0.5)
        ax.set_title(f'{stat}', fontsize=14, fontweight='bold', color='#1a1a2e')
        ax.set_ylim(0, max(vals) * 1.25)
        ax.grid(axis='y', alpha=0.3)
        for bar, val in zip(bars, vals):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(vals)*0.02,
                    f'{val:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

    fig.suptitle(f"{p['name']} - 2025 vs 2026 Season Comparison", fontsize=16, fontweight='bold', color='#1a1a2e', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def generate_grades_chart(p, path):
    categories = ['Contact', 'Power', 'Discipline', 'Speed', 'Defense', 'Arm', 'Clutch', 'Leadership']
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
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def build_html(p):
    html = HTML_TEMPLATE
    html = html.replace('__TITLE__', f"{p['name']} 球探报告")
    html = html.replace('__PLAYER_NAME__', p['name'])
    html = html.replace('__SUBTITLE__', p['subtitle'])
    html = html.replace('__COVER_IMG__', f"{p['last_name']}_report_cover.png")
    html = html.replace('__INFO_GRID__', build_info_grid(p))
    html = html.replace('__SCOUTING_SUMMARY__', p['summary'])
    html = html.replace('__CAREER_HIGHLIGHTS__', p['career_highlights'])
    html = html.replace('__STATS_2026_GRID__', build_stats_2026_grid(p))
    html = html.replace('__SEASON_CHART__', f"{p['last_name']}_season_comparison.png")
    html = html.replace('__SEASON_TABLE__', build_season_table(p))
    html = html.replace('__ANALYSIS__', p['analysis'])
    html = html.replace('__PROS__', build_pros_cons(p['pros']))
    html = html.replace('__CONS__', build_pros_cons(p['cons']))
    html = html.replace('__GRADES_RADAR__', f"{p['last_name']}_overall_grades.png")
    html = html.replace('__GRADES_GRID__', build_grades_grid(p))
    html = html.replace('__OVERALL_GRADE__', str(p['overall_grade']))
    html = html.replace('__OVERALL_DESC__', p['overall_desc'])
    html = html.replace('__OVERALL_LABEL__', p['overall_label'])
    html = html.replace('__FUTURE_OUTLOOK__', p['future_outlook'])
    html = html.replace('__BACKGROUND__', p['background'])
    html = html.replace('__FOOTER_DATE__', TODAY)
    html = html.replace('__DATA_DATE__', DATA_DATE)
    return html


def build_md(p):
    s26 = p['stats_2026']
    lines = [
        f"# {p['name']} 球探报告",
        "",
        f"> **Los Angeles Dodgers #{p['number']} | {p['position']}**",
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
        f"- **击球/投球**：{p['bats_throws']}",
        f"- **出生日期**：{p['birth_date']}（{p['age']}岁）",
        f"- **MLB首秀**：{p['debut']}",
        "",
        "---",
        "",
        "## 📊 2026赛季数据",
        "",
        f"| G | AVG | OBP | SLG | OPS | HR | RBI | SB | BB | SO |",
        f"|---|---|---|---|---|---|---|---|---|---|",
        f"| {s26['G']} | {s26['AVG']} | {s26['OBP']} | {s26['SLG']} | {s26['OPS']} | {s26['HR']} | {s26['RBI']} | {s26['SB']} | {s26['BB']} | {s26['SO']} |",
        "",
        "---",
        "",
        "## 📝 备注",
        "",
        "此报告为详细版球探报告，包含图表和深度分析。",
        "",
        f"*数据来源：MLB Stats API | 生成时间：{TODAY}*",
    ]
    return "\n".join(lines)


def main():
    print("=" * 70)
    print("Generating detailed scouting reports for next 4 players")
    print("=" * 70)
    for p in PLAYERS:
        output_dir = os.path.join(BASE_DIR, p['slug'])
        os.makedirs(output_dir, exist_ok=True)
        print(f"\n[{p['name']}] -> {output_dir}")

        # Charts
        cover_path = os.path.join(output_dir, f"{p['last_name']}_report_cover.png")
        season_path = os.path.join(output_dir, f"{p['last_name']}_season_comparison.png")
        grades_path = os.path.join(output_dir, f"{p['last_name']}_overall_grades.png")

        generate_cover(p, cover_path)
        generate_season_chart(p, season_path)
        generate_grades_chart(p, grades_path)
        print(f"  Charts: cover, season, grades")

        # HTML
        html = build_html(p)
        html_path = os.path.join(output_dir, f"{p['slug']}-scouting-report.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  HTML: {html_path}")

        # Markdown
        md = build_md(p)
        md_path = os.path.join(output_dir, f"{p['slug']}-scouting-report.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"  MD:   {md_path}")

    print("\n" + "=" * 70)
    print("All 4 reports generated successfully!")
    print("=" * 70)


if __name__ == '__main__':
    main()
