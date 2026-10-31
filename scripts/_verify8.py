# -*- coding: utf-8 -*-
"""验证剩余 8 人 + 取数"""
import io, json, os, re

BASE = r'D:\baseball'
fs = json.load(open(os.path.join(BASE, 'data', 'final-stats.json'), encoding='utf-8'))

P = {
 'chuckie-robinson': {'id':'642020','kind':'hit'},
 'alek-thomas':      {'id':'677950','kind':'hit'},
 'charlie-barnes':   {'id':'656212','kind':'pitch'},
 'cole-irvin':       {'id':'608344','kind':'pitch'},
 'ryan-ward':        {'id':'669899','kind':'hit'},
 'wyatt-mills':      {'id':'670090','kind':'pitch'},
 'jake-eder':        {'id':'671109','kind':'pitch'},
 'chayce-mcdermott': {'id':'694646','kind':'pitch'},
}
out = io.open(os.path.join(BASE,'scripts','_verify8.txt'),'w',encoding='utf-8')
for slug, info in P.items():
    out.write('===== %s (id=%s) =====\n' % (slug, info['id']))
    grp = 'pitching_2026' if info['kind']=='pitch' else 'hitting_2026'
    fsd = fs.get(grp,{}).get(info['id'])
    if fsd:
        if info['kind']=='pitch':
            out.write('FS26: G=%s GS=%s W=%s L=%s ERA=%s IP=%s WHIP=%s K=%s BB=%s HR=%s H=%s\n' % (
                fsd.get('gamesPlayed'), fsd.get('gamesStarted'), fsd.get('wins'), fsd.get('losses'),
                fsd.get('era'), fsd.get('inningsPitched'), fsd.get('whip'),
                fsd.get('strikeOuts'), fsd.get('baseOnBalls'), fsd.get('homeRuns'), fsd.get('hits')))
        else:
            out.write('FS26: G=%s AVG=%s OBP=%s SLG=%s OPS=%s HR=%s RBI=%s BB=%s SO=%s AB=%s H=%s\n' % (
                fsd.get('gamesPlayed'), fsd.get('avg'), fsd.get('obp'), fsd.get('slg'), fsd.get('ops'),
                fsd.get('homeRuns'), fsd.get('rbi'), fsd.get('baseOnBalls'), fsd.get('strikeOuts'),
                fsd.get('atBats'), fsd.get('hits')))
            try:
                ops=float(fsd['ops']); diff=abs(ops-float(fsd['obp'])-float(fsd['slg']))
                out.write('OPS identity diff=%.4f\n' % diff)
            except Exception as e:
                out.write('OPS check err %s\n' % e)
    else:
        out.write('FS26: NO ENTRY\n')
    g25 = 'pitching_2025' if info['kind']=='pitch' else 'hitting_2025'
    out.write('FS25: %s\n' % ('YES' if fs.get(g25,{}).get(info['id']) else 'no'))
    hp = os.path.join(BASE,'report',slug,'%s-scouting-report.html' % slug)
    if os.path.exists(hp):
        t = io.open(hp,encoding='utf-8').read()
        out.write('html dates: %s\n' % re.findall(r'报告生成时间：([^<|]+)', t))
        if fsd:
            if info['kind']=='pitch':
                for key,lab in [('era','ERA'),('inningsPitched','IP'),('whip','WHIP')]:
                    v = str(fsd.get(key))
                    if v != 'None':
                        out.write('  html has %s=%s: %s\n' % (lab, v, v in t))
            else:
                for key in ['avg','obp','slg']:
                    v = fsd.get(key)
                    if v:
                        out.write('  html has %s=%s: %s\n' % (key, v, v in t))
    out.write('\n')
out.close()
print('done')
