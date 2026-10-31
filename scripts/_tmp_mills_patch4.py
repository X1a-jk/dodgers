import io
path = r'D:\baseball\report\wyatt-mills\wyatt-mills-scouting-report.html'
t = io.open(path, encoding='utf-8').read()
t = t.replace('<li>2026 年 BB/9 14.54，控球严重失控</li>', '<li>2026 年 BB/9 13.28，控球严重失控</li>', 1)
t = t.replace('<li>WHIP 2.31，被上垒率极高</li>', '<li>WHIP 2.21，被上垒率极高</li>', 1)
io.open(path, 'w', encoding='utf-8').write(t)
print('done')
