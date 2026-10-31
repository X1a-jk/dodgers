import matplotlib.pyplot as plt
import numpy as np
import os

# Create directory
output_dir = r'D:\baseball\report\will-smith'
os.makedirs(output_dir, exist_ok=True)

# ===== 1. Season Comparison Radar Chart =====
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))

categories = ['AVG', 'OBP', 'SLG', 'OPS', 'HR/162', 'RBI/162']
N = len(categories)

# Data for different seasons (normalized to 0-100 scale)
seasons = {
    '2022': [70, 72, 68, 70, 75, 78],
    '2023': [70, 74, 65, 69, 65, 73],
    '2024': [65, 68, 62, 65, 70, 72],
    '2025': [85, 82, 80, 82, 65, 68],
    '2026 (IL-10)': [70, 70, 60, 64, 55, 60]
}

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

colors = ['#32CD32', '#1E90FF', '#FF6347', '#FFD700', '#808080']
linestyles = ['-', '-', '-', '-', '--']

for (season, values), color, ls in zip(seasons.items(), colors, linestyles):
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, label=season, color=color, linestyle=ls)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=11)
ax.set_ylim(0, 100)
ax.set_title('Will Smith - Season Comparison\n(2022-2026)', size=16, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
ax.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'smith_season_comparison.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 2. Career Stats Trend =====
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

seasons_list = ['2022', '2023', '2024', '2025', '2026']
avg = [.260, .261, .248, .296, .249]
obp = [.343, .359, .327, .404, .338]
slg = [.465, .438, .433, .497, .382]
ops = [.808, .797, .760, .901, .720]
hr = [24, 19, 20, 17, 6]
rbi = [87, 76, 75, 61, 23]

# AVG
ax1.plot(seasons_list, avg, 'o-', color='#1E90FF', linewidth=2, markersize=8)
ax1.axhline(y=.250, color='gray', linestyle='--', alpha=0.5)
ax1.set_title('Batting Average', fontweight='bold')
ax1.set_ylim(.200, .320)
ax1.grid(True, alpha=0.3)

# OBP
ax2.plot(seasons_list, obp, 'o-', color='#32CD32', linewidth=2, markersize=8)
ax2.axhline(y=.350, color='gray', linestyle='--', alpha=0.5)
ax2.set_title('On-Base Percentage', fontweight='bold')
ax2.set_ylim(.300, .420)
ax2.grid(True, alpha=0.3)

# SLG
ax3.plot(seasons_list, slg, 'o-', color='#FF6347', linewidth=2, markersize=8)
ax3.axhline(y=.400, color='gray', linestyle='--', alpha=0.5)
ax3.set_title('Slugging Percentage', fontweight='bold')
ax3.set_ylim(.350, .520)
ax3.grid(True, alpha=0.3)

# OPS
ax4.plot(seasons_list, ops, 'o-', color='#FFD700', linewidth=2, markersize=8)
ax4.axhline(y=.750, color='gray', linestyle='--', alpha=0.5)
ax4.set_title('OPS', fontweight='bold')
ax4.set_ylim(.650, .950)
ax4.grid(True, alpha=0.3)

fig.suptitle('Will Smith - Career Stats Trend (2022-2026)', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'smith_career_trends.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 3. Overall Grades Radar Chart (20-80 Scale) =====
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))

attributes = ['Hit', 'Power', 'Plate\nDiscipline', 'Arm', 'Defense', 'Game\nCalling', 'Blocking', 'Leadership']
grades = [60, 65, 65, 70, 60, 65, 60, 70]  # 20-80 scale
N = len(attributes)

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]
grades += grades[:1]

ax.fill(angles, grades, color='#1E90FF', alpha=0.25)
ax.plot(angles, grades, 'o-', linewidth=2, color='#1E90FF', markersize=8)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(attributes, size=10, fontweight='bold')
ax.set_ylim(20, 80)
ax.set_yticks([20, 30, 40, 50, 60, 70, 80])
ax.set_yticklabels(['20', '30', '40', '50', '60', '70', '80'], color='grey', size=8)
ax.set_title('Will Smith - Scouting Grades\n(20-80 Scale)', size=16, fontweight='bold', pad=20)

for angle, grade, attr in zip(angles[:-1], grades[:-1], attributes):
    ax.text(angle, grade + 3, str(grade), ha='center', va='center', 
            fontsize=10, fontweight='bold', color='darkblue')

ax.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'smith_overall_grades.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 4. Report Cover =====
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')

ax.text(0.5, 0.85, 'WILL SMITH', fontsize=36, fontweight='bold', 
        ha='center', va='center', transform=ax.transAxes, color='#1E90FF')
ax.text(0.5, 0.75, 'Los Angeles Dodgers #16 | Catcher', fontsize=18, 
        ha='center', va='center', transform=ax.transAxes, color='#333333')

stats = [
    ('ALL-STAR', '2023, 2024'),
    ('2025 AVG', '.296'),
    ('2025 OPS', '.901'),
    ('CAREER HR', '86+'),
]

for i, (label, value) in enumerate(stats):
    x = 0.15 + i * 0.22
    y = 0.55
    rect = plt.Rectangle((x-0.08, y-0.08), 0.16, 0.16, 
                          facecolor='#f0f0f0', edgecolor='#1E90FF', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y+0.03, label, fontsize=10, fontweight='bold', ha='center', va='center', color='#1E90FF')
    ax.text(x, y-0.04, value, fontsize=14, fontweight='bold', ha='center', va='center', color='#333333')

rect = plt.Rectangle((0.25, 0.25), 0.5, 0.12, 
                      facecolor='#FFE4E1', edgecolor='#FF4500', linewidth=2)
ax.add_patch(rect)
ax.text(0.5, 0.31, '⚠️ CURRENT STATUS: IL-10 (Injured List)', fontsize=14, 
        fontweight='bold', ha='center', va='center', color='#FF4500')

ax.text(0.5, 0.15, 'Scouting Report | 2026-07-11', fontsize=12, 
        ha='center', va='center', transform=ax.transAxes, color='#666666')
ax.text(0.5, 0.10, 'Los Angeles Dodgers Scouting Department', fontsize=10, 
        ha='center', va='center', transform=ax.transAxes, color='#999999')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'smith_report_cover.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Charts generated successfully!")
print(f"Output directory: {output_dir}")
