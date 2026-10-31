# -*- coding: utf-8 -*-
"""NLCS G4 补赛果 + 移除未打 slot（对齐 NLDS 约定）"""
import json, io, shutil, os

p = r'D:\baseball\data\postseason.json'
d = json.load(io.open(p, encoding='utf-8'))
cs = d['rounds']['NL']['cs']
games = cs['games']

g4 = [g for g in games if g['gamePk'] == 849810]
assert len(g4) == 1, 'G4 slot not found'
g4 = g4[0]
g4['status'] = 'Final'
g4['final'] = True
g4['away']['score'] = 6
g4['home']['score'] = 4
g4['winnerSide'] = 'away'

cs['games'] = [g for g in games if g['final'] or g['gamePk'] == 849810]
cs['wins'] = {'158': 4}
cs['gamesPlayed'] = 4

io.open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))

# 同步存档快照
snap = r'D:\baseball\seasons\2026\snapshots\postseason.json'
shutil.copyfile(p, snap)
print('NLCS patched: games =', [(g['gamePk'], g['away']['score'], g['home']['score']) for g in cs['games']])
print('wins:', cs['wins'], '| gamesPlayed:', cs['gamesPlayed'])
print('snapshot synced:', os.path.exists(snap))
