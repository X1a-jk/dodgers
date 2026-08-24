import json
from datetime import datetime

old_players = {
    "Ben Casparius": ("78", "IL-60"),
    "Jake Cousins": ("", "IL-60"),
    "Edwin Díaz": ("3", "活跃"),
    "Jack Dreyer": ("86", "活跃"),
    "Carlos Duran": ("", "小联盟"),
    "Paul Gervase": ("65", "小联盟"),
    "Tyler Glasnow": ("31", "IL-60"),
    "Brusdar Graterol": ("48", "IL-60"),
    "Seth Halvorsen": ("", "小联盟"),
    "Edgardo Henriquez": ("60", "活跃"),
    "Kyle Hurt": ("63", "小联盟"),
    "Will Klein": ("61", "活跃"),
    "Landon Knack": ("96", "小联盟"),
    "Ronan Kopp": ("83", "小联盟"),
    "Eric Lauer": ("33", "活跃"),
    "Chayce McDermott": ("62", "小联盟"),
    "Bobby Miller": ("28", "IL-60"),
    "Wyatt Mills": ("58", "小联盟"),
    "Evan Phillips": ("59", "活跃"),
    "River Ryan": ("77", "小联盟"),
    "Roki Sasaki": ("11", "活跃"),
    "Tanner Scott": ("66", "活跃"),
    "Emmet Sheehan": ("80", "活跃"),
    "Blake Snell": ("7", "IL-60"),
    "Brock Stewart": ("41", "活跃"),
    "Gavin Stone": ("35", "IL-60"),
    "Blake Treinen": ("49", "IL-15"),
    "Alex Vesia": ("51", "活跃"),
    "Justin Wrobleski": ("70", "活跃"),
    "Yoshinobu Yamamoto": ("18", "活跃"),
    "Shohei Ohtani": ("17", "活跃"),
    "Eliezer Alfonzo": ("64", "活跃"),
    "Dalton Rushing": ("68", "活跃"),
    "Will Smith": ("16", "IL-60"),
    "Mookie Betts": ("50", "活跃"),
    "Alex Freeland": ("76", "小联盟"),
    "Freddie Freeman": ("5", "活跃"),
    "Enrique Hernández": ("8", "活跃"),
    "Hyeseong Kim": ("6", "小联盟"),
    "Max Muncy": ("13", "活跃"),
    "Miguel Rojas": ("72", "活跃"),
    "Alex Call": ("12", "活跃"),
    "Tommy Edman": ("25", "活跃"),
    "Teoscar Hernández": ("37", "活跃"),
    "Andy Pages": ("44", "活跃"),
    "Alek Thomas": ("5", "小联盟"),
    "Kyle Tucker": ("23", "活跃"),
    "Ryan Ward": ("67", "小联盟"),
}

today_api = [
    {"name": "Alek Thomas", "num": "", "status": "RM"},
    {"name": "Alex Call", "num": "12", "status": "A"},
    {"name": "Alex Freeland", "num": "76", "status": "RM"},
    {"name": "Alex Vesia", "num": "51", "status": "A"},
    {"name": "Andy Pages", "num": "44", "status": "A"},
    {"name": "Ben Casparius", "num": "78", "status": "D60"},
    {"name": "Blake Snell", "num": "7", "status": "D60"},
    {"name": "Blake Treinen", "num": "49", "status": "D15"},
    {"name": "Bobby Miller", "num": "28", "status": "D60"},
    {"name": "Brock Stewart", "num": "41", "status": "D15"},
    {"name": "Brusdar Graterol", "num": "48", "status": "D60"},
    {"name": "Carlos Duran", "num": "", "status": "RM"},
    {"name": "Cole Irvin", "num": "38", "status": "A"},
    {"name": "Dalton Rushing", "num": "68", "status": "A"},
    {"name": "Edgardo Henriquez", "num": "60", "status": "A"},
    {"name": "Edwin Díaz", "num": "3", "status": "A"},
    {"name": "Eliezer Alfonzo", "num": "64", "status": "A"},
    {"name": "Emmet Sheehan", "num": "80", "status": "A"},
    {"name": "Enrique Hernández", "num": "8", "status": "A"},
    {"name": "Eric Lauer", "num": "33", "status": "A"},
    {"name": "Evan Phillips", "num": "59", "status": "A"},
    {"name": "Freddie Freeman", "num": "5", "status": "A"},
    {"name": "Gavin Stone", "num": "35", "status": "D60"},
    {"name": "Hyeseong Kim", "num": "6", "status": "RM"},
    {"name": "Jack Dreyer", "num": "86", "status": "A"},
    {"name": "Jake Cousins", "num": "", "status": "D60"},
    {"name": "Justin Wrobleski", "num": "70", "status": "A"},
    {"name": "Kyle Hurt", "num": "63", "status": "RM"},
    {"name": "Kyle Tucker", "num": "23", "status": "A"},
    {"name": "Landon Knack", "num": "96", "status": "RM"},
    {"name": "Max Muncy", "num": "13", "status": "A"},
    {"name": "Miguel Rojas", "num": "72", "status": "A"},
    {"name": "Mookie Betts", "num": "50", "status": "A"},
    {"name": "Paul Gervase", "num": "65", "status": "RM"},
    {"name": "River Ryan", "num": "77", "status": "RM"},
    {"name": "Roki Sasaki", "num": "11", "status": "A"},
    {"name": "Ronan Kopp", "num": "83", "status": "RM"},
    {"name": "Ryan Ward", "num": "67", "status": "RM"},
    {"name": "Seth Halvorsen", "num": "", "status": "RM"},
    {"name": "Shohei Ohtani", "num": "17", "status": "A"},
    {"name": "Tanner Scott", "num": "66", "status": "A"},
    {"name": "Teoscar Hernández", "num": "37", "status": "A"},
    {"name": "Tommy Edman", "num": "25", "status": "A"},
    {"name": "Tyler Glasnow", "num": "31", "status": "D60"},
    {"name": "Will Klein", "num": "61", "status": "A"},
    {"name": "Will Smith", "num": "16", "status": "D60"},
    {"name": "Wyatt Mills", "num": "58", "status": "RM"},
    {"name": "Yoshinobu Yamamoto", "num": "18", "status": "A"},
]

status_map = {"A": "活跃", "RM": "小联盟", "D10": "IL-10", "D15": "IL-15", "D60": "IL-60"}

today_names = {p["name"] for p in today_api}
old_names = set(old_players.keys())

added = today_names - old_names
removed = old_names - today_names

changed = []
for p in today_api:
    name = p["name"]
    if name in old_players:
        old_num, old_status = old_players[name]
        new_status = status_map[p["status"]]
        if old_status != new_status:
            changed.append((name, old_num, old_status, p["num"], new_status))

print("新增40人名单:", added)
print("移出40人名单:", removed)
print("状态变化:")
for c in changed:
    print(f"  {c[0]}: {c[2]} -> {c[4]}")
