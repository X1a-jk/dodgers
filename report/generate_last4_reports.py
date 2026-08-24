#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为剩余4名道奇球员（Ronan Kopp / Chayce McDermott / Wyatt Mills / Alek Thomas）
生成佐佐木朗希级别的完整定制化球探报告。
复用 generate_custom_report.py 的模板与图表引擎。
"""
import sys
import os

# 把脚本所在目录加入路径，确保能 import generate_custom_report
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import generate_custom_report as gcr

# ---------------------------------------------------------------------------
# 球员配置列表
# ---------------------------------------------------------------------------
PLAYERS = [
    {
        "name": "Ronan Kopp",
        "slug": "ronan-kopp",
        "last_name": "kopp",
        "number": "83",
        "position": "左投后援 (LHP)",
        "position_code": "P",
        "bats_throws": "左打 / 左投",
        "birth_date": "2002-07-28",
        "age": "24",
        "birthplace": "美国密歇根州 (Michigan, USA)",
        "height_weight": "6'7\" / 250 lbs",
        "debut": "尚未首秀",
        "college": "Arizona State University",
        "nickname": "The Big Lefty",
        "status": "Minors",
        "type": "pitcher",
        "summary": """
            <p style="margin-bottom: 15px;">Ronan Kopp 是道奇农场体系中备受瞩目的高大左投后援。身高 6 英尺 7 英寸、体重 250 磅的庞大身躯，让他在投手丘上拥有极具压迫感的存在感与陡峭的放球角度。</p>
            <p style="margin-bottom: 15px;">Kopp 尚未登上大联盟，但他在小联盟的持续成长让球探对他充满期待。作为一名左投，他的快速球与滑球组合已经具备大联盟后援的雏形；若能进一步提升控球与稳定性，他有望成为道奇未来牛棚的重要左投力量。</p>
            <p>他的天花板取决于控球进步幅度与伤病管理。考虑到道奇牛棚对左投的持续需求，Kopp 是组织内值得长期培养的新秀之一。</p>
        """,
        "career_highlights": """
            <div class="career-highlight"><h4>🎓 大学时期 - Arizona State 强投</h4><p>Kopp 在亚利桑那州立大学展现潜力，凭借高大的身材与左投优势成为选秀市场上的热门名字。大学经验帮助他建立了基本的投球机制与比赛节奏。</p></div>
            <div class="career-highlight"><h4>⚾ 选秀加盟道奇</h4><p>道奇在选秀中选择 Kopp，看中他稀有的左投身材、伸卡潜质与未来发展空间。进入职业体系后，球队着重改造他的配球与控球。</p></div>
            <div class="career-highlight"><h4>🚀 小联盟快速成长</h4><p>在道奇农场体系中，Kopp 快速穿越低阶小联盟。他的三振能力出色，持续用球速与身材优势压制同层级打者，并逐步在高阶小联盟接受考验。</p></div>
            <div class="career-highlight"><h4>🔮 2026年 - 接近大联盟门口</h4><p>2026年 Kopp 位于俄克拉荷马城彗星队（Oklahoma City Comets），处于大联盟门槛。道奇球探与教练团持续监控他的控球进步，伺机给他上大联盟的机会。</p></div>
        """,
        "stats_2026": {"G": "—", "GS": "—", "W": "—", "L": "—", "ERA": "—", "IP": "—", "K": "—", "BB": "—", "WHIP": "—", "K/9": "—", "BB/9": "—", "HR": "—"},
        "stats_2025": {"G": "—", "GS": "—", "W": "—", "L": "—", "ERA": "—", "IP": "—", "K": "—", "BB": "—", "WHIP": "—", "K/9": "—", "BB/9": "—", "HR": "—"},
        "cover_stats": [("Age", "24"), ("Height", "6'7\""), ("Weight", "250"), ("Throws", "L"), ("Level", "AAA"), ("Status", "Minors"), ("Debut", "—"), ("Role", "LHP RP")],
        "season_chart_2025": [0.0, 0.0, 0.0, 0.0],
        "season_chart_2026": [0.0, 0.0, 0.0, 0.0],
        "season_chart_stats": ["ERA", "WHIP", "K/9", "BB/9"],
        "pitch_arsenal": [
            {"name": "四缝快速球 (Four-Seam Fastball)", "velocity": "94-97 mph", "avg": "95.5", "desc": "Kopp 的招牌球种。凭借 6 尺 7 寸的放球高度与左投角度，快速球从打者视角极具压迫感，常能制造挥空与软弱击球。"},
            {"name": "滑球 (Slider)", "velocity": "82-85 mph", "avg": "83.5", "desc": "主要的三振与对左打者武器。横向位移明显，在两好球后能有效诱导追打。提升一致性与sharpness是下一步关键。"},
            {"name": "伸卡球 / 二缝线 (Sinker / Two-Seam)", "velocity": "93-96 mph", "avg": "94.5", "desc": "利用高大身材制造的下坠角度，是 Kopp 的另一项潜力武器。若能稳定进垒，可显著提升 his ground-ball rate。"},
            {"name": "变速球 (Changeup)", "velocity": "86-89 mph", "avg": "87.5", "desc": "尚在开发中的第四球种，用来对付右打者。当前使用频率低，但若发展成熟，将让他的轮值/后援价值更上一层楼。"}
        ],
        "analysis": """
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">身材带来的先天优势</h3>
                <p>6 尺 7 寸的身高让 Kopp 的放球点高于一般后援，打者较难判断球路轨迹。他的左投身份在牛棚市场中尤为稀缺，只要能稳定出赛，便具备很高战术价值。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">控球是最大问号</h3>
                <p>高大的投手往往面临机械一致性挑战。Kopp 的快速球与滑球已有大联盟雏形，但能否持续把速球投进好球带边缘，将决定他是能成为 high-leverage 左投，还是仅仅是一名边缘牛棚。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">角色定位</h3>
                <p>短期内 Kopp 最可能以左投后援身份起步，面对左打者为主。若控球与变化球进步，他有机会成长为 multi-inning 后援，甚至挑战 setup 角色。长期来看，道奇也可能尝试让他先发出赛。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">伤病与耐久</h3>
                <p>年轻投手都需要重视工作管理。Kopp 目前健康，但道奇会谨慎控制他的局数与连续出赛频率，以保护他宝贵的左投手臂。</p>
            </div>
        """,
        "pros": [
            "罕见的 6 尺 7 寸左投身材，放球角度极具优势",
            "四缝线快速球具备 94-97 mph 的球速",
            "滑球是可靠的出局武器",
            "伸卡球潜质出色，有机会提升滚地球率",
            "年龄仅 24 岁，成长空间巨大",
            "左投身份在道奇牛棚中极具战术价值",
            "小联盟三振能力出色",
            "有挑战 multi-inning 后援甚至先发的身材条件"
        ],
        "cons": [
            "尚未登上大联盟，缺乏最高层级经验",
            "控球一致性仍需大幅改善",
            "变速球尚未成熟，右打者可能有机可乘",
            "高个子投手的机械重复性挑战",
            "小联盟样本尚未证明能稳定贡献",
            "面对精英打者时配球智慧待考验",
            "需要保持健康并避免过度使用"
        ],
        "grades": [
            {"label": "Fastball", "value": 60, "grade": "B+"},
            {"label": "Slider", "value": 55, "grade": "B"},
            {"label": "Changeup", "value": 45, "grade": "C+"},
            {"label": "Control", "value": 45, "grade": "C+"},
            {"label": "Command", "value": 45, "grade": "C+"},
            {"label": "Stamina", "value": 50, "grade": "B-"},
            {"label": "Durability", "value": 50, "grade": "B-"},
            {"label": "Mental", "value": 50, "grade": "B-"}
        ],
        "overall_grade": 51,
        "overall_label": "B- 级 / 潜力左投后援",
        "overall_desc": "拥有罕见身材与左投优势的新秀后援，球速与滑球已达大联盟门槛。控球与经验是他能否站稳大联盟的关键变量。",
        "future_outlook": """
            <div style="margin-top: 20px;">
                <p>Kopp 的未来取决于控球进步速度。他具备成为道奇牛棚稳定左投的身体条件，但需要在 AAA 持续证明可以把球投进好球带，并减少保送与中心击球。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>提升控球一致性：</strong>将保送率压低至可接受范围，建立 first-pitch strike 优势。</li>
                    <li><strong>发展变速球：</strong>增加面对右打者的武器，避免被针对。</li>
                    <li><strong>稳定投球机制：</strong>利用身材优势而非被其拖累，保持可重复的手臂路径。</li>
                    <li><strong>健康管理：</strong>在 AAA 完成完整赛季，为下一年大联盟机会做准备。</li>
                </ol>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
                <p><strong>2026 下半季：</strong>继续于 AAA 出赛，争取获得大联盟首次征召。</p>
                <p><strong>2027：</strong>若控球进步，有机会成为道奇牛棚左投选项，出赛 30-50 场。</p>
                <p><strong>2028+：</strong>若快速球与滑球组合稳定，有望成为 setup 级别的左投后援。</p>

                <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3>
                <ul style="margin-left: 20px; line-height: 2;">
                    <li>控球未改善时，容易被精英打者选掉</li>
                    <li>高个子投手的伤病风险需持续关注</li>
                    <li>变化球发展停滞会限制 ceiling</li>
                </ul>
            </div>
        """,
        "background": """
            <div style="margin-top: 20px;">
                <p>Ronan Kopp 出生于美国密歇根州，身高 6 英尺 7 英寸、体重 250 磅，是道奇农场中体型最醒目的投手之一。他在亚利桑那州立大学（Arizona State University）完成大学生涯，凭借左投与身材优势进入职业棒球。</p>
                <p>加盟道奇后，Kopp 在教练团指导下逐步改造配球与投球机制。球队希望将他的身材优势转化为稳定的速球压制力，同时改善他的控球问题。</p>
                <p>场外，Kopp 以谦逊与努力著称。他深知自己并非完成品，经常在牛棚中加练滑球与变速球。队友与教练都认为他是农场体系中进步最快的年轻投手之一。</p>
            </div>
        """
    },
    {
        "name": "Chayce McDermott",
        "slug": "chayce-mcdermott",
        "last_name": "mcdermott",
        "number": "62",
        "position": "右投先发 / 长中继 (RHP)",
        "position_code": "P",
        "bats_throws": "左打 / 右投",
        "birth_date": "1998-08-22",
        "age": "27",
        "birthplace": "美国加利福尼亚州 (California, USA)",
        "height_weight": "6'3\" / 190 lbs",
        "debut": "2024-07-24",
        "college": "Sam Houston State University",
        "nickname": "Chayce",
        "status": "Minors",
        "type": "pitcher",
        "summary": """
            <p style="margin-bottom: 15px;">Chayce McDermott 是一名在大联盟已有初体验的右投，2024 年 7 月 24 日于巴尔的摩金莺完成首秀。2025 年在金莺短暂登板表现挣扎后，2026 年转战洛杉矶道奇体系，目前于小联盟持续调整。</p>
            <p style="margin-bottom: 15px;">McDermott 的球风属于控球型右投，配球以快速球搭配多种变化球为主。他的身材条件不算突出，但具备吃下局数的能力与比赛智慧。在金莺的小样本（8.2 局 ERA 15.58）不能代表真实实力，反而显示他在适应大联盟节奏时遇到挑战。</p>
            <p>加盟道奇后，McDermott 的首要任务是在 AAA 找回控球节奏，争取成为道奇轮值深度或长中继选项。他的 floor 是一名可以上下大联盟的 sixth starter / swingman。</p>
        """,
        "career_highlights": """
            <div class="career-highlight"><h4>🎓 Sam Houston State 王牌</h4><p>McDermott 在大学时期是 Sam Houston State 的主力投手，展现出优秀的控球与比赛节奏，为进入职业棒球打下坚实基础。</p></div>
            <div class="career-highlight"><h4>⚾ 2021年选秀 - 金莺选中</h4><p>McDermott 在 2021 年选秀中被巴尔的摩金莺选中。他在金莺农场体系中逐步攀升，以稳定先发与长局数能力著称。</p></div>
            <div class="career-highlight"><h4>🌟 2024年 - 大联盟首秀</h4><p>2024 年 7 月 24 日，McDermott 登上大联盟完成首秀。虽然机会有限，但他终于踏上最高舞台，积累了宝贵经验。</p></div>
            <div class="career-highlight"><h4>🔵 2026年 - 加盟道奇</h4><p>McDermott 加入道奇组织，为球队提供轮值深度。在道奇教练团体系下，他有机会重塑自己的配球策略与球路组合。</p></div>
        """,
        "stats_2026": {"G": 2, "GS": 0, "W": 0, "L": 0, "ERA": "7.71", "IP": "2.1", "K": 1, "BB": 0, "WHIP": "1.29", "K/9": "3.86", "BB/9": "0.00", "HR": 1},
        "stats_2025": {"G": 4, "GS": 1, "W": 0, "L": 1, "ERA": "15.58", "IP": "8.2", "K": 9, "BB": 12, "WHIP": "2.77", "K/9": "9.35", "BB/9": "12.46", "HR": 3},
        "cover_stats": [("ERA 2026", "7.71"), ("IP 2026", "2.1"), ("K", "1"), ("BB", "0"), ("ERA 2025", "15.58"), ("BB/9 2025", "12.46"), ("Age", "27"), ("Debut", "2024")],
        "season_chart_2025": [15.58, 2.77, 9.35, 12.46],
        "season_chart_2026": [7.71, 1.29, 3.86, 0.00],
        "season_chart_stats": ["ERA", "WHIP", "K/9", "BB/9"],
        "pitch_arsenal": [
            {"name": "四缝快速球 (Four-Seam Fastball)", "velocity": "91-94 mph", "avg": "92.5", "desc": "McDermott 的速球球速不突出，主要依靠控球与角度来压制打者。他需要精准地把球投到好球带边缘，避免被强打者坐待中心球。"},
            {"name": "曲球 (Curveball)", "velocity": "76-79 mph", "avg": "77.5", "desc": "他的主要变化球之一，具备不错的大弧度下坠。在两好球后用来诱导追打，但需要更稳定的落点控制。"},
            {"name": "滑球 (Slider)", "velocity": "83-86 mph", "avg": "84.5", "desc": "对付右打者的重要武器，横向位移可制造 weak contact。2025 年小样本中控球不稳，导致这颗球未能发挥应有效果。"},
            {"name": "变速球 (Changeup)", "velocity": "84-87 mph", "avg": "85.5", "desc": "对付左打者的关键变化球。若能改善速度差与放球点一致性，将显著提升他面对左打时的生存能力。"}
        ],
        "analysis": """
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">控球危机是首要问题</h3>
                <p>2025 年在金莺的 8.2 局中送出 12 次保送，BB/9 高达 12.46，这是他表现崩盘的主因。无论球路品质如何，无法把球投进好球带都会让自己陷入被动。加盟道奇后，重建控球信心是当务之急。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">小样本警示</h3>
                <p>2025 年 8.2 局与 2026 年 2.1 局的样本都极小，不能据此判定 McDermott 的真实实力。他在小联盟可能有更稳定的数据，只是在大联盟舞台上尚未找到节奏。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">球路组合具备轮换深度价值</h3>
                <p>McDermott 拥有四缝线、曲球、滑球与变速球四种球路，理论上足以担任后端先发或长中继。问题不在球种数量，而在执行稳定性。道奇的投教团队擅长改造这类控球型投手。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">角色定位</h3>
                <p>他的最佳角色可能是 swingman：在先发轮值需要深度时顶上，或在牛棚需要 long relief 时吃下 2-3 局。这种角色对控球和体能都有要求，正是 McDermott 需要证明的地方。</p>
            </div>
        """,
        "pros": [
            "具备先发与长中继的 swingman 身材条件",
            "大学时期有良好控球基础",
            "四种球路组合增加配球变化",
            "2025 年 K/9 9.35 显示三振潜力",
            "有过大联盟首秀经验，适应过最高舞台",
            "道奇体系擅长改造控球型投手",
            "右投身份在轮值深度中具价值",
            "能吃局数的潜质"
        ],
        "cons": [
            "2025 年 BB/9 12.46，控球严重失控",
            "2025 年 WHIP 2.77，被上垒率极高",
            "2025 年 8.2 局被轰 3 支全垒打",
            "快速球球速不突出，压制力有限",
            "2026 年小联盟/大联盟样本仍极小",
            "面对精英打者时配球执行不稳",
            "尚未证明自己能在道奇体系中稳定贡献"
        ],
        "grades": [
            {"label": "Fastball", "value": 50, "grade": "B-"},
            {"label": "Curveball", "value": 55, "grade": "B"},
            {"label": "Slider", "value": 50, "grade": "B-"},
            {"label": "Changeup", "value": 50, "grade": "B-"},
            {"label": "Control", "value": 40, "grade": "C"},
            {"label": "Command", "value": 40, "grade": "C"},
            {"label": "Stamina", "value": 55, "grade": "B"},
            {"label": "Mental", "value": 50, "grade": "B-"}
        ],
        "overall_grade": 48,
        "overall_label": "C+ 级 / 轮值深度/长中继候选人",
        "overall_desc": "具备多种球路与吃局数能力，但控球在大联盟小样本中崩盘。能否在道奇体系下找回节奏，将决定他是否能在 MLB 站稳脚跟。",
        "future_outlook": """
            <div style="margin-top: 20px;">
                <p>McDermott 的 2026 年目标是在 AAA 稳定出赛，把保送率压回生涯平均水平。若能找回大学时期的控球感觉，他有机会在道奇伤病潮或轮值深度不足时获得上大联盟的机会。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>重建控球：</strong>把 BB/9 压回 4.0 以下，恢复 first-pitch strike 比例。</li>
                    <li><strong>简化配球：</strong>先以快速球+曲球为主轴，逐步加入滑球与变速球。</li>
                    <li><strong>提升心理韧性：</strong>2025 年崩盘的阴影需要透过稳定出赛来摆脱。</li>
                    <li><strong>定位 swingman：</strong>接受长中继/第六先发的角色，增加球队价值。</li>
                </ol>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
                <p><strong>2026 下半季：</strong>在 AAA 稳定先发，争取 100+ 局，ERA 控制在 4.50 以下。</p>
                <p><strong>2027：</strong>有机会以 sixth starter / long relief 身份进入道奇大联盟名单。</p>
                <p><strong>2028+：</strong>若控球稳定，可成为道奇轮值深度与牛棚长局数的重要选项。</p>

                <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3>
                <ul style="margin-left: 20px; line-height: 2;">
                    <li>控球若无法改善，容易被 DFA 或退回小联盟</li>
                    <li>球速不足导致面对强打阵容时压制力有限</li>
                    <li>伤病会压缩他在轮换中的机会窗口</li>
                </ul>
            </div>
        """,
        "background": """
            <div style="margin-top: 20px;">
                <p>Chayce McDermott 出生于美国加州，大学时期是 Sam Houston State University 的当家投手。他在 2021 年选秀中被巴尔的摩金莺选中，在金莺农场体系中逐步成长为具有轮换深度的右投。</p>
                <p>2024 年 7 月 24 日，McDermott 终于踏上大联盟舞台。然而后续机会有限，表现也未能延续小联盟的稳定性。2026 年他加入洛杉矶道奇，希望在这座以投教闻名的组织中重新证明自己。</p>
                <p>场外，McDermott 以沉稳与善于学习著称。他积极接受教练团改造，专注于恢复大学时期的控球优势。对道奇而言，他是低风险、可能中回报的轮值深度投资。</p>
            </div>
        """
    },
    {
        "name": "Wyatt Mills",
        "slug": "wyatt-mills",
        "last_name": "mills",
        "number": "58",
        "position": "右投后援 (RHP)",
        "position_code": "P",
        "bats_throws": "右打 / 右投",
        "birth_date": "1995-01-25",
        "age": "31",
        "birthplace": "美国华盛顿州斯波坎 (Spokane, WA)",
        "height_weight": "6'4\" / 220 lbs",
        "debut": "2021-05-01",
        "college": "Gonzaga University",
        "nickname": "Wyatt",
        "status": "Minors",
        "type": "pitcher",
        "summary": """
            <p style="margin-bottom: 15px;">Wyatt Mills 是一名经验丰富的右投后援，2021 年 5 月 1 日在西雅图水手完成大联盟首秀。他辗转水手、堪萨斯城皇家等队，2026 年加入洛杉矶道奇组织，目前位于小联盟，争取再次获得大联盟机会。</p>
            <p style="margin-bottom: 15px;">Mills 的球风以侧投/低肩放球点著称，擅长制造横向位移与 weak contact。他的球速不突出，但依靠独特的放球角度与配球智慧在大联盟生存。2026 年在道奇的 4.1 局小样本中，ERA 6.23、WHIP 2.31，显示出控球问题仍需改善。</p>
            <p>31 岁的 Mills 已经进入生涯后期，他的价值在于经验、低肩角度与能吃局数。若能在道奇牛棚中找到定位，他可以作为 situational reliever 或 innings eater 提供深度。</p>
        """,
        "career_highlights": """
            <div class="career-highlight"><h4>🎓 Gonzaga 大学时期</h4><p>Mills 在冈萨加大学（Gonzaga University）成长为可靠的后援投手，以低肩侧投与控球能力著称。大学表现让他进入职业棒球雷达。</p></div>
            <div class="career-highlight"><h4>⚾ 2017年选秀 - 水手第11轮</h4><p>西雅图水手在 2017 年选秀第 11 轮选中 Mills。他在水手农场体系中逐步攀升，以低肩角度与变化球组合建立特色。</p></div>
            <div class="career-highlight"><h4>🌟 2021年 - 大联盟首秀</h4><p>2021 年 5 月 1 日，Mills 代表水手登上大联盟。随后他也在堪萨斯城皇家等队效力，积累了丰富的上下大联盟经验。</p></div>
            <div class="career-highlight"><h4>🔵 2026年 - 加盟道奇</h4><p>2026 年 Mills 加入道奇组织，为牛棚提供 veteran depth。虽然年龄与球速限制了他的 ceiling，但他的经验与独特角度仍具价值。</p></div>
        """,
        "stats_2026": {"G": 5, "GS": 0, "W": 0, "L": 0, "ERA": "6.23", "IP": "4.1", "K": 4, "BB": 7, "WHIP": "2.31", "K/9": "8.31", "BB/9": "14.54", "HR": 0},
        "stats_2025": {"G": "—", "GS": "—", "W": "—", "L": "—", "ERA": "—", "IP": "—", "K": "—", "BB": "—", "WHIP": "—", "K/9": "—", "BB/9": "—", "HR": "—"},
        "cover_stats": [("ERA 2026", "6.23"), ("IP 2026", "4.1"), ("K", "4"), ("BB", "7"), ("BB/9", "14.54"), ("Age", "31"), ("Debut", "2021"), ("Role", "RHP RP")],
        "season_chart_2025": [0.0, 0.0, 0.0, 0.0],
        "season_chart_2026": [6.23, 2.31, 8.31, 14.54],
        "season_chart_stats": ["ERA", "WHIP", "K/9", "BB/9"],
        "pitch_arsenal": [
            {"name": "伸卡球 / 二缝线 (Sinker / Two-Seam)", "velocity": "89-92 mph", "avg": "90.5", "desc": "Mills 的招牌球种。低肩放球角度让伸卡球带有显著横向位移与下坠，是他的地面球制造机。他依靠这颗球让打者击出软弱滚地球。"},
            {"name": "滑球 (Slider)", "velocity": "80-83 mph", "avg": "81.5", "desc": "主要出局球，横向位移大。对付右打者内角与左打者外角都有威胁，但同样需要精准控制落点。"},
            {"name": "变速球 (Changeup)", "velocity": "82-85 mph", "avg": "83.5", "desc": "偶尔用来对付左打者，改变速度节奏。使用频率不高，但能增加配球变化，避免打者坐待伸卡球。"},
            {"name": "曲球 (Curveball)", "velocity": "74-77 mph", "avg": "75.5", "desc": "作为展示球种使用，用来在两好球后改变打者视线。大弧度下坠可与伸卡球的横向位移形成对比。"}
        ],
        "analysis": """
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">侧投角度的战术价值</h3>
                <p>Mills 最大的武器不是球速，而是低肩/侧投的放球点。这种角度让打者难以适应，尤其面对同侧右打者时，伸卡球与滑球的组合能制造大量滚地球与挥空。对道奇而言，他可作为 situational reliever 使用。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">2026 年控球危机</h3>
                <p>4.1 局送出 7 次保送，BB/9 高达 14.54，这是不可接受的。无论角度多刁钻，无法把球投进好球带都会让自己和球队陷入被动。Mills 必须立即改善控球，否则很快会被取代。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">年龄与天花板</h3>
                <p>31 岁的 Mills 已经进入生涯后期，不太可能成为道奇牛棚的长期答案。但他的经验和独特角度让他在特定 matchup 中仍有价值，例如需要地面球或面对右打者集中的局数。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">角色定位</h3>
                <p>理想角色是低 leverage 的 innings eater 或 situational righty。他不适合高压局面，但在牛棚需要休息日时，可以上场吃下 1-2 局。</p>
            </div>
        """,
        "pros": [
            "独特的低肩/侧投放球角度",
            "伸卡球能制造大量滚地球",
            "丰富的上下大联盟经验",
            "能吃局数，适合长中继或牛棚休息日用",
            "滑球是同侧打者的有效武器",
            "31 岁仍具备即战力潜力",
            "道奇体系能最大化他的配球优势",
            "低成本的牛棚深度选项"
        ],
        "cons": [
            "2026 年 BB/9 14.54，控球严重失控",
            "WHIP 2.31，被上垒率极高",
            "球速不足，压制力有限",
            "面对左打者时效果通常不佳",
            "31 岁，天花板与发展空间有限",
            "不适合 high-leverage 局面",
            "小样本数据代表性有限"
        ],
        "grades": [
            {"label": "Sinker", "value": 55, "grade": "B"},
            {"label": "Slider", "value": 50, "grade": "B-"},
            {"label": "Changeup", "value": 45, "grade": "C+"},
            {"label": "Curveball", "value": 45, "grade": "C+"},
            {"label": "Control", "value": 35, "grade": "D+"},
            {"label": "Command", "value": 40, "grade": "C"},
            {"label": "Stamina", "value": 50, "grade": "B-"},
            {"label": "Mental", "value": 55, "grade": "B"}
        ],
        "overall_grade": 47,
        "overall_label": "C+ 级 / 侧投牛棚深度",
        "overall_desc": "经验丰富、角度独特的侧投后援，但 2026 年控球崩盘。若无法迅速找回好球带，他的大联盟生涯可能进入尾声。",
        "future_outlook": """
            <div style="margin-top: 20px;">
                <p>Mills 的未来取决于他能否在道奇体系中找回控球。他的伸卡球与角度仍有价值，但 31 岁的年龄意味着机会窗口有限。他需要在每一次大联盟机会中证明自己还能贡献。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>首要改善控球：</strong>将 BB/9 压回 4.0 以下，否则无法在大联盟立足。</li>
                    <li><strong>强化伸卡球指令：</strong>利用低肩角度，让球更稳定地钻进下段好球带。</li>
                    <li><strong>面对左打者的策略：</strong>增加变速球使用，避免被左打者坐待伸卡球。</li>
                    <li><strong>接受角色定位：</strong>作为 low-leverage innings eater，珍惜每一次机会。</li>
                </ol>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
                <p><strong>2026 下半季：</strong>若控球改善，可能偶尔被征召上大联盟；否则继续在 AAA 担任 veteran depth。</p>
                <p><strong>2027：</strong>若无法稳定贡献，可能转战独立联盟或海外联赛。</p>
                <p><strong>2028+：</strong>大联盟生涯基本取决于 2026-2027 年的表现。</p>

                <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3>
                <ul style="margin-left: 20px; line-height: 2;">
                    <li>控球持续崩盘将导致被 DFA</li>
                    <li>年龄增长进一步降低球速与恢复能力</li>
                    <li>左打者针对性打击会压缩他的使用情境</li>
                </ul>
            </div>
        """,
        "background": """
            <div style="margin-top: 20px;">
                <p>Wyatt Mills 出生于华盛顿州斯波坎（Spokane, WA），在冈萨加大学（Gonzaga University）度过大学时光。他以低肩/侧投姿势和控球能力进入职业棒球，2017 年被西雅图水手在第 11 轮选中。</p>
                <p>在水手农场体系中，Mills 逐步成长为具备大联盟经验的牛棚投手。2021 年他完成大联盟首秀，此后也曾在堪萨斯城皇家等队效力。他的职业生涯一直与"角度专家"和"深度后援"的标签相伴。</p>
                <p>2026 年加盟道奇后，Mills 希望在这座冠军球队中重新证明自己。他的经验和独特角度是资产，但年龄与控球问题也让他的未来充满不确定性。</p>
            </div>
        """
    },
    {
        "name": "Alek Thomas",
        "slug": "alek-thomas",
        "last_name": "thomas",
        "number": "5",
        "position": "中外野手 (CF)",
        "position_code": "CF",
        "bats_throws": "左打 / 左投",
        "birth_date": "2000-04-28",
        "age": "26",
        "birthplace": "美国伊利诺伊州芝加哥 (Chicago, IL)",
        "height_weight": "5'9\" / 175 lbs",
        "debut": "2022-05-08",
        "college": "",
        "nickname": "AT",
        "status": "Minors",
        "type": "batter",
        "summary": """
            <p style="margin-bottom: 15px;">Alek Thomas 是一名以防守著称的左打中外野手，2022 年 5 月 8 日在亚利桑那响尾蛇完成大联盟首秀。他曾是响尾蛇 2023 年国联冠军队的重要成员，以 elite 的中外野防守与关键时刻打击闻名。</p>
            <p style="margin-bottom: 15px;">2025 年 Thomas 在响尾蛇出赛 143 场，缴出 .249/.289/.370、OPS .659 的成绩，外加 9 轰与 7 次盗垒。他的防守依旧出色，但打击表现起伏，尤其是上垒率偏低。2026 年他转战道奇体系，目前位于小联盟，道奇希望他能在需要时提供顶级中外野防守与板凳深度。</p>
            <p>Thomas 的 value proposition 非常明确：防守优先、速度加持、偶尔长打。在道奇这样进攻火力强大的球队中，他不需要成为核心打者，只需在防守与跑垒端做出贡献即可。</p>
        """,
        "career_highlights": """
            <div class="career-highlight"><h4>⭐ 2018年选秀 - 响尾蛇第2轮</h4><p>Thomas 在 2018 年选秀第 2 轮被亚利桑那响尾蛇选中。他出身于芝加哥，高中时期已是备受瞩目的五拍子中外野手新秀。</p></div>
            <div class="career-highlight"><h4>🌟 2022年 - 大联盟首秀</h4><p>2022 年 5 月 8 日，Thomas 登上大联盟。他迅速以惊人的中外野防守与左打长打潜力赢得球迷喜爱。</p></div>
            <div class="career-highlight"><h4>🏆 2023年 - 国联冠军</h4><p>Thomas 是响尾蛇 2023 年闯入世界大赛的关键成员。他在季后赛多次贡献关键安打与防守 play，包括在世界大赛中的精彩守备。</p></div>
            <div class="career-highlight"><h4>🔵 2026年 - 加盟道奇</h4><p>Thomas 加入道奇组织，为球队提供 elite 中外野防守选项与左打板凳深度。在 Mookie Betts、Andy Pages 等人之外，他是道奇外野防守的重要保险。</p></div>
        """,
        "stats_2026": {"G": 28, "AVG": ".181", "OBP": ".222", "SLG": ".340", "OPS": ".562", "HR": 2, "RBI": 10, "SB": 4, "BB": 3, "SO": 23},
        "stats_2025": {"G": 143, "AVG": ".249", "OBP": ".289", "SLG": ".370", "OPS": ".659", "HR": 9, "RBI": 38, "SB": 7, "BB": 21, "SO": 122},
        "cover_stats": [("AVG 2026", ".181"), ("OPS 2026", ".562"), ("HR 2025", "9"), ("RBI 2025", "38"), ("SB 2025", "7"), ("Age", "26"), ("Debut", "2022"), ("Pos", "CF")],
        "season_chart_2025": [0.249, 0.289, 0.370, 0.659],
        "season_chart_2026": [0.181, 0.222, 0.340, 0.562],
        "season_chart_stats": ["AVG", "OBP", "SLG", "OPS"],
        "pitch_arsenal": [],
        "analysis": """
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">Elite 中外野防守</h3>
                <p>Thomas 是联盟中少数能真正镇守中外野的球员之一。他的 range、跳跃能力与接球稳定性都达到大联盟精英水准。无论打击如何，他的手套都能让他在大联盟名单中占有一席之地。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">打击是明显短板</h3>
                <p>2025 年 .289 上垒率与 2026 年 .222 上垒率都偏低。Thomas 的选球耐心不足，容易被诱导追打坏球。他的长打能力偶尔闪现（2025 年 9 轰），但不足以弥补上垒能力的欠缺。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">2026 年小样本警示</h3>
                <p>2026 年 28 场 .181/.222/.340 的数据样本有限，可能受转会适应与角色不确定性影响。道奇更看重他的防守与跑垒价值，而非短期打击数据。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">速度与跑垒</h3>
                <p>Thomas 具备 Above-average 速度，能在垒上制造威胁。2025 年 7 盗与 2026 年 4 盗显示他的跑垒侵略性。在道奇体系中，他可作为 late-inning pinch-runner 或 defensive replacement 使用。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">角色定位</h3>
                <p>在道奇，Thomas 最可能是第四/第五外野与防守替补。他不会撼动 Pages、Betts 或 Tucker 的地位，但当需要守下领先局数或面对强打阵容时，他的中外野防守极具价值。</p>
            </div>
        """,
        "pros": [
            "联盟顶级的精英中外野防守",
            "Above-average 速度与跑垒价值",
            "左打身份增加阵容平衡",
            "2023 年国联冠军队季后赛经验",
            "偶尔能贡献长打与关键安打",
            "年轻（26岁），仍有改善空间",
            "可作为 late-inning defensive replacement",
            "在道奇不需要承担核心进攻压力"
        ],
        "cons": [
            "上垒率偏低，选球耐心不足",
            "2026 年打击三围仅 .181/.222/.340",
            "三振率偏高，容易被三振",
            "长打输出不稳定",
            "在道奇外野竞争中处于劣势",
            "目前位于小联盟，大联盟机会不确定",
            "进攻天花板有限，难以成为 everyday player"
        ],
        "grades": [
            {"label": "Hitting", "value": 45, "grade": "C+"},
            {"label": "Power", "value": 50, "grade": "B-"},
            {"label": "Discipline", "value": 40, "grade": "C"},
            {"label": "Speed", "value": 60, "grade": "B+"},
            {"label": "Defense", "value": 75, "grade": "A+"},
            {"label": "Arm", "value": 55, "grade": "B"},
            {"label": "Clutch", "value": 55, "grade": "B"},
            {"label": "Baseball IQ", "value": 55, "grade": "B"}
        ],
        "overall_grade": 54,
        "overall_label": "B 级 / 精英防守型中外野手",
        "overall_desc": "防守是 Thomas 立足大联盟的根本，速度与季后赛经验是加分项。若能提升上垒率，他将成为更全面的中外野答案。",
        "future_outlook": """
            <div style="margin-top: 20px;">
                <p>Thomas 在道奇的未来取决于教练团如何定位他的角色。最可能的发展路径是作为防守替补与板凳深度，在季后赛中发挥守备价值。若能改善选球，他甚至有机会争夺更多先发机会。</p>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>提升选球与上垒：</strong>将 OBP 提升至 .300 以上，增加先发机会。</li>
                    <li><strong>减少三振：</strong>改进 two-strike approach，避免追打坏球。</li>
                    <li><strong>保持防守优势：</strong>继续作为 elite 中外野手存在，这是他的核心价值。</li>
                    <li><strong>善用跑垒：</strong>作为 pinch-runner 与 defensive replacement 增加球队价值。</li>
                </ol>

                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
                <p><strong>2026 下半季：</strong>争取上大联盟机会，主要作为外野防守替补与跑垒工具人。</p>
                <p><strong>2027：</strong>若防守稳定且 offense 略有回升，可能成为道奇第四外野。</p>
                <p><strong>2028+：</strong>防守型中外野手的角色可能延续至 30 岁初期，但需持续提升 offense 才能延长生涯。</p>

                <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3>
                <ul style="margin-left: 20px; line-height: 2;">
                    <li>进攻若无法改善，可能被更年轻或打击更好的外野手取代</li>
                    <li>伤病会影响赖以生存的防守与速度</li>
                    <li>在道奇竞争激烈的外野阵容中机会有限</li>
                </ul>
            </div>
        """,
        "background": """
            <div style="margin-top: 20px;">
                <p>Alek Thomas 出生于伊利诺伊州芝加哥，是一名来自城市棒球环境的外野手。他在高中时期展现五拍子潜力，尤其以速度、防守与左打长打闻名。2018 年他被亚利桑那响尾蛇在第 2 轮选中。</p>
                <p>在响尾蛇体系中，Thomas 快速攀升，2022 年完成大联盟首秀，并在 2023 年帮助球队闯入世界大赛。他的季后赛表现，包括关键守备与安打，让他在亚利桑那球迷心中留下深刻印象。</p>
                <p>2026 年 Thomas 加盟洛杉矶道奇，为这支卫冕冠军提供外野防守深度。尽管打击起伏，他的手套与速度仍使他在争冠球队中具备明确价值。场外他以职业态度与团队精神著称。</p>
            </div>
        """
    }
]


def main():
    print("=" * 70)
    print("Generating last 4 Dodgers scouting reports (customized)")
    print("=" * 70)
    for cfg in PLAYERS:
        print(f"\n[Generating] {cfg['name']} ...")
        gcr.PLAYER = cfg
        gcr.main()
    print("\n" + "=" * 70)
    print("All 4 reports completed!")
    print("=" * 70)


if __name__ == '__main__':
    main()
