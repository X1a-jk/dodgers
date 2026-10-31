players = ['edwin-diaz','jonathan-hernandez','enrique-hernandez','teoscar-hernandez','seth-halvorsen']
for p in players:
    html = open(f'D:/baseball/report/{p}/{p}-scouting-report.html',encoding='utf-8').read()
    header_end = html.split('<div class="header">')[1]
    hero = header_end.split('<div class="player-card">')[0]
    has_rc = 'report_cover' in hero
    has_og_hero = 'overall_grades' in hero
    grades_parts = html.split('<h2>📊 综合评分</h2>')
    if len(grades_parts) > 1:
        grades_section = grades_parts[1].split('<div class="stats-grid">')[0]
        has_og_grades = 'overall_grades' in grades_section
    else:
        has_og_grades = False
    print(f'{p}: hero_report_cover={has_rc}, hero_overall_grades={has_og_hero}, grades_section_overall_grades={has_og_grades}')
