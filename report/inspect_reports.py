#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pathlib import Path

base = Path('D:/baseball/report')
players = [d for d in base.iterdir() if d.is_dir() and (d / f'{d.name}-scouting-report.html').exists()]

def extract_sections(html):
    pattern = re.compile(r'<div class="section"[^>]*>.*?<h2>(.*?)</h2>', re.DOTALL)
    return pattern.findall(html)

out_lines = []
out_lines.append(f'Found {len(players)} player reports\n')
out_lines.append(f'{"Player":<35s} | {"Size":>7s} | CH | Intro | Career | pvel')
out_lines.append('-' * 90)
for p in sorted(players, key=lambda x: x.name):
    html_path = p / f'{p.name}-scouting-report.html'
    html = html_path.read_text(encoding='utf-8')
    sections = extract_sections(html)
    has_pitch_arsenal_img = 'pitch_velocities.png' in html
    has_career_highlight = 'career-highlight' in html
    has_player_intro = '球员简介' in html
    has_career = '职业生涯亮点' in html
    size = html_path.stat().st_size
    out_lines.append(f'{p.name:<35s} | {size:>7d} | {"Y" if has_career_highlight else "N"}  | {"Y" if has_player_intro else "N"}     | {"Y" if has_career else "N"}      | {"Y" if has_pitch_arsenal_img else "N"}')
    for s in sections:
        out_lines.append(f'   - {s}')
    out_lines.append('')

Path('report_inspection.txt').write_text('\n'.join(out_lines), encoding='utf-8')
print('Results written to report_inspection.txt')
