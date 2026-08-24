import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import sys
import json

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def normalize(value, low, high, invert=False):
    """将数值标准化到 0-100，越接近 high 越好（invert=False）"""
    val = float(value)
    if invert:
        val = high - val + low
    ratio = (val - low) / (high - low)
    ratio = max(0.0, min(1.0, ratio))
    return ratio * 100

def grade_color(value):
    if value >= 60:
        return '#4caf50'
    elif value >= 50:
        return '#4fc3f7'
    elif value >= 40:
        return '#ff9800'
    else:
        return '#f44336'

def generate_cover(player_name, info, stats, output_path):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    title_text = player_name
    subtitle = f"Los Angeles Dodgers #{info.get('number', '—')} | {info.get('position', '')}"
    report_text = 'SCOUTING REPORT 2026'

    ax.text(0.5, 0.85, title_text, fontsize=30, fontweight='bold', ha='center',
            color='white', transform=ax.transAxes)
    ax.text(0.5, 0.75, subtitle, fontsize=16, ha='center',
            color='#4fc3f7', transform=ax.transAxes)
    ax.text(0.5, 0.65, report_text, fontsize=20, fontweight='bold', ha='center',
            color='#ff9800', transform=ax.transAxes)

    stat_items = stats[:6]
    y_pos = 0.45
    for i, (label, value) in enumerate(stat_items):
        x_pos = 0.15 + (i % 3) * 0.35
        if i >= 3:
            y_pos = 0.25
        ax.text(x_pos, y_pos, str(value), fontsize=24, fontweight='bold', ha='center',
                color='#4fc3f7', transform=ax.transAxes)
        ax.text(x_pos, y_pos - 0.08, label, fontsize=12, ha='center',
                color='#90a4ae', transform=ax.transAxes)

    ax.text(0.5, 0.02, 'Generated: 2026-07-24 | Data: MLB.com, Baseball Savant, Fangraphs',
            fontsize=10, ha='center', color='#666', transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()

def generate_pitch_velocities(arsenal, output_path):
    if not arsenal:
        return
    fig, ax = plt.subplots(figsize=(12, 6))
    pitches = list(arsenal.keys())
    min_v = [arsenal[p]['min'] for p in pitches]
    max_v = [arsenal[p]['max'] for p in pitches]
    avg_v = [(a + b) / 2 for a, b in zip(min_v, max_v)]

    x = np.arange(len(pitches))
    width = 0.35
    ax.bar(x - width/2, min_v, width, label='Min Velocity', color='#4fc3f7', alpha=0.8)
    ax.bar(x + width/2, max_v, width, label='Max Velocity', color='#ff9800', alpha=0.8)

    for i, avg in enumerate(avg_v):
        ax.plot([i - width/2, i + width/2], [avg, avg], 'r--', linewidth=2, alpha=0.7)
        ax.text(i, avg + 0.5, f'Avg: {avg:.1f}', ha='center', va='bottom',
                fontweight='bold', color='red', fontsize=9)

    ax.set_xlabel('Pitch Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Velocity (mph)', fontsize=12, fontweight='bold')
    ax.set_title('Pitch Arsenal Velocity Distribution', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(pitches, fontsize=9)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def generate_game_trends(games_data, output_path):
    if not games_data or len(games_data) < 3:
        return
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    labels = [g['label'] for g in games_data]
    era_values = [g['era'] for g in games_data]
    ip_values = [g['ip'] for g in games_data]
    k_values = [g['k'] for g in games_data]
    bb_values = [g['bb'] for g in games_data]

    ax1.plot(labels, era_values, 'o-', linewidth=2, markersize=8, color='#f44336', label='Game ERA')
    ax1.fill_between(range(len(labels)), era_values, alpha=0.2, color='#f44336')
    ax1.set_ylabel('ERA', fontsize=12, fontweight='bold')
    ax1.set_title('2026 Season ERA Trend by Game', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2_twin = ax2.twinx()
    ax2.bar(labels, ip_values, alpha=0.6, color='#4fc3f7', label='IP')
    ax2_twin.plot(labels, k_values, 'o-', color='#4caf50', linewidth=2, markersize=8, label='K')
    ax2_twin.plot(labels, bb_values, 's-', color='#ff9800', linewidth=2, markersize=8, label='BB')

    ax2.set_ylabel('Innings Pitched (IP)', fontsize=12, fontweight='bold')
    ax2_twin.set_ylabel('Strikeouts / Walks', fontsize=12, fontweight='bold')
    ax2.set_title('IP vs Strikeouts and Walks', fontsize=14, fontweight='bold')

    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def generate_overall_grades(grades, output_path):
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    categories = list(grades.keys())
    values = list(grades.values())
    values += values[:1]
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    ax.plot(angles, values, 'o-', linewidth=2, color='#4fc3f7', markersize=8)
    ax.fill(angles, values, alpha=0.3, color='#4fc3f7')

    for angle, value, cat in zip(angles[:-1], values[:-1], categories):
        ax.text(angle, value + 3, str(value), ha='center', va='center',
                fontweight='bold', fontsize=10, color=grade_color(value))

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=10)
    ax.set_ylim(0, 80)
    ax.set_title('Overall Grades (20-80 Scale)', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True)
    ax.axhspan(60, 80, alpha=0.1, color='green')
    ax.axhspan(50, 60, alpha=0.1, color='yellow')
    ax.axhspan(0, 50, alpha=0.1, color='red')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def generate_season_comparison(data_current, data_previous, categories, output_path):
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    N = len(categories)

    def compute_values(data, cats):
        values = []
        for cat in cats:
            item = data.get(cat, {})
            raw = float(item.get('value', 0))
            values.append(normalize(raw, item.get('low', 0), item.get('high', 10), item.get('invert', False)))
        return values

    values_current = compute_values(data_current, categories) + [compute_values(data_current, categories)[0]]
    values_prev = compute_values(data_previous, categories) + [compute_values(data_previous, categories)[0]]
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    ax.plot(angles, values_prev, 'o-', linewidth=2, label='2025', color='#4fc3f7')
    ax.fill(angles, values_prev, alpha=0.25, color='#4fc3f7')
    ax.plot(angles, values_current, 'o-', linewidth=2, label='2026', color='#ff9800')
    ax.fill(angles, values_current, alpha=0.25, color='#ff9800')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=12)
    ax.set_ylim(0, 100)
    ax.set_title('Season Comparison (Normalized)', size=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_player_charts.py <config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    output_dir = config['output_dir']
    os.makedirs(output_dir, exist_ok=True)
    prefix = config.get('prefix', config['player_slug'])

    if 'cover' in config:
        generate_cover(
            config['player_name'],
            config['info'],
            config['cover']['stats'],
            os.path.join(output_dir, f'{prefix}_report_cover.png')
        )
        print(f"[OK] {prefix}_report_cover.png")

    if 'pitch_velocities' in config:
        generate_pitch_velocities(
            config['pitch_velocities'],
            os.path.join(output_dir, f'{prefix}_pitch_velocities.png')
        )
        print(f"[OK] {prefix}_pitch_velocities.png")

    if 'game_trends' in config:
        generate_game_trends(
            config['game_trends'],
            os.path.join(output_dir, f'{prefix}_game_trends.png')
        )
        print(f"[OK] {prefix}_game_trends.png")

    if 'overall_grades' in config:
        generate_overall_grades(
            config['overall_grades'],
            os.path.join(output_dir, f'{prefix}_overall_grades.png')
        )
        print(f"[OK] {prefix}_overall_grades.png")

    if 'season_comparison' in config:
        generate_season_comparison(
            config['season_comparison']['current'],
            config['season_comparison']['previous'],
            config['season_comparison']['categories'],
            os.path.join(output_dir, f'{prefix}_season_comparison.png')
        )
        print(f"[OK] {prefix}_season_comparison.png")

    print(f"\nAll charts for {config['player_name']} generated in {output_dir}")
