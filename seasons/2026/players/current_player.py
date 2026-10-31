# current_player.py - Tommy Edman 配置
PLAYER = {
    "name": "Tommy Edman",
    "slug": "tommy-edman",
    "last_name": "edman",
    "number": "25",
    "position": "外野/内野工具人 (OF/IF Utility)",
    "position_code": "OF/IF",
    "bats_throws": "左右开弓 / 右投",
    "birth_date": "1995-05-09",
    "age": "31",
    "birthplace": "美国密歇根州庞蒂亚克 (Pontiac, MI)",
    "height_weight": "5'10\" / 193 lbs",
    "debut": "2019-06-08",
    "college": "Stanford",
    "nickname": "Eddie",
    "status": "活跃",
    "type": "batter",
    "summary": """
        <p style="margin-bottom: 15px;">Tommy Edman 是道奇阵容中最宝贵的<span class="highlight">多面手工具人</span>，能够出任二垒、游击、三垒、中外野和右外野。他以左右开弓的打击、出色的跑垒、 elite 防守和冠军级心理素质著称，是2024年国联冠军赛MVP。</p>
        <p style="margin-bottom: 15px;">2025年他虽然在常规赛打击表现下滑（.225/.274/.382），但仍贡献13支全垒打和49分打点，并在季后赛中多次建功，包括世界大赛第3战的关键防守。2026年因伤病导致样本较小，但目前在打击率上强势反弹至 .333/.410/.464。</p>
        <p>Edman 的价值无法用传统数据完全衡量。他的防守弹性、跑垒智慧和关键时刻的稳定发挥，使他成为道奇冠军阵容中不可或缺的 glue guy。</p>
    """,
    "career_highlights": """
        <div class="career-highlight">
            <h4>🎓 2016年 - 斯坦福 + 红雀第6轮选中</h4>
            <p>在 Stanford 大学三年入选 Pac-12 防守阵容和学术第一队。大三时领跑球队得分、安打、三垒打和盗垒。2016年选秀第6轮（总第196顺位）被圣路易红雀选中。</p>
        </div>
        <div class="career-highlight">
            <h4>🌟 2019年 - 大联盟首秀 + 新人王投票</h4>
            <p>2019年6月8日登上大联盟。首个完整赛季2020年因疫情缩短，但2021年已站稳脚跟，成为红雀主力工具人。曾多次在国联新人王和MVP投票中得票。</p>
        </div>
        <div class="career-highlight">
            <h4>🏆 2024年 - 交易至道奇 + 国联冠军赛MVP</h4>
            <p>7月29日经三方交易从红雀来到道奇。因手腕手术和脚踝问题缺席上半年，但9月复出后状态火热。国联冠军赛 slash .407/.393/.630，11支安打、11分打点，追平道奇单一季后赛系列赛队史纪录，获选NLCS MVP。</p>
        </div>
        <div class="career-highlight">
            <h4>💪 2025年 - 世界大赛冠军 + 关键守备</h4>
            <p>开季9场5轰，前30场8轰24打点。季中两次进入IL。世界大赛第3战18局大战中，完成一次不可思议的飞扑接球，从 Freddie Freeman 手套弹出的球中救出局面，并精准传三垒封杀跑者，成为冠军战的关键瞬间。</p>
        </div>
        <div class="career-highlight">
            <h4>🔥 2026年 - 强势反弹中</h4>
            <p>23场比赛、.333/.410/.464，显示健康状态下的打击能力。虽然目前仍在找回比赛节奏和完整出赛时间，但已经证明自己仍是高端多面手。</p>
        </div>
    """,
    "stats_2026": {
        "G": 23, "AVG": ".333", "OBP": ".410", "SLG": ".464", "OPS": ".874",
        "HR": 1, "RBI": 11, "SB": 2, "BB": 8, "SO": 16
    },
    "stats_2025": {
        "G": 97, "AVG": ".225", "OBP": ".274", "SLG": ".382", "OPS": ".656",
        "HR": 13, "RBI": 49, "SB": 3, "BB": 19, "SO": 61
    },
    "cover_stats": [
        ("AVG", ".333"), ("HR", "1"), ("RBI", "11"), ("SB", "2"),
        ("OPS", ".874"), ("2025 HR", "13"), ("Age", "31"), ("Career OPS", ".720")
    ],
    "season_chart_2025": [.225, .274, .382, .656],
    "season_chart_2026": [.333, .410, .464, .874],
    "season_chart_stats": ["AVG", "OBP", "SLG", "OPS"],
    "pitch_arsenal": [],
    "analysis": """
        <div style="margin-top: 20px;">
            <h3 style="color: #4fc3f7; margin-bottom: 15px;">多面防守价值</h3>
            <p>Edman 的防守弹性是他的核心价值。他能在二垒、三垒、游击和中外野之间无缝切换， glove work 和 range 都达到联盟优秀水准。他的 arm 适合内野和中外野，但不像一些外野重炮手那样强劲。他是道奇教练团在调配阵容时最重要的棋子。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">打击风格与2025年下滑</h3>
            <p>Edman 是 switch-hitter，以 contact 和 line drive 为主，不善于长打。2025年 OPS 仅 .656，主要因为选球耐心下降（BB/SO 比从生涯水准滑落）和 BABIP 偏低。但他仍能在开季打出火热状态，说明状态并非完全衰退。脚踝和手腕伤病可能影响了他的挥棒力量和节奏。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">2026年反弹讯号</h3>
            <p>2026年小样本下 .333/.410/.464，上垒率和选球明显回升。虽然长打能力尚未完全恢复，但他的接触和跑垒能力仍在。若健康稳定，他有望成为道奇阵中的 table setter 和防守救火员。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">跑垒与战术价值</h3>
            <p>Edman 生涯已经跑出117次盗垒，成功率优秀。他的速度让他能执行 hit-and-run、双盗垒和 scoring from first on doubles。在道奇强调 IQ 和 situational hitting 的打线中，他非常适合前几棒或第9棒角色。</p>
        </div>
    """,
    "pros": [
        "联盟顶级的多位置防守能力（2B/SS/3B/CF/RF）",
        "2024年 NLCS MVP，季后赛表现卓越",
        "左右开弓，打击弹性高",
        "生涯117次盗垒，跑垒智商优秀",
        "冠军级心理素质和关键时刻稳定发挥",
        "2026年反弹中，上垒率回升至 .410",
        "能上能下，可胜任 leadoff 或 bottom-of-order 工具人",
        "低 maintenance 的 clubhouse leader 型球员"
    ],
    "cons": [
        "2025年打击大幅衰退（.225/.274/.382）",
        "长打能力有限，生涯 SLG 仅 .427",
        "2025年选球耐心不足，BB/SO 比偏低",
        "伤病史较多（手腕、脚踝）影响出勤率",
        "2026年样本小，仍需验证反弹持续性",
        "面对左投时作为 switch-hitter 有时表现不稳定",
        "臂力不足以胜任强肩外野位置（如右外野长传）"
    ],
    "grades": [
        {"label": "Hitting", "value": 55, "grade": "B"},
        {"label": "Power", "value": 45, "grade": "C+"},
        {"label": "Discipline", "value": 50, "grade": "B-"},
        {"label": "Speed", "value": 65, "grade": "A-"},
        {"label": "Defense", "value": 70, "grade": "A"},
        {"label": "Arm", "value": 55, "grade": "B"},
        {"label": "Versatility", "value": 80, "grade": "A+"},
        {"label": "Baseball IQ", "value": 70, "grade": "A"}
    ],
    "overall_grade": 62,
    "overall_label": "A- 级 / 冠军级多面手",
    "overall_desc": "防守弹性、跑垒和季后赛表现是 Edman 的核心价值。只要保持健康，他是道奇夺冠阵容不可或缺的 glue player。",
    "future_outlook": """
        <div style="margin-top: 20px;">
            <p>Tommy Edman 的生涯正处于黄金后期，但他的价值不完全依赖身体素质。他的防守IQ和跑垒智慧会随着年龄增长而保持。在道奇，他将继续作为超级工具人，填补任何需要的防守位置，并在季后赛中提供经验。</p>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
            <ol style="margin-left: 20px; line-height: 2;">
                <li><strong>保持健康：</strong>避免脚踝和手腕伤病复发，争取单季120+出赛。</li>
                <li><strong>提升选球：</strong>恢复生涯平均 BB/SO 比，提高上垒率至 .320+。</li>
                <li><strong>稳定打击：</strong>目标单季 .250/.310/.400，并提供10-15轰和15-20盗垒。</li>
                <li><strong>继续发挥防守弹性：</strong>维持 multiple Gold Glove caliber 的防守表现。</li>
            </ol>

            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>
            <p><strong>2026（下半季）：</strong>若健康，打击率有望回到 .260-.270，OPS 接近 .730，出赛100-120场。</p>
            <p><strong>2027-2028：</strong>继续作为道奇主力工具人，年出赛120-130场，提供稳定防守和跑垒。</p>
            <p><strong>2029+：</strong>可能逐渐转为更专职的内野/外野替补角色，但经验和防守仍具价值。</p>

            <h3 style="color: #ff9800; margin: 20px 0 15px 0;">风险因素</h3>
            <ul style="margin-left: 20px; line-height: 2;">
                <li>脚踝和手腕伤病可能反复影响出勤</li>
                <li>打击能力随着年龄增长可能进一步下滑</li>
                <li>多位置使用增加了身体磨损和受伤风险</li>
            </ul>
        </div>
    """,
    "background": """
        <div style="margin-top: 20px;">
            <p>Thomas Hyunsu Edman 出生于美国密歇根州庞蒂亚克（Pontiac），父亲是 Williams College 的游击手、现任 La Jolla Country Day School 棒球队总教练 John Edman，母亲 Maureen 出生于韩国，小时候移居美国。Edman 具有韩国血统，这也让他成为亚洲球迷关注的焦点。</p>
            <p>他在圣地亚哥的 La Jolla Country Day School 高中毕业后，进入 Stanford 大学打了三年棒球。大三时入选 All-Pac-12 第一队、防守阵容和学术第一队，并在球队中领跑得分、安打、三垒打和盗垒。他也是近40年来 Stanford 棒球队 GPA 最高的球员之一。</p>
            <p>2016年，红雀在第6轮选中 Edman。他在2019年登上大联盟，迅速以 multi-position 能力和 energetic 球风赢得球迷喜爱。2024年他被交易至道奇，并在季后赛中大放异彩，成为国联冠军赛MVP。他与妻子 Kristen 育有一子一女，家庭观念浓厚，也是道奇更衣室中深受欢迎的队友。</p>
        </div>
    """
}
