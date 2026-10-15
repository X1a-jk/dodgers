"""测试各新闻源可抓取性"""
import requests, re, sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def test(name, url, pattern=None, timeout=15):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        body = r.text
        print(f"\n=== {name} ===")
        print(f"status={r.status_code} len={len(body)}")
        if pattern:
            m = re.findall(pattern, body)
            print(f"matches({pattern}): {len(m)}")
            for x in m[:5]:
                print("  ", x if isinstance(x, str) else x)
        else:
            print(body[:500])
    except Exception as e:
        print(f"\n=== {name} === FAIL: {type(e).__name__}: {e}")

# 1. MLB.com Dodgers RSS
test("MLB.com Dodgers RSS", "https://www.mlb.com/feeds/news/rss/119",
     r"<title>([^<]+)</title>")

# 2. Dodgers Nation feed
test("Dodgers Nation feed", "https://www.dodgersnation.com/feed/",
     r"<title>([^<]+)</title>")

# 3. The Athletic Dodgers page
test("The Athletic Dodgers", "https://theathletic.com/mlb/team/dodgers/",
     r'"headline":"([^"]+)"')

# 4. X/Twitter syndication timeline
test("X syndication @Dodgers", "https://cdn.syndication.twimg.com/timeline/profile?screen_name=Dodgers&lang=en&dnt=true&limit=10",
     None)
