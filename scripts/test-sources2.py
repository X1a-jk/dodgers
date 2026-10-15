"""第二轮测试：找可用的抓取方式"""
import requests, re, json

H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
     "Accept-Language": "en-US,en;q=0.9"}

# --- MLB.com 候选 RSS ---
for url in ["https://www.mlb.com/feeds/news/rss.xml",
            "https://www.mlb.com/feeds/news/rss/team/119",
            "https://www.mlb.com/feeds/news/rss?teamId=119",
            "https://www.mlb.com/rss/news"]:
    try:
        r = requests.get(url, headers=H, timeout=15)
        titles = re.findall(r"<title>([^<]+)</title>", r.text)
        print(f"[MLB] {url} -> {r.status_code} len={len(r.text)} titles={len(titles)}")
        for t in titles[:3]: print("   ", t)
    except Exception as e:
        print(f"[MLB] {url} -> FAIL {e}")

print()

# --- Dodgers Nation: Googlebot UA + wp-json ---
GH = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
for url in ["https://www.dodgersnation.com/feed/", "https://www.dodgersnation.com/wp-json/wp/v2/posts?per_page=10&_fields=title,link,date"]:
    try:
        r = requests.get(url, headers=GH, timeout=15)
        print(f"[DN] {url} -> {r.status_code} len={len(r.text)}")
        if "wp-json" in url and r.status_code == 200:
            posts = r.json()
            for p in posts[:5]: print("   ", p["title"]["rendered"], "|", p["link"])
        else:
            titles = re.findall(r"<title>([^<]+)</title>", r.text)
            for t in titles[:5]: print("   ", t)
    except Exception as e:
        print(f"[DN] {url} -> FAIL {type(e).__name__}: {e}")

print()

# --- The Athletic: 解析 next data ---
r = requests.get("https://theathletic.com/mlb/team/dodgers/", headers=H, timeout=20)
text = r.text
# 在 __next_f chunks 里找 title
pats = [r'\\?"title\\?":\\?"([^"\\]{15,120})\\?"', r'"title":"([^"]{15,120})"']
for p in pats:
    m = re.findall(p, text)
    print(f"[Athletic] pattern {p[:30]}... -> {len(m)} matches")
    seen = set()
    cnt = 0
    for x in m:
        if x not in seen and cnt < 12:
            seen.add(x); cnt += 1
            print("   ", x)

print()

# --- X: syndication v2 & Google News fallback ---
for url in ["https://syndication.twitter.com/srv/timeline-profile/screen-name/Dodgers?dnt=true&limit=10",
            "https://publish.twitter.com/oembed?url=https://twitter.com/Dodgers"]:
    try:
        r = requests.get(url, headers=H, timeout=15)
        print(f"[X] {url[:60]}... -> {r.status_code} len={len(r.text)}")
        print("   ", r.text[:300].replace("\n", " "))
    except Exception as e:
        print(f"[X] {url[:60]} -> FAIL {type(e).__name__}: {e}")

# Google News RSS for Dodgers twitter
try:
    r = requests.get("https://news.google.com/rss/search?q=from%3ADodgers%20site%3Ax.com&hl=en-US&gl=US&ceid=US:en", headers=H, timeout=15)
    titles = re.findall(r"<title>([^<]+)</title>", r.text)
    print(f"[X-GNews] -> {r.status_code} titles={len(titles)}")
    for t in titles[:6]: print("   ", t)
except Exception as e:
    print(f"[X-GNews] FAIL {e}")
