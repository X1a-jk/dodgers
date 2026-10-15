# -*- coding: utf-8 -*-
import json, io, sys
from datetime import datetime, timezone

BASE = r"D:\baseball\news"
CACHE = BASE + r"\cache"
OUT = BASE + r"\news-cn.json"

caches = {}
for src in ("mlb", "dn", "athletic"):
    with io.open(CACHE + "\\" + src + ".json", encoding="utf-8") as f:
        caches[src] = json.load(f)["items"]

with io.open(OUT, encoding="utf-8") as f:
    old = json.load(f)

# map url -> existing translated item
old_by_url = {it["url"]: it for it in old["items"]}

new_items = []
for src in ("mlb", "dn", "athletic"):
    for it in caches[src]:
        url = it["url"]
        if url in old_by_url:
            prev = old_by_url[url]
            item = {
                "title_cn": prev["title_cn"],
                "title_en": it["title"],
                "url": url,
                "source": src,
                "time": it["time"],
                "topics": prev["topics"],
            }
            if prev.get("top"):
                item["top"] = True
        else:
            # untranslated fallback (should not happen)
            item = {
                "title_cn": it["title"],
                "title_en": it["title"],
                "url": url,
                "source": src,
                "time": it["time"],
                "topics": ["game"],
            }
        new_items.append(item)

new = {
    "generated": datetime.now(timezone.utc).isoformat(),
    "digest": old["digest"],
    "top": old["top"],
    "items": new_items,
}

with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(new, f, ensure_ascii=False, indent=1)
    f.write("\n")

# ---- validation ----
with io.open(OUT, encoding="utf-8") as f:
    data = json.load(f)
errors = []
allowed = {"mlb", "dn", "athletic"}
for it in data["items"]:
    if it["source"] not in allowed:
        errors.append("bad source: " + it["source"])
    if not it.get("title_cn"):
        errors.append("missing title_cn: " + it["url"])
    t = it.get("topics", [])
    if not (1 <= len(t) <= 3):
        errors.append("bad topics: " + it["url"])
total = sum(len(caches[s]) for s in caches)
if len(data["items"]) != total:
    errors.append("item count %d != cache total %d" % (len(data["items"]), total))
if not data.get("digest"):
    errors.append("digest empty")
if not (3 <= len(data.get("top", [])) <= 6):
    errors.append("top count out of range")

if errors:
    print("VALIDATION FAILED")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("VALIDATION OK")
print("items:", len(data["items"]), "| digest:", len(data["digest"]), "| top:", len(data["top"]))
print("generated:", data["generated"])
