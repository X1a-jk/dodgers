import matplotlib.pyplot as plt
import numpy as np
import os

output_dir = r'D:\baseball\report\mookie-betts'
os.makedirs(output_dir, exist_ok=True)

# 统一风格参数
BG_COLOR = '#1a1a2e'
TITLE_COLOR = 'white'
SUBTITLE_COLOR = '#4fc3f7'
REPORT_COLOR = '#ff9800'
STAT_VALUE_COLOR = '#4fc3f7'
STAT_LABEL_COLOR = '#90a4ae'

# ========== 1. 封面图 (Yamamoto风格) ==========
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

ax.text(0.5, 0.85, 'Mookie Betts', fontsize=32, fontweight='bold', ha='center', 
        color=TITLE_COLOR, transform=ax.transAxes)
ax.text(0.5, 0.75, 'Los Angeles Dodgers #50 | SS/OF', fontsize=18, ha='center', 
        color=SUBTITLE_COLOR, transform=ax.transAxes)
ax.text(0.5, 0.65, 'SCOUTING REPORT 2026', fontsize=22, fontweight='bold', ha='center', 
        color=REPORT_COLOR, transform=ax.transAxes)

stats_data = [
    ('AVG', '.263'), ('HR', '121+'), ('SB', '70+'), ('OPS', '.850'),
    ('OBP', '.360'), ('SLG', '.470'), ('MVP', '2018'), ('Age', '33')
]

y_pos = 0.45
for i, (label, value) in enumerate(stats_data):
    x_pos = 0.15 + (i % 4) * 0.23
    if i >= 4:
        y_pos = 0.25
    ax.text(x_pos, y_pos, value, fontsize=26, fontweight='bold', ha='center',
            color=STAT_VALUE_COLOR, transform=ax.transAxes)
    ax.text(x_pos, y_pos - 0.08, label, fontsize=12, ha='center',
            color=STAT_LABEL_COLOR, transform=ax.transAxes)

ax.text(0.5, 0.08, '2018 AL MVP | 2019 Silver Slugger | 2020 WS Champion', fontsize=14, ha='center',
        color='#90a4ae', transform=ax.transAxes, style='italic')
ax.text(0.5, 0.02, 'Generated: 2026-07-11 | Data: MLB.com, MLB Stats API', 
        fontsize=10, ha='center', color='#666', transform=ax.transAxes)

plt.savefig(os.path.join(output_dir, 'betts_report_cover.png'), dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

# ========== 2. 赛季对比雷达图 ==========
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))

categories = ['AVG', 'OBP', 'SLG', 'OPS', 'HR/162', 'SB/162', 'R/162', 'RBI/162']
N = len(categories)

# Normalized to 0-100 scale
seasons = {
    '2018 (BOS - MVP)': [100, 98, 95, 95, 85, 95, 95, 75],
    '2023 (LAD)': [85, 90, 88, 88, 95, 60, 95, 95],
    '2024 (LAD)': [80, 82, 75, 78, 70, 70, 70, 70],
    '2025 (LAD)': [72, 72, 65, 68, 70, 55, 70, 75],
    '2026 (LAD)': [65, 65, 68, 68, 65, 45, 60, 65]
}

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

colors = ['#FFD700', '#1E90FF', '#FF6347', '#32CD32', '#808080']
linestyles = ['-', '-', '-', '-', '--']

for (season, values), color, ls in zip(seasons.items(), colors, linestyles):
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, label=season, color=color, linestyle=ls)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=10)
ax.set_ylim(0, 100)
ax.set_title('Mookie Betts - Season Comparison\n(2018-2026)', size=16, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
ax.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'betts_season_comparison.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ========== 3. 职业生涯趋势图 ==========
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

seasons_list = ['2018', '2023', '2024', '2025', '2026']
avg = [.346, .307, .289, .258, .238]
obp = [.438, .408, .372, .326, .298]
slg = [.640, .579, .491, .406, .424]
ops = [1.078, .987, .863, .732, .722]

ax1.plot(seasons_list, avg, 'o-', color='#1E90FF', linewidth=2, markersize=8)
ax1.axhline(y=.250, color='gray', linestyle='--', alpha=0.5)
ax1.set_title('Batting Average', fontweight='bold')
ax1.set_ylim(.200, .370)
ax1.grid(True, alpha=0.3)

ax2.plot(seasons_list, obp, 'o-', color='#32CD32', linewidth=2, markersize=8)
ax2.axhline(y=.350, color='gray', linestyle='--', alpha=0.5)
ax2.set_title('On-Base Percentage', fontweight='bold')
ax2.set_ylim(.280, .460)
ax2.grid(True, alpha=0.3)

ax3.plot(seasons_list, slg, 'o-', color='#FF6347', linewidth=2, markersize=8)
ax3.axhline(y=.400, color='gray', linestyle='--', alpha=0.5)
ax3.set_title('Slugging Percentage', fontweight='bold')
ax3.set_ylim(.350, .700)
ax3.grid(True, alpha=0.3)

ax4.plot(seasons_list, ops, 'o-', color='#FFD700', linewidth=2, markersize=8)
ax4.axhline(y=.750, color='gray', linestyle='--', alpha=0.5)
ax4.set_title('OPS', fontweight='bold')
ax4.set_ylim(.650, 1.100)
ax4.grid(True, alpha=0.3)

fig.suptitle('Mookie Betts - Career Stats Trend (2018-2026)', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'betts_career_trends.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ========== 4. 综合评分雷达图 ==========
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))

categories = ['Hit', 'Power', 'Plate\nDiscipline', 'Speed', 'Defense', 'Arm', 'Leadership', 'Versatility']
values = [65, 65, 70, 65, 70, 60, 70, 75]
values += values[:1]

N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

ax.plot(angles, values, 'o-', linewidth=2, color='#1E90FF', markersize=8)
ax.fill(angles, values, alpha=0.25, color='#1E90FF')

for angle, value in zip(angles[:-1], values[:-1]):
    ax.text(angle, value + 3, str(value), ha='center', va='center', fontweight='bold', fontsize=10, color='darkblue')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=10, fontweight='bold')
ax.set_ylim(20, 80)
ax.set_yticks([20, 30, 40, 50, 60, 70, 80])
ax.set_yticklabels(['20', '30', '40', '50', '60', '70', '80'], color='grey', size=8)
ax.set_title('Mookie Betts - Scouting Grades\n(20-80 Scale)', size=16, fontweight='bold', pad=20)
ax.grid(True)
ax.axhspan(60, 80, alpha=0.05, color='green')
ax.axhspan(50, 60, alpha=0.05, color='yellow')
ax.axhspan(0, 50, alpha=0.05, color='red')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'betts_overall_grades.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"All charts saved to {output_dir}")
