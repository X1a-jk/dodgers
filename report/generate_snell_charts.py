import matplotlib.pyplot as plt
import numpy as np
import os

# Create directory
output_dir = r'D:\baseball\report\blake-snell'
os.makedirs(output_dir, exist_ok=True)

# ===== 1. Season Comparison Radar Chart =====
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))

# Categories for radar chart
categories = ['ERA', 'K/9', 'WHIP', 'IP/G', 'W%', 'K-BB%']
N = len(categories)

# Data for different seasons (normalized to 0-100 scale)
# 2018 (Cy Young), 2023 (Cy Young), 2025 (Dodgers), 2026 (injured)
# ERA: lower is better, so we invert
# Normalize based on typical ranges
seasons = {
    '2018 (TB - Cy Young)': [90, 75, 92, 80, 95, 70],
    '2023 (SD - Cy Young)': [88, 82, 80, 85, 65, 70],
    '2024 (SF)': [75, 85, 82, 78, 65, 80],
    '2025 (LAD)': [82, 72, 65, 70, 55, 60],
    '2026 (LAD - injured)': [20, 85, 15, 20, 0, 40]  # Small sample
}

# Compute angle for each category
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

# Plot each season
for season, values in seasons.items():
    values += values[:1]
    if '2018' in season:
        ax.plot(angles, values, 'o-', linewidth=2, label=season, color='#1E90FF')
    elif '2023' in season:
        ax.plot(angles, values, 'o-', linewidth=2, label=season, color='#FFD700')
    elif '2025' in season:
        ax.plot(angles, values, 'o-', linewidth=2, label=season, color='#FF6347')
    elif '2026' in season:
        ax.plot(angles, values, 'o-', linewidth=1.5, label=season, color='#808080', linestyle='--')
    else:
        ax.plot(angles, values, 'o-', linewidth=2, label=season, color='#32CD32')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=11)
ax.set_ylim(0, 100)
ax.set_title('Blake Snell - Season Comparison\n(2018-2026)', size=16, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
ax.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'snell_season_comparison.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 2. Pitch Velocities Bar Chart =====
fig, ax = plt.subplots(figsize=(10, 6))

pitches = ['Four-Seam\nFastball', 'Curveball', 'Changeup', 'Slider']
velocities = [94, 79, 86, 84]  # Approximate average velocities
velo_ranges = [(92, 96), (77, 81), (84, 88), (82, 86)]  # Min/Max ranges

colors = ['#FF4500', '#4169E1', '#32CD32', '#FFD700']

bars = ax.bar(pitches, velocities, color=colors, edgecolor='black', linewidth=1.2, alpha=0.8)

# Add error bars for range
yerr_lower = [v - r[0] for v, r in zip(velocities, velo_ranges)]
yerr_upper = [r[1] - v for v, r in zip(velocities, velo_ranges)]
ax.errorbar(pitches, velocities, yerr=[yerr_lower, yerr_upper], 
            fmt='none', ecolor='black', capsize=5, capthick=2, alpha=0.7)

# Add value labels on bars
for bar, velo in zip(bars, velocities):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{velo} mph', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylabel('Velocity (mph)', fontsize=12, fontweight='bold')
ax.set_title('Blake Snell - Pitch Arsenal Velocities\n(Average with Range)', fontsize=14, fontweight='bold')
ax.set_ylim(70, 100)
ax.grid(axis='y', alpha=0.3)
ax.axhline(y=90, color='red', linestyle='--', alpha=0.5, label='Elite Velocity (90+)')
ax.legend()

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'snell_pitch_velocities.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 3. Game Trends (Last 5 games from 2025-2026) =====
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

games = ['2025-09-15', '2025-09-20', '2025-09-25', '2025-10-01', '2026-03-30']
innings = [6.0, 5.0, 7.0, 6.0, 3.0]
era_per_game = [2.00, 4.50, 1.29, 3.00, 12.00]

# Innings pitched trend
ax1.plot(games, innings, 'o-', color='#1E90FF', linewidth=2, markersize=8, label='IP')
ax1.axhline(y=6.0, color='green', linestyle='--', alpha=0.5, label='Target (6 IP)')
ax1.set_ylabel('Innings Pitched', fontsize=11, fontweight='bold')
ax1.set_title('Blake Snell - Game-by-Game Trends', fontsize=14, fontweight='bold')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 8)

# ERA trend
ax2.plot(games, era_per_game, 'o-', color='#FF4500', linewidth=2, markersize=8, label='Game ERA')
ax2.axhline(y=3.00, color='green', linestyle='--', alpha=0.5, label='Elite ERA (3.00)')
ax2.axhline(y=4.00, color='orange', linestyle='--', alpha=0.5, label='Average ERA (4.00)')
ax2.set_ylabel('Game ERA', fontsize=11, fontweight='bold')
ax2.set_xlabel('Game Date', fontsize=11, fontweight='bold')
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 14)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'snell_game_trends.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 4. Overall Grades Radar Chart (20-80 Scale) =====
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))

# Grades for different tools
attributes = ['Fastball', 'Curveball', 'Changeup', 'Slider', 'Control', 'Command', 'Stamina', 'Mental']
grades = [60, 55, 50, 65, 40, 55, 55, 70]  # 20-80 scale
N = len(attributes)

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]
grades += grades[:1]

# Color based on grade
ax.fill(angles, grades, color='#1E90FF', alpha=0.25)
ax.plot(angles, grades, 'o-', linewidth=2, color='#1E90FF', markersize=8)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(attributes, size=11, fontweight='bold')
ax.set_ylim(20, 80)
ax.set_yticks([20, 30, 40, 50, 60, 70, 80])
ax.set_yticklabels(['20', '30', '40', '50', '60', '70', '80'], color='grey', size=8)
ax.set_title('Blake Snell - Scouting Grades\n(20-80 Scale)', size=16, fontweight='bold', pad=20)

# Add grade labels on each point
for angle, grade, attr in zip(angles[:-1], grades[:-1], attributes):
    ax.text(angle, grade + 3, str(grade), ha='center', va='center', 
            fontsize=10, fontweight='bold', color='darkblue')

ax.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'snell_overall_grades.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 5. Report Cover =====
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')

# Title
ax.text(0.5, 0.85, 'BLAKE SNELL', fontsize=36, fontweight='bold', 
        ha='center', va='center', transform=ax.transAxes, color='#1E90FF')
ax.text(0.5, 0.75, 'Los Angeles Dodgers #7 | LHP', fontsize=18, 
        ha='center', va='center', transform=ax.transAxes, color='#333333')

# Key stats boxes
stats = [
    ('2× CY YOUNG', '2018, 2023'),
    ('CAREER ERA', '3.24'),
    ('CAREER K/9', '10.6'),
    ('2025 ERA', '2.35'),
]

for i, (label, value) in enumerate(stats):
    x = 0.15 + i * 0.22
    y = 0.55
    rect = plt.Rectangle((x-0.08, y-0.08), 0.16, 0.16, 
                          facecolor='#f0f0f0', edgecolor='#1E90FF', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y+0.03, label, fontsize=10, fontweight='bold', ha='center', va='center', color='#1E90FF')
    ax.text(x, y-0.04, value, fontsize=14, fontweight='bold', ha='center', va='center', color='#333333')

# Status box
rect = plt.Rectangle((0.25, 0.25), 0.5, 0.12, 
                      facecolor='#FFE4E1', edgecolor='#FF4500', linewidth=2)
ax.add_patch(rect)
ax.text(0.5, 0.31, '⚠️ CURRENT STATUS: IL-60 (Injured List)', fontsize=14, 
        fontweight='bold', ha='center', va='center', color='#FF4500')

# Footer
ax.text(0.5, 0.15, 'Scouting Report | 2026-07-11', fontsize=12, 
        ha='center', va='center', transform=ax.transAxes, color='#666666')
ax.text(0.5, 0.10, 'Los Angeles Dodgers Scouting Department', fontsize=10, 
        ha='center', va='center', transform=ax.transAxes, color='#999999')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'snell_report_cover.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Charts generated successfully!")
print(f"Output directory: {output_dir}")
