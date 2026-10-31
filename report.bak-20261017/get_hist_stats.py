import requests, json, time

players = {
    "621242": ("Edwin Diaz", "pitching"),
    "642546": ("Jonathan Hernandez", "pitching"),
    "571771": ("Enrique Hernandez", "batting"),
    "606192": ("Teoscar Hernandez", "batting"),
    "678020": ("Seth Halvorsen", "pitching"),
}
out = {}
for pid, (name, group) in players.items():
    seasons = []
    for season in [2021, 2022, 2023, 2024, 2025]:
        url = f"https://statsapi.mlb.com/api/v1/people/{pid}?hydrate=stats(group=[{group}],type=[season],season={season})"
        try:
            r = requests.get(url, timeout=30)
            data = r.json()
            out[f"{pid}_{season}"] = {"name": name, "group": group, "data": data}
        except Exception as e:
            out[f"{pid}_{season}"] = {"error": str(e)}
        time.sleep(0.3)

with open("D:/baseball/report/historical_stats.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("saved")
