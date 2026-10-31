import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# 统一的道奇蓝色调
dodger_blue = '#005A9C'
dark_blue = '#0a1628'
light_blue = '#4fc3f7'
white = '#ffffff'
gold = '#FFD700'

# ============================================================
# BLAKE SNELL COVER
# ============================================================
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')

# 深蓝渐变背景
gradient = np.linspace(0, 1, 256).reshape(256, -1)
gradient = np.vstack((gradient, gradient))
ax.imshow(gradient, extent=[0, 12, 0, 8], aspect='auto', cmap='Blues', alpha=0.3, zorder=0)

# 背景色块
bg = patches.FancyBboxPatch((0, 0), 12, 8, boxstyle="square,pad=0", 
                             facecolor=dark_blue, edgecolor='none', zorder=1)
ax.add_patch(bg)

# 顶部蓝色装饰条
top_bar = patches.Rectangle((0, 7.2), 12, 0.8, facecolor=dodger_blue, alpha=0.9, zorder=2)
ax.add_patch(top_bar)

# 底部蓝色装饰条
bottom_bar = patches.Rectangle((0, 0), 12, 0.4, facecolor=dodger_blue, alpha=0.9, zorder=2)
ax.add_patch(bottom_bar)

# 左侧竖线装饰
left_line = patches.Rectangle((0.3, 1.5), 0.08, 5.5, facecolor=light_blue, alpha=0.8, zorder=2)
ax.add_patch(left_line)

# 球员名字 - 大号白色
ax.text(6, 6.5, 'BLAKE SNELL', fontsize=44, fontweight='bold', color=white,
        ha='center', va='center', zorder=3)

# 副标题
ax.text(6, 5.6, 'Los Angeles Dodgers  #7  |  LHP  |  Age 33', fontsize=14, color=light_blue,
        ha='center', va='center', zorder=3, style='italic')

# 赛扬奖金色标记
ax.text(6, 4.8, '2× CY YOUNG AWARD WINNER', fontsize=12, color=gold,
        ha='center', va='center', zorder=3, fontweight='bold')

# 中间分割线
ax.plot([2, 10], [4.3, 4.3], color=light_blue, alpha=0.4, linewidth=1, zorder=2)

# 关键数据卡片 - 横向排列
stats = [
    ('CAREER ERA', '3.24'),
    ('CAREER K/9', '10.6'),
    ('2025 ERA', '2.35'),
    ('2026 STATUS', 'IL-60'),
]

for i, (label, value) in enumerate(stats):
    x = 1.5 + i * 2.5
    y = 2.8
    
    # 卡片背景
    card = patches.FancyBboxPatch((x - 1.1, y - 0.6), 2.2, 1.2,
                                    boxstyle="round,pad=0.05,rounding_size=0.1",
                                    facecolor='#132238', edgecolor=light_blue, alpha=0.9, zorder=2)
    ax.add_patch(card)
    
    ax.text(x, y + 0.2, label, fontsize=8, color=light_blue, ha='center', va='center', zorder=3)
    
    if 'IL-60' in value:
        ax.text(x, y - 0.25, value, fontsize=14, color='#f44336', ha='center', va='center', zorder=3, fontweight='bold')
    else:
        ax.text(x, y - 0.25, value, fontsize=14, color=white, ha='center', va='center', zorder=3, fontweight='bold')

# 底部信息
ax.text(6, 0.7, 'SCOUTING REPORT', fontsize=18, color=white, ha='center', va='center', 
        zorder=3, fontweight='bold', alpha=0.8)
ax.text(6, 0.2, 'Los Angeles Dodgers Baseball Operations  |  Generated 2026-07-11', 
        fontsize=8, color=light_blue, ha='center', va='center', zorder=3, alpha=0.7)

# 右上角装饰 - 道奇 LA logo 占位
ax.text(11.2, 7.6, 'LA', fontsize=20, color=gold, ha='center', va='center', 
        zorder=3, fontweight='bold', alpha=0.9)

plt.tight_layout(pad=0)
plt.savefig(r'D:\baseball\report\blake-snell\snell_report_cover.png', 
            dpi=150, bbox_inches='tight', facecolor=dark_blue, edgecolor='none')
plt.close()

# ============================================================
# WILL SMITH COVER
# ============================================================
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')

bg = patches.FancyBboxPatch((0, 0), 12, 8, boxstyle="square,pad=0", 
                             facecolor=dark_blue, edgecolor='none', zorder=1)
ax.add_patch(bg)

top_bar = patches.Rectangle((0, 7.2), 12, 0.8, facecolor=dodger_blue, alpha=0.9, zorder=2)
ax.add_patch(top_bar)

bottom_bar = patches.Rectangle((0, 0), 12, 0.4, facecolor=dodger_blue, alpha=0.9, zorder=2)
ax.add_patch(bottom_bar)

left_line = patches.Rectangle((0.3, 1.5), 0.08, 5.5, facecolor=light_blue, alpha=0.8, zorder=2)
ax.add_patch(left_line)

ax.text(6, 6.5, 'WILL SMITH', fontsize=44, fontweight='bold', color=white,
        ha='center', va='center', zorder=3)

ax.text(6, 5.6, 'Los Angeles Dodgers  #16  |  Catcher  |  Age 31', fontsize=14, color=light_blue,
        ha='center', va='center', zorder=3, style='italic')

ax.text(6, 4.8, '2× ALL-STAR  |  2020 WORLD SERIES CHAMPION', fontsize=12, color=gold,
        ha='center', va='center', zorder=3, fontweight='bold')

ax.plot([2, 10], [4.3, 4.3], color=light_blue, alpha=0.4, linewidth=1, zorder=2)

stats = [
    ('CAREER AVG', '.263'),
    ('CAREER OPS', '.800'),
    ('2025 AVG', '.296'),
    ('2026 STATUS', 'IL-10'),
]

for i, (label, value) in enumerate(stats):
    x = 1.5 + i * 2.5
    y = 2.8
    
    card = patches.FancyBboxPatch((x - 1.1, y - 0.6), 2.2, 1.2,
                                    boxstyle="round,pad=0.05,rounding_size=0.1",
                                    facecolor='#132238', edgecolor=light_blue, alpha=0.9, zorder=2)
    ax.add_patch(card)
    
    ax.text(x, y + 0.2, label, fontsize=8, color=light_blue, ha='center', va='center', zorder=3)
    
    if 'IL-10' in value:
        ax.text(x, y - 0.25, value, fontsize=14, color='#f44336', ha='center', va='center', zorder=3, fontweight='bold')
    else:
        ax.text(x, y - 0.25, value, fontsize=14, color=white, ha='center', va='center', zorder=3, fontweight='bold')

ax.text(6, 0.7, 'SCOUTING REPORT', fontsize=18, color=white, ha='center', va='center', 
        zorder=3, fontweight='bold', alpha=0.8)
ax.text(6, 0.2, 'Los Angeles Dodgers Baseball Operations  |  Generated 2026-07-11', 
        fontsize=8, color=light_blue, ha='center', va='center', zorder=3, alpha=0.7)

ax.text(11.2, 7.6, 'LA', fontsize=20, color=gold, ha='center', va='center', 
        zorder=3, fontweight='bold', alpha=0.9)

plt.tight_layout(pad=0)
plt.savefig(r'D:\baseball\report\will-smith\smith_report_cover.png', 
            dpi=150, bbox_inches='tight', facecolor=dark_blue, edgecolor='none')
plt.close()

print("Cover images regenerated!")
