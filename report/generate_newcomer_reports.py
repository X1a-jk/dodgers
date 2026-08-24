#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成三名新加盟道奇球员（Kris Bubic, Hunter Feduccia, Ben Rortvedt）的球探报告。
输出 Markdown + HTML + 图表，风格与 alex-vesia / tanner-scott 一致。
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
TODAY = datetime.now().strftime('%Y-%m-%d')

OUTPUT_BASE = r'D:\baseball\report'

PLAYERS = [
    {
        "name": "Kris Bubic",
        "slug": "kris-bubic",
        "number": "50",
        "position": "左投先发 (LHP)",
        "position_code": "P",
        "bats_throws": "左投 / 左打",
        "birth_date": "1997-08-19",
        "age": "28",
        "birthplace": "美国加州 Cupertino",
        "height_weight": "6'3\" / 220 lbs",
        "debut": "2020-07-31",
        "college": "Stanford University",
        "high_school": "Archbishop Mitty HS",
        "draft": "2018年 CB-A 轮 第40顺位 (Kansas City Royals)",
        "status": "IL-60（左肘酸痛，2026年8月3日交易至道奇）",
        "type": "pitcher",
        "summary": """
            <p style="margin-bottom: 15px;">Kris Bubic 是一名经历起伏的左投先发，2023年接受 Tommy John 手术后，2024年以牛棚角色强势回归，2025年更以 20 场先发、2.55 ERA 入选美联全明星。然而 2026 年季中左肘再次出问题，7月进入伤病名单，8月3日被交易至道奇时仍位于 IL-60。</p>
            <p style="margin-bottom: 15px;">Bubic 的招牌武器是<span class="success">变速球</span>，2025年靠着压制全垒打（HR/9 0.46）和稳定控球缴出精英级成绩。他的四缝线快速球均速仅 92-94 mph，不属 elite，但配上变速球与滑球仍能制造大量挥空。2026 年他在皇家 9 场先发 4.11 ERA，三振保送比明显下滑，显示伤病已影响表现。</p>
            <p>道奇交易他时赌的是 2025 年全明星版本的反弹。若左肘康复，他能成为轮值后端可靠的左投；若无法恢复，可能转型为长中继或左 specialized reliever。</p>
        """,
        "career_highlights": """
            <div class="career-highlight"><h4>🎓 2018年 - Stanford 大学 / Royals 第40顺位</h4><p>Kris Bubic 在 Stanford 大学大三时 8-1、2.62 ERA、101 K，Pac-12 冠军成员。2018 年选秀被 Royals 在 CB-A 轮第40顺位选中。</p></div>
            <div class="career-highlight"><h4>🌟 2020年 - 大联盟首秀</h4><p>2020年7月31日对 White Sox 先发初登板，成为 Royals 史上第8位在选秀后两季内登上大联盟的先发投手。</p></div>
            <div class="career-highlight"><h4>💪 2021年 - 完整轮值年</h4><p>20场先发、130局、6-7、4.43 ERA，20次双杀诱导并列联盟第3，写下 Royals 新人连续17.2局无失分纪录。</p></div>
            <div class="career-highlight"><h4>🏥 2023年 - Tommy John 手术</h4><p>4月先 adds slider，但仅 3 场先发后接受 Tommy John 手术，整季报销。术后447天于 2024 年7月重返大联盟。</p></div>
            <div class="career-highlight"><h4>⭐ 2025年 - 美联全明星</h4><p>20 场先发、8-7、2.55 ERA、116.1 IP、116 K，HR/9 仅 0.46 全联盟最低（至少20场先发），首次入选全明星赛。</p></div>
            <div class="career-highlight"><h4>🔵 2026年 - 交易至道奇</h4><p>2026年4月改穿 #50，季中因左肘酸痛进入 IL-60，8月3日被 Royals 交易至 Los Angeles Dodgers。道奇赌其康复后重回 2025 年全明星水准。</p></div>
        """,
        "stats_2026": {"G": 9, "GS": 9, "W": 3, "L": 2, "ERA": "4.11", "IP": "50.1", "K": 51, "BB": 26, "WHIP": "1.23", "K/9": "9.12", "BB/9": "4.65", "HR": 4},
        "stats_2025": {"G": 20, "GS": 20, "W": 8, "L": 7, "ERA": "2.55", "IP": "116.1", "K": 116, "BB": 39, "WHIP": "1.18", "K/9": "8.97", "BB/9": "3.02", "HR": 6},
        "stats_2024": {"G": 27, "GS": 0, "W": 1, "L": 1, "ERA": "2.67", "IP": "30.1", "K": 39, "BB": 5, "WHIP": "1.02", "K/9": "11.57", "BB/9": "1.48", "HR": 2, "SV": 1, "HLD": 7},
        "season_chart_years": ["2024", "2025", "2026"],
        "season_chart_stats": ["ERA", "WHIP", "K/9", "BB/9"],
        "season_chart_data": [[2.67, 2.55, 4.11], [1.02, 1.18, 1.23], [11.57, 8.97, 9.12], [1.48, 3.02, 4.65]],
        "cover_stats": [("ERA", "4.11"), ("W-L", "3-2"), ("K", "51"), ("IP", "50.1"), ("WHIP", "1.23"), ("K/9", "9.12"), ("Age", "28"), ("All-Star", "2025")],
        "pitch_arsenal": [
            {"name": "四缝线快速球 (Four-Seam Fastball)", "velocity": "92-94 mph", "desc": "Bubic 的快速球均速约 93 mph，在先发左投中不算 elite。球路进垒点偏高时容易被硬打，但搭配变速球形成速差仍是主要抢 strike 武器。"},
            {"name": "变速球 (Changeup)", "velocity": "84-87 mph", "desc": "Bubic 的招牌球种。出手动作与快速球相似，约 8-9 mph 速差加上下沉位移，能有效让左右打者击出滚地球或挥空。2025 年 HR/9 0.46 的关键功臣。"},
            {"name": "滑球 (Slider)", "velocity": "82-85 mph", "desc": "2023年开刀前加入的球种。横移明显，主要用来对付右打者，两好球后的出局球。术后复出后使用频率增加，成为搭配变速球的重要武器。"},
            {"name": "曲球 (Curveball)", "velocity": "78-81 mph", "desc": "第四球种，用来打乱节奏和制造不同下坠角度。使用频率较低，品质尚可但非主要出局武器。"}
        ],
        "analysis": """
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">投球机制与球风</h3>
                <p>Bubic 采用高四分之三出手点，动作流畅且重复性不错。身为左投，他的跨步角度与身体侧对打者，让快速球从较侧角度进入好球带。术后复健团队重点维持他的手臂路径与 follow-through，避免给肘部韧带带来额外压力。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">近三年趋势（2024-2026）</h3>
                <p>2024 年从 TJ 术后回归，先在小联盟复健，7月升上大联盟后完全以牛棚身份出赛，缴出 2.67 ERA、1.02 WHIP、39 K / 5 BB 的绝佳成绩。2025 年转型回先发，116.1 局、2.55 ERA，并入选全明星，HR/9 0.46 为大联盟先发最低。2026 年 9 场先发 4.11 ERA，三振保送比从 2025 年的 3.0:1 恶化到约 2.0:1，BB/9 从 3.02 上升到 4.65，显示左肘酸痛已影响控球与 command。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">2026年数据解读</h3>
                <p>2026 年 4.11 ERA 看似平庸，但前 4 场先发其实仍有亮点。5月中后 BB/9 急剧攀升，WHIP 也达到 1.23，最终因左肘不适进入 IL。50.1 局样本下，他仍能维持 9.12 K/9，说明三振能力未完全消失，但控球与续航明显受肘部影响。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">全垒打控制与伤病关联</h3>
                <p>2025 年最亮眼的是全垒打控制：仅 6 轰、HR/9 0.46。2026 年 50.1 局已掉 4 轰，HR/9 回升到 0.71。这通常与控球失准有关——当快速球与变速球无法精准进垒时，打者更容易等到甜球。左肘问题可能让他不敢全力使用变速球，进一步削弱压制力。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">在道奇的角色定位</h3>
                <p>Bubic 被交易至道奇时仍位于 IL-60，因此不可能立即先发。复健完成后，道奇可能先让他从长中继或 piggyback 角色开始，逐步增加局数。若恢复 2025 年水准，他能成为轮值后端左投；若肘部持续困扰，可能转为 bullpen lefty specialist 或 long reliever。</p>
            </div>
        """,
        "pros": [
            "2025年全明星表现：20 先发 2.55 ERA，证明具备轮值中端实力",
            "招牌变速球品质出色，HR/9 控制能力在健康时 elite",
            "左投身份在轮值中具战略价值，尤其面对左打者",
            "术后复健成功，2024 牛棚 2.67 ERA / 1.02 WHIP",
            "能胜任先发与牛棚两种角色，弹性高",
            "三振能力健康时可达 9 K/9 左右",
            "道奇医疗与投手发展体系有利于伤病管理"
        ],
        "cons": [
            "2026 年左肘酸痛进入 IL-60，伤病风险高",
            "2026 年 BB/9 从 3.02 暴增至 4.65，控球明显恶化",
            "四缝线快速球均速仅 92-94 mph，不具 elite velocity",
            "过度依赖变速球，快速球偏高时容易被长打",
            "Tommy John 术后才两年，肘部再次出问题令人担忧",
            "交易时无法立即贡献，复健时间不确定",
            "2022 年曾有 5.58 ERA 的糟糕赛季，稳定性待验证"
        ],
        "grades": [
            {"label": "Fastball", "value": 50, "grade": "B-"},
            {"label": "Changeup", "value": 65, "grade": "A-"},
            {"label": "Slider", "value": 55, "grade": "B+"},
            {"label": "Curveball", "value": 45, "grade": "C+"},
            {"label": "Control", "value": 50, "grade": "B-"},
            {"label": "Command", "value": 55, "grade": "B+"},
            {"label": "Stamina", "value": 50, "grade": "B-"},
            {"label": "Mental", "value": 55, "grade": "B+"}
        ],
        "overall_grade": 55,
        "overall_label": "B 级 / 有伤病风险的左投轮值深度",
        "overall_desc": "Kris Bubic 的天赋上限是 2025 年全明星版的中段左投先发，但左肘伤病让当前估值大幅下修。若能在道奇医疗体系下康复，他有望在 2027 年提供轮值后段或长中继价值；反之，可能沦为伤病名单常客。",
        "future_outlook": """
            <div style="margin-top: 20px;">
                <p>Bubic 的未来几乎完全取决于左肘康复程度。他才 28 岁，技术底子与变速球品质仍在，但 2026 年的肘部复发让球团必须谨慎。</p>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>完整复健：</strong>不要急于在 2026 年回归，确保肘部完全恢复。</li>
                    <li><strong>从牛棚/长中继起步：</strong>减少单季局数压力，逐步重建投球量。</li>
                    <li><strong>强化控球：</strong>重点降低 BB/9，恢复 2025 年 3.0 左右的水准。</li>
                    <li><strong>增加 Sinker 或 Cutter：</strong>用更多地面球武器减少长打风险。</li>
                </ol>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期轨迹</h3>
                <p><strong>2026 下半季：</strong>复健为主，可能 9 月后以牛棚身份短暂回归。</p>
                <p><strong>2027：</strong>若健康，目标 20-25 场先发或 50-60 局长中继，ERA 3.50-4.20。</p>
                <p><strong>2028+：</strong>若能维持变速球品质，仍可作为左投轮值后端；否则转为 specialized reliever。</p>
                <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险</h3>
                <ul style="margin-left: 20px; line-height: 2;">
                    <li>左肘再次手术将严重打击生涯</li>
                    <li>快速球 velocity 若再下滑，先发角色难以维持</li>
                    <li>控球问题若持续，将失去轮值价值</li>
                </ul>
            </div>
        """,
        "background": """
            <div style="margin-top: 20px;">
                <p>Kristofer Bubic 出生于加州 Cupertino，毕业于 Archbishop Mitty High School。2015 年高中毕业后进入 Stanford University，2018 年大三赛季以 8-1、2.62 ERA、101 次三振的优异成绩帮助 Stanford 夺得 Pac-12 冠军，并获 Golden Spikes Award 季中观察名单提名。</p>
                <p>2018 年选秀，Royals 在竞争平衡 A 轮第40顺位选中他。2020 年7月31日，Bubic 对 White Sox 完成大联盟首秀，成为 Royals 史上自 2012 年 Will Smith 以来最年轻以先发身份登板的左投。</p>
                <p>2021 年他完整先发 20 场，但 2022 年陷入低潮（5.58 ERA），2023 年仅 3 场先发后因 Tommy John 手术报销。经过 2024 年的牛棚复健与 2025 年的全明星反弹，Bubic 一度被视为 Royals 轮值复兴希望。但 2026 年左肘问题再起，最终在 8 月3 日被交易至道奇，背号改穿 #50。</p>
            </div>
        """
    },
    {
        "name": "Hunter Feduccia",
        "slug": "hunter-feduccia",
        "number": "46",
        "position": "捕手 (Catcher)",
        "position_code": "C",
        "bats_throws": "左打 / 右投",
        "birth_date": "1997-06-05",
        "age": "29",
        "birthplace": "美国路易斯安那州 Lake Charles",
        "height_weight": "6'1\" / 215 lbs",
        "debut": "2024-07-31",
        "college": "Louisiana State University (LSU)",
        "high_school": "Barbe (La.) High School",
        "draft": "2018年 第12轮 第374顺位 (Los Angeles Dodgers)",
        "status": "活跃（2026年8月3日从光芒回到道奇）",
        "type": "hitter",
        "summary": """
            <p style="margin-bottom: 15px;">Hunter Feduccia 是道奇自家农场出身的替补捕手，2024 年完成大联盟首秀，2025 年季中被交易至光芒，2026 年8月3日又被交易回道奇。他是一名以<span class="warning">选球与守备</span>见长的左打捕手，但大联盟打击样本有限，且面对左投表现极差。</p>
            <p style="margin-bottom: 15px;">2026 年在光芒 60 场出赛缴出 .234/.306/.340、2 轰、12 打点，相比 2025 年的 .151 有显著进步。他在 Triple-A 曾展现 .280+/.400+ 的上垒能力，但尚未稳定转化到大联盟。道奇重新拿回他，主要是为补强捕手深度并提供便宜的左打替补选择。</p>
            <p>29 岁的 Feduccia 已接近定型：天花板是稳定的 backup catcher，关键价值在于 framing、阻挡与偶尔对右投的贡献。</p>
        """,
        "career_highlights": """
            <div class="career-highlight"><h4>🎓 2018年 - LSU / Dodgers 第12轮</h4><p>出身 Barbe 高中，在 LSU-Eunice 两年打下 .390 生涯平均后转 LSU。2018 年道奇第12轮（374顺位）选中他。</p></div>
            <div class="career-highlight"><h4>🌟 2024年 - 大联盟首秀</h4><p>2024年7月31日对教士以代打身份完成大联盟首秀。该年道奇 5 场出赛、4 安打、1 打点。</p></div>
            <div class="career-highlight"><h4>🔁 2025年 - 交易至光芒</h4><p>7月31日被道奇交易至光芒，换来 Paul Gervase、Adam Serwinowski 与 Ben Rortvedt。在光芒 36 场出赛，打击率 .151。</p></div>
            <div class="career-highlight"><h4>🔵 2026年 - 重返道奇</h4><p>8月3日光芒将他与 RHP Jacob Kmatz 交易回道奇，换来外野手 Jack Suwinski。背号 #46。</p></div>
        """,
        "stats_2026": {"G": 60, "AB": 141, "PA": 160, "R": 15, "H": 33, "2B": 7, "3B": 1, "HR": 2, "RBI": 12, "BB": 14, "SO": 44, "AVG": ".234", "OBP": ".306", "SLG": ".340", "OPS": ".646", "SB": 0},
        "stats_2025": {"G": 36, "AB": 86, "PA": 102, "R": 5, "H": 13, "2B": 5, "3B": 0, "HR": 0, "RBI": 8, "BB": 14, "SO": 28, "AVG": ".151", "OBP": ".265", "SLG": ".209", "OPS": ".474", "SB": 1},
        "stats_2024": {"G": 5, "AB": 12, "PA": 14, "R": 2, "H": 4, "2B": 0, "3B": 0, "HR": 0, "RBI": 1, "BB": 2, "SO": 2, "AVG": ".333", "OBP": ".429", "SLG": ".333", "OPS": ".762", "SB": 0},
        "season_chart_years": ["2024", "2025", "2026"],
        "season_chart_stats": ["AVG", "OBP", "SLG", "OPS"],
        "season_chart_data": [[0.333, 0.151, 0.234], [0.429, 0.265, 0.306], [0.333, 0.209, 0.340], [0.762, 0.474, 0.646]],
        "cover_stats": [("AVG", ".234"), ("OBP", ".306"), ("SLG", ".340"), ("OPS", ".646"), ("HR", "2"), ("RBI", "12"), ("G", "60"), ("Age", "29")],
        "analysis": """
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">打击机制与选球</h3>
                <p>Feduccia 采用左打者常见的紧凑姿势，挥棒路径较为水平，擅长把球打向反方向。他的主要价值在于选球：2025 年在光芒 102 打席 14 保送，BB/PA 约 13.7%，在至少 100 PA 的捕手中名列前茅。问题是三振率也高达 27.5%，显示他在两好球后常追打坏球。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">近三年趋势（2024-2026）</h3>
                <p>2024 年道奇 5 场小样本 .333/.429；2025 年光芒 36 场 .151/.265 严重低潮；2026 年 60 场回升到 .234/.306/.340。虽然 OPS 仅 .646，但对一名 backup catcher 已属可接受范围。关键在于他能否维持在 .240/.320/.350 左右的水准。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">对左右投表现</h3>
                <p>2025 年数据清楚显示他对左投几乎无法打击：对右投 .321 OBP 还有基本贡献，对左投 OBP 仅 .048。这限制他只能作为 platoon 后半的右投 specialist。道奇若要使用他，必须严格避免左投 matchup。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">守备与配球</h3>
                <p>光芒时期 28 场先发捕手没有失误与漏接，显示接捕基本功稳定。Triple-A 时期 framing 与阻挡能力获得好评，虽然大联盟 framing 数据样本不足。他的配球经验主要来自道奇农场，对道奇投手群相对熟悉，这是交易回他的隐性价值。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">在道奇的角色定位</h3>
                <p>Feduccia 回到道奇后预计担任第三捕手或 Will Smith 的替补。他可能在 Smith 需要休息、面对右投先发时获得首发机会。除非 Smith 长期伤病，否则他的上场时间有限。</p>
            </div>
        """,
        "pros": [
            "选球能力出色，BB/PA 在捕手中名列前茅",
            "2026 年打击大幅回升，从 .151 提升到 .234",
            "对右投有基本贡献，能上垒并制造长打机会",
            "道奇农场出身，对投手群熟悉",
            "守备基本功稳定，2025 年 28 场先发无失误无漏接",
            "Triple-A 长期表现优于大联盟，仍有上调空间",
            "左打身份在替补捕手市场有价值"
        ],
        "cons": [
            "对左投打击能力极差，2025 年对左投 OBP 仅 .048",
            "大联盟样本仍小，2026 年 OPS 仅 .646",
            "三振率偏高，2025 年达 27.5%",
            "力量有限，大联盟 2 年仅 2 轰",
            "已 29 岁，接近定型，天花板有限",
            "盗垒阻杀与 framing 大联盟数据不足",
            "多次上下大联盟，稳定性待验证"
        ],
        "grades": [
            {"label": "Hitting", "value": 40, "grade": "C+"},
            {"label": "Power", "value": 40, "grade": "C+"},
            {"label": "Plate Discipline", "value": 50, "grade": "B-"},
            {"label": "Arm", "value": 50, "grade": "B-"},
            {"label": "Defense", "value": 50, "grade": "B-"},
            {"label": "Framing", "value": 50, "grade": "B-"},
            {"label": "Blocking", "value": 50, "grade": "B-"},
            {"label": "Game Calling", "value": 45, "grade": "C+"},
            {"label": "Running", "value": 35, "grade": "C"}
        ],
        "overall_grade": 45,
        "overall_label": "C+ 级 / 替补捕手深度",
        "overall_desc": "Hunter Feduccia 是一名合格的 backup catcher，主要价值在于选球与守备稳定性。他能在面对右投时提供有限进攻贡献，但无法对抗左投。29 岁的年龄让他的天花板受限，未来定位是道奇第三捕手或交易筹码。",
        "future_outlook": """
            <div style="margin-top: 20px;">
                <p>Feduccia 回到道奇后，短期定位明确：Will Smith 的替补或第三捕手。他不需要承担大量先发，但必须在有限机会中证明能维持 2026 年 .234/.306/.340 的水准。</p>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>强化对左投：</strong>至少达到能担任代打而不自动出局的水准。</li>
                    <li><strong>保持选球：</strong>继续发挥 BB/PA 优势，弥补打击率不足。</li>
                    <li><strong>降低三振：</strong>两好球后的追打率需要改善。</li>
                    <li><strong>巩固守备数据：</strong>在大联盟累积 framing 与阻杀样本，证明能稳定蹲捕。</li>
                </ol>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期轨迹</h3>
                <p><strong>2026 下半季：</strong>道奇第三捕手，预计 20-30 场出赛，主要面对右投先发。</p>
                <p><strong>2027：</strong>若 Smith 健康，仍 backup；若 Smith 离队或受伤，可能升任主要替补。</p>
                <p><strong>2028+：</strong>天花板为稳定 backup catcher，OPS 约 .650-.700。</p>
            </div>
        """,
        "background": """
            <div style="margin-top: 20px;">
                <p>Hunter Feduccia 出生于路易斯安那州 Lake Charles，在 Barbe High School 度过高中时期。该校是路易斯安那州棒球名校，培养出 Wade LeBlanc 等 MLB 球员。Feduccia 在高中时直到高三才成为常规先发，该年打出 .353 并获得 all-district 荣誉。</p>
                <p>大学时期他先就读 LSU-Eunice 两年，创下 .390 生涯打击率并保持校史纪录；随后转入 Louisiana State University (LSU)。2018 年道奇在第12轮（374顺位）选中他。</p>
                <p>他在道奇农场体系缓慢爬升，2023 年在 Triple-A Oklahoma City 打出 .279/.387/.451、11 轰、57 打点的成绩。2024 年完成大联盟首秀，2025 年被交易至光芒，2026 年8月3日又被光芒送回道奇，换来 Jack Suwinski。</p>
            </div>
        """
    },
    {
        "name": "Ben Rortvedt",
        "slug": "ben-rortvedt",
        "number": "47",
        "position": "捕手 (Catcher)",
        "position_code": "C",
        "bats_throws": "左打 / 右投",
        "birth_date": "1997-09-25",
        "age": "28",
        "birthplace": "美国威斯康星州 Madison",
        "height_weight": "5'10\" / 210 lbs",
        "debut": "2021-04-30",
        "high_school": "Verona Area High School, WI",
        "draft": "2016年 第2轮 第56顺位 (Minnesota Twins)",
        "status": "活跃（2026年8月3日从大都会交易至道奇）",
        "type": "hitter",
        "summary": """
            <p style="margin-bottom: 15px;">Ben Rortvedt 是一名以<span class="success">防守与接捕技巧</span>著称的左打捕手， offense 是其明显短板。2024 年在光芒担任主战捕手 112 场，打击率 .228/.317/.303，并被 Statcast 评为 framing 第17名。2025-2026 年因多重伤病与交易辗转多队，2026 年8月3日才从大都会被交易回道奇。</p>
            <p style="margin-bottom: 15px;">Rortvedt 的生涯大联盟打击率仅 .189，OPS .547，几乎没有任何进攻威胁。但他的接球能力、配球经验与季后赛经历（2025 年世界大赛冠军成员）让他成为道奇想要的便宜守备型替补。</p>
            <p>在道奇阵中，Rortvedt 的定位是第三捕手或 Smith 受伤时的紧急备胎。他不需要上场打击，只需要稳定蹲捕、阻止盗垒、做好 framing。</p>
        """,
        "career_highlights": """
            <div class="career-highlight"><h4>🎓 2016年 - Twins 第2轮</h4><p>来自威斯康星州 Verona Area High School，2016 年选秀第2轮（56顺位）被 Minnesota Twins 选中，被视为防守优先的捕手新秀。</p></div>
            <div class="career-highlight"><h4>🌟 2021年 - 大联盟首秀</h4><p>2021年4月30日对 Royals 完成大联盟首秀，首打席就获得保送，并在八局敲出生涯首安与首打点。该年 39 场，打击率 .169。</p></div>
            <div class="career-highlight"><h4>🏥 2022-2023年 - 伤病与手术</h4><p>2022 年因右腹斜肌与左膝半月板手术整季报销；2023 年在洋基因左肩动脉瘤手术缺席前半季，5月才回归。</p></div>
            <div class="career-highlight"><h4>🔒 2024年 - 光芒主战捕手</h4><p>112 场出赛（87 场先发），.228/.317/.303，3 轰，31 打点。Statcast framing 排名大联盟第17，确立防守型主战捕手地位。</p></div>
            <div class="career-highlight"><h4>🏆 2025年 - 世界大赛冠军</h4><p>虽然仅出赛 44 场、打击率 .152，但随洛杉矶道奇（2025 年季中从光芒转至道奇）获得世界大赛冠军戒指。</p></div>
            <div class="career-highlight"><h4>🔵 2026年 - 回到道奇</h4><p>2026 年经历红袜、道奇、大都会、小联盟的辗转，8月3日被大都会交易回道奇，换来 RHP Chayce McDermott。背号 #47。</p></div>
        """,
        "stats_2026": {"G": 2, "AB": 2, "PA": 2, "R": 0, "H": 0, "2B": 0, "3B": 0, "HR": 0, "RBI": 0, "BB": 0, "SO": 0, "AVG": ".000", "OBP": ".000", "SLG": ".000", "OPS": ".000", "SB": 0},
        "stats_2025": {"G": 44, "AB": 112, "PA": 125, "R": 10, "H": 17, "2B": 3, "3B": 0, "HR": 1, "RBI": 10, "BB": 11, "SO": 34, "AVG": ".152", "OBP": ".236", "SLG": ".205", "OPS": ".441", "SB": 0},
        "stats_2024": {"G": 112, "AB": 290, "PA": 328, "R": 27, "H": 66, "2B": 13, "3B": 0, "HR": 3, "RBI": 31, "BB": 34, "SO": 88, "AVG": ".228", "OBP": ".317", "SLG": ".303", "OPS": ".620", "SB": 1},
        "season_chart_years": ["2024", "2025", "2026"],
        "season_chart_stats": ["AVG", "OBP", "SLG", "OPS"],
        "season_chart_data": [[0.228, 0.152, 0.000], [0.317, 0.236, 0.000], [0.303, 0.205, 0.000], [0.620, 0.441, 0.000]],
        "cover_stats": [("AVG", ".189"), ("OBP", ".278"), ("SLG", ".269"), ("OPS", ".547"), ("HR", "9"), ("RBI", "52"), ("G", "229"), ("Age", "28")],
        "analysis": """
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">打击机制与进攻能力</h3>
                <p>Rortvedt 的打击机制偏向 contact-oriented，但挥棒速度不快，难以产生 barrel 与长打。他生涯大联盟 OPS 仅 .547，AVG .189，几乎每三位打者就有一位无法上垒。他的选球不算差（生涯 BB/PA 约 9%），但三振率偏高，且打出去的球多为软弱滚地球或飞球。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">近三年趋势（2024-2026）</h3>
                <p>2024 年是 Rortvedt 生涯最佳进攻年：112 场、.228/.317/.303、OPS .620。虽然仍低于联盟平均，但对防守型捕手已算可接受。2025 年他被下放并交易，44 场仅 .152/.236/.205。2026 年因伤病与球队转换，仅 2 打席无安打。整体趋势是下滑，而非上升。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">防守与接捕技巧</h3>
                <p>Rortvedt 的核心价值在防守。2024 年 Statcast framing 排名大联盟第17，显示他能稳定帮投手争取好球判决。他的 pop time 与阻杀能力也在平均以上。配球方面，他在 2023 年与 Gerrit Cole 合作时 catcher ERA 仅 2.25，证明他能与王牌投手配合。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">伤病与耐用性</h3>
                <p>Rortvedt 的伤病史令人担忧：2022 年右腹斜肌 + 左膝半月板手术整季报销；2023 年左肩动脉瘤手术。这些都不是小伤。虽然他 2024 年能出战 112 场，但 2025-2026 年再次频繁进出伤病名单，显示身体耐用性有限。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">在道奇的角色定位</h3>
                <p>Rortvedt 回到道奇后是明确的第三捕手/防守备胎。他可能在 Smith 轮休或面对强力左投先发时蹲捕，但进攻端不应期待任何贡献。他的价值完全建立在 framing、阻杀与配球经验上。</p>
            </div>
        """,
        "pros": [
            "2024 年 Statcast framing 排名大联盟第17，接球技巧 elite",
            "阻杀与 pop time 在平均以上",
            "能与王牌投手配合（2023年与Cole合作 catcher ERA 2.25）",
            "2025 年世界大赛冠军成员，季后赛经验宝贵",
            "防守型捕手，能在 Smith 休息时维持投手群稳定",
            "左打身份，在 backup catcher 市场有价值",
            " Triple-A 打击表现优于大联盟（.286/.395/.505 in 2023）"
        ],
        "cons": [
            "生涯大联盟打击率仅 .189，OPS .547，进攻端近乎黑洞",
            "力量严重不足，生涯 229 场仅 9 轰",
            "伤病史严重：2022年膝/腹斜肌、2023年动脉瘤手术",
            "2025-2026 年打击持续下滑，2026年仅 2 打席",
            "对左投打击能力有限，容易被专门对付",
            "29 岁将届，进攻天花板几乎为零",
            "2024 年后半段 .130 打击率，显示后期疲劳明显"
        ],
        "grades": [
            {"label": "Hitting", "value": 30, "grade": "D"},
            {"label": "Power", "value": 30, "grade": "D"},
            {"label": "Plate Discipline", "value": 40, "grade": "C+"},
            {"label": "Arm", "value": 55, "grade": "B+"},
            {"label": "Defense", "value": 55, "grade": "B+"},
            {"label": "Framing", "value": 60, "grade": "B+"},
            {"label": "Blocking", "value": 50, "grade": "B-"},
            {"label": "Game Calling", "value": 55, "grade": "B+"},
            {"label": "Running", "value": 35, "grade": "C"}
        ],
        "overall_grade": 45,
        "overall_label": "C+ 级 / 防守型替补捕手",
        "overall_desc": "Ben Rortvedt 的进攻几乎无法为球队贡献，但他的 framing、防守与配球经验让他成为一名合格的防守型 backup catcher。道奇拿回他主要是为捕手深度与季后赛经验，不应期待任何 offense。",
        "future_outlook": """
            <div style="margin-top: 20px;">
                <p>Rortvedt 回到道奇后的定位非常清晰：第三捕手或紧急情况下的防守备胎。他的生涯已进入防守 specialist 阶段，28-29 岁的年龄让进攻改善几乎不可能。</p>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>保持防守 elite：</strong>继续发挥 framing 优势，争取更多好球判决。</li>
                    <li><strong>健康管理：</strong>避免再次进入伤病名单，证明自己能稳定蹲捕。</li>
                    <li><strong>减少追打：</strong>至少把三振率控制在 25% 以下，避免完全无效。</li>
                    <li><strong> mentoring 年轻捕手：</strong>把经验传给 Dalton Rushing 等新秀。</li>
                </ol>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期轨迹</h3>
                <p><strong>2026 下半季：</strong>道奇第三捕手，预计 10-20 场出赛，主要防守用途。</p>
                <p><strong>2027：</strong>若健康，仍 backup；若 Smith 受伤，可能短暂承担更多蹲捕。</p>
                <p><strong>2028+：</strong>随着年龄增长， offense 更难进步，可能逐渐退出大联盟或转为教练/小联盟 mentor。</p>
            </div>
        """,
        "background": """
            <div style="margin-top: 20px;">
                <p>Benjamin Thomas Rortvedt 出生于威斯康星州 Madison，在 Verona Area High School 就读。高中时期他多才多艺，除了棒球还担任美式足球跑锋、线卫、踢球手与弃踢手。2016 年选秀，Minnesota Twins 在第2轮（56顺位）选中这位防守型捕手。</p>
                <p>2021 年4月30日 Rortvedt 完成大联盟首秀，并在生涯前几场就击出首轰与首打点。然而他的进攻始终未能发展，2022 年因右腹斜肌与左膝半月板手术整季报销。2023 年他被交易至 Yankees，但赛季初因左肩动脉瘤手术缺席大半季。</p>
                <p>2024 年他在 Tampa Bay Rays 迎来生涯最高光的一年，112 场出赛并展现 elite framing。2025 年季中他被交易至 Dodgers 并随队夺得世界大赛冠军。2026 年他经历 Reds、Mets 的辗转，最终在 8 月3 日再次被交易回 Dodgers，换来 Chayce McDermott。</p>
            </div>
        """
    }
]

# CSS/HTML 模板与工具函数（ pitcher / hitter 共用部分）
HTML_CSS = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: #e0e0e0; line-height: 1.6; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; padding: 40px 0; background: linear-gradient(90deg, #005A9C 0%, #1a5490 50%, #005A9C 100%); border-radius: 15px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .header h1 { font-size: 3em; color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); margin-bottom: 10px; }
        .header .subtitle { font-size: 1.2em; color: #e0e0e0; font-style: italic; }
        .player-card { background: rgba(255,255,255,0.1); border-radius: 15px; padding: 30px; margin-bottom: 30px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); display: flex; gap: 30px; flex-wrap: wrap; }
        .player-info { flex: 1; min-width: 250px; }
        .player-info h2 { color: #4fc3f7; margin-bottom: 15px; font-size: 1.8em; }
        .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .info-item { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; }
        .info-item .label { font-size: 0.9em; color: #90a4ae; text-transform: uppercase; letter-spacing: 1px; }
        .info-item .value { font-size: 1.2em; color: #fff; font-weight: bold; }
        .section { background: rgba(255,255,255,0.05); border-radius: 15px; padding: 30px; margin-bottom: 30px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }
        .section h2 { color: #4fc3f7; margin-bottom: 20px; font-size: 1.8em; border-bottom: 2px solid #4fc3f7; padding-bottom: 10px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px; }
        .stat-card { background: linear-gradient(135deg, rgba(0,90,156,0.3) 0%, rgba(26,84,144,0.3) 100%); border-radius: 10px; padding: 20px; text-align: center; border: 1px solid rgba(79,195,247,0.3); transition: transform 0.3s ease; }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-card .stat-value { font-size: 2.5em; font-weight: bold; color: #4fc3f7; display: block; }
        .stat-card .stat-label { font-size: 0.9em; color: #90a4ae; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; }
        .comparison-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .comparison-table th, .comparison-table td { padding: 12px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .comparison-table th { background: rgba(0,90,156,0.3); color: #4fc3f7; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
        .comparison-table tr:hover { background: rgba(255,255,255,0.05); }
        .pitch-arsenal { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
        .pitch-card { background: linear-gradient(135deg, rgba(0,90,156,0.2) 0%, rgba(26,84,144,0.2) 100%); border-radius: 10px; padding: 20px; border-left: 4px solid #4fc3f7; }
        .pitch-card h3 { color: #4fc3f7; margin-bottom: 10px; }
        .pitch-card .velocity { font-size: 1.5em; color: #fff; font-weight: bold; }
        .pros-cons { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
        .pros, .cons { background: rgba(255,255,255,0.05); border-radius: 10px; padding: 20px; }
        .pros h3 { color: #4caf50; margin-bottom: 15px; }
        .cons h3 { color: #f44336; margin-bottom: 15px; }
        .pros ul, .cons ul { list-style: none; }
        .pros li, .cons li { padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .pros li::before { content: "✓ "; color: #4caf50; font-weight: bold; }
        .cons li::before { content: "✗ "; color: #f44336; font-weight: bold; }
        .grade { display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9em; }
        .grade-a { background: rgba(76,175,80,0.3); color: #4caf50; }
        .grade-b { background: rgba(79,195,247,0.3); color: #4fc3f7; }
        .grade-c { background: rgba(255,152,0,0.3); color: #ff9800; }
        .grade-d { background: rgba(244,67,54,0.3); color: #f44336; }
        .highlight { color: #4fc3f7; font-weight: bold; }
        .warning { color: #ff9800; font-weight: bold; }
        .success { color: #4caf50; font-weight: bold; }
        .danger { color: #f44336; font-weight: bold; }
        .career-highlight { background: rgba(255,215,0,0.1); border: 1px solid rgba(255,215,0,0.3); border-radius: 10px; padding: 15px; margin: 15px 0; }
        .career-highlight h4 { color: #FFD700; margin-bottom: 10px; }
        .footer { text-align: center; padding: 20px; color: #90a4ae; font-size: 0.9em; }
        .section table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 0.95em; }
        .section th, .section td { padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .section th { background: rgba(0,90,156,0.3); color: #4fc3f7; font-weight: bold; }
        .section tr:hover { background: rgba(255,255,255,0.05); }
        .section h3 { color: #4fc3f7; margin: 20px 0 12px 0; font-size: 1.2em; }
        .section p { margin-bottom: 12px; }
        .section strong { color: #4fc3f7; }
        .section ul { margin-left: 25px; margin-bottom: 15px; }
        .section li { margin-bottom: 8px; }
        @media (max-width: 768px) { .header h1 { font-size: 2em; } .stats-grid { grid-template-columns: repeat(2, 1fr); } }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__TITLE__</title>
    <style>__CSS__</style>
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
                <p style="margin-top: 15px;"><span class="grade __OVERALL_CLASS__" style="font-size: 1.2em;">__OVERALL_LABEL__</span></p>
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


def grade_class(value):
    if value >= 60: return 'grade-a'
    if value >= 50: return 'grade-b'
    if value >= 40: return 'grade-c'
    return 'grade-d'


def generate_cover(p, output_path):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    ax.text(0.5, 0.85, p['name'], fontsize=32, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.75, f"Los Angeles Dodgers #{p['number']} | {p['position']}", fontsize=18, ha='center', color='#4fc3f7', transform=ax.transAxes)
    ax.text(0.5, 0.65, 'SCOUTING REPORT 2026', fontsize=22, fontweight='bold', ha='center', color='#ff9800', transform=ax.transAxes)
    y_pos = 0.45
    for i, (label, value) in enumerate(p['cover_stats']):
        x_pos = 0.15 + (i % 4) * 0.23
        if i >= 4: y_pos = 0.25
        ax.text(x_pos, y_pos, value, fontsize=26, fontweight='bold', ha='center', color='#4fc3f7', transform=ax.transAxes)
        ax.text(x_pos, y_pos - 0.08, label, fontsize=12, ha='center', color='#90a4ae', transform=ax.transAxes)
    subtitle = f"{p['status']} | {p.get('college', p.get('high_school', ''))} | MLB Debut {p['debut']}"
    ax.text(0.5, 0.08, subtitle, fontsize=14, ha='center', color='#90a4ae', transform=ax.transAxes, style='italic')
    ax.text(0.5, 0.02, f'Generated: {TODAY} | Data: MLB.com, MLB Stats API', fontsize=10, ha='center', color='#666', transform=ax.transAxes)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()


def generate_season_chart(p, output_path):
    stats = p['season_chart_stats']
    data = p['season_chart_data']
    years = p['season_chart_years']
    colors = ['#4fc3f7', '#4caf50', '#ff9800', '#f44336']
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    for idx, stat in enumerate(stats):
        ax = axes[idx]
        vals = data[idx]
        x = np.arange(len(years))
        bars = ax.bar(x, vals, color=colors, edgecolor='white', alpha=0.9, width=0.5)
        ax.set_title(stat, fontsize=14, fontweight='bold', color='#1a1a2e')
        max_val = max(vals) * 1.25 if max(vals) != 0 else 1
        ax.set_ylim(0, max_val)
        ax.set_xticks(x)
        ax.set_xticklabels(years)
        ax.grid(axis='y', alpha=0.3)
        for bar, val in zip(bars, vals):
            height = bar.get_height()
            text = f'{val:.3f}' if stat in ['AVG', 'OBP', 'SLG', 'OPS'] else f'{val:.2f}'
            ax.text(bar.get_x() + bar.get_width()/2., height + max_val*0.02, text, ha='center', va='bottom', fontweight='bold', fontsize=11)
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
    min_velo, max_velo = [], []
    for a in arsenal:
        try:
            rng = a['velocity'].split('（')[0].strip().replace('mph', '').split('-')
            min_velo.append(float(rng[0].strip()))
            max_velo.append(float(rng[1].strip()))
        except Exception:
            min_velo.append(0)
            max_velo.append(0)
    avg_velo = [(m + M) / 2 for m, M in zip(min_velo, max_velo)]
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
    ax.set_xticklabels(pitches, fontsize=9)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(75, 105)
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


def build_info_grid(p):
    items = [("全名", p['name']), ("出生日期", p['birth_date']), ("年龄", p['age'] + "岁"), ("出生地", p['birthplace']), ("身高/体重", p['height_weight']), ("击球/投球", p['bats_throws']), ("位置", p['position']), ("MLB首秀", p['debut'])]
    if p.get('college'): items.append(("大学", p['college']))
    if p.get('high_school'): items.append(("高中", p['high_school']))
    items.extend([("选秀", p['draft']), ("背号", "#" + p['number']), ("状态", p['status'])])
    return "\n".join(f'                    <div class="info-item"><div class="label">{label}</div><div class="value">{value}</div></div>' for label, value in items)


def build_pitching_grid(stats):
    order = [('G', '出赛'), ('GS', '先发'), ('W', '胜'), ('L', '败'), ('ERA', 'ERA'), ('IP', 'IP'), ('K', 'K'), ('BB', 'BB'), ('WHIP', 'WHIP'), ('K/9', 'K/9'), ('BB/9', 'BB/9'), ('HR', '被全垒打')]
    html = ""
    for k, label in order:
        val = stats.get(k, '—')
        color = "#4fc3f7"
        if k == 'ERA':
            try:
                v = float(val)
                color = "#4caf50" if v < 3.5 else "#ff9800" if v < 5.0 else "#f44336"
            except: pass
        html += f'                <div class="stat-card"><span class="stat-value" style="color: {color};">{val}</span><div class="stat-label">{label}</div></div>\n'
    return html


def build_hitting_grid(stats):
    order = [('G', '出赛'), ('AB', '打数'), ('PA', '打席'), ('R', '得分'), ('H', '安打'), ('2B', '二垒'), ('3B', '三垒'), ('HR', '本垒打'), ('RBI', '打点'), ('BB', '保送'), ('SO', '三振'), ('AVG', 'AVG'), ('OBP', 'OBP'), ('SLG', 'SLG'), ('OPS', 'OPS'), ('SB', '盗垒')]
    html = ""
    for k, label in order:
        val = stats.get(k, '—')
        color = "#4fc3f7"
        if k == 'OPS':
            try:
                v = float(val.replace('.', '') if val.startswith('.') else val)
                if val.startswith('.'): v = float(val)
                color = "#4caf50" if v > 0.800 else "#ff9800" if v > 0.650 else "#f44336"
            except: pass
        html += f'                <div class="stat-card"><span class="stat-value" style="color: {color};">{val}</span><div class="stat-label">{label}</div></div>\n'
    return html


def build_pitching_table(s24, s25, s26):
    rows = ""
    for year, s in [("2024", s24), ("2025", s25), ("2026", s26)]:
        year_class = 'warning' if year == '2026' else 'highlight' if year == '2025' else 'success'
        rows += f'                    <tr><td class="{year_class}">{year}</td><td>{s.get("G","—")}</td><td>{s.get("GS","—")}</td><td>{s.get("W","—")}-{s.get("L","—")}</td><td>{s.get("ERA","—")}</td><td>{s.get("IP","—")}</td><td>{s.get("K","—")}</td><td>{s.get("BB","—")}</td><td>{s.get("WHIP","—")}</td><td>{s.get("K/9","—")}</td></tr>\n'
    return rows


def build_hitting_table(s24, s25, s26):
    rows = ""
    for year, s in [("2024", s24), ("2025", s25), ("2026", s26)]:
        year_class = 'warning' if year == '2026' else 'highlight' if year == '2025' else 'success'
        rows += f'                    <tr><td class="{year_class}">{year}</td><td>{s.get("G","—")}</td><td>{s.get("AB","—")}</td><td>{s.get("PA","—")}</td><td>{s.get("HR","—")}</td><td>{s.get("RBI","—")}</td><td>{s.get("BB","—")}</td><td>{s.get("SO","—")}</td><td>{s.get("AVG","—")}</td><td>{s.get("OBP","—")}</td><td>{s.get("SLG","—")}</td><td>{s.get("OPS","—")}</td></tr>\n'
    return rows


def build_pitch_arsenal_html(p):
    if not p.get('pitch_arsenal'):
        return ""
    cards = "\n".join(f'                <div class="pitch-card"><h3>{a["name"]}</h3><p><span class="velocity">{a["velocity"]}</span></p><p>{a["desc"]}</p></div>' for a in p['pitch_arsenal'])
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
    return "\n".join(f'                <div class="stat-card"><span class="stat-value" style="color: {"#4caf50" if g["value"] >= 60 else "#4fc3f7" if g["value"] >= 50 else "#ff9800"};">{g["value"]}</span><div class="stat-label">{g["label"]}</div><span class="grade {grade_class(g["value"])}">{g["grade"]}</span></div>' for g in grades)


def build_pros_cons(items):
    return "\n".join(f'                        <li>{item}</li>' for item in items)


def build_html(p):
    html = HTML_TEMPLATE
    html = html.replace('__TITLE__', f"{p['name']} 球探报告")
    html = html.replace('__PLAYER_NAME__', p['name'])
    html = html.replace('__SUBTITLE__', f"Los Angeles Dodgers #{p['number']} | {p['position']} | {p['status']}")
    html = html.replace('__CSS__', HTML_CSS)
    html = html.replace('__COVER_IMG__', f"{p['slug']}_report_cover.png")
    html = html.replace('__INFO_GRID__', build_info_grid(p))
    html = html.replace('__SCOUTING_SUMMARY__', p['summary'])
    html = html.replace('__CAREER_HIGHLIGHTS__', p['career_highlights'])

    if p['type'] == 'pitcher':
        stats_section = f'''
        <div class="section">
            <h2>📊 2026赛季投球数据</h2>
            <div class="stats-grid">
{build_pitching_grid(p['stats_2026'])}
            </div>
        </div>'''
        season_section = f'''
        <div class="section">
            <h2>📊 2024-2026 近三年赛季对比</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="{p['slug']}_season_comparison.png" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
            <h3 style="margin-top: 30px; color: #4fc3f7;">近三年投球数据对比</h3>
            <table class="comparison-table">
                <thead><tr><th>赛季</th><th>G</th><th>GS</th><th>W-L</th><th>ERA</th><th>IP</th><th>K</th><th>BB</th><th>WHIP</th><th>K/9</th></tr></thead>
                <tbody>
{build_pitching_table(p['stats_2024'], p['stats_2025'], p['stats_2026'])}
                </tbody>
            </table>
        </div>'''
    else:
        stats_section = f'''
        <div class="section">
            <h2>📊 2026赛季打击数据</h2>
            <div class="stats-grid">
{build_hitting_grid(p['stats_2026'])}
            </div>
        </div>'''
        season_section = f'''
        <div class="section">
            <h2>📊 2024-2026 近三年赛季对比</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="{p['slug']}_season_comparison.png" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
            <h3 style="margin-top: 30px; color: #4fc3f7;">近三年打击数据对比</h3>
            <table class="comparison-table">
                <thead><tr><th>赛季</th><th>G</th><th>AB</th><th>PA</th><th>HR</th><th>RBI</th><th>BB</th><th>SO</th><th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th></tr></thead>
                <tbody>
{build_hitting_table(p['stats_2024'], p['stats_2025'], p['stats_2026'])}
                </tbody>
            </table>
        </div>'''

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
    html = html.replace('__OVERALL_CLASS__', grade_class(p['overall_grade']))
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
        f"- **选秀**：{p['draft']}",
        "",
        "---",
        "",
        "## 📊 2026赛季数据",
        ""
    ]
    if p['type'] == 'pitcher':
        lines.extend([
            "| G | GS | W | L | ERA | IP | K | BB | WHIP | K/9 |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
            f"| {s26.get('G','—')} | {s26.get('GS','—')} | {s26.get('W','—')} | {s26.get('L','—')} | {s26.get('ERA','—')} | {s26.get('IP','—')} | {s26.get('K','—')} | {s26.get('BB','—')} | {s26.get('WHIP','—')} | {s26.get('K/9','—')} |",
            "",
            "---",
            "",
            "## 📊 2024-2026 近三年投球数据对比",
            "",
            "| 赛季 | G | GS | W-L | ERA | IP | K | BB | WHIP | K/9 |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
            f"| 2024 | {s24.get('G','—')} | {s24.get('GS','—')} | {s24.get('W','—')}-{s24.get('L','—')} | {s24.get('ERA','—')} | {s24.get('IP','—')} | {s24.get('K','—')} | {s24.get('BB','—')} | {s24.get('WHIP','—')} | {s24.get('K/9','—')} |",
            f"| 2025 | {s25.get('G','—')} | {s25.get('GS','—')} | {s25.get('W','—')}-{s25.get('L','—')} | {s25.get('ERA','—')} | {s25.get('IP','—')} | {s25.get('K','—')} | {s25.get('BB','—')} | {s25.get('WHIP','—')} | {s25.get('K/9','—')} |",
            f"| 2026 | {s26.get('G','—')} | {s26.get('GS','—')} | {s26.get('W','—')}-{s26.get('L','—')} | {s26.get('ERA','—')} | {s26.get('IP','—')} | {s26.get('K','—')} | {s26.get('BB','—')} | {s26.get('WHIP','—')} | {s26.get('K/9','—')} |",
        ])
    else:
        lines.extend([
            "| G | AB | PA | HR | RBI | BB | SO | AVG | OBP | SLG | OPS |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
            f"| {s26.get('G','—')} | {s26.get('AB','—')} | {s26.get('PA','—')} | {s26.get('HR','—')} | {s26.get('RBI','—')} | {s26.get('BB','—')} | {s26.get('SO','—')} | {s26.get('AVG','—')} | {s26.get('OBP','—')} | {s26.get('SLG','—')} | {s26.get('OPS','—')} |",
            "",
            "---",
            "",
            "## 📊 2024-2026 近三年打击数据对比",
            "",
            "| 赛季 | G | AB | PA | HR | RBI | BB | SO | AVG | OBP | SLG | OPS |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|",
            f"| 2024 | {s24.get('G','—')} | {s24.get('AB','—')} | {s24.get('PA','—')} | {s24.get('HR','—')} | {s24.get('RBI','—')} | {s24.get('BB','—')} | {s24.get('SO','—')} | {s24.get('AVG','—')} | {s24.get('OBP','—')} | {s24.get('SLG','—')} | {s24.get('OPS','—')} |",
            f"| 2025 | {s25.get('G','—')} | {s25.get('AB','—')} | {s25.get('PA','—')} | {s25.get('HR','—')} | {s25.get('RBI','—')} | {s25.get('BB','—')} | {s25.get('SO','—')} | {s25.get('AVG','—')} | {s25.get('OBP','—')} | {s25.get('SLG','—')} | {s25.get('OPS','—')} |",
            f"| 2026 | {s26.get('G','—')} | {s26.get('AB','—')} | {s26.get('PA','—')} | {s26.get('HR','—')} | {s26.get('RBI','—')} | {s26.get('BB','—')} | {s26.get('SO','—')} | {s26.get('AVG','—')} | {s26.get('OBP','—')} | {s26.get('SLG','—')} | {s26.get('OPS','—')} |",
        ])
    lines.extend([
        "",
        "---",
        "",
        "## 📊 综合评分",
        "",
        f"总体评分：**{p['overall_grade']}**（{p['overall_label']}）",
        "",
        "| 项目 | 评分 (20-80) | 等级 |",
        "|---|---|---|"
    ])
    for g in p['grades']:
        lines.append(f"| {g['label']} | {g['value']} | {g['grade']} |")
    lines.extend([
        "",
        "---",
        "",
        "## 📚 数据来源",
        "",
        "- MLB.com / MLB Stats API",
        "- Baseball Savant (Statcast)",
        "- Fangraphs",
        "",
        f"*数据来源：MLB.com / MLB Stats API | 生成时间：{TODAY}*"
    ])
    return "\n".join(lines)


def main():
    for p in PLAYERS:
        output_dir = os.path.join(OUTPUT_BASE, p['slug'])
        os.makedirs(output_dir, exist_ok=True)
        print(f"\nGenerating report for {p['name']} -> {output_dir}")
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

    print("\nAll newcomer reports completed!")


if __name__ == '__main__':
    main()
