players = ['edwin-diaz','jonathan-hernandez','enrique-hernandez','teoscar-hernandez','seth-halvorsen']
for p in players:
    html = open(f'D:/baseball/report/{p}/{p}-scouting-report.html',encoding='utf-8').read()
    parts = html.split('<div class="player-card">')
    if len(parts) > 1:
        snippet = parts[1].split('<div class="section">')[0]
        print(f'{p}: player-info count = {snippet.count("player-info")}, starts with section? {snippet.strip().startswith("<div")}')
    else:
        print(f'{p}: no player-card found')
