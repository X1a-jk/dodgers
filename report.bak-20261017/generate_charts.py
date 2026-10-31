import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 输出目录
output_dir = r'D:\baseball\report'
os.makedirs(output_dir, exist_ok=True)

# 1. 赛季数据对比雷达图
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

categories = ['ERA', 'WHIP', 'K/9', 'BB/9', 'HR/9', 'IP/GS']
N = len(categories)

# 2025赛季数据（标准化到0-100）
# ERA: 越低越好，4.46 -> 55
# WHIP: 越低越好，1.43 -> 55
# K/9: 越高越好，6.94 -> 45
# BB/9: 越低越好，5.45 -> 35
# HR/9: 越低越好，1.49 -> 55
# IP/GS: 越高越好，4.5 -> 45
values_2025 = [55, 55, 45, 35, 55, 45]
values_2025 += values_2025[:1]

# 2026赛季数据
# ERA: 5.33 -> 45
# WHIP: 1.36 -> 58
# K/9: 8.89 -> 65
# BB/9: 3.67 -> 55
# HR/9: 2.11 -> 40
# IP/GS: 5.1 -> 52
values_2026 = [45, 58, 65, 55, 40, 52]
values_2026 += values_2026[:1]

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

ax.plot(angles, values_2025, 'o-', linewidth=2, label='2025 Season', color='#4fc3f7')
ax.fill(angles, values_2025, alpha=0.25, color='#4fc3f7')
ax.plot(angles, values_2026, 'o-', linewidth=2, label='2026 Season', color='#ff9800')
ax.fill(angles, values_2026, alpha=0.25, color='#ff9800')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=12)
ax.set_ylim(0, 100)
ax.set_title('佐佐木朗希 赛季数据对比\nRoki Sasaki Season Comparison', size=16, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
ax.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'sasaki_season_comparison.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("[OK] Season comparison radar chart generated")

# 2. 投球武器库速度分布
fig, ax = plt.subplots(figsize=(12, 6))

pitches = ['Fastball\n(Four-Seam)', 'Splitter\n(Split-Finger)', 'Slider\n(Slider)', 'Curveball\n(Curveball)']
min_velo = [96, 87, 84, 78]
max_velo = [101, 91, 88, 82]
avg_velo = [(min_v + max_v) / 2 for min_v, max_v in zip(min_velo, max_velo)]

x = np.arange(len(pitches))
width = 0.35

bars1 = ax.bar(x - width/2, min_velo, width, label='Min Velocity', color='#4fc3f7', alpha=0.8)
bars2 = ax.bar(x + width/2, max_velo, width, label='Max Velocity', color='#ff9800', alpha=0.8)

# Add average line
for i, avg in enumerate(avg_velo):
    ax.plot([i - width/2, i + width/2], [avg, avg], 'r--', linewidth=2, alpha=0.7)
    ax.text(i, avg + 0.5, f'Avg: {avg:.1f}', ha='center', va='bottom', fontweight='bold', color='red')

ax.set_xlabel('Pitch Type', fontsize=12, fontweight='bold')
ax.set_ylabel('Velocity (mph)', fontsize=12, fontweight='bold')
ax.set_title('Roki Sasaki Pitch Arsenal Velocity Distribution', size=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(pitches)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Add background color zones
ax.axhspan(95, 102, alpha=0.1, color='green')
ax.axhspan(85, 95, alpha=0.1, color='yellow')
ax.axhspan(75, 85, alpha=0.1, color='orange')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'sasaki_pitch_velocities.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("[OK] Pitch arsenal velocity chart generated")

# 3. 2026赛季逐场表现趋势
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

games = ['G1\n03/30', 'G2\n04/05', 'G3\n04/12', 'G4\n04/19', 'G5\n04/25']
era_by_game = [2.25, 7.00, 6.23, 6.11, 6.35]
ip_by_game = [4.0, 5.0, 4.0, 4.2, 5.0]
k_by_game = [4, 5, 6, 2, 5]
bb_by_game = [2, 3, 5, 2, 1]

# ERA trend
ax1.plot(games, era_by_game, 'o-', linewidth=2, markersize=8, color='#f44336', label='ERA')
ax1.axhline(y=5.33, color='gray', linestyle='--', alpha=0.5, label='Season ERA (5.33)')
ax1.fill_between(range(len(games)), era_by_game, alpha=0.2, color='#f44336')
ax1.set_ylabel('ERA', fontsize=12, fontweight='bold')
ax1.set_title('2026 Season ERA Trend by Game', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# IP vs K/BB
ax2_twin = ax2.twinx()

bars = ax2.bar(games, ip_by_game, alpha=0.6, color='#4fc3f7', label='IP')
line1 = ax2_twin.plot(games, k_by_game, 'o-', color='#4caf50', linewidth=2, markersize=8, label='K')
line2 = ax2_twin.plot(games, bb_by_game, 's-', color='#ff9800', linewidth=2, markersize=8, label='BB')

ax2.set_ylabel('Innings Pitched (IP)', fontsize=12, fontweight='bold')
ax2_twin.set_ylabel('Strikeouts / Walks', fontsize=12, fontweight='bold')
ax2.set_title('IP vs Strikeouts and Walks', fontsize=14, fontweight='bold')

# Combine legends
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_twin.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'sasaki_game_trends.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("[OK] Game trends chart generated")

# 4. 综合评分雷达图
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

categories = ['Fastball', 'Splitter', 'Slider', 'Curveball', 
              'Control', 'Command', 'Mental', 'Stamina']
values = [70, 70, 55, 45, 45, 60, 65, 55]
values += values[:1]

N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

ax.plot(angles, values, 'o-', linewidth=2, color='#4fc3f7', markersize=8)
ax.fill(angles, values, alpha=0.3, color='#4fc3f7')

# Add score labels
for angle, value, cat in zip(angles[:-1], values[:-1], categories):
    ax.text(angle, value + 3, str(value), ha='center', va='center', fontweight='bold', fontsize=10)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=10)
ax.set_ylim(0, 80)
ax.set_title('Roki Sasaki Overall Grades (20-80 Scale)', size=14, fontweight='bold', pad=20)
ax.grid(True)

# Add grade zones
ax.axhspan(60, 80, alpha=0.1, color='green')
ax.axhspan(50, 60, alpha=0.1, color='yellow')
ax.axhspan(0, 50, alpha=0.1, color='red')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'sasaki_overall_grades.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("[OK] Overall grades radar chart generated")

# 5. 球探报告封面图
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')

# Background
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')

# Title
title_text = 'Roki Sasaki (佐佐木朗希)'
subtitle_text = 'Los Angeles Dodgers #11 | RHP'
report_text = 'SCOUTING REPORT 2026'

ax.text(0.5, 0.85, title_text, fontsize=32, fontweight='bold', ha='center', 
        color='white', transform=ax.transAxes)
ax.text(0.5, 0.75, subtitle_text, fontsize=18, ha='center', 
        color='#4fc3f7', transform=ax.transAxes)
ax.text(0.5, 0.65, report_text, fontsize=22, fontweight='bold', ha='center', 
        color='#ff9800', transform=ax.transAxes)

# Key stats display
stats_data = [
    ('ERA', '5.33'),
    ('W-L', '3-5'),
    ('K', '80'),
    ('IP', '81.0'),
    ('WHIP', '1.36'),
    ('AGE', '24')
]

y_pos = 0.45
for i, (label, value) in enumerate(stats_data):
    x_pos = 0.15 + (i % 3) * 0.35
    if i >= 3:
        y_pos = 0.25
    
    ax.text(x_pos, y_pos, value, fontsize=26, fontweight='bold', ha='center',
            color='#4fc3f7', transform=ax.transAxes)
    ax.text(x_pos, y_pos - 0.08, label, fontsize=12, ha='center',
            color='#90a4ae', transform=ax.transAxes)

# Bottom info
ax.text(0.5, 0.08, 'Monster of the Reiwa Era | 令和怪物', fontsize=14, ha='center',
        color='#90a4ae', transform=ax.transAxes, style='italic')
ax.text(0.5, 0.02, 'Generated: 2026-07-09 | Data: MLB.com, Baseball Savant, Fangraphs', 
        fontsize=10, ha='center', color='#666', transform=ax.transAxes)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'sasaki_report_cover.png'), dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()

print("[OK] Report cover generated")

print(f"\nAll charts generated successfully!")
print(f"Output directory: {output_dir}")
print("\nGenerated files:")
print("  1. sasaki_report_cover.png - Report cover")
print("  2. sasaki_season_comparison.png - Season comparison radar")
print("  3. sasaki_pitch_velocities.png - Pitch arsenal velocities")
print("  4. sasaki_game_trends.png - Game-by-game trends")
print("  5. sasaki_overall_grades.png - Overall grades radar")
