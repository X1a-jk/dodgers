#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from bs4 import BeautifulSoup

TARGETS = {
    'alex-call', 'alex-freeland', 'ben-casparius', 'blake-treinen', 'bobby-miller',
    'brock-stewart', 'brusdar-graterol', 'charlie-barnes', 'dalton-rushing',
    'edwin-diaz', 'eliezer-alfonzo', 'evan-phillips', 'gavin-stone', 'hyeseong-kim',
    'jack-dreyer', 'jake-cousins', 'kyle-hurt', 'landon-knack', 'nick-frasso',
    'paul-gervase', 'river-ryan', 'roki-sasaki', 'ryan-ward', 'will-klein'
}

base = Path(r'D:\baseball\report')
lines = []
for slug in sorted(TARGETS):
    html_path = base / slug / f'{slug}-scouting-report.html'
    html = html_path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    sub = soup.find('p', class_='subtitle')
    sub_text = sub.get_text(strip=True) if sub else 'NO SUBTITLE'
    h2s = [h.get_text(strip=True) for h in soup.find_all('h2')]
    lines.append(f'{slug:25s} | {sub_text}')
    lines.append(f'   sections: {h2s}')

Path('unify_check.txt').write_text('\n'.join(lines), encoding='utf-8')
print('written to unify_check.txt')
