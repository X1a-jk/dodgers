import subprocess
import json
import os
import sys
import time

# 活跃球员列表（排除已生成的Roki Sasaki）
active_players = [
    # 投手
    {"name": "Jack Dreyer", "position": "P", "number": "86"},
    {"name": "Edgardo Henriquez", "position": "P", "number": "60"},
    {"name": "Kyle Hurt", "position": "P", "number": "63"},
    {"name": "Will Klein", "position": "P", "number": "61"},
    {"name": "Eric Lauer", "position": "P", "number": "33"},
    {"name": "Evan Phillips", "position": "P", "number": "59"},
    {"name": "Tanner Scott", "position": "P", "number": "66"},
    {"name": "Emmet Sheehan", "position": "P", "number": "80"},
    {"name": "Brock Stewart", "position": "P", "number": "41"},
    {"name": "Alex Vesia", "position": "P", "number": "51"},
    {"name": "Justin Wrobleski", "position": "P", "number": "70"},
    {"name": "Yoshinobu Yamamoto", "position": "P", "number": "18"},
    # 双向
    {"name": "Shohei Ohtani", "position": "DH/P", "number": "17"},
    # 捕手
    {"name": "Eliezer Alfonzo", "position": "C", "number": "64"},
    {"name": "Dalton Rushing", "position": "C", "number": "68"},
    # 内野手
    {"name": "Mookie Betts", "position": "IF/OF", "number": "50"},
    {"name": "Alex Freeland", "position": "IF", "number": "76"},
    {"name": "Freddie Freeman", "position": "1B", "number": "5"},
    {"name": "Max Muncy", "position": "3B", "number": "13"},
    {"name": "Miguel Rojas", "position": "SS", "number": "72"},
    # 外野手
    {"name": "Alex Call", "position": "OF", "number": "12"},
    {"name": "Tommy Edman", "position": "OF/IF", "number": "25"},
    {"name": "Teoscar Hernández", "position": "OF", "number": "37"},
    {"name": "Andy Pages", "position": "OF", "number": "44"},
    {"name": "Kyle Tucker", "position": "OF", "number": "23"}
]

def get_player_stats(player_name):
    """获取球员统计数据"""
    try:
        result = subprocess.run(
            ['python', r'C:\Users\Junkai XIA\.openclaw\workspace\skills\baseball\scripts\baseball.py', 
             'stats', player_name, '--format', 'json'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            # 提取JSON部分
            output = result.stdout
            try:
                json_start = output.index('{')
                json_data = output[json_start:]
                return json.loads(json_data)
            except (ValueError, json.JSONDecodeError):
                return None
        return None
    except Exception as e:
        print(f"Error getting stats for {player_name}: {e}")
        return None

def generate_basic_report(player, stats_data):
    """生成基础报告"""
    player_slug = player['name'].lower().replace(' ', '-')
    output_dir = f"D:\\baseball\\report\\{player_slug}"
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成Markdown报告
    md_content = f"""# {player['name']} 球探报告

> **Los Angeles Dodgers #{player['number']} | {player['position']}**
> 
> 报告生成时间：2026-07-09

---

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| **姓名** | {player['name']} |
| **背号** | #{player['number']} |
| **位置** | {player['position']} |
| **球队** | Los Angeles Dodgers |

---

## 📊 统计数据

"""
    
    if stats_data:
        md_content += f"```json\n{json.dumps(stats_data, indent=2, ensure_ascii=False)}\n```\n\n"
    else:
        md_content += "*统计数据获取中...*\n\n"
    
    md_content += f"""
---

## 📝 备注

此报告为批量生成的基础版本。详细分析将在后续补充。

数据来源：MLB Stats API
"""
    
    # 保存Markdown文件
    md_path = os.path.join(output_dir, f"{player_slug}-scouting-report.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return output_dir

def main():
    print("=" * 60)
    print("Dodgers Active Players Scouting Report Generator")
    print("=" * 60)
    print(f"\nTotal players to process: {len(active_players)}\n")
    
    success_count = 0
    failed_players = []
    
    for i, player in enumerate(active_players, 1):
        print(f"[{i}/{len(active_players)}] Processing {player['name']}...", end=" ")
        
        try:
            # 获取统计数据
            stats = get_player_stats(player['name'])
            
            # 生成报告
            output_dir = generate_basic_report(player, stats)
            
            print(f"[OK] -> {output_dir}")
            success_count += 1
            
            # 避免请求过快
            time.sleep(1)
            
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            failed_players.append(player['name'])
    
    print("\n" + "=" * 60)
    print(f"Completed: {success_count}/{len(active_players)}")
    if failed_players:
        print(f"Failed: {', '.join(failed_players)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
