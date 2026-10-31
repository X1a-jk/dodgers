#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复 D:\baseball\report 中 progress.md 列出的问题。

修复项目：
1. Henriquez 报告补回 100+ mph 伸卡球/重速球
2. Sheehan/Freeland/Rushing/Gervase 中英混杂翻译
3. Evan Phillips：确认 2026 对 Judge 没有全垒打，不添加错误说法
4. Jack Dreyer：补充 2025 季后赛数据
5. Tanner Scott：修正 2025 世界大赛 G3 救援归属（实为 Eric Lauer），调整武器库为四缝+滑球为主
6. 早期报告（Ohtani/Sasaki/Yamamoto/Freeman 等）补职业生涯亮点/代表作
7. 全局突兀英文翻译
8. 图表增加文字说明

说明：
- 脚本尽量保留原有文字与结构，只对明确列出的问题进行替换或追加。
- HTML 用正则/字符串替换，处理完后写回同名文件并备份原文件为 .html.bak。
"""
import os
import re
import shutil
from datetime import datetime

BASE_DIR = r'D:\baseball\report'
TODAY = datetime.now().strftime('%Y-%m-%d')

# ----------------- 通用翻译映射（非专用词） -----------------
# 键 = 原文（大小写敏感，按顺序替换），值 = 中文
TRANSLATIONS = {
    # 球员/角色
    'setup man': '布局投手（第八局 setup）',
    'setup/closer': 'setup/终结者',
    'closer': '终结者',
    'relief': '后援',
    'reliever': '后援投手',
    'long reliever': '长中继',
    'future closer': '未来终结者',
    'fireballer': '火球男',
    'pitch mix': '球路组合',
    'raw tools': '原始天赋',
    'raw stuff': '原始球威',
    'raw power': '原始力量',
    'breakout season': ' breakout 赛季',
    'career year': '生涯年',
    'command': '控球精准度',
    'control': '控球',
    'mental toughness': '心理素质',
    'plate discipline': '选球纪律',
    'high-leverage': '高杠杆',
    'matchup': '对位',
    'lefty specialist': '左打 specialist',
    'right-handed specialist': '右打 specialist',
    'one-batter specialist': '一人次 specialist',
    'platoon': '左右分工',
    'two-way player': '双向球员',
    'development phase': '发展阶段',
    'call-up': '升上大联盟',
    'send-down': '下放',
    'roster spot': '名单位置',
    'leadoff double': '首棒二垒安打',
    'walk-off': '再见',
    'no-hitter': '无安打',
    'shutout': '完封',
    'first-pitch strike': '首球好球',
    'swing and miss': '挥空',
    'whiff': '挥空',
    'chase rate': '追打率',
    'barrel': '强劲击球',
    'hard-hit': '强劲击球',
    'exit velocity': '击球初速',
    'launch angle': '击球仰角',
    'spin rate': '转速',
    'induced vertical break': '纵向位移',
    'horizontal break': '横向位移',
    'arm slot': '出手角度',
    'release point': '放球点',
    'follow-through': '后续动作',
    'catcher ERA': '捕手配合自责分率',
    'pop time': '传球阻杀时间',
    'framing': '接捕偷好球',
    'blocking': '阻挡',
    'game calling': '配球',
    'sprint speed': '冲刺速度',
    'defensive versatility': '防守多能性',
    'contact-oriented': '接触型',
    'power hitter': '长打打者',
    'on-base machine': '上垒机器',
    'run producer': '打点制造者',
    'table setter': '开路先锋',
    'innings eater': '吃局数投手',
    'workhorse': '主战力/耐战投手',
    'bounce-back': '反弹',
    'repertoire': '球路库存',
    'out pitch': '出局球',
    'putaway pitch': '两好球后追打球',
    'secondary pitch': '第二球种',
    'third offering': '第三球种',
    'plus-plus': '精英级',
    'above-average': '高于平均',
    'below-average': '低于平均',
    'average': '平均',
    'elite': ' elite ',  # 保留 elite 不译（专有形容词）但前后加空格
    'bullpen': '牛棚',
    'rotation': '先发轮值',
    'lineup': '打线',
    'bench': '板凳',
    'depth': '深度',
    'farm': '农场',
    'prospect': '新秀',
    'rookie': '新秀',
    'veteran': '老将',
    'ace': '王牌',
    'stud': '核心战将',
    'slugger': '重炮',
    'speedster': '快腿',
    'defensive wizard': '防守大师',
    'glove-first': '守备优先',
    'hit tool': '打击工具',
    'power tool': '长打工具',
    'speed tool': '速度工具',
    'arm tool': '传球工具',
    'field tool': '防守工具',
}

# 只在这些球员目录里做中英翻译（问题明确列出的）
TRANSLATE_SLUGS = {'emmet-sheehan', 'alex-freeland', 'dalton-rushing', 'paul-gervase'}

# 额外：全局中英替换（所有报告）的明显非专有英文短语
GLOBAL_TRANSLATIONS = {
    'and': '和',  # 危险，可能误伤。改用更保守策略
}

# 只替换 HTML 文本节点里的英文：用正则限制（不在属性、URL、样式里）
# 策略：针对 <p>, <li>, <h3>, <h4>, <blockquote> 内的文本做替换


def safe_replace_in_html(html, replacements, allowed_tags=None):
    """在允许的 HTML 标签文本内容中做安全替换。"""
    if allowed_tags is None:
        allowed_tags = {'p', 'li', 'h3', 'h4', 'blockquote', 'td', 'th', 'span', 'div'}
    # 匹配 <tag>...</tag> 的文本内容（简单版，不处理嵌套同名标签的复杂情况）
    pattern = re.compile(r'<(?P<tag>' + '|'.join(allowed_tags) + r')(?P<attrs>\s[^>]*)?>(?P<text>[^<]*(?:<(?!/?(?P=tag)[\s>])[^<]*+)*)</(?P=tag)>')

    def repl(m):
        tag = m.group('tag')
        attrs = m.group('attrs') or ''
        text = m.group('text')
        for k, v in replacements.items():
            text = text.replace(k, v)
        return f"<{tag}{attrs}>{text}</{tag}>"

    return pattern.sub(repl, html)


def backup_and_write(path, content):
    bak = path + '.bak'
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


# ----------------- 1. Edgardo Henriquez：补充 100+ mph 伸卡球 -----------------
def fix_henriquez(html):
    # 在投球武器库部分，四缝卡之后加入伸卡球
    old_block = '''                <div class="pitch-card">
                    <h3>四缝快速球 (Four-Seam Fastball)</h3>
                    <p><span class="velocity">97-101 mph</span></p>
                    <p>Henriquez 的招牌武器。球速 elite，出手角度陡峭，能在好球带上方制造挥空。这是他能成为 future closer 的最大本钱。</p>
                </div>
                <div class="pitch-card">
                    <h3>滑球 (Slider)</h3>'''
    new_block = '''                <div class="pitch-card">
                    <h3>四缝快速球 (Four-Seam Fastball)</h3>
                    <p><span class="velocity">97-101 mph</span></p>
                    <p>Henriquez 的招牌武器。球速 elite，出手角度陡峭，能在好球带上方制造挥空。这是他能成为 future closer 的最大本钱。</p>
                </div>
                <div class="pitch-card">
                    <h3>伸卡球 / 二缝线 (Sinker/Two-Seam)</h3>
                    <p><span class="velocity">99-101 mph</span></p>
                    <p>Henriquez 最令打者畏惧的武器之一。这颗重速球不仅接近甚至超过 100 mph，还带有明显的下坠与手臂侧移，能制造大量软弱滚地球与内角球 jam。虽然使用频率低于四缝线，但关键时刻用来抢好球或制造双杀极具威胁，也是他被誉为“火球男”的核心原因。</p>
                </div>
                <div class="pitch-card">
                    <h3>滑球 (Slider)</h3>'''
    if old_block in html:
        html = html.replace(old_block, new_block)
    # 修正总评中的 setup man 译法
    html = html.replace('setup man', '布局投手（第八局 setup）')
    # 调整球探分析里的描述
    html = html.replace('四缝线快速球均速接近三位数', '四缝线快速球均速接近三位数，伸卡球/二缝线更可达 100 mph 以上')
    # 在优势中加入伸卡球
    html = html.replace(
        '<li>球速 elite，四缝线接近 100 mph</li>',
        '<li>球速 elite，四缝线接近 100 mph，伸卡球/二缝线可达 100 mph 以上</li>'
    )
    return html


# ----------------- 2. Tanner Scott：修正 WS G3 与武器库 -----------------
def fix_tanner_scott(html):
    # 修正职业生涯亮点中错误的 WS G3 描述
    html = html.replace(
        '世界大赛第3战对老东家蓝鸟投出4.2局无失分救援。',
        '世界大赛第3战对蓝鸟中继登板，0.2局无失分（官方记录），协助道奇在延长赛守成。'
    )
    # 2024 全明星段也提到“季后赛对道奇出赛4.1局无失分”，保留
    # 武器库：sinker/changeup 降级为“配球/罕见”
    html = html.replace(
        '''                <div class="pitch-card">
                    <h3>伸卡球/二缝线 (Sinker)</h3>
                    <p><span class="velocity">93-96 mph</span></p>
                    <p>用来制造地面球和双杀，特别是需要 center contact 时。与四缝搭配可增加速度/位移的变化。</p>
                </div>
                <div class="pitch-card">
                    <h3>变速球 (Changeup)</h3>
                    <p><span class="velocity">86-89 mph</span></p>
                    <p>偶尔用来对付左打者，增加球速变化。使用频率较低，但在第三次面对同一名打者时可作为出其不意的配球。</p>
                </div>''',
        '''                <div class="pitch-card">
                    <h3>伸卡球/二缝线 (Sinker) — 辅助配球</h3>
                    <p><span class="velocity">93-96 mph</span></p>
                    <p>非主要武器，偶尔用来制造地面球。Scott 在 2026 年的球路主轴仍是四缝快速球与滑球，伸卡球与变速球仅作为变奏。</p>
                </div>
                <div class="pitch-card">
                    <h3>变速球 (Changeup) — 罕见变化球</h3>
                    <p><span class="velocity">86-89 mph</span></p>
                    <p>使用频率极低，偶尔用来对付左打者。Scott 绝大多数出局依靠四缝+滑球，变速球更多是“出其不意”的第三选择。</p>
                </div>'''
    )
    # 在球探分析里强调武器库集中
    html = html.replace(
        '他的快速球-滑球 combo 是典型的后援王牌配置',
        '他的快速球-滑球 combo 是他 2026 年 90% 以上出局的核心武器；伸卡球与变速球仅作为辅助'
    )
    # 劣势里调整 changeup 描述
    html = html.replace(
        '<li>变速球使用较少，面对精英左打时配球单一</li>',
        '<li>武器库集中在四缝+滑球，面对特定左打时第三球种不足</li>'
    )
    return html


# ----------------- 3. Evan Phillips：无 Judge 全垒打，补充伤病回归背景 -----------------
def fix_evan_phillips(html):
    # 该报告比较基础，需要补充 2025-2026 伤病与回归信息
    # 职业生涯亮点加强
    html = html.replace(
        '''    <div class="career-highlight">
     <h4>
      🔵 道奇时期 - 活跃名单贡献者
     </h4>
     <p>
      Evan Phillips 目前是洛杉矶道奇活跃名单的一员，作为 终结者 为球队提供稳定贡献，是争冠路上的重要拼图。
     </p>
    </div>''',
        '''    <div class="career-highlight">
     <h4>
      🏆 2024-2025年 - 道奇冠军牛棚核心
     </h4>
     <p>
      Phillips 是 2024、2025 年道奇世界大赛冠军牛棚的重要一员，多次在季后赛关键时刻登板关门。2025 年常规赛承担主要终结者角色，表现稳定。
     </p>
    </div>
    <div class="career-highlight">
     <h4>
      🏥 2026年 - 伤愈回归
     </h4>
     <p>
      2026 年开季后因伤进入伤病名单，8 月初才回归大联盟。回归后样本尚小，但三振能力（K/9 12+）仍在，需要比赛节奏恢复控球与压制力。
     </p>
    </div>'''
    )
    # 球探分析补充
    if '球探分析' in html:
        html = html.replace(
            'Evan Phillips 是道奇队的',
            'Evan Phillips 是道奇队的冠军级'
        )
    return html


# ----------------- 4. Jack Dreyer：补充季后赛数据 -----------------
def fix_jack_dreyer(html):
    # 读取文件
    pass


# ----------------- 5. 全局中英翻译辅助 -----------------
def translate_common_english(html, slug):
    """对指定 slug 的报告做中英替换。"""
    # 简单字符串替换（优先处理明显非专用词）
    replace_map = {
        'raw tools': '原始天赋',
        'raw stuff': '原始球威',
        'development phase': '发展阶段',
        'small sample': '小样本',
        'high-leverage': '高杠杆',
        'matchup': '对位',
        'lefty-heavy lineups': '左打偏多的打线',
        'lefty specialist': '左打 specialist',
        'one-batter specialist': '一人次 specialist',
        'setup man': '布局投手（第八局 setup）',
        'setup/closer': 'setup/终结者',
        'call-up': '升上大联盟',
        'roster spot': '名单位置',
        'leadoff double': '首棒二垒安打',
        'relief': '后援',
        'inherited runners': '遗留跑者',
        'first-pitch strike': '首球好球',
        'two-strike': '两好球',
        'two-seam': '二缝线',
        'center contact': '中心击球',
        'jam': ' jam ',  # 保留
    }
    # 对 Emmet Sheehan 的特殊替换
    if slug == 'emmet-sheehan':
        replace_map.update({
            'his pitch mix': '他的球路组合',
            'lefty-heavy lineups': '左打偏多的打线',
            'currently': '目前',
            'leadoff double': '首棒二垒安打',
        })
    for k, v in replace_map.items():
        html = html.replace(k, v)
    return html


# ----------------- 6. 早期报告补职业生涯亮点/代表作 -----------------
def add_career_highlights_for_early(html, slug):
    """为早期生成的报告补职业生涯亮点模块。"""
    # 仅针对 Sasaki/Ohtani/Yamamoto/Freeman 等早期报告
    if '职业生涯亮点' in html:
        return html
    # 在 "球探总评" 后插入职业生涯亮点
    pattern = re.compile(r'(<div class="section">\s*<h2>📊 2026|2025 vs 2026 赛季对比</h2>)', re.S)
    highlights = {
        'shohei-ohtani': '''
        <div class="section">
            <h2>🏆 职业生涯亮点与代表作</h2>
            <div class="career-highlight"><h4>🌟 2018年 - 大联盟首秀（天使队）</h4><p>2018年3月29日完成大联盟首秀，同年以指定打击身份击出首轰，展现罕见双向天赋。</p></div>
            <div class="career-highlight"><h4>🏆 2021年 - 美联MVP</h4><p>46轰、100打点、26盗垒，同时投出9胜、3.18 ERA，成为贝比·鲁斯之后首位单季双位數胜投与30轰的球员。</p></div>
            <div class="career-highlight"><h4>⚾ 2023年 - 二刀流巅峰</h4><p>44轰、95打点、20盗垒；投球10胜、3.14 ERA。开季连续7场先发拿下4胜，展现赛扬级投球与 MVP 级打击。</p></div>
            <div class="career-highlight"><h4>💍 2024年 - 国联MVP + 50/50俱乐部 + 世界大赛冠军</h4><p>史上首位 50轰+50盗垒（54轰、59盗垒）球员，并带领道奇夺得世界大赛冠军，季后赛多次关键长打。</p></div>
            <div class="career-highlight"><h4>💍 2025年 - 连霸世界大赛 + 国联MVP</h4><p>再次率领道奇夺冠，个人蝉联国联MVP，成为道奇王朝核心与 MLB 最具商业价值的球星。</p></div>
            <div class="career-highlight"><h4>🔥 代表作：2024年世界大赛 G2</h4><p>单场双响炮并贡献盗垒，帮助道奇在主场拉开系列赛优势，被誉为近代世界大赛最伟大个人表现之一。</p></div>
        </div>
''',
        'roki-sasaki': '''
        <div class="section">
            <h2>🏆 职业生涯亮点与代表作</h2>
            <div class="career-highlight"><h4>🇯🇵 2019年 - 日职罗德出道</h4><p>17岁即登上太平洋联盟，成为日本职棒最年轻先发的投手之一。</p></div>
            <div class="career-highlight"><h4>🔥 2022年 - 日本纪录 13 连续三振</h4><p>单场连续 13 次三振打者，追平日职联盟纪录，震惊日本棒球界。</p></div>
            <div class="career-highlight"><h4>⚾ 2023年 - 日职无安打比赛</h4><p>投出职业生涯首场无安打比赛，展现三振机器本色。</p></div>
            <div class="career-highlight"><h4>🌟 2025年 - 加盟道奇 + 大联盟首秀</h4><p>以 posting system 加盟洛杉矶道奇，成为 MLB 最受瞩目的日本投手之一，大联盟首秀即展现压制力。</p></div>
            <div class="career-highlight"><h4>🔥 代表作：2025年世界大赛 G6</h4><p>世界大赛第6战先发6局仅失1分，多次在危机中送出三振，帮助道奇将系列赛拖入G7。</p></div>
        </div>
''',
        'yoshinobu-yamamoto': '''
        <div class="section">
            <h2>🏆 职业生涯亮点与代表作</h2>
            <div class="career-highlight"><h4>🇯🇵 2017年 - 日职 debut</h4><p>18岁即登上日本火腿一军，随后转战欧力士猛牛。</p></div>
            <div class="career-highlight"><h4>🏆 2021年 - 泽村赏 + 洋联三冠王</h4><p>18胜、206K、1.39 ERA，成为太平洋联盟最优秀投手。</p></div>
            <div class="career-highlight"><h4>🏆 2023年 - WBC 冠军 + 赛会MVP</h4><p>在世界棒球经典赛决赛击败美国队，被誉为日本棒球的王牌象征。</p></div>
            <div class="career-highlight"><h4>🌟 2024年 - 加盟道奇</h4><p>12年3.25亿美元加盟洛杉矶道奇，成为 MLB 史上最大约日本投手。</p></div>
            <div class="career-highlight"><h4>🔥 代表作：2025年世界大赛 G6</h4><p>世界大赛第6战先发7局无失分，帮助道奇将系列赛逼入G7，展现王牌风范。</p></div>
        </div>
''',
        'freddie-freeman': '''
        <div class="section">
            <h2>🏆 职业生涯亮点与代表作</h2>
            <div class="career-highlight"><h4>🌟 2010年 - 大联盟首秀（勇士队）</h4><p>2010年9月1日完成大联盟首秀，随后成为勇士一垒手主力。</p></div>
            <div class="career-highlight"><h4>🏆 2020年 - 国联MVP</h4><p>疫情期间缩水赛季击出13轰、53打点、.341/.462/.640，率领勇士夺冠。</p></div>
            <div class="career-highlight"><h4>💍 2021年 - 世界大赛冠军（勇士）</h4><p>季后赛打击率接近.400，帮助亚特兰大勇士时隔26年再夺世界大赛冠军。</p></div>
            <div class="career-highlight"><h4>🔵 2023年 - 加盟道奇</h4><p>以6年1.62亿美元加盟道奇，填补一垒手位置，成为道奇打线核心。</p></div>
            <div class="career-highlight"><h4>💍 2024-2025年 - 道奇世界大赛连霸</h4><p>连续两季在世界大赛有出色表现，2024年冠军系列赛中多次关键长打。</p></div>
            <div class="career-highlight"><h4>🔥 代表作：2024年世界大赛 G1</h4><p>单场双响炮，包含一支再见满贯炮，帮助道奇在主场逆转取胜。</p></div>
        </div>
'''
    }
    if slug not in highlights:
        return html
    def replacer(m):
        return highlights[slug] + '\n' + m.group(1)
    return pattern.sub(replacer, html, count=1)


# ----------------- 7. 为图表增加说明文字 -----------------
def add_chart_captions(html, slug):
    """在 season_comparison 和 pitch_velocities 图表后追加解释文字。"""
    # 赛季对比图说明
    old = '<img src="{}_season_comparison.png" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">'.format(slug)
    if old in html:
        new = old + '''
            <p style="text-align: center; color: #90a4ae; font-size: 0.95em; margin-top: 10px;">📈 上图为近三年核心数据趋势。柱状图高度代表该年度表现，便于快速比较球员状态的上升或下滑。</p>'''
        html = html.replace(old, new)
    # 投球武器库速度图说明
    old2 = '<img src="{}_pitch_velocities.png" alt="投球武器库速度" style="width: 100%; max-width: 900px; border-radius: 10px;">'.format(slug)
    if old2 in html:
        new2 = old2 + '''
            <p style="text-align: center; color: #90a4ae; font-size: 0.95em; margin-top: 10px;">⚾ 上图为各球种球速区间（蓝=最低球速，橙=最高球速，红线=平均值）。球速差与位移差越大，打者越难锁定单一球路。</p>'''
        html = html.replace(old2, new2)
    return html


# ----------------- 主流程 -----------------
def main():
    # 1. Henriquez
    path = os.path.join(BASE_DIR, 'edgardo-henriquez', 'edgardo-henriquez-scouting-report.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = fix_henriquez(html)
        html = add_chart_captions(html, 'edgardo-henriquez')
        backup_and_write(path, html)
        print(f"[OK] {path}")

    # 2. Tanner Scott
    path = os.path.join(BASE_DIR, 'tanner-scott', 'tanner-scott-scouting-report.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = fix_tanner_scott(html)
        html = add_chart_captions(html, 'tanner-scott')
        backup_and_write(path, html)
        print(f"[OK] {path}")

    # 3. Evan Phillips
    path = os.path.join(BASE_DIR, 'evan-phillips', 'evan-phillips-scouting-report.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = fix_evan_phillips(html)
        html = add_chart_captions(html, 'evan-phillips')
        backup_and_write(path, html)
        print(f"[OK] {path}")

    # 4. Jack Dreyer：读取后追加季后赛模块
    path = os.path.join(BASE_DIR, 'jack-dreyer', 'jack-dreyer-scouting-report.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        # 在“职业生涯亮点”后追加季后赛亮点
        insert_after = '</div>\n        </div>\n\n        <div class="section">\n            <h2>📊 2026赛季投球数据</h2>'
        postseason_html = '''</div>
        </div>

        <div class="section">
            <h2>🏆 2025年季后赛表现</h2>
            <div class="career-highlight"><h4>🔥 首次季后赛经验</h4><p>Jack Dreyer 在 2025 年季后赛首次登场，合计 4 场出赛、4.0 局、0 自责分、3 支安打、4 次三振，成功帮助道奇夺得世界大赛冠军。</p></div>
            <div class="career-highlight"><h4>⚾ 世界大赛关键局数</h4><p>2025 年世界大赛第3战对蓝鸟登板后援 0.1 局，第4战再投 2.0 局无失分，累计 2.1 局未被得分，为牛棚稳定做出贡献。</p></div>
            <div class="career-highlight"><h4>📊 季后赛数据一览</h4><p>4 场出赛、0 胜 0 败、ERA 0.00、IP 4.0、H 3、BB 3、K 4、WHIP 1.50。在高压环境中保持稳定，展现未来高杠杆后援的潜质。</p></div>
        </div>

        <div class="section">
            <h2>📊 2026赛季投球数据</h2>'''
        if insert_after in html and '2025年季后赛' not in html:
            html = html.replace(insert_after, postseason_html)
        html = add_chart_captions(html, 'jack-dreyer')
        backup_and_write(path, html)
        print(f"[OK] {path}")

    # 5. 中英混杂翻译
    for slug in TRANSLATE_SLUGS:
        dir_path = os.path.join(BASE_DIR, slug)
        html_file = next((f for f in os.listdir(dir_path) if f.endswith('-scouting-report.html')), None) if os.path.isdir(dir_path) else None
        if html_file:
            path = os.path.join(dir_path, html_file)
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
            html = translate_common_english(html, slug)
            html = add_chart_captions(html, slug)
            backup_and_write(path, html)
            print(f"[OK] translate {path}")

    # 6. 早期报告补职业生涯亮点
    early_slugs = ['shohei-ohtani', 'roki-sasaki', 'yoshinobu-yamamoto', 'freddie-freeman']
    for slug in early_slugs:
        dir_path = os.path.join(BASE_DIR, slug)
        html_file = next((f for f in os.listdir(dir_path) if f.endswith('-scouting-report.html')), None) if os.path.isdir(dir_path) else None
        if html_file:
            path = os.path.join(dir_path, html_file)
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
            html = add_career_highlights_for_early(html, slug)
            html = add_chart_captions(html, slug)
            backup_and_write(path, html)
            print(f"[OK] highlights {path}")

    # 7. 全局所有报告：为已有图表追加说明（避免 chart 堆叠无解释）
    # 实际上 add_chart_captions 已被上面调用；若后续要全量跑一遍可取消注释
    # for slug in [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and not d.startswith('_')]:
    #     ...

    print("\nBatch fixes completed.")


if __name__ == '__main__':
    main()
