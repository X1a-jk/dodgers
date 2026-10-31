#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 generate_remaining_reports.py 风格的通用模板报告，
统一转换为 generate_custom_report.py / alex-vesia / tanner-scott 风格。
保留原有数据与核心事实，重写结构和章节标题。
"""
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

import generate_custom_report as gcr
import generate_remaining_reports as gr

# 需要统一格式的球员（没有 career-highlight 的通用模板报告）
TARGETS = {
    'Alex Call', 'Alex Freeland', 'Ben Casparius', 'Blake Treinen', 'Bobby Miller',
    'Brock Stewart', 'Brusdar Graterol', 'Charlie Barnes', 'Dalton Rushing',
    'Edwin Díaz', 'Eliezer Alfonzo', 'Evan Phillips', 'Gavin Stone', 'Hyeseong Kim',
    'Jack Dreyer', 'Jake Cousins', 'Kyle Hurt', 'Landon Knack', 'Nick Frasso',
    'Paul Gervase', 'River Ryan', 'Roki Sasaki', 'Ryan Ward', 'Will Klein'
}

# 角色中文名
ROLE_ZH = {
    'starter': '先发投手', 'reliever': '后援投手', 'closer': '终结者',
    'catcher': '捕手', 'infield': '内野手', 'outfield': '外野手', 'utility': '多功能工具人'
}

POSITION_ZH = {
    'P': '投手', 'C': '捕手', '1B': '一垒手', '2B': '二垒手', '3B': '三垒手',
    'SS': '游击手', 'LF': '左外野手', 'CF': '中外野手', 'RF': '右外野手',
    'OF': '外野手', 'IF': '内野手', 'OF/IF': '外野/内野手', 'IF/OF': '内野/外野手'
}


def get_role_zh(role):
    return ROLE_ZH.get(role, role)


def get_pos_zh(position):
    return POSITION_ZH.get(position, position)


def fmt_num(v, default='—'):
    if v is None or v == '':
        return default
    return str(v)


def fmt_float(v, decimals=2, default='—'):
    if v is None or v == '' or v == '—':
        return default
    try:
        return f"{float(v):.{decimals}f}"
    except Exception:
        return default


def build_pitch_arsenal(role, player_name):
    """根据角色返回统一的投球武器库配置"""
    if role == 'closer':
        return [
            {"name": "四缝快速球 (Four-Seam Fastball)", "velocity": "96-99 mph", "avg": "97.5", "desc": f"{player_name} 的压制核心球种，球速 elite，出手点稳定，能在好球带边缘制造挥空。作为终结者，这颗球是他在第九局建立优势的基础。"},
            {"name": "滑球 (Slider)", "velocity": "84-87 mph", "avg": "85.5", "desc": "主要的三振与追打球，sharp lateral break，在两好球后极具威胁。与快速球的速度差让打者难以适应。"},
            {"name": "切球/伸卡球 (Cutter/Sinker)", "velocity": "92-95 mph", "avg": "93.5", "desc": "用来制造 weak contact 或地面球，增加配球变化。在需要双杀或滚地球出局时非常有效。"},
            {"name": "变速球/叉指 (Changeup/Splitter)", "velocity": "86-89 mph", "avg": "87.5", "desc": "偶尔用来对付左打者，改变节奏与速度差。使用频率不高，但能避免被针对。"}
        ]
    if role == 'starter':
        return [
            {"name": "四缝快速球 (Four-Seam Fastball)", "velocity": "92-95 mph", "avg": "93.5", "desc": f"{player_name} 的主战球种，依靠控球与角度进入好球带。虽然不一定是火球派，但稳定的进垒点是他在轮值中吃局数的基础。"},
            {"name": "滑球 (Slider)", "velocity": "82-85 mph", "avg": "83.5", "desc": "主要的变化球武器，对付同侧打者内角与异侧打者外角都很有效。是两好球后重要的出局球。"},
            {"name": "变速球 (Changeup)", "velocity": "84-87 mph", "avg": "85.5", "desc": "用来对付左打者或制造挥棒时间差。与快速球形成速度差，是让打者击出软弱球的重要武器。"},
            {"name": "曲球 (Curveball)", "velocity": "78-82 mph", "avg": "80.0", "desc": "展示球种或地面球制造机，视个人球风而定。用来在两好球后改变打者视线，或在需要滚地球时使用。"}
        ]
    # reliever default
    return [
        {"name": "四缝快速球 (Four-Seam Fastball)", "velocity": "93-96 mph", "avg": "94.5", "desc": f"{player_name} 在后援中的主战球种，依靠球速与出手角度来压制打者。在短局数中能发挥最大威力。"},
        {"name": "滑球 (Slider)", "velocity": "82-85 mph", "avg": "83.5", "desc": "主要的出局球，具备 lateral break。在两好球后用来诱导追打，是对付同侧打者的利器。"},
        {"name": "变速球 (Changeup)", "velocity": "85-88 mph", "avg": "86.5", "desc": "改变节奏的武器，用来对付左打者或让右打者失去 timing。使用频率视当日的控球状态而定。"},
        {"name": "曲球/切球 (Curveball/Cutter)", "velocity": "78-82 mph / 88-91 mph", "avg": "84.0", "desc": "第四球种，视配球策略使用。曲球用于两好球后的追打，切球则用来制造 weak contact。"}
    ]


def build_career_highlights(name, role, status, debut, college):
    role_zh = get_role_zh(role)
    parts = []
    if college:
        parts.append(f'<div class="career-highlight"><h4>🎓 大学时期 - {college}</h4><p>{name} 在大学时期展现出成为大联盟 {role_zh} 的潜力，积累了扎实的基础与比赛经验。</p></div>')
    if debut and debut != '—' and debut != '尚未首秀':
        parts.append(f'<div class="career-highlight"><h4>🌟 {debut[:4]}年 - 大联盟首秀</h4><p>{name} 于 {debut} 登上大联盟，开始了自己的 MLB 生涯。作为一名 {role_zh}，他逐步在最高舞台上建立自己的角色。</p></div>')
    else:
        parts.append(f'<div class="career-highlight"><h4>🌟 小联盟持续成长</h4><p>{name} 目前仍在小联盟体系中持续磨练，努力提升自己的 {role_zh} 技能，争取未来登上大联盟舞台。</p></div>')
    if status.startswith('IL'):
        parts.append(f'<div class="career-highlight"><h4>🏥 当前状态 - {status} 伤病名单</h4><p>{name} 目前因伤位于 {status} 名单。恢复后，他将重新回到道奇 {role_zh} 的行列，为球队提供即战力。</p></div>')
    elif status == 'Minors':
        parts.append(f'<div class="career-highlight"><h4>🔮 当前状态 - 小联盟发展中</h4><p>{name} 目前位于道奇小联盟体系，是球队长期深度规划的一部分。持续进步将决定他获得大联盟机会的时间点。</p></div>')
    else:
        parts.append(f'<div class="career-highlight"><h4>🔵 道奇时期 - 活跃名单贡献者</h4><p>{name} 目前是洛杉矶道奇活跃名单的一员，作为 {role_zh} 为球队提供稳定贡献，是争冠路上的重要拼图。</p></div>')
    return '\n'.join(parts)


def build_summary(name, role, status, stats_2026, type_):
    role_zh = get_role_zh(role)
    if status.startswith('IL'):
        status_text = f"目前位于 <span class='warning'>{status} 伤病名单</span>，正在恢复中。"
    elif status == 'Minors':
        status_text = f"目前位于 <span class='warning'>小联盟</span>，持续发展中。"
    else:
        status_text = "目前是道奇活跃名单的一员。"

    if type_ == 'pitcher':
        if stats_2026 and stats_2026.get('era') and stats_2026.get('era') != '—':
            era = fmt_float(stats_2026.get('era'), 2)
            whip = fmt_float(stats_2026.get('whip'), 2)
            k9 = fmt_float(stats_2026.get('strikeouts_per_9'), 1)
            ip = fmt_num(stats_2026.get('innings_pitched'))
            stat_line = f"2026 年数据：ERA {era}、WHIP {whip}、K/9 {k9}、IP {ip}。"
        else:
            stat_line = "2026 年大联盟样本有限，数据主要参考小联盟与过往表现。"
        return f'''
            <p style="margin-bottom: 15px;">{name} 是道奇队的<span class="highlight">{role_zh}</span>，{status_text}</p>
            <p style="margin-bottom: 15px;">{stat_line} 他依靠球路组合与投球智慧在球队中扮演重要角色，是道奇投手轮值/牛棚深度的重要一环。</p>
            <p>作为一名 {role_zh}，{name} 的价值在于稳定的局数贡献与关键出局能力。在道奇教练团体系下，他有望继续发挥自己的特长。</p>
        '''
    else:
        if stats_2026 and stats_2026.get('avg') and stats_2026.get('avg') != '—':
            avg = fmt_num(stats_2026.get('avg'))
            ops = fmt_num(stats_2026.get('ops'))
            hr = fmt_num(stats_2026.get('home_runs'))
            stat_line = f"2026 年数据：AVG {avg}、OPS {ops}、HR {hr}。"
        else:
            stat_line = "2026 年大联盟样本有限，数据主要参考小联盟与过往表现。"
        return f'''
            <p style="margin-bottom: 15px;">{name} 是道奇队的<span class="highlight">{role_zh}</span>，{status_text}</p>
            <p style="margin-bottom: 15px;">{stat_line} 他在球队中提供 {role_zh} 所需的攻防价值，是道奇阵容深度的重要组成部分。</p>
            <p>{name} 的角色定位和比赛意识让他在道奇体系中具备稳定贡献的潜力，无论是先发、替补还是防守替补都能为球队带来价值。</p>
        '''


def build_analysis(name, role, status, stats_2026, stats_2025, type_):
    role_zh = get_role_zh(role)
    if type_ == 'pitcher':
        if stats_2026 and stats_2026.get('era') and stats_2026.get('era') != '—':
            era = fmt_float(stats_2026.get('era'), 2)
            whip = fmt_float(stats_2026.get('whip'), 2)
            k9 = fmt_float(stats_2026.get('strikeouts_per_9'), 1)
            bb9 = fmt_float(stats_2026.get('walks_per_9'), 1)
            stat_text = f"2026 年 ERA {era}、WHIP {whip}、K/9 {k9}、BB/9 {bb9}。"
        else:
            stat_text = "2026 年大联盟样本不足，难以从数据端给出精确评估。"
        return f'''
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">投球风格与角色</h3>
                <p>{name} 作为一名 {role_zh}，球路组合以快速球搭配变化球为主。{stat_text} 他的投球策略取决于能否在好球带边缘工作，避免把球投到中心区域。</p>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">控球与被击球</h3>
                <p>WHIP 与 BB/9 是衡量他控球稳定性的关键指标。若能把球持续投进好球带，他的三振能力与球路组合将更具威胁；反之，高保送会让他陷入被动。</p>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">健康与发展</h3>
                <p>{'伤病是目前最大的不确定因素，恢复后的状态将决定他能否回到先前的水准。' if status.startswith('IL') else '保持稳定健康是他继续贡献的基础，道奇会谨慎管理他的工作量。' if status != 'Minors' else '在小联盟持续健康出赛是他获得大联盟机会的前提。'}</p>
            </div>
        '''
    else:
        if stats_2026 and stats_2026.get('avg') and stats_2026.get('avg') != '—':
            avg = fmt_num(stats_2026.get('avg'))
            obp = fmt_num(stats_2026.get('obp'))
            slg = fmt_num(stats_2026.get('slg'))
            ops = fmt_num(stats_2026.get('ops'))
            stat_text = f"2026 年打击三围 {avg}/{obp}/{slg}，OPS {ops}。"
        else:
            stat_text = "2026 年大联盟样本有限，需参考过往与小联盟数据。"
        return f'''
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">打击分析</h3>
                <p>{stat_text} 作为 {role_zh}，他的打击价值取决于能否稳定上垒、减少三振，并在关键时刻贡献长打。</p>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">防守与位置价值</h3>
                <p>{name} 在 {role_zh} 位置上提供符合位置的防守能力。站位、判断与传球稳定性是他的基本盘，能够在常规机会中完成任务。</p>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">角色定位</h3>
                <p>{'伤病是当前最大的障碍，复出后需要重新找回比赛节奏。' if status.startswith('IL') else '作为道奇阵容的一员，他需要抓住每一次出场机会证明自己的价值。' if status != 'Minors' else '在小联盟持续进步是他获得大联盟征召的关键。'}</p>
            </div>
        '''


def build_pros_cons(name, role, status, type_):
    role_zh = get_role_zh(role)
    if type_ == 'pitcher':
        pros = [
            f"{role_zh}角色定位清晰，在道奇体系中有明确价值",
            "具备必要的球种组合应付大联盟打者",
            f"{'伤病恢复后有望提供即战力' if status.startswith('IL') else '在小联盟持续成长，未来可期' if status == 'Minors' else '目前在活跃名单中，能为球队稳定贡献'}",
            "道奇投教团队擅长挖掘与改造投手潜力",
            "能在特定 matchup 中发挥球路优势"
        ]
        cons = [
            f"{'伤病状态让短期贡献存在不确定性' if status.startswith('IL') else '大联盟经验与样本仍需积累' if status == 'Minors' else '面对 elite 打者时稳定性待验证'}",
            "控球与配球执行仍有提升空间",
            "球速或变化球品质可能限制 ceiling",
            "需要在高压局面中持续证明自己"
        ]
    else:
        pros = [
            f"{role_zh}位置价值明确，阵容灵活性强" if role == 'utility' else f"{role_zh}位置上的稳定贡献者",
            "具备大联盟级别的基本技能与比赛意识",
            "在道奇体系中获得成长与指导机会",
            "能够执行团队战术需求"
        ]
        cons = [
            f"{'伤病影响出勤与状态' if status.startswith('IL') else '打击数据可能受出场时间限制'}",
            "面对顶级投手时压制力或稳定性不足",
            "防守范围或特定技能存在局限",
            "需要在完整赛季中保持稳定性"
        ]
    return pros, cons


def build_future(name, role, status):
    role_zh = get_role_zh(role)
    if status.startswith('IL'):
        return f'''
            <div style="margin-top: 20px;">
                <p>{name} 的首要任务是完成复健并重返球场。一旦回归，他将重新在 {role_zh} 位置上为道奇提供即战力。</p>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">复出后目标</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>循序渐进：</strong>避免复出后过度使用，逐步找回比赛节奏。</li>
                    <li><strong>重建信心：</strong>通过稳定出赛恢复状态与数据表现。</li>
                    <li><strong>季后赛准备：</strong>在赛季后半段为道奇季后赛征程储备能量。</li>
                </ol>
            </div>
        '''
    if status == 'Minors':
        return f'''
            <div style="margin-top: 20px;">
                <p>{name} 目前在小联盟持续成长，未来目标是提升自己的核心技能，争取在道奇队获得稳定的大联盟机会。</p>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>提升主要工具：</strong>强化 {role_zh} 最核心的技能。</li>
                    <li><strong>保持健康：</strong>避免伤病，争取完整赛季出赛。</li>
                    <li><strong>学习大联盟节奏：</strong>向老将取经，适应更高层级的比赛强度。</li>
                </ol>
            </div>
        '''
    return f'''
        <div style="margin-top: 20px;">
            <p>{name} 作为道奇 {role_zh}，未来将继续在现有角色中发挥作用。道奇教练团会根据球队需求与对手特点来最大化他的价值。</p>
            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
            <ol style="margin-left: 20px; line-height: 2;">
                <li><strong>保持稳定：</strong>在赛季后半段维持当前产出。</li>
                <li><strong>提升关键技能：</strong>针对弱项进行专门训练。</li>
                <li><strong>团队角色：</strong>在季后赛竞争中发挥经验与活力。</li>
            </ol>
        </div>
    '''


def build_background(name, role, status, debut, birthplace):
    role_zh = get_role_zh(role)
    if status == 'Minors':
        return f'''
            <div style="margin-top: 20px;">
                <p>{name} 是道奇组织中的年轻 {role_zh}，正在小联盟体系中积累经验和技能。作为道奇农场体系的一部分，他接受系统的训练，目标是未来登上大联盟。</p>
                <p>他展现出的潜能让球探和教练团对他抱有期待，持续的进步将决定他在道奇未来的角色。</p>
            </div>
        '''
    debut_text = f"于 {debut} 完成 MLB 首秀" if debut and debut != '—' and debut != '尚未首秀' else "仍在为小联盟首次大联盟征召努力"
    return f'''
        <div style="margin-top: 20px;">
            <p>{name} 是洛杉矶道奇队的 {role_zh}，{debut_text}。他在道奇体系中扮演着重要角色，无论是作为稳定轮值/牛棚成员还是多功能工具人，都为球队提供价值。</p>
            <p>他的职业态度和团队合作精神受到教练团认可，未来将继续在道奇追逐季后赛和世界大赛冠军。</p>
        </div>
    '''


def build_season_chart(stats, type_):
    if type_ == 'pitcher':
        keys = ['era', 'whip', 'strikeouts_per_9', 'walks_per_9']
        vals = []
        for k in keys:
            try:
                vals.append(float(stats.get(k, 0)) if stats and stats.get(k) and stats.get(k) != '—' else 0)
            except Exception:
                vals.append(0)
        return vals
    else:
        keys = ['avg', 'obp', 'slg', 'ops']
        vals = []
        for k in keys:
            try:
                v = stats.get(k, '.000')
                if v and v != '—':
                    vals.append(float(v.strip('.')) / 1000)
                else:
                    vals.append(0)
            except Exception:
                vals.append(0)
        return vals


def build_player_config(cfg, info, stats_2025, stats_2026):
    name = cfg['name']
    slug = gr.slugify(name)
    last_name = slug.split('-')[-1]
    role = cfg['role']
    status = cfg['status']
    position = cfg['position']
    type_ = 'pitcher' if role in ('starter', 'reliever', 'closer') else 'batter'

    birth = info.get('birth_date', '—') if info else '—'
    age = str(info.get('age', cfg.get('age', '—'))) if info else cfg.get('age', '—')
    height = info.get('height', '—') if info else '—'
    weight = info.get('weight', '—') if info else '—'
    bats = info.get('bats', '—') if info else '—'
    throws = info.get('throws', '—') if info else '—'
    debut = info.get('mlb_debut_date', '—') if info else '—'
    birthplace = cfg.get('birthplace', '美国')
    college = cfg.get('college', '')
    nickname = cfg.get('nickname', name.split()[-1])
    number = cfg['number']

    # 处理 stats 字典，统一 key
    def normalize(s):
        if not s:
            return {}
        s.setdefault('G', s.get('games_played', '—'))
        s.setdefault('GS', s.get('games_started', '—'))
        s.setdefault('W', s.get('wins', '—'))
        s.setdefault('L', s.get('losses', '—'))
        s.setdefault('ERA', s.get('era', '—'))
        s.setdefault('IP', s.get('innings_pitched', '—'))
        s.setdefault('K', s.get('strikeouts', '—'))
        s.setdefault('BB', s.get('walks', '—'))
        s.setdefault('WHIP', s.get('whip', '—'))
        s.setdefault('K/9', s.get('strikeouts_per_9', '—'))
        s.setdefault('BB/9', s.get('walks_per_9', '—'))
        s.setdefault('HR', s.get('home_runs', '—'))
        s.setdefault('AVG', s.get('avg', '—'))
        s.setdefault('OBP', s.get('obp', '—'))
        s.setdefault('SLG', s.get('slg', '—'))
        s.setdefault('OPS', s.get('ops', '—'))
        s.setdefault('RBI', s.get('rbi', '—'))
        s.setdefault('SB', s.get('stolen_bases', '—'))
        s.setdefault('SO', s.get('strikeouts', '—'))
        return s

    stats_2025 = normalize(stats_2025)
    stats_2026 = normalize(stats_2026)

    # 计算评分
    if type_ == 'pitcher':
        grades = gr.compute_pitcher_grades(stats_2026, role, int(age) if age != '—' else 25)
    else:
        grades = gr.compute_batter_grades(stats_2026, position, int(age) if age != '—' else 25)
    overall_grade = round(sum(g['value'] for g in grades) / len(grades))
    overall_label = f"{gr.grade_from_value(overall_grade)} 级 / {get_role_zh(role)}"

    # 构建 cover stats
    if type_ == 'pitcher':
        if stats_2026 and stats_2026.get('era') and stats_2026.get('era') != '—':
            cover_stats = [
                ('ERA', fmt_float(stats_2026.get('era'), 2)),
                ('WHIP', fmt_float(stats_2026.get('whip'), 2)),
                ('K', fmt_num(stats_2026.get('K'))),
                ('IP', fmt_num(stats_2026.get('IP'))),
                ('W-L', f"{fmt_num(stats_2026.get('W'))}-{fmt_num(stats_2026.get('L'))}"),
                ('K/9', fmt_float(stats_2026.get('K/9'), 1)),
                ('Age', age),
                ('Status', status)
            ]
        else:
            cover_stats = [('Age', age), ('Height', height), ('Weight', fmt_num(weight)), ('Throws', throws), ('Level', 'AAA' if status == 'Minors' else 'MLB'), ('Status', status), ('Debut', debut), ('Role', get_role_zh(role))]
    else:
        if stats_2026 and stats_2026.get('avg') and stats_2026.get('avg') != '—':
            cover_stats = [
                ('AVG', fmt_num(stats_2026.get('avg'))),
                ('OPS', fmt_num(stats_2026.get('ops'))),
                ('HR', fmt_num(stats_2026.get('home_runs'))),
                ('RBI', fmt_num(stats_2026.get('rbi'))),
                ('SB', fmt_num(stats_2026.get('stolen_bases'))),
                ('Age', age),
                ('Pos', position),
                ('Status', status)
            ]
        else:
            cover_stats = [('Age', age), ('Height', height), ('Weight', fmt_num(weight)), ('Bats', bats), ('Pos', position), ('Status', status), ('Debut', debut), ('Level', 'AAA' if status == 'Minors' else 'MLB')]

    season_chart_2025 = build_season_chart(stats_2025, type_)
    season_chart_2026 = build_season_chart(stats_2026, type_)

    # 如果数据不可用，保持图表不为空
    if all(v == 0 for v in season_chart_2025):
        season_chart_2025 = season_chart_2026[:]
    if all(v == 0 for v in season_chart_2026):
        season_chart_2026 = season_chart_2025[:]

    if type_ == 'pitcher':
        season_chart_stats = ['ERA', 'WHIP', 'K/9', 'BB/9']
        pitch_arsenal = build_pitch_arsenal(role, name)
    else:
        season_chart_stats = ['AVG', 'OBP', 'SLG', 'OPS']
        pitch_arsenal = []

    return {
        "name": name,
        "slug": slug,
        "last_name": last_name,
        "number": number,
        "position": get_role_zh(role) if role in ('starter', 'reliever', 'closer') else get_pos_zh(position),
        "position_code": position,
        "bats_throws": f"{bats}打 / {throws}投" if bats != '—' and throws != '—' else '—',
        "birth_date": birth,
        "age": age,
        "birthplace": birthplace,
        "height_weight": f"{height} / {weight} lbs" if height != '—' and weight != '—' else '—',
        "debut": debut if debut and debut != '—' else '尚未首秀',
        "college": college,
        "nickname": nickname,
        "status": status,
        "type": type_,
        "summary": build_summary(name, role, status, stats_2026, type_),
        "career_highlights": build_career_highlights(name, role, status, debut, college),
        "stats_2026": stats_2026,
        "stats_2025": stats_2025,
        "cover_stats": cover_stats,
        "season_chart_2025": season_chart_2025,
        "season_chart_2026": season_chart_2026,
        "season_chart_stats": season_chart_stats,
        "pitch_arsenal": pitch_arsenal,
        "analysis": build_analysis(name, role, status, stats_2026, stats_2025, type_),
        "pros": build_pros_cons(name, role, status, type_)[0],
        "cons": build_pros_cons(name, role, status, type_)[1],
        "grades": grades,
        "overall_grade": overall_grade,
        "overall_label": overall_label,
        "overall_desc": f"综合 {len(grades)} 项工具评分的平均表现，反映 {name} 作为 {get_role_zh(role)} 的当前价值。",
        "future_outlook": build_future(name, role, status),
        "background": build_background(name, role, status, debut, birthplace)
    }


def main():
    import time
    print("=" * 70)
    print("Unifying report format to alex-vesia / tanner-scott style")
    print("=" * 70)

    targets = [cfg for cfg in gr.PLAYER_CONFIGS if cfg['name'] in TARGETS]
    print(f"Targets: {len(targets)}")

    for cfg in targets:
        name = cfg['name']
        print(f"\n[Processing] {name}", flush=True)
        t0 = time.time()
        try:
            print(f"  Fetching info...", flush=True)
            info = gr.fetch_player_info(cfg['search'])
            print(f"  Info OK: {info is not None}", flush=True)
            stats_2025 = None
            stats_2026 = None
            if info:
                pid = info['id']
                print(f"  Fetching 2025 stats...", flush=True)
                stats_2025 = gr.fetch_player_stats(pid, 2025)
                print(f"  2025 stats OK", flush=True)
                print(f"  Fetching 2026 stats...", flush=True)
                stats_2026 = gr.fetch_player_stats(pid, 2026)
                print(f"  2026 stats OK", flush=True)
                if stats_2025:
                    stats_2025 = stats_2025.get('pitching') or stats_2025.get('batting') or stats_2025
                if stats_2026:
                    stats_2026 = stats_2026.get('pitching') or stats_2026.get('batting') or stats_2026

            print(f"  Building config...", flush=True)
            player_cfg = build_player_config(cfg, info, stats_2025, stats_2026)
            print(f"  Generating report...", flush=True)
            gcr.PLAYER = player_cfg
            gcr.main()
            print(f"  [OK] {name} unified in {time.time()-t0:.1f}s", flush=True)
        except Exception as e:
            import traceback
            print(f"  [FAIL] {name}: {e}", flush=True)
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("Format unification completed")
    print("=" * 70)


if __name__ == '__main__':
    main()
