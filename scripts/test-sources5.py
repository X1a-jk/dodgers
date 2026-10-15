import requests, re, io, sys, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"}

# --- dapi 候选 ---
for sel in ["sel-t119-news-list", "sel-lad-news", "sel-dodgers-news-list", "sel-mlb-news-list-t-119"]:
    url = f"https://dapi.cms.mlbinfra.com/v2/content/en-us/{sel}"
    try:
        r = requests.get(url, headers=H, timeout=10)
        j = r.json() if r.status_code == 200 else {}
        items = j.get("items", j.get("docs", [])) if isinstance(j, dict) else []
        print(sel, r.status_code, "items:", len(items))
        for it in items[:3]:
            print("   ", (it.get("title") or "?")[:90])
    except Exception as e:
        print(sel, "FAIL", type(e).__name__)

print()
# --- Google News RSS: theathletic dodgers ---
for q in ["site:theathletic.com dodgers", "dodgers site:theathletic.com/mlb"]:
    url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(q) + "&hl=en-US&gl=US&ceid=US:en"
    r = requests.get(url, headers=H, timeout=15)
    items = re.findall(r"<item>.*?</item>", r.text, re.S)
    print("gnews:", q, "->", len(items))
    for it in items[:5]:
        ti = re.search(r"<title>([^<]+)</title>", it)
        pu = re.search(r"<pubDate>([^<]+)</pubDate>", it)
        print("   ", ti.group(1)[:90] if ti else "?", "|", pu.group(1) if pu else "?")

print()
# --- X syndication 重试(带退避) ---
import time
for attempt in range(3):
    r = requests.get("https://cdn.syndication.twimg.com/timeline/profile?screen_name=Dodgers&lang=en&dnt=true&limit=8",
                     headers=H, timeout=15)
    print("x attempt", attempt, r.status_code, len(r.text))
    if r.status_code == 200 and len(r.text) > 100:
        open("D:/baseball/data/x-test.html", "w", encoding="utf-8").write(r.text)
        break
    time.sleep(5)
