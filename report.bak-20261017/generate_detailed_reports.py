import subprocess
import json
import os
import sys
import time
from datetime import datetime

# 配置
OUTPUT_BASE = r"D:\baseball\report"
CHART_SCRIPT = os.path.join(OUTPUT_BASE, "generate_charts.py")

def get_player_stats(player_name):
    """获取球员统计数据"""
    try:
        result = subprocess.run(
            ['python', r'C:\Users\Junkai XIA\.openclaw\workspace\skills\baseball\scripts\baseball.py', 
             'stats', player_name, '--format', 'json'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            output = result.stdout
            try:
                json_start = output.index('{')
                json_data = output[json_start:]
                return json.loads(json_data)
            except (ValueError, json.JSONDecodeError):
                return None
        return None
    except Exception as e:
        print(f"Error getting stats for {player_name}: {e}")
        return None

def generate_html_report(player, stats_data, output_dir):
    """生成HTML详细报告"""
    player_name = player['name']
    player_slug = player_name.lower().replace(' ', '-')
    
    # 提取数据
    batting = stats_data.get('batting', {}) if stats_data else {}
    pitching = stats_data.get('pitching', {}) if stats_data else {}
    player_info = stats_data.get('player', {}) if stats_data else {}
    
    # 判断球员类型
    is_pitcher = player['position'] == 'P' or player.get('type') == 'pitcher'
    is_two_way = player.get('type') == 'two-way'
    
    # 生成HTML
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{player_name} 球探报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e0e0e0;
            line-height: 1.6;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            padding: 40px 0;
            background: linear-gradient(90deg, #005A9C 0%, #1a5490 50%, #005A9C 100%);
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }}
        .header h1 {{ font-size: 3em; color: #fff; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); margin-bottom: 10px; }}
        .header .subtitle {{ font-size: 1.2em; color: #e0e0e0; font-style: italic; }}
        .section {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .section h2 {{
            color: #4fc3f7;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 2px solid #4fc3f7;
            padding-bottom: 10px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, rgba(0, 90, 156, 0.3) 0%, rgba(26, 84, 144, 0.3) 100%);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(79, 195, 247, 0.3);
        }}
        .stat-card .stat-value {{ font-size: 2.5em; font-weight: bold; color: #4fc3f7; display: block; }}
        .stat-card .stat-label {{ font-size: 0.9em; color: #90a4ae; text-transform: uppercase; margin-top: 5px; }}
        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        .comparison-table th, .comparison-table td {{
            padding: 15px;
            text-align: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .comparison-table th {{
            background: rgba(0, 90, 156, 0.3);
            color: #4fc3f7;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .comparison-table tr:hover {{ background: rgba(255, 255, 255, 0.05); }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }}
        .info-item {{
            background: rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 8px;
        }}
        .info-item .label {{ font-size: 0.9em; color: #90a4ae; text-transform: uppercase; }}
        .info-item .value {{ font-size: 1.2em; color: #fff; font-weight: bold; }}
        .player-card {{
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
        }}
        .player-info {{ flex: 1; min-width: 250px; }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #90a4ae;
            font-size: 0.9em;
        }}
        .grade {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        .grade-a {{ background: rgba(76, 175, 80, 0.3); color: #4caf50; }}
        .grade-b {{ background: rgba(79, 195, 247, 0.3); color: #4fc3f7; }}
        .grade-c {{ background: rgba(255, 152, 0, 0.3); color: #ff9800; }}
        .grade-d {{ background: rgba(244, 67, 54, 0.3); color: #f44336; }}
        .highlight {{ color: #4fc3f7; font-weight: bold; }}
        .warning {{ color: #ff9800; font-weight: bold; }}
        .success {{ color: #4caf50; font-weight: bold; }}
        .danger {{ color: #f44336; font-weight: bold; }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2em; }}
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚾ {player_name}</h1>
            <p class="subtitle">Los Angeles Dodgers #{player.get('number', '—')} | {player['position']} | 球探报告</p>
        </div>
"""

    # 基本信息部分
    html_content += f"""
        <div class="section">
            <h2>📋 基本信息</h2>
            <div class="player-card">
                <div class="player-info">
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="label">姓名</div>
                            <div class="value">{player_name}</div>
                        </div>
                        <div class="info-item">
                            <div class="label">背号</div>
                            <div class="value">#{player.get('number', '—')}</div>
                        </div>
                        <div class="info-item">
                            <div class="label">位置</div>
                            <div class="value">{player['position']}</div>
                        </div>
                        <div class="info-item">
                            <div class="label">状态</div>
                            <div class="value">{player.get('status', '活跃')}</div>
                        </div>
                        <div class="info-item">
                            <div class="label">球队</div>
                            <div class="value">Los Angeles Dodgers</div>
                        </div>
                        <div class="info-item">
                            <div class="label">报告日期</div>
                            <div class="value">2026-07-09</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
"""

    # 统计数据部分
    if is_pitcher or is_two_way:
        if pitching:
            html_content += f"""
        <div class="section">
            <h2>📊 投球数据</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-value">{pitching.get('wins', 0)}</span>
                    <div class="stat-label">胜场 (W)</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{pitching.get('losses', 0)}</span>
                    <div class="stat-label">败场 (L)</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{pitching.get('era', '—')}</span>
                    <div class="stat-label">ERA</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{pitching.get('innings_pitched', '—')}</span>
                    <div class="stat-label">投球局数</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{pitching.get('strikeouts', 0)}</span>
                    <div class="stat-label">三振 (K)</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{pitching.get('walks', 0)}</span>
                    <div class="stat-label">保送 (BB)</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{pitching.get('whip', '—')}</span>
                    <div class="stat-label">WHIP</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{pitching.get('strikeouts_per_9', '—')}</span>
                    <div class="stat-label">K/9</div>
                </div>
            </div>
        </div>
"""

    if (batting and not is_pitcher) or is_two_way:
        html_content += f"""
        <div class="section">
            <h2>📊 打击数据</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-value">{batting.get('games_played', 0)}</span>
                    <div class="stat-label">出赛场次</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{batting.get('avg', '—')}</span>
                    <div class="stat-label">打击率</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{batting.get('home_runs', 0)}</span>
                    <div class="stat-label">全垒打</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{batting.get('rbi', 0)}</span>
                    <div class="stat-label">打点</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{batting.get('ops', '—')}</span>
                    <div class="stat-label">OPS</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{batting.get('stolen_bases', 0)}</span>
                    <div class="stat-label">盗垒</div>
                </div>
            </div>
        </div>
"""

    # 分析评价部分（基于数据自动生成）
    analysis = generate_analysis(player, batting, pitching, is_pitcher, is_two_way)
    html_content += f"""
        <div class="section">
            <h2>🔍 球探分析</h2>
            {analysis}
        </div>
"""

    # 综合评分
    grades = generate_grades(player, batting, pitching, is_pitcher, is_two_way)
    html_content += f"""
        <div class="section">
            <h2>📊 综合评分</h2>
            <div class="stats-grid">
                {grades}
            </div>
        </div>
"""

    # 底部
    html_content += f"""
        <div class="footer">
            <p>数据来源：MLB.com | Baseball Savant | MLB Stats API</p>
            <p>报告生成时间：2026-07-09</p>
            <p>⚾ 洛杉矶道奇队球探报告</p>
        </div>
    </div>
</body>
</html>
"""

    # 保存HTML
    html_path = os.path.join(output_dir, f"{player_slug}-scouting-report.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return html_path

def generate_analysis(player, batting, pitching, is_pitcher, is_two_way):
    """基于数据生成分析评价"""
    analysis = ""
    
    if is_pitcher or is_two_way:
        if pitching:
            era = float(pitching.get('era', 99))
            whip = float(pitching.get('whip', 99))
            k9 = float(pitching.get('strikeouts_per_9', 0))
            bb9 = float(pitching.get('walks_per_9', 0))
            
            analysis += "<h3 style='color: #4fc3f7; margin: 15px 0;'>投球分析</h3><ul>"
            
            if era < 3.0:
                analysis += "<li><span class='success'>ERA表现优异</span>：{:.2f}，联盟顶级水平</li>".format(era)
            elif era < 4.0:
                analysis += "<li><span class='highlight'>ERA表现良好</span>：{:.2f}，高于联盟平均</li>".format(era)
            elif era < 5.0:
                analysis += "<li><span class='warning'>ERA表现一般</span>：{:.2f}，需要改善</li>".format(era)
            else:
                analysis += "<li><span class='danger'>ERA表现不佳</span>：{:.2f}，急需调整</li>".format(era)
            
            if whip < 1.1:
                analysis += "<li><span class='success'>WHIP控制出色</span>：{:.2f}，上垒率控制极佳</li>".format(whip)
            elif whip < 1.3:
                analysis += "<li><span class='highlight'>WHIP控制良好</span>：{:.2f}，符合先发标准</li>".format(whip)
            else:
                analysis += "<li><span class='warning'>WHIP偏高</span>：{:.2f}，被上垒率需要改善</li>".format(whip)
            
            if k9 > 9:
                analysis += "<li><span class='success'>三振能力优秀</span>：K/9 = {:.1f}，压制力强</li>".format(k9)
            elif k9 > 7:
                analysis += "<li><span class='highlight'>三振能力良好</span>：K/9 = {:.1f}，具备压制能力</li>".format(k9)
            else:
                analysis += "<li><span class='warning'>三振能力一般</span>：K/9 = {:.1f}，需要提升压制力</li>".format(k9)
            
            if bb9 < 3:
                analysis += "<li><span class='success'>保送控制优秀</span>：BB/9 = {:.1f}，控球精准</li>".format(bb9)
            elif bb9 < 4:
                analysis += "<li><span class='highlight'>保送控制良好</span>：BB/9 = {:.1f}，符合标准</li>".format(bb9)
            else:
                analysis += "<li><span class='danger'>保送偏多</span>：BB/9 = {:.1f}，控球需改善</li>".format(bb9)
            
            analysis += "</ul>"
    
    if batting and (not is_pitcher or is_two_way):
        avg = batting.get('avg', '0')
        ops = batting.get('ops', '0')
        hr = batting.get('home_runs', 0)
        
        try:
            avg_val = float(avg.strip('.')) / 1000 if avg != '—' else 0
            ops_val = float(ops.strip('.')) / 1000 if ops != '—' else 0
        except:
            avg_val = 0
            ops_val = 0
        
        analysis += "<h3 style='color: #4fc3f7; margin: 15px 0;'>打击分析</h3><ul>"
        
        if avg_val >= 0.280:
            analysis += f"<li><span class='success'>打击率优秀</span>：{avg}，contact能力出色</li>"
        elif avg_val >= 0.250:
            analysis += f"<li><span class='highlight'>打击率良好</span>：{avg}，稳定产出</li>"
        else:
            analysis += f"<li><span class='warning'>打击率偏低</span>：{avg}，需要调整</li>"
        
        if ops_val >= 0.850:
            analysis += f"<li><span class='success'>长打能力优秀</span>：OPS = {ops}</li>"
        elif ops_val >= 0.750:
            analysis += f"<li><span class='highlight'>长打能力良好</span>：OPS = {ops}</li>"
        else:
            analysis += f"<li><span class='warning'>长打能力一般</span>：OPS = {ops}</li>"
        
        if hr >= 15:
            analysis += f"<li><span class='success'>力量输出出色</span>：{hr}支全垒打</li>"
        elif hr >= 5:
            analysis += f"<li><span class='highlight'>具备长打能力</span>：{hr}支全垒打</li>"
        else:
            analysis += f"<li><span class='warning'>力量输出不足</span>：{hr}支全垒打</li>"
        
        analysis += "</ul>"
    
    return analysis

def generate_grades(player, batting, pitching, is_pitcher, is_two_way):
    """生成评分卡片"""
    grades_html = ""
    
    if is_pitcher or is_two_way:
        if pitching:
            era = float(pitching.get('era', 99))
            whip = float(pitching.get('whip', 99))
            k9 = float(pitching.get('strikeouts_per_9', 0))
            
            # ERA评分
            if era < 3.0: grade, label = 70, 'A'
            elif era < 4.0: grade, label = 60, 'B+'
            elif era < 5.0: grade, label = 50, 'B'
            else: grade, label = 40, 'C'
            
            grades_html += f"""
                <div class="stat-card">
                    <span class="stat-value" style="color: {'#4caf50' if grade >= 60 else '#4fc3f7' if grade >= 50 else '#ff9800'};">{grade}</span>
                    <div class="stat-label">ERA</div>
                    <span class="grade grade-{'a' if grade >= 60 else 'b' if grade >= 50 else 'c'}">{label}</span>
                </div>
            """
            
            # WHIP评分
            if whip < 1.1: grade, label = 70, 'A'
            elif whip < 1.3: grade, label = 60, 'B+'
            else: grade, label = 45, 'C+'
            
            grades_html += f"""
                <div class="stat-card">
                    <span class="stat-value" style="color: {'#4caf50' if grade >= 60 else '#4fc3f7' if grade >= 50 else '#ff9800'};">{grade}</span>
                    <div class="stat-label">控球</div>
                    <span class="grade grade-{'a' if grade >= 60 else 'b' if grade >= 50 else 'c'}">{label}</span>
                </div>
            """
            
            # K能力
            if k9 > 9: grade, label = 70, 'A'
            elif k9 > 7: grade, label = 60, 'B+'
            else: grade, label = 50, 'B'
            
            grades_html += f"""
                <div class="stat-card">
                    <span class="stat-value" style="color: {'#4caf50' if grade >= 60 else '#4fc3f7'};">{grade}</span>
                    <div class="stat-label">三振能力</div>
                    <span class="grade grade-{'a' if grade >= 60 else 'b'}">{label}</span>
                </div>
            """
    
    if batting and (not is_pitcher or is_two_way):
        avg = batting.get('avg', '0')
        ops = batting.get('ops', '0')
        
        try:
            avg_val = float(avg.strip('.')) / 1000 if avg != '—' else 0
            ops_val = float(ops.strip('.')) / 1000 if ops != '—' else 0
        except:
            avg_val = 0
            ops_val = 0
        
        # 打击率
        if avg_val >= 0.280: grade, label = 65, 'A-'
        elif avg_val >= 0.250: grade, label = 55, 'B'
        else: grade, label = 45, 'C+'
        
        grades_html += f"""
            <div class="stat-card">
                <span class="stat-value" style="color: {'#4caf50' if grade >= 60 else '#4fc3f7' if grade >= 50 else '#ff9800'};">{grade}</span>
                <div class="stat-label">打击能力</div>
                <span class="grade grade-{'a' if grade >= 60 else 'b' if grade >= 50 else 'c'}">{label}</span>
            </div>
        """
        
        # 长打能力
        if ops_val >= 0.850: grade, label = 70, 'A'
        elif ops_val >= 0.750: grade, label = 60, 'B+'
        else: grade, label = 50, 'B'
        
        grades_html += f"""
            <div class="stat-card">
                <span class="stat-value" style="color: {'#4caf50' if grade >= 60 else '#4fc3f7'};">{grade}</span>
                <div class="stat-label">长打能力</div>
                <span class="grade grade-{'a' if grade >= 60 else 'b'}">{label}</span>
            </div>
        """
    
    return grades_html

def generate_markdown_report(player, stats_data, output_dir):
    """生成Markdown详细报告"""
    player_name = player['name']
    player_slug = player_name.lower().replace(' ', '-')
    
    batting = stats_data.get('batting', {}) if stats_data else {}
    pitching = stats_data.get('pitching', {}) if stats_data else {}
    
    is_pitcher = player['position'] == 'P' or player.get('type') == 'pitcher'
    is_two_way = player.get('type') == 'two-way'
    
    md_content = f"""# {player_name} 球探报告

> **Los Angeles Dodgers #{player.get('number', '—')} | {player['position']}**
> 
> 报告生成时间：2026-07-09

---

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| **姓名** | {player_name} |
| **背号** | #{player.get('number', '—')} |
| **位置** | {player['position']} |
| **状态** | {player.get('status', '活跃')} |
| **球队** | Los Angeles Dodgers |

"""

    if is_pitcher or is_two_way:
        if pitching:
            md_content += f"""
## 📊 投球数据

| 统计 | 数值 |
|------|------|
| **胜** | {pitching.get('wins', 0)} |
| **败** | {pitching.get('losses', 0)} |
| **ERA** | {pitching.get('era', '—')} |
| **IP** | {pitching.get('innings_pitched', '—')} |
| **K** | {pitching.get('strikeouts', 0)} |
| **BB** | {pitching.get('walks', 0)} |
| **WHIP** | {pitching.get('whip', '—')} |
| **K/9** | {pitching.get('strikeouts_per_9', '—')} |

"""

    if batting and (not is_pitcher or is_two_way):
        md_content += f"""
## 📊 打击数据

| 统计 | 数值 |
|------|------|
| **G** | {batting.get('games_played', 0)} |
| **AVG** | {batting.get('avg', '—')} |
| **OPS** | {batting.get('ops', '—')} |
| **HR** | {batting.get('home_runs', 0)} |
| **RBI** | {batting.get('rbi', 0)} |
| **SB** | {batting.get('stolen_bases', 0)} |

"""

    md_content += """
---

*数据来源：MLB Stats API*
*详细分析版本待补充*
"""

    md_path = os.path.join(output_dir, f"{player_slug}-scouting-report.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return md_path

def main():
    # 合并所有球员
    all_players = [
        # 活跃投手
        {"name": "Jack Dreyer", "position": "P", "number": "86", "type": "pitcher", "status": "活跃"},
        {"name": "Edgardo Henriquez", "position": "P", "number": "60", "type": "pitcher", "status": "活跃"},
        {"name": "Kyle Hurt", "position": "P", "number": "63", "type": "pitcher", "status": "活跃"},
        {"name": "Will Klein", "position": "P", "number": "61", "type": "pitcher", "status": "活跃"},
        {"name": "Eric Lauer", "position": "P", "number": "33", "type": "pitcher", "status": "活跃"},
        {"name": "Evan Phillips", "position": "P", "number": "59", "type": "pitcher", "status": "活跃"},
        {"name": "Tanner Scott", "position": "P", "number": "66", "type": "pitcher", "status": "活跃"},
        {"name": "Emmet Sheehan", "position": "P", "number": "80", "type": "pitcher", "status": "活跃"},
        {"name": "Brock Stewart", "position": "P", "number": "41", "type": "pitcher", "status": "活跃"},
        {"name": "Alex Vesia", "position": "P", "number": "51", "type": "pitcher", "status": "活跃"},
        {"name": "Justin Wrobleski", "position": "P", "number": "70", "type": "pitcher", "status": "活跃"},
        {"name": "Yoshinobu Yamamoto", "position": "P", "number": "18", "type": "pitcher", "status": "活跃"},
        # 双向
        {"name": "Shohei Ohtani", "position": "DH/P", "number": "17", "type": "two-way", "status": "活跃"},
        # 捕手
        {"name": "Eliezer Alfonzo", "position": "C", "number": "64", "status": "活跃"},
        {"name": "Dalton Rushing", "position": "C", "number": "68", "status": "活跃"},
        # 内野手
        {"name": "Mookie Betts", "position": "IF/OF", "number": "50", "status": "活跃"},
        {"name": "Alex Freeland", "position": "IF", "number": "76", "status": "活跃"},
        {"name": "Freddie Freeman", "position": "1B", "number": "5", "status": "活跃"},
        {"name": "Max Muncy", "position": "3B", "number": "13", "status": "活跃"},
        {"name": "Miguel Rojas", "position": "SS", "number": "72", "status": "活跃"},
        # 外野手
        {"name": "Alex Call", "position": "OF", "number": "12", "status": "活跃"},
        {"name": "Tommy Edman", "position": "OF/IF", "number": "25", "status": "活跃"},
        {"name": "Teoscar Hernandez", "position": "OF", "number": "37", "status": "活跃"},
        {"name": "Andy Pages", "position": "OF", "number": "44", "status": "活跃"},
        {"name": "Kyle Tucker", "position": "OF", "number": "23", "status": "活跃"},
        # IL球员
        {"name": "Will Smith", "position": "C", "number": "16", "status": "IL-10"},
        {"name": "Enrique Hernandez", "position": "IF", "number": "8", "status": "IL-10"},
        {"name": "Blake Treinen", "position": "P", "number": "49", "type": "pitcher", "status": "IL-15"},
        {"name": "Ben Casparius", "position": "P", "number": "78", "type": "pitcher", "status": "IL-60"},
        {"name": "Tyler Glasnow", "position": "P", "number": "31", "type": "pitcher", "status": "IL-60"},
        {"name": "Brusdar Graterol", "position": "P", "number": "48", "type": "pitcher", "status": "IL-60"},
        {"name": "Edwin Diaz", "position": "P", "number": "3", "type": "pitcher", "status": "IL-60"},
        {"name": "Landon Knack", "position": "P", "number": "96", "type": "pitcher", "status": "IL-60"},
        {"name": "Bobby Miller", "position": "P", "number": "28", "type": "pitcher", "status": "IL-60"},
        {"name": "Blake Snell", "position": "P", "number": "7", "type": "pitcher", "status": "IL-60"},
        {"name": "Gavin Stone", "position": "P", "number": "35", "type": "pitcher", "status": "IL-60"},
        {"name": "Jake Cousins", "position": "P", "number": "—", "type": "pitcher", "status": "IL-60"},
        # 小联盟
        {"name": "Charlie Barnes", "position": "P", "number": "57", "type": "pitcher", "status": "Minors"},
        {"name": "Nick Frasso", "position": "P", "number": "—", "type": "pitcher", "status": "Minors"},
        {"name": "Paul Gervase", "position": "P", "number": "65", "type": "pitcher", "status": "Minors"},
        {"name": "Ronan Kopp", "position": "P", "number": "83", "type": "pitcher", "status": "Minors"},
        {"name": "Chayce McDermott", "position": "P", "number": "62", "type": "pitcher", "status": "Minors"},
        {"name": "Wyatt Mills", "position": "P", "number": "58", "type": "pitcher", "status": "Minors"},
        {"name": "River Ryan", "position": "P", "number": "77", "type": "pitcher", "status": "Minors"},
        {"name": "Hyeseong Kim", "position": "IF", "number": "6", "status": "Minors"},
        {"name": "Alek Thomas", "position": "OF", "number": "5", "status": "Minors"},
        {"name": "Ryan Ward", "position": "OF", "number": "67", "status": "Minors"},
    ]
    
    print("=" * 70)
    print("Dodgers Complete Scouting Report Generator")
    print("=" * 70)
    print(f"\nTotal players: {len(all_players)}\n")
    
    success_count = 0
    failed_players = []
    
    for i, player in enumerate(all_players, 1):
        player_name = player['name']
        player_slug = player_name.lower().replace(' ', '-')
        output_dir = os.path.join(OUTPUT_BASE, player_slug)
        os.makedirs(output_dir, exist_ok=True)
        
        status_icon = "[IL]" if player['status'].startswith('IL') else "[MIN]" if player['status'] == 'Minors' else "[ACT]"
        print(f"[{i:2d}/{len(all_players)}] {status_icon} {player_name:<25} ... ", end="", flush=True)
        
        try:
            # 获取统计数据
            stats_data = get_player_stats(player_name)
            
            # 生成HTML报告
            html_path = generate_html_report(player, stats_data, output_dir)
            
            # 生成Markdown报告
            md_path = generate_markdown_report(player, stats_data, output_dir)
            
            print(f"OK (HTML + MD)")
            success_count += 1
            
            time.sleep(0.5)  # 避免请求过快
            
        except Exception as e:
            print(f"FAIL: {str(e)[:50]}")
            failed_players.append(player_name)
    
    print("\n" + "=" * 70)
    print(f"Completed: {success_count}/{len(all_players)}")
    if failed_players:
        print(f"Failed ({len(failed_players)}): {', '.join(failed_players)}")
    print("=" * 70)

if __name__ == "__main__":
    main()
