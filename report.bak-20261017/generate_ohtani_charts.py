import matplotlib.pyplot as plt
import numpy as np
import os

output_dir = r'D:\baseball\report\shohei-ohtani'
os.makedirs(output_dir, exist_ok=True)

# 1. 封面图
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')

ax.text(0.5, 0.85, 'Shohei Ohtani', fontsize=32, fontweight='bold', ha='center', 
        color='white', transform=ax.transAxes)
ax.text(0.5, 0.75, 'Los Angeles Dodgers #17 | Two-Way Player | L/R', fontsize=18, ha='center', 
        color='#4fc3f7', transform=ax.transAxes)
ax.text(0.5, 0.65, 'SCOUTING REPORT 2026', fontsize=22, fontweight='bold', ha='center', 
        color='#ff9800', transform=ax.transAxes)

stats_data = [
    ('ERA', '1.79'), ('W-L', '8-2'), ('K', '95'), ('IP', '85.2'),
    ('AVG', '.290'), ('HR', '20'), ('OPS', '.939'), ('SB', '6')
]

y_pos = 0.45
for i, (label, value) in enumerate(stats_data):
    x_pos = 0.15 + (i % 4) * 0.23
    if i >= 4:
        y_pos = 0.25
    ax.text(x_pos, y_pos, value, fontsize=26, fontweight='bold', ha='center',
            color='#4fc3f7', transform=ax.transAxes)
    ax.text(x_pos, y_pos - 0.08, label, fontsize=12, ha='center',
            color='#90a4ae', transform=ax.transAxes)

ax.text(0.5, 0.08, 'Showtime | MLB MVP x3 | World Series Champion', fontsize=14, ha='center',
        color='#90a4ae', transform=ax.transAxes, style='italic')
ax.text(0.5, 0.02, 'Generated: 2026-07-09 | Data: MLB.com, MLB Stats API', 
        fontsize=10, ha='center', color='#666', transform=ax.transAxes)

plt.savefig(os.path.join(output_dir, 'ohtani_report_cover.png'), dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()

# 2. 投球赛季对比
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 2025 vs 2026 投球数据
pitching_stats = ['ERA', 'WHIP', 'K/9', 'W', 'IP', 'BB/9']
pitching_2025 = [2.87, 1.04, 11.87, 1, 47.0, 1.72]
pitching_2026 = [1.79, 0.95, 9.98, 8, 85.2, 2.73]

x = np.arange(len(pitching_stats))
width = 0.35

bars1 = ax1.bar(x - width/2, pitching_2025, width, label='2025', color='#4fc3f7', alpha=0.8)
bars2 = ax1.bar(x + width/2, pitching_2026, width, label='2026', color='#ff9800', alpha=0.8)
ax1.set_xlabel('Statistics', fontsize=12, fontweight='bold')
ax1.set_ylabel('Value', fontsize=12, fontweight='bold')
ax1.set_title('Pitching: 2025 vs 2026', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(pitching_stats, fontsize=10)
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# 打击数据 2026
batting_stats = ['AVG', 'OBP', 'SLG', 'OPS', 'HR/100', 'RBI/100']
batting_values = [290, 405, 534, 939, 22, 63]  # scaled for display
x2 = np.arange(len(batting_stats))
bars3 = ax2.bar(x2, batting_values, color='#4caf50', alpha=0.8)
ax2.set_xlabel('Statistics', fontsize=12, fontweight='bold')
ax2.set_title('Hitting 2026 (scaled)', fontsize=14, fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(batting_stats, fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')

for i, v in enumerate(batting_values):
    ax2.text(i, v + 15, f'{v:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'ohtani_season_comparison.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 3. 综合评分雷达图
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

categories = ['Fastball', 'Splitter', 'Slider', 'Control', 'Command', 'Mental', 'Hitting', 'Power', 'Speed', 'Defense']
values = [70, 75, 55, 65, 70, 75, 70, 75, 60, 50]
values += values[:1]

N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

ax.plot(angles, values, 'o-', linewidth=2, color='#4fc3f7', markersize=8)
ax.fill(angles, values, alpha=0.3, color='#4fc3f7')

for angle, value in zip(angles[:-1], values[:-1]):
    ax.text(angle, value + 3, str(value), ha='center', va='center', fontweight='bold', fontsize=10)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=10)
ax.set_ylim(0, 85)
ax.set_title('Shohei Ohtani Overall Grades (20-80 Scale)', size=14, fontweight='bold', pad=20)
ax.grid(True)
ax.axhspan(60, 80, alpha=0.1, color='green')
ax.axhspan(50, 60, alpha=0.1, color='yellow')
ax.axhspan(0, 50, alpha=0.1, color='red')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'ohtani_overall_grades.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print(f"All charts saved to {output_dir}")
print("Files:")
print("  - ohtani_report_cover.png")
print("  - ohtani_season_comparison.png")
print("  - ohtani_overall_grades.png")
