import requests, re, io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"}
t = requests.get("https://theathletic.com/mlb/team/dodgers/", headers=H, timeout=20).text

# 找 permalink 附近的原始文本结构
i = t.find("nytimes.com/athletic/7580876")
print("context around permalink:")
print(t[i-400:i+200].replace("\\u0026", "&"))
