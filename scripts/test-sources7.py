import requests, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

# dapi item 字段
j = requests.get("https://dapi.cms.mlbinfra.com/v2/content/en-us/sel-t119-news-list", headers=H, timeout=15).json()
it = j["items"][0]
print("dapi item keys:", sorted(it.keys()))
print({k: it[k] for k in ["title", "url", "slug", "created"] if k in it})
print("date-ish:", {k: v for k, v in it.items() if "date" in k.lower() or "time" in k.lower()})

print()
# Athletic 文章页 og:title
u = "https://www.nytimes.com/athletic/7580876/2026/09/10/dodgers-shohei-ohtani-josue-de-paula/"
r = requests.get(u, headers=H, timeout=15)
print("article page:", r.status_code, len(r.text))
og = re.search(r'property="og:title" content="([^"]+)"', r.text)
pub = re.search(r'(?:article:published_time|datePublished)"?\s*(?:content=)?"([^"]+)"', r.text)
print("og:title:", og.group(1) if og else None)
print("pub:", pub.group(1) if pub else None)
