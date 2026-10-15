# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open(r'C:\Users\Junkai XIA\.openclaw\workspace\skills\mlb-daily-scores\fetch_mlb.py', encoding='utf-8').read()
for m in re.finditer(r'[^\n]*(?:gameType|schedule|gamePk|sportId)[^\n]*', t):
    print(m.group(0).strip()[:160])
