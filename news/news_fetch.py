#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dodgers 新闻抓取核心 — 门户服务器与独立新闻服务共用。

数据源：
- mlb:      MLB.com 道奇专属新闻 (dapi sel-t119-news-list)
- dn:       Dodgers Nation (wp-json，需 Googlebot UA 过 Cloudflare)
- athletic: The Athletic 道奇频道 (JSON-LD 链接 + 逐篇 og:title)
- x:        官方 X 由浏览器直连 widgets.js，服务端无操作
"""
import html
import json
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import requests

NEWS_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(NEWS_DIR, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
GH_UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
H = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
GH = {"User-Agent": GH_UA}

MODULES = ["mlb", "dn", "athletic", "x"]
LABELS = {
    "mlb": "MLB.com",
    "dn": "Dodgers Nation",
    "athletic": "The Athletic",
    "x": "Dodgers 官方 X",
}

_lock = threading.Lock()


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def norm_time(s):
    """把各种时间字符串归一成 ISO；失败返回 None"""
    if not s:
        return None
    s = s.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat(timespec="seconds")
        except ValueError:
            continue
    return None


# ---------------- 抓取器 ----------------

def fetch_mlb():
    r = requests.get(
        "https://dapi.cms.mlbinfra.com/v2/content/en-us/sel-t119-news-list",
        headers=H, timeout=12)
    r.raise_for_status()
    items = []
    for it in r.json().get("items", [])[:20]:
        slug = it.get("slug")
        if not slug or not it.get("title"):
            continue
        items.append({
            "title": it["title"],
            "url": f"https://www.mlb.com/news/{slug}",
            "time": norm_time(it.get("contentDate")),
        })
    return items


def fetch_dn():
    r = requests.get(
        "https://www.dodgersnation.com/wp-json/wp/v2/posts"
        "?per_page=12&_fields=title,link,date",
        headers=GH, timeout=12)
    r.raise_for_status()
    items = []
    for p in r.json():
        title = html.unescape(re.sub(r"<[^>]+>", "", p["title"]["rendered"]))
        items.append({"title": title, "url": p["link"],
                      "time": norm_time(p.get("date"))})
    return items


def _slug_title(url):
    seg = url.rstrip("/").split("/")[-1]
    return re.sub(r"\s+", " ", seg.replace("-", " ")).title()


def _athletic_detail(url):
    try:
        t = requests.get(url, headers=H, timeout=8).text
        og = re.search(r'property="og:title" content="([^"]+)"', t)
        if og:
            return html.unescape(og.group(1)).strip()
    except Exception:
        pass
    return _slug_title(url)


def fetch_athletic():
    t = requests.get("https://theathletic.com/mlb/team/dodgers/",
                     headers=H, timeout=15).text
    urls = []
    for u in re.findall(r'"(https://www\.nytimes\.com/athletic/\d+/[^"]+)"', t):
        if u not in urls:
            urls.append(u)
    urls = urls[:8]
    items = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(lambda u: (u, _athletic_detail(u)), urls))
    for u, title in results:
        m = re.search(r"/athletic/\d+/(\d{4})/(\d{2})/(\d{2})/", u)
        time_iso = None
        if m:
            time_iso = norm_time(f"{m.group(1)}-{m.group(2)}-{m.group(3)} 12:00:00")
        items.append({"title": title, "url": u, "time": time_iso})
    if not items:
        raise RuntimeError("The Athletic 页面结构变化，未解析到文章")
    return items


FETCHERS = {"mlb": fetch_mlb, "dn": fetch_dn, "athletic": fetch_athletic}


def cache_path(mid):
    return os.path.join(CACHE_DIR, f"{mid}.json")


def read_cache(mid):
    try:
        with open(cache_path(mid), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def read_all_caches():
    return {mid: read_cache(mid) for mid in MODULES}


def write_cache(mid, items):
    data = {"module": mid, "label": LABELS[mid], "updated": now_iso(),
            "items": items}
    with _lock:
        tmp = cache_path(mid) + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        os.replace(tmp, cache_path(mid))
    return data


def refresh(mid):
    """返回 (ok, data_or_None, error)"""
    if mid == "x":
        return True, read_cache(mid) or {"module": "x", "label": LABELS["x"],
                                         "updated": None, "items": []}, None
    fn = FETCHERS.get(mid)
    if not fn:
        return False, read_cache(mid), "未知模块"
    try:
        items = fn()
        if not items:
            raise RuntimeError("抓取结果为空")
        return True, write_cache(mid, items), None
    except Exception as e:
        return False, read_cache(mid), f"{type(e).__name__}: {e}"


def warm():
    """补齐缺失的缓存（不覆盖已有）"""
    for mid in ("mlb", "dn", "athletic"):
        if not os.path.exists(cache_path(mid)):
            refresh(mid)


if __name__ == "__main__":
    # 手动测试: python news_fetch.py [模块名...]
    import sys
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ids = sys.argv[1:] or ["mlb", "dn", "athletic"]
    for mid in ids:
        ok, data, err = refresh(mid)
        n = len((data or {}).get("items") or [])
        print(f"[{mid}] ok={ok} items={n} err={err}")
