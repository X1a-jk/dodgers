import io
path = r'D:\baseball\report\wyatt-mills\wyatt-mills-scouting-report.html'
t = io.open(path, encoding='utf-8').read()
a1 = '<div class="label">状态</div><div class="value">Minors</div>'
b1 = '<div class="label">状态</div><div class="value">已离队（8/6 被国民捡走、9/17 被释出）</div>'
print('status found:', a1 in t)
t = t.replace(a1, b1, 1)
old = ('<td class="warning">2026</td>\n <td>5</td>\n <td>0</td>\n <td>0-0</td>\n <td>6.23</td>\n '
       '<td>4.1</td>\n <td>4</td>\n <td>7</td>\n <td>2.31</td>\n <td>8.31</td>')
new = ('<td class="warning">2026</td>\n <td>6</td>\n <td>0</td>\n <td>0-0</td>\n <td>5.68</td>\n '
       '<td>6.1</td>\n <td>5</td>\n <td>9</td>\n <td>2.21</td>\n <td>7.38</td>')
print('row found:', old in t)
t = t.replace(old, new, 1)
io.open(path, 'w', encoding='utf-8').write(t)
print('saved')
