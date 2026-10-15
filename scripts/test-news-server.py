import requests, io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = "http://localhost:8964"

# 1. 页面
r = requests.get(BASE + "/", timeout=10)
print("GET / ->", r.status_code, "len", len(r.text), "has-grid:", 'id="grid"' in r.text)

# 2. 缓存
j = requests.get(BASE + "/api/all", timeout=10).json()
for mid, m in j["modules"].items():
    print(f"\n[{mid}] items={len(m.get('items') or [])} updated={m.get('updated')}")
    for it in (m.get("items") or [])[:3]:
        print("   -", (it.get("title") or "?")[:75], "|", it.get("time"))

# 3. 单模块刷新 (POST)
for mid in ["mlb", "dn", "athletic", "x"]:
    try:
        r = requests.post(BASE + "/api/refresh?id=" + mid, timeout=40)
        jj = r.json()
        m = jj.get("module") or {}
        print(f"\nPOST refresh {mid} -> ok={jj.get('ok')} items={len(m.get('items') or [])} err={jj.get('error')}")
    except Exception as e:
        print(f"\nPOST refresh {mid} -> FAIL {type(e).__name__}: {e}")
