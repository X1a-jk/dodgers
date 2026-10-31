import re
import os
import sys

def md_to_html(md_content, player_name, title, input_path="", header_bg="#005A9C"):
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e0e0e0;
            line-height: 1.8;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(90deg, {header_bg} 0%, #1a5490 50%, {header_bg} 100%);
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }}
        .header h1 {{ font-size: 2.5em; color: #fff; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); margin-bottom: 10px; }}
        .header .subtitle {{ font-size: 1.1em; color: #e0e0e0; font-style: italic; }}
        .section {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
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
            font-size: 1.6em;
            border-bottom: 2px solid #4fc3f7;
            padding-bottom: 10px;
        }}
        .section h3 {{
            color: #4fc3f7;
            margin: 20px 0 12px 0;
            font-size: 1.2em;
        }}
        .section p {{ margin-bottom: 12px; }}
        .section ul {{ margin-left: 25px; margin-bottom: 15px; }}
        .section li {{ margin-bottom: 8px; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 0.95em;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        th {{
            background: rgba(0, 90, 156, 0.3);
            color: #4fc3f7;
            font-weight: bold;
        }}
        tr:hover {{ background: rgba(255, 255, 255, 0.05); }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .chart-grid img {{
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #90a4ae;
            font-size: 0.9em;
        }}
        blockquote {{
            border-left: 4px solid #4fc3f7;
            padding-left: 15px;
            margin: 15px 0;
            color: #b0bec5;
            font-style: italic;
        }}
        strong {{ color: #4fc3f7; }}
        hr {{ border: none; border-top: 1px solid rgba(255, 255, 255, 0.1); margin: 20px 0; }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8em; }}
            .chart-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚾ {player_name}</h1>
            <p class="subtitle">{title}</p>
        </div>
"""

    # Convert markdown content
    lines = md_content.split('\n')
    in_table = False
    in_list = False
    table_lines = []
    list_items = []
    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith('# ') and i == 0:
            # Skip main title, already in header
            i += 1
            continue
        if line.startswith('> '):
            html += f'<blockquote>{line[2:]}</blockquote>\n'
            i += 1
            continue
        if line.startswith('---'):
            html += '<hr>\n'
            i += 1
            continue
        if line.startswith('## '):
            if in_list:
                html += '<ul>\n' + '\n'.join(f'<li>{item}</li>' for item in list_items) + '\n</ul>\n'
                list_items = []
                in_list = False
            if in_table:
                html += render_table(table_lines)
                table_lines = []
                in_table = False
            title_text = line[3:]
            html += f'<div class="section">\n<h2>{title_text}</h2>\n'
            i += 1
            continue
        if line.startswith('### '):
            html += f'<h3>{line[4:]}</h3>\n'
            i += 1
            continue
        if line.startswith('- ') or line.startswith('- ✅') or line.startswith('- ❌'):
            if in_table:
                html += render_table(table_lines)
                table_lines = []
                in_table = False
            item = line[2:]
            item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
            list_items.append(item)
            in_list = True
            i += 1
            continue
        if in_list and (line.strip() == '' or not line.startswith('- ')):
            if line.strip() != '' and not line.startswith('|'):
                html += '<ul>\n' + '\n'.join(f'<li>{item}</li>' for item in list_items) + '\n</ul>\n'
                list_items = []
                in_list = False
            elif line.strip() == '':
                html += '<ul>\n' + '\n'.join(f'<li>{item}</li>' for item in list_items) + '\n</ul>\n'
                list_items = []
                in_list = False
        if line.startswith('|'):
            if in_list:
                html += '<ul>\n' + '\n'.join(f'<li>{item}</li>' for item in list_items) + '\n</ul>\n'
                list_items = []
                in_list = False
            table_lines.append(line)
            in_table = True
            i += 1
            continue
        if in_table and not line.startswith('|'):
            html += render_table(table_lines)
            table_lines = []
            in_table = False

        if line.strip() == '':
            i += 1
            continue

        para = line
        para = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', para)
        html += f'<p>{para}</p>\n'
        i += 1

    if in_list:
        html += '<ul>\n' + '\n'.join(f'<li>{item}</li>' for item in list_items) + '\n</ul>\n'
    if in_table:
        html += render_table(table_lines)

    # Close last section if open
    html += '</div>\n'

    # Add chart gallery if images exist
    if input_path:
        chart_files = []
        input_dir = os.path.dirname(input_path)
        for fname in sorted(os.listdir(input_dir)):
            if fname.endswith('.png') and not fname.endswith('_cover.png'):
                chart_files.append(fname)
        if chart_files:
            html += '<div class="section">\n<h2>📈 数据图表</h2>\n<div class="chart-grid">\n'
            for fname in chart_files:
                html += f'<div><img src="{fname}" alt="{fname}"></div>\n'
            html += '</div>\n</div>\n'

    html += """
        <div class="footer">
            <p>⚾ 洛杉矶道奇队球探报告</p>
            <p>数据来源：MLB.com | Baseball Savant | MLB Stats API</p>
        </div>
    </div>
</body>
</html>
"""
    return html

def render_table(lines):
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.split('|')]
        cells = [c for c in cells if c]
        if all(set(c) <= set('-:| ') for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return ''
    html = '<table>\n<thead>\n<tr>'
    for cell in rows[0]:
        html += f'<th>{format_inline(cell)}</th>'
    html += '</tr>\n</thead>\n<tbody>\n'
    for row in rows[1:]:
        html += '<tr>'
        for cell in row:
            html += f'<td>{format_inline(cell)}</td>'
        html += '</tr>\n'
    html += '</tbody>\n</table>\n'
    return html

def format_inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python md_to_html.py <input.md> <output.html> <player_name>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    player_name = sys.argv[3]

    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    title_match = re.search(r'^# (.+?) 球探报告', md_content, re.MULTILINE)
    title = title_match.group(1) + ' Scouting Report' if title_match else 'Scouting Report'

    html = md_to_html(md_content, player_name, title, input_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated: {output_path}")
