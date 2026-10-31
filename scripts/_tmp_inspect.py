import io, re, sys
slug = sys.argv[1]
t = io.open(rf'D:\baseball\report\{slug}\{slug}-scouting-report.html', encoding='utf-8').read()
print('length:', len(t))
m = re.search(r'subtitle"?\s*>(.*?)</p>', t, re.S)
print('subtitle:', m.group(1).strip() if m else None)
i = t.find('报告生成时间')
print(re.sub(r'<[^>]+>', ' ', t[i:i+150]).strip())
for mm in re.finditer(r'stat-value[^>]*>([^<]*)</span><div class="stat-label">([^<]*)</div>', t):
    print('CARD:', mm.group(2), '=', mm.group(1))
rows = re.findall(r'<td[^>]*>([^<]*)</td>', t)
print('cells sample:', rows[:40])
