import re
h = open(r'D:\baseball\report\tommy-edman\tommy-edman-scouting-report.html', encoding='utf-8').read()
for i, m in enumerate(re.finditer(r'<table class="comparison-table">(.*?)</table>', h, re.S)):
    print(f'--- TABLE {i} ---')
    print(m.group(0))
    print()
# find h2 sections
for m in re.finditer(r'<h2>(.*?)</h2>', h):
    print('H2:', m.group(1))
