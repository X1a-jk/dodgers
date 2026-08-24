import matplotlib.pyplot as plt
import numpy as np
import os

output_dir = r'D:\baseball\report\yoshinobu-yamamoto'
os.makedirs(output_dir, exist_ok=True)

# 1. 封面图
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')

ax.text(0.5, 0.85, 'Yoshinobu Yamamoto', fontsize=32, fontweight='bold', ha='center', 
        color='white', transform=ax.transAxes)
ax.text(0.5, 0.75, 'Los Angeles Dodgers #18 | RHP', fontsize=18, ha='center', 
        color='#4fc3f7', transform=ax.transAxes)
ax.text(0.5, 0.65, 'SCOUTING REPORT 2026', fontsize=22, fontweight='bold', ha='center', 
        color='#ff9800', transform=ax.transAxes)

stats_data = [
    ('ERA', '2.49'), ('W-L', '9-5'), ('K', '100'), ('IP', '104.2'),
    ('WHIP', '0.88'), ('K/9', '8.60'), ('BB/9', '1.81'), ('Age', '27')
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

ax.text(0.5, 0.08, 'NPB Triple Crown | 2023 WBC Champion | 2025 WS MVP', fontsize=14, ha='center',
        color='#90a4ae', transform=ax.transAxes, style='italic')
ax.text(0.5, 0.02, 'Generated: 2026-07-09 | Data: MLB.com, MLB Stats API', 
        fontsize=10, ha='center', color='#666', transform=ax.transAxes)

plt.savefig(os.path.join(output_dir, 'yamamoto_report_cover.png'), dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()

# 2. 赛季对比图
fig, ax = plt.subplots(figsize=(12, 6))

pitching_stats = ['ERA', 'WHIP', 'K/9', 'W', 'IP', 'BB/9']
pitching_2025 = [2.49, 0.99, 10.42, 12, 173.2, 3.06]
pitching_2026 = [2.49, 0.88, 8.60, 9, 104.2, 1.81]

x = np.arange(len(pitching_stats))
width = 0.35

bars1 = ax.bar(x - width/2, pitching_2025, width, label='2025', color='#4fc3f7', alpha=0.8)
bars2 = ax.bar(x + width/2, pitching_2026, width, label='2026', color='#ff9800', alpha=0.8)

ax.set_xlabel('Statistics', fontsize=12, fontweight='bold')
ax.set_ylabel('Value', fontsize=12, fontweight='bold')
ax.set_title('Yoshinobu Yamamoto: 2025 vs 2026 Pitching', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(pitching_stats)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'yamamoto_season_comparison.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 3. 综合评分雷达图
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

categories = ['Fastball', 'Curveball', 'Slider', 'Cutter', 'Control', 'Command', 'Stamina', 'Mental']
values = [60, 70, 55, 65, 65, 70, 65, 70]
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
ax.set_ylim(0, 80)
ax.set_title('Yoshinobu Yamamoto Overall Grades (20-80)', size=14, fontweight='bold', pad=20)
ax.grid(True)
ax.axhspan(60, 80, alpha=0.1, color='green')
ax.axhspan(50, 60, alpha=0.1, color='yellow')
ax.axhspan(0, 50, alpha=0.1, color='red')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'yamamoto_overall_grades.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print(f"All charts saved to {output_dir}")
