import requests, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"}

# --- The Athletic 标题解析 ---
r = requests.get("https://theathletic.com/mlb/team/dodgers/", headers=H, timeout=20)
t = r.text
pats = {
    "p1": r'"id":"\d+","title":"([^"]{20,150})","seoKeywords',
    "p2": r'"title":"([^"]{20,150})","alternativeHeadline',
    "permalink": r'"permalink":"([^"]+)"',
    "slug": r'"slug":"([a-z0-9\-]{15,100})"',
}
for k, p in pats.items():
    m = re.findall(p, t)
    print(k, len(m))
    seen = []
    for x in m:
        if x not in seen:
            seen.append(x)
    for x in seen[:10]:
        print("   ", x)

print()
# --- MLB team news feed 候选 ---
for url in [
    "https://www.mlb.com/feeds/news/rss.xml?teamId=119",
    "https://dapi.cms.mlbinfra.com/v2/content/en-us/sel-lad-news-list",
    "https://www.mlb.com/dodgers/news",
]:
    try:
        r = requests.get(url, headers=H, timeout=15)
        print(url, "->", r.status_code, len(r.text))
        if "feeds" in url:
            titles = re.findall(r"<title><!\[CDATA\[([^\]]+)\]\]></title>", r.text)
            for x in titles[:5]:
                print("   ", x)
        if "dapi" in url and r.status_code == 200:
            j = r.json()
            print("   json keys:", list(j.keys())[:10])
            items = j.get("items", j.get("docs", []))
            for it in items[:5]:
                print("   ", it.get("title", "?"))
    except Exception as e:
        print(url, "FAIL", e)
