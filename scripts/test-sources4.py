import requests, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"}

# --- Athletic: headline escaped pattern ---
r = requests.get("https://theathletic.com/mlb/team/dodgers/", headers=H, timeout=20)
t = r.text
for name, p in [("headline-esc", r'\\"headline\\":\\"([^\\"]{15,150})\\"'),
                ("headline-plain", r'"headline":"([^"]{15,150})"')]:
    m = re.findall(p, t)
    seen = []
    for x in m:
        if x not in seen: seen.append(x)
    print(name, len(m), "unique", len(seen))
    for x in seen[:10]: print("   ", x)

print()
# --- mlb.com/dodgers/news 页面找 dapi 接口和文章 ---
r = requests.get("https://www.mlb.com/dodgers/news", headers=H, timeout=20)
t = r.text
dapi = set(re.findall(r'https://dapi\.cms\.mlbinfra\.com[^"\'\\ ]+', t))
for d in list(dapi)[:10]: print("dapi:", d[:160])
titles = re.findall(r'"title":"([^"]{20,150})"', t)
seen = []
for x in titles:
    if x not in seen: seen.append(x)
print("titles:", len(seen))
for x in seen[:12]: print("   ", x)
