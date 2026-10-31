# batch1_players.py - Miguel Rojas, Edgardo Henriquez, Alex Vesia, Enrique Hernández
PLAYERS = [
    {
        "name": "Miguel Rojas",
        "slug": "miguel-rojas",
        "last_name": "rojas",
        "number": "72",
        "position": "内野手 (SS/2B/3B)",
        "position_code": "IF",
        "bats_throws": "右打 / 右投",
        "birth_date": "1989-02-24",
        "age": "37",
        "birthplace": "委内瑞拉洛斯特克斯 (Los Teques, Venezuela)",
        "height_weight": "5'10\" / 188 lbs",
        "debut": "2014-06-06",
        "college": "",
        "nickname": "Miggy Ro",
        "status": "活跃",
        "type": "batter",
        "summary": """
            <p style="margin-bottom: 15px;">Miguel Rojas 是道奇阵容中经验最丰富的老将之一，也是球队的精神领袖。他以 elite 防守、稳定控场和关键时刻的大心脏著称，能在游击、二垒、三垒之间无缝切换。</p>
            <p style="margin-bottom: 15px;">2026年他已经37岁，但打击表现反而有所提升：65场比赛 .290/.335/.420，OPS .755，超过2025年的 .715。同时他仍然是道奇内野防守的定海神针，在 Mookie Betts 缺阵或轮休时经常担任关键位置。</p>
            <p>Rojas 的价值远超出数据。他是2024年 Roy Campanella Award 得主，象征着道奇最珍视的领导力和团队精神。2025年世界大赛第7战的致胜全垒打，更是他传奇生涯中的巅峰时刻。</p>
        """,
        "career_highlights": """
            <div class="career-highlight"><h4>🇻🇪 2014年 - 大联盟首秀</h4><p>2014年6月6日代表迈阿密马林鱼登上大联盟。早期以防守型内野手定位，逐步在辛辛那提和迈阿密体系成长。</p></div>
            <div class="career-highlight"><h4>🏅 2020-2021年 - 马林鱼主力游击手</h4><p>成为马林鱼首发游击手，以 .986 守备率和稳定守备著称。2021年击出生涯新高的 37 支二垒安打。</p></div>
            <div class="career-highlight"><h4>🔵 2023年 - 加盟道奇</h4><p>被交易至洛杉矶道奇，成为内野防守和 clubhouse 领袖。他的经验和防守弹性迅速赢得教练团信任。</p></div>
            <div class="career-highlight"><h4>🏆 2024年 - Roy Campanella Award</h4><p>被队友和教练票选为 Roy Campanella Award 得主，表彰最能体现道奇精神和领导力的球员。单季 WAR 3.4 创生涯新高。</p></div>
            <div class="career-highlight"><h4>💣 2025年 - 世界大赛第7战致胜轰</h4><p>在11月1日世界大赛第7战对多伦多蓝鸟的 387 英尺致胜全垒打，是他当年度第二轰对同侧投手，也是道奇夺冠的关键一击。</p></div>
        """,
        "stats_2026": {"G": 65, "AVG": ".290", "OBP": ".335", "SLG": ".420", "OPS": ".755", "HR": 3, "RBI": 17, "SB": 0, "BB": 10, "SO": 16},
        "stats_2025": {"G": 114, "AVG": ".262", "OBP": ".318", "SLG": ".397", "OPS": ".715", "HR": 7, "RBI": 27, "SB": 5, "BB": 24, "SO": 46},
        "cover_stats": [("AVG", ".290"), ("HR", "3"), ("RBI", "17"), ("OPS", ".755"), ("Age", "37"), ("2025 HR", "7"), ("Career", ".261"), ("WAR 2024", "3.4")],
        "season_chart_2025": [.262, .318, .397, .715],
        "season_chart_2026": [.290, .335, .420, .755],
        "season_chart_stats": ["AVG", "OBP", "SLG", "OPS"],
        "pitch_arsenal": [],
        "analysis": """
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">防守价值</h3><p>Rojas 的防守是他继续在大联盟立足的核心。他在游击位置的 range、 glove work 和传球稳定性都达到优秀水准，也能胜任二垒和三垒。他的防守 IQ 和站位选择是年轻内野手的学习对象。</p></div>
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">2026年打击回暖</h3><p>37岁老将的打击率从 .262 提升至 .290，OPS 从 .715 提升至 .755。这显示他依然能保持良好的接触能力和选球。虽然长打有限，但他的打击足以让他在阵容中占据位置。</p></div>
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">领导力和关键时刻</h3><p>Rojas 是道奇更衣室的 leader。他能在逆境中稳定军心，并在大场面下打出关键一击。2025年世界大赛第7战的全垒打是最佳例证。</p></div>
        """,
        "pros": ["精英级内野防守和多重位置能力", "37岁仍保持 .290 打击率", "2025年世界大赛第7战致胜轰", "2024年 Roy Campanella Award 得主", "丰富的季后赛和夺冠经验", " clubhouse 领袖和年轻球员的导师", "关键时刻心理素质极佳", "对左投表现出色（2025 OPS .879）"],
        "cons": ["年龄37岁，未来体能和守备范围可能下滑", "长打能力有限，生涯 SLG 仅 .378", "盗垒能力已大幅下降", "面对右投 OPS 偏低", "容易因小伤缺席", "不属于未来核心规划"],
        "grades": [
            {"label": "Hitting", "value": 50, "grade": "B-"},
            {"label": "Power", "value": 40, "grade": "C+"},
            {"label": "Discipline", "value": 50, "grade": "B-"},
            {"label": "Speed", "value": 35, "grade": "D+"},
            {"label": "Defense", "value": 70, "grade": "A"},
            {"label": "Arm", "value": 65, "grade": "A-"},
            {"label": "Versatility", "value": 65, "grade": "A-"},
            {"label": "Baseball IQ", "value": 75, "grade": "A+"}
        ],
        "overall_grade": 58,
        "overall_label": "B 级 / 冠军老将内野",
        "overall_desc": "防守和领导力的价值远超传统数据。他是道奇夺冠文化的传承者，关键时刻从不手软。",
        "future_outlook": """
            <div style="margin-top: 20px;"><p>Rojas 已进入生涯末期，但他仍有望在未来1-2年继续作为道奇内野替补和 clubhouse 领袖。他的防守和大赛经验使他非常适合季后赛阵容。</p>
            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
            <ol style="margin-left: 20px; line-height: 2;"><li><strong>保持健康和守备：</strong>目标年出赛80-100场，避免受伤。</li><li><strong>延续对左投优势：</strong>继续作为 platoon 或 pinch-hit 选项。</li><li><strong>传承领导力：</strong>指导年轻内野手如 Alex Freeland。</li></ol>
            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
            <p><strong>2026-2027：</strong>继续担任内野替补和防守救火员，年出赛80-100场。</p><p><strong>2028+：</strong>可能退役或转型教练/管理岗位。</p>
            <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3><ul style="margin-left: 20px; line-height: 2;"><li>年龄导致守备范围下滑</li><li>打击能力随着年龄进一步衰退</li><li>伤病风险增加</li></ul></div>
        """,
        "background": """
            <div style="margin-top: 20px;"><p>Miguel Elias Rojas Naidenoff 出生于委内瑞拉洛斯特克斯（Los Teques）。他是道奇阵中的委内瑞拉老将代表之一，与 Brusdar Graterol 等同乡球员共同组成了拉丁裔核心。</p>
            <p>Rojas 与妻子 Mariana 育有一子一女。他非常重视家庭，并以其幽默和 locker room 存在感深受队友喜爱。2017年他曾与 Martín Prado 等人一起赢得马林鱼更衣室 fantasy football 联盟冠军。</p>
            <p>2022年他将背号从19改为11，以纪念去世的祖父——正是祖父在委内瑞拉点燃了他对棒球的热爱。2025年他又将11号让给 Roki Sasaki，自己改穿72号，展现了对年轻队友的无私支持。</p></div>
        """
    },
    {
        "name": "Edgardo Henriquez",
        "slug": "edgardo-henriquez",
        "last_name": "henriquez",
        "number": "60",
        "position": "右投后援 (RHP)",
        "position_code": "P",
        "bats_throws": "右打 / 右投",
        "birth_date": "2002-06-24",
        "age": "24",
        "birthplace": "委内瑞拉库马纳 (Cumana, Venezuela)",
        "height_weight": "6'4\" / 200 lbs",
        "debut": "2024-09-24",
        "college": "",
        "nickname": "Edgardo",
        "status": "活跃",
        "type": "pitcher",
        "summary": """
            <p style="margin-bottom: 15px;">Edgardo Henriquez 是道奇牛棚中年轻且具有爆发力的火球右投。2024年9月24日完成大联盟首秀，2025年克服左脚骨折从 IL 复出，在世界大赛第3战18局大战中投出2局无失分救援，2026年已成为道奇最可靠的 setup man 之一。</p>
            <p style="margin-bottom: 15px;">2026年他37场出赛、ERA 2.29、WHIP 0.94、K/9 8.47，并成功吞下39.1局。对于一个24岁的年轻后援来说，这样的稳定性非常难得。他的球速和变化球组合让他在 future closer 的讨论中占有一席之地。</p>
            <p>Henriquez 的成长轨迹是道奇培养年轻投手的典范：从 Tommy John 手术复出，到快速穿越四个小联盟层级，再到世界大赛建功，他的未来值得期待。</p>
        """,
        "career_highlights": """
            <div class="career-highlight"><h4>🔥 2021年 - 道奇签约</h4><p>作为国际自由球员签约，进入道奇农场。他在 ACL 展现出潜力，但随后面临 Tommy John 手术的重大挑战。</p></div>
            <div class="career-highlight"><h4>🏥 2022-2023年 - Tommy John 复健</h4><p>2022年8月19日进入60天IL，随后接受 Tommy John 手术，2023年整季缺席。这段经历磨练了他的耐心和心理素质。</p></div>
            <div class="career-highlight"><h4>🚀 2024年 - 四级跳 + 大联盟首秀</h4><p>单季跨越四个小联盟层级，合计43场2.72 ERA、88 K。9月24日完成大联盟首秀，并在季后赛中出赛，展现大将之风。</p></div>
            <div class="career-highlight"><h4>🏆 2025年 - 世界大赛冠军</h4><p>开季因左脚骨折从 IL 开始，7月22日完成赛季首秀。世界大赛第3战对多伦多蓝鸟投出13、14局2局无失分救援，成为18局大战的隐藏英雄。</p></div>
            <div class="career-highlight"><h4>🌟 2026年 - 牛棚中坚</h4><p>37场、ERA 2.29、WHIP 0.94、1次救援成功、6次 hold。他已经从潜力新秀成长为道奇牛棚中不可或缺的一员。</p></div>
        """,
        "stats_2026": {"G": 37, "GS": 0, "W": 4, "L": 1, "ERA": "2.29", "IP": "39.1", "K": 37, "BB": 15, "WHIP": "0.94", "K/9": "8.47", "BB/9": "3.43", "HR": 1, "SV": 1, "HLD": 6},
        "stats_2025": {"G": 22, "GS": 0, "W": 2, "L": 1, "ERA": "2.37", "IP": "19.0", "K": 18, "BB": 5, "WHIP": "1.16", "K/9": "8.53", "BB/9": "2.37", "HR": 2, "SV": 1, "HLD": 5},
        "cover_stats": [("ERA", "2.29"), ("W-L", "4-1"), ("K", "37"), ("IP", "39.1"), ("WHIP", "0.94"), ("K/9", "8.47"), ("Age", "24"), ("HLD", "6")],
        "season_chart_2025": [2.37, 1.16, 8.53, 2.37],
        "season_chart_2026": [2.29, 0.94, 8.47, 3.43],
        "season_chart_stats": ["ERA", "WHIP", "K/9", "BB/9"],
        "pitch_arsenal": [
            {"name": "四缝快速球 (Four-Seam Fastball)", "velocity": "97-101 mph", "avg": "99.0", "desc": "Henriquez 的招牌武器。球速 elite，出手角度陡峭，能在好球带上方制造挥空。这是他能成为 future closer 的最大本钱。"},
            {"name": "滑球 (Slider)", "velocity": "85-88 mph", "avg": "86.5", "desc": "主要出局球，具有 late break。与快速球的速度差和横向位移让他在两好球后极具威胁。"},
            {"name": "变速球 (Changeup)", "velocity": "86-89 mph", "avg": "87.5", "desc": "对付左打者的关键变化球。使用频率较低，但能打乱打者的节奏和 timing。"}
        ],
        "analysis": """
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">火球与球路组合</h3><p>Henriquez 的四缝线快速球均速接近三位数，配上 sharp slider，已经是标准后援王牌配置。他的 changeup 还在发展中，若能提升到平均水平，他将更难被针对。</p></div>
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">2026年稳定成长</h3><p>从2025年19局小样本到2026年39.1局，Henriquez 不仅保持了 ERA 和 WHIP，还承担了更多重要局数。他的 hold 数（6次）和胜场（4次）显示教练团 increasingly trust him in high-leverage。</p></div>
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">健康与伤病史</h3><p>Tommy John 手术和2025年左脚骨折是他需要克服的阴影。2026年能稳定出赛37场是积极讯号，但道奇仍需监控他的工作量和恢复。</p></div>
        """,
        "pros": ["球速 elite，四缝线接近 100 mph", "滑球是可靠的出局武器", "2025年世界大赛已证明抗压能力", "24岁，未来成长空间大", "2026年 ERA 2.29、WHIP 0.94 稳定性佳", "左打右打都能应付的球路组合", "从 Tommy John 手术成功复出", "道奇牛棚未来 closer 候选人"],
        "cons": ["保送率 3.43 略高于理想值", "变化球（变速球）仍在发展中", "小联盟样本和 Tommy John 病史", "连续出赛时控球可能波动", "尚未长期承担 setup/closer 重任", "面对 elite 打者的三振率还有提升空间"],
        "grades": [
            {"label": "Fastball", "value": 75, "grade": "A+"},
            {"label": "Slider", "value": 65, "grade": "A-"},
            {"label": "Changeup", "value": 50, "grade": "B-"},
            {"label": "Control", "value": 55, "grade": "B"},
            {"label": "Command", "value": 55, "grade": "B"},
            {"label": "Mental", "value": 60, "grade": "B+"},
            {"label": "Stamina", "value": 55, "grade": "B"},
            {"label": "Durability", "value": 50, "grade": "B-"}
        ],
        "overall_grade": 62,
        "overall_label": "A- 级 / 未来 closer 候选人",
        "overall_desc": "火球右投，已证明自己能在世界大赛和常规赛中稳定贡献。若健康和控球持续进步，有望成为道奇未来终结者。",
        "future_outlook": """
            <div style="margin-top: 20px;"><p>Henriquez 的未来非常光明。24岁的他已经在大舞台证明过自己，球速和滑球都达到 elite 水准。他的发展将决定他能否从 setup man 晋升为 closer。</p>
            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
            <ol style="margin-left: 20px; line-height: 2;"><li><strong>提升控球：</strong>将 BB/9 压到 3.0 以下，增加 first-pitch strike。</li><li><strong>发展变速球：</strong>增加面对左打时的武器选择。</li><li><strong>增加局数：</strong>目标年出赛 60-65 场，吃下 60+ 局。</li><li><strong>健康管理：</strong>避免过度使用，防止手肘复发。</li></ol>
            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
            <p><strong>2026-2027：</strong>继续担任 setup man，ERA 2.20-2.80，年出赛 60 场。</p><p><strong>2028+：</strong>若发展顺利，可能接任道奇 closer 角色。</p>
            <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3><ul style="margin-left: 20px; line-height: 2;"><li>Tommy John 复发风险</li><li>控球不稳导致高保送</li><li>变化球未发展时容易被 elite 左打针对</li></ul></div>
        """,
        "background": """
            <div style="margin-top: 20px;"><p>Edgardo Luis Henriquez 出生于委内瑞拉库马纳（Cumana）。他是道奇众多委内瑞拉球员之一，与 Miguel Rojas、Brusdar Graterol 等同乡球员并肩作战。</p>
            <p>他在2021年以国际自由球员身份加入道奇，但随后遭遇 Tommy John 手术，2023年整季缺席。2024年他以惊人的速度康复并跨越四个小联盟层级，最终在9月24日登上大联盟。</p>
            <p>Henriquez 以沉稳和专注著称。尽管年纪轻轻，他已经在世界大赛第3战这种史诗级比赛中挺身而出，展现了超越年龄的心理素质。</p></div>
        """
    },
    {
        "name": "Alex Vesia",
        "slug": "alex-vesia",
        "last_name": "vesia",
        "number": "51",
        "position": "左投后援 (LHP)",
        "position_code": "P",
        "bats_throws": "左打 / 左投",
        "birth_date": "1996-04-11",
        "age": "30",
        "birthplace": "美国加州阿尔派恩 (Alpine, CA)",
        "height_weight": "6'1\" / 209 lbs",
        "debut": "2020-07-25",
        "college": "Cal State East Bay",
        "nickname": "Vesia",
        "status": "活跃",
        "type": "pitcher",
        "summary": """
            <p style="margin-bottom: 15px;">Alex Vesia 是道奇牛棚中稳定且多才多艺的左投后援。2024年他以 1.76 ERA 缔造生涯年，2025年则成为球队 hold 王（26次），2026年继续提供 elite 的三振能力（K/9 12.79）和稳定出局。</p>
            <p style="margin-bottom: 15px;">Vesia 的球风以高侧投、快速球上飘和锐利滑球为主。他能在第6到第8局承担 setup 任务，也能在紧急情况下救援。他的职业生涯 ERA 仅 2.85，显示他已经从早期起伏成长为可靠的中继核心。</p>
            <p>作为一名30岁的成熟后援，Vesia 是道奇争冠路上不可或缺的 lefty specialist 和 setup man。他的经验和三振能力让他在季后赛中极具价值。</p>
        """,
        "career_highlights": """
            <div class="career-highlight"><h4>🎓 2018年 - 马林鱼第17轮选中</h4><p>来自 Cal State East Bay，2018年选秀第17轮（总第507顺位）被迈阿密马林鱼选中。低顺位起步，但凭借出色表现快速上升。</p></div>
            <div class="career-highlight"><h4>🌟 2020年 - 大联盟首秀</h4><p>2020年7月25日代表马林鱼登上大联盟。早期成绩起伏，但展现了左投后援的潜力。</p></div>
            <div class="career-highlight"><h4>🔵 2021年 - 交易至道奇</h4><p>被交易至洛杉矶道奇，开始在新体系中成长。他的控球和球路组合在道奇教练团指导下逐步成熟。</p></div>
            <div class="career-highlight"><h4>💪 2024年 - 生涯年</h4><p>1.76 ERA、.148 被打击率、0.99 WHIP，缔造多项生涯新高。世界大赛第2战仅用1球完成救援，创造历史。</p></div>
            <div class="career-highlight"><h4>🏆 2025年 - 道奇 hold 王</h4><p>68场出赛、26次 hold、3.02 ERA。成为道奇最信赖的中继左投，季后赛中也有关键表现。</p></div>
        """,
        "stats_2026": {"G": 42, "GS": 0, "W": 1, "L": 1, "ERA": "2.27", "IP": "31.2", "K": 45, "BB": 20, "WHIP": "1.14", "K/9": "12.79", "BB/9": "5.68", "HR": 0, "SV": 3, "HLD": 15},
        "stats_2025": {"G": 68, "GS": 0, "W": 4, "L": 2, "ERA": "3.02", "IP": "59.2", "K": 80, "BB": 22, "WHIP": "0.99", "K/9": "12.07", "BB/9": "3.32", "HR": 9, "SV": 5, "HLD": 26},
        "cover_stats": [("ERA", "2.27"), ("HLD", "15"), ("K", "45"), ("IP", "31.2"), ("WHIP", "1.14"), ("K/9", "12.79"), ("Age", "30"), ("2025 HLD", "26")],
        "season_chart_2025": [3.02, 0.99, 12.07, 3.32],
        "season_chart_2026": [2.27, 1.14, 12.79, 5.68],
        "season_chart_stats": ["ERA", "WHIP", "K/9", "BB/9"],
        "pitch_arsenal": [
            {"name": "四缝快速球 (Four-Seam Fastball)", "velocity": "92-95 mph", "avg": "93.5", "desc": "Vesia 的压制核心。出手点高，具有 good ride，能在好球带上角制造大量挥空。他善于利用快速球抢 strike。"},
            {"name": "滑球 (Slider)", "velocity": "80-83 mph", "avg": "81.5", "desc": "主要出局球，sharp lateral break。对付左打者内角和右打者外角都很有效。是他 K/9 高企的关键。"},
            {"name": "变速球 (Changeup)", "velocity": "84-87 mph", "avg": "85.5", "desc": "偶尔用来对付右打者，制造速度差。使用频率较低，但能增加配球变化。"}
        ],
        "analysis": """
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">左投后援王牌</h3><p>Vesia 是道奇最值得信赖的左投 setup man。他的快速球上飘和 slider 的 combo 让他在面对左右打者时都有三振能力。2024年 .148 被打击率证明了他的压制力。</p></div>
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">2026年三振能力更上层楼</h3><p>K/9 从12.07提升至12.79，ERA 降至2.27。虽然 WHIP 因保送增加而上升到1.14，但他的三振能力让他在 high-leverage 中仍然可靠。若能减少保送，ERA 有望逼近2.00。</p></div>
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">2025年 hold 王的价值</h3><p>26次 hold 显示教练团在领先时 frequently go to him。他能在第6-8局稳定局势，是世界大赛夺冠的重要拼图。</p></div>
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">伤病与稳定性</h3><p>2025年8月曾因右斜肌拉伤进入 IL，但复出后迅速找回状态。2026年目前42场出赛，显示健康状况良好。</p></div>
        """,
        "pros": ["K/9 12.79，三振能力 elite", "2025年道奇 hold 王（26次）", "左投身份在牛棚中极具战术价值", "2024年生涯年 1.76 ERA", "能快速从伤病中恢复", "面对左右打者都有三振能力", "季后赛经验丰富，2024年世界第一球救援", "道奇牛棚稳定核心"],
        "cons": ["2026年 BB/9 5.68，保送率偏高", "WHIP 从0.99升至1.14", "身材和球速限制了 ceiling", "连续出赛时控球可能不稳", "不属于传统 fireball closer", "面对强打阵容时 occasionally 被长打"],
        "grades": [
            {"label": "Fastball", "value": 60, "grade": "B+"},
            {"label": "Slider", "value": 65, "grade": "A-"},
            {"label": "Changeup", "value": 50, "grade": "B-"},
            {"label": "Control", "value": 55, "grade": "B"},
            {"label": "Command", "value": 55, "grade": "B"},
            {"label": "Mental", "value": 65, "grade": "A-"},
            {"label": "Stamina", "value": 60, "grade": "B+"},
            {"label": "Durability", "value": 55, "grade": "B"}
        ],
        "overall_grade": 60,
        "overall_label": "B+ 级 / 精英左投 setup man",
        "overall_desc": "三振能力 elite，经验丰富。若减少保送，将成为联盟顶级左投后援。",
        "future_outlook": """
            <div style="margin-top: 20px;"><p>Vesia 正处于后援投手的黄金期。他的球路组合和大赛经验让他在未来2-3年仍将是道奇牛棚的核心。改善控球是他迈向 elite closer 的关键。</p>
            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
            <ol style="margin-left: 20px; line-height: 2;"><li><strong>降低保送率：</strong>将 BB/9 压回 3.5 以下。</li><li><strong>保持三振优势：</strong>继续利用 slider 和 fastball ride 制造挥空。</li><li><strong>增加局数弹性：</strong>能在多局数 situation 中稳定出局。</li><li><strong>健康管理：</strong>避免斜肌和肩部伤病复发。</li></ol>
            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
            <p><strong>2026-2027：</strong>继续担任 setup man，ERA 2.20-3.00，年出赛 65-70 场。</p><p><strong>2028+：</strong>若控球进步，可能转型为终结者或 lefty specialist 王牌。</p>
            <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3><ul style="margin-left: 20px; line-height: 2;"><li>保送率过高导致上垒</li><li>斜肌伤病复发</li><li>面对 elite 右打时 fastball 压制力有限</li></ul></div>
        """,
        "background": """
            <div style="margin-top: 20px;"><p>Alexander Victor Vesia 出生于加州圣地亚哥郡的 Alpine。他在 Cal State East Bay 大学就读，主修休闲管理，并曾在2019年亚利桑那秋季联盟后，在圣地亚哥州立大学橄榄球招募办公室实习。</p>
            <p>2018年马林鱼在第17轮选中他，2020年登上大联盟。2021年被交易至道奇后，他在教练团指导下逐步成长为联盟最可靠的左投后援之一。2024年1月，他与妻子 Kayla 结婚。</p>
            <p>Vesia 以勤奋和低调著称。他从低顺位新秀到世界冠军牛棚核心，是道奇球探和培养体系的又一成功案例。</p></div>
        """
    },
    {
        "name": "Enrique Hernández",
        "slug": "enrique-hernandez",
        "last_name": "hernandez",
        "number": "8",
        "position": "多面手工具人 (IF/OF)",
        "position_code": "IF/OF",
        "bats_throws": "右打 / 右投",
        "birth_date": "1991-08-24",
        "age": "34",
        "birthplace": "波多黎各圣胡安 (San Juan, Puerto Rico)",
        "height_weight": "5'10\" / 195 lbs",
        "debut": "2014-07-01",
        "college": "",
        "nickname": "Kiké",
        "status": "IL-10 / 小联盟复健中",
        "type": "batter",
        "summary": """
            <p style="margin-bottom: 15px;">Enrique "Kiké" Hernández 是道奇球迷最喜爱的多面手工具人之一。他能在内野和外野多个位置出赛，偶尔还能上丘投球，是球队最具娱乐性和战术价值的球员之一。</p>
            <p style="margin-bottom: 15px;">2025年他展现了惊人的多功能性：他是现代大联盟唯一一位在单场比赛中没有先发的状态下，同时得分多次、守多个位置并投出无失分局数的球员（4月29日对马林鱼）。他甚至在2025年5月31日成为大联盟唯二至少10轰且至少4次登板的球员（另一位是 Shohei Ohtani）。</p>
            <p>2026年目前他因左肘发炎在 IL-10/小联盟复健中，样本极小。但他在2025年季后赛中的关键表现，包括世界大赛第3战的多次安打，证明他仍是道奇争冠的重要拼图。</p>
        """,
        "career_highlights": """
            <div class="career-highlight"><h4>🎓 2009年 - 太空人第6轮选中</h4><p>来自波多黎各 American Military Academy，2009年选秀第6轮（总第191顺位）被休士顿太空人选中。同年获选湾岸联盟太空人队 MVP。</p></div>
            <div class="career-highlight"><h4>🌟 2014年 - 大联盟首秀</h4><p>2014年7月1日登上大联盟。早期在太空人、马林鱼和道奇之间辗转，逐步确立多面手角色。</p></div>
            <div class="career-highlight"><h4>🍌 2015年 - Rally Banana 诞生</h4><p>因在道奇更衣室穿香蕉装为球队打气而被称为 "Rally Banana"，成为球迷宠儿。他的幽默和能量为球队注入活力。</p></div>
            <div class="career-highlight"><h4>🏆 2020年 / 2024年 / 2025年 - 三届世界冠军</h4><p>作为道奇重要角色球员，参与了2020、2024和2025年的世界冠军。他在多个季后赛系列赛中贡献关键安打和防守。</p></div>
            <div class="career-highlight"><h4>🎭 2016年 - 客串肥皂剧</h4><p>曾在《The Bold and the Beautiful》中客串演出自己，展现了他的明星魅力。</p></div>
        """,
        "stats_2026": {"G": 2, "AVG": "1.000", "OBP": "1.000", "SLG": "2.250", "OPS": "3.250", "HR": 1, "RBI": 2, "SB": 0, "BB": 0, "SO": 0},
        "stats_2025": {"G": 93, "AVG": ".203", "OBP": ".255", "SLG": ".366", "OPS": ".621", "HR": 10, "RBI": 35, "SB": 0, "BB": 18, "SO": 68},
        "cover_stats": [("AVG", "1.000"), ("HR", "1"), ("RBI", "2"), ("OPS", "3.250"), ("Age", "34"), ("2025 HR", "10"), ("Career HR", "131"), ("Pos", "多面手")],
        "season_chart_2025": [.203, .255, .366, .621],
        "season_chart_2026": [1.000, 1.000, 2.250, 3.250],
        "season_chart_stats": ["AVG", "OBP", "SLG", "OPS"],
        "pitch_arsenal": [],
        "analysis": """
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">多面手价值</h3><p>Hernández 能在二垒、三垒、游击、外野甚至投手丘上出现。他的防守虽不 elite，但足以应付各种紧急情况。他是道奇阵容中的「万能胶」，让教练团在调度上拥有极大弹性。</p></div>
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">2025年打击低谷</h3><p>.203/.255/.366 的 OPS 仅 .621，是他近年最低迷的进攻赛季。但他的长打和关键安打仍具价值，尤其是面对左投时偶尔能爆发。</p></div>
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">投手丘上的惊喜</h3><p>2025年5次登板，虽然 ERA 15.19 不佳，但他能在比赛中吞局数，避免牛棚过度消耗。他与 Ohtani 成为唯二10轰+4登板的球员，展现了他独特的多功能性。</p></div>
            <div style="margin-top: 20px;"><h3 style="color: #4fc3f7; margin-bottom: 15px;">2026年伤病</h3><p>左肘发炎让他在2026年目前只出赛2场。道奇需要他在健康后回归，提供板凳深度和季后赛经验。</p></div>
        """,
        "pros": ["多位置防守弹性（内野 + 外野）", "能偶尔上丘投球，战术价值独特", "三届世界冠军成员，季后赛经验丰富", "关键时刻常有惊人之举", "球迷人气高，更衣室气氛带动者", "2025年10轰+4登板，历史级多功能性", "面对左投时偶尔能爆发长打", "低成本、高价值的板凳深度"],
        "cons": ["2025年打击 .203/.255/.366 大幅衰退", "防守不 elite，无法长期担任单一位置主力", "2026年左肘伤病影响出勤", "三振率偏高，选球耐心不足", "投球能力有限，仅应急使用", "34岁，运动能力下滑", "2026年样本极小，状态未知"],
        "grades": [
            {"label": "Hitting", "value": 45, "grade": "C+"},
            {"label": "Power", "value": 50, "grade": "B-"},
            {"label": "Discipline", "value": 40, "grade": "C+"},
            {"label": "Speed", "value": 45, "grade": "C+"},
            {"label": "Defense", "value": 55, "grade": "B"},
            {"label": "Arm", "value": 50, "grade": "B-"},
            {"label": "Versatility", "value": 75, "grade": "A+"},
            {"label": "Baseball IQ", "value": 65, "grade": "A-"}
        ],
        "overall_grade": 55,
        "overall_label": "B 级 / 冠军级多面手",
        "overall_desc": "虽然打击衰退，但他的多功能性、经验和更衣室价值使他仍是道奇不可或缺的板凳球员。健康回归是关键。",
        "future_outlook": """
            <div style="margin-top: 20px;"><p>Hernández 的生涯已进入后期，但他的角色定位清晰：板凳多面手、气氛带动者和季后赛经验来源。只要保持健康，他仍能在道奇发挥价值。</p>
            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
            <ol style="margin-left: 20px; line-height: 2;"><li><strong>健康回归：</strong>从左肘发炎中完全恢复，避免复发。</li><li><strong>提升打击：</strong>目标回到 .230/.290/.400 水平。</li><li><strong>保持多功能性：</strong>继续作为内野/外野救火员。</li><li><strong>控制投球使用：</strong>避免过度登板造成手臂负担。</li></ol>
            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
            <p><strong>2026-2027：</strong>若健康，年出赛 80-100 场，作为多面手替补。</p><p><strong>2028+：</strong>可能退役或转型教练/评论员。</p>
            <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3><ul style="margin-left: 20px; line-height: 2;"><li>左肘伤病可能复发</li><li>打击能力持续衰退</li><li>年龄增加导致守备范围下降</li></ul></div>
        """,
        "background": """
            <div style="margin-top: 20px;"><p>Enrique J. Hernández 出生于波多黎各圣胡安（San Juan），绰号 "Kiké"（发音 KEE-kay）。他的父亲 Enrique 曾是海盗队和洛矶队的球探。他在 American Military Academy 高中毕业，2009年被太空人选中。</p>
            <p>2012年8月，一场在 Whataburger Field 的比赛中因停电，他跳起了 Bee Gees 的 "Night Fever" 娱乐观众，展现了他的娱乐天性。2015年他开始在道奇更衣室穿香蕉装，被称为 "Rally Banana"，成为球队吉祥物般的存在。</p>
            <p>Hernández 与妻子 Mariana 育有两个孩子。他在2022年前是道奇最后一位穿14号的球员，该号码随后为 Gil Hodges 退役。他在2023年短暂效力波士顿红袜后，被交易回道奇，并帮助球队在2024和2025年夺冠。</p></div>
        """
    }
]
