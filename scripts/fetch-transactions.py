#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易与人员变动追踪：道奇 2026 赛季全部 transactions。
输出 D:\\baseball\\data\\transactions.json，由每日任务调用。
分类：trade / dfa / outright / option / recall / selected / signed / released / il
"""
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
BASE_DIR = Path(r"D:\baseball")
OUTPUT_FILE = BASE_DIR / "data" / "transactions.json"
SEASON = datetime.now().year
API = "https://statsapi.mlb.com/api/v1"


def api_get(path, params=None, retries=4, timeout=30):
    for i in range(retries):
        try:
            r = requests.get(API + path, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"  [retry {i+1}/{retries}] {path}: {type(e).__name__}", flush=True)
            time.sleep(1.5 * (i + 1))
    return {}


def classify(t):
    d = (t.get("typeDesc") or "").strip().lower()
    desc = (t.get("description") or "").lower()
    if "trade" in d:
        return "trade"
    if "designated" in d:
        return "dfa"
    if "outright" in d:
        return "outright"
    if "option" in d:
        return "option"
    if "recalled" in d or "selected" in d or "contract purchased" in d:
        return "recall"
    if "released" in d:
        return "released"
    if "assigned" in d:
        return "rehab" if "rehab" in desc else "other"
    # \bsigned\b："assigned" 也包含 signed 子串，必须先排除 assigned 分支
    import re as _re
    if _re.search(r"\bsigned\b", d):
        return "signed"
    if "status change" in d:
        return "il" if (" il" in desc or "injured" in desc or "injury" in desc) else "status"
    return "other"


CAT_CN = {
    "trade": "交易", "dfa": "指定让渡", "outright": "Outright 下放",
    "option": "下放小联盟", "recall": "上调/回归", "signed": "签约",
    "released": "释出", "il": "伤病名单", "rehab": "康复指派", "status": "状态变更", "other": "其他",
}
MOVE_CATS = {"trade", "dfa", "outright", "option", "recall", "released", "signed"}


def main():
    print(f"[INFO] Fetching Dodgers transactions for {SEASON}...")
    # 分两段抓，避免单次返回过多被截断
    all_tx = []
    ranges = [
        (f"{SEASON}-01-01", f"{SEASON}-06-30"),
        (f"{SEASON}-07-01", datetime.now().strftime("%Y-%m-%d")),
    ]
    for start, end in ranges:
        j = api_get("/transactions", {"teamId": 119, "startDate": start, "endDate": end})
        txs = j.get("transactions", [])
        print(f"  {start} ~ {end}: {len(txs)} 条")
        all_tx.extend(txs)
        time.sleep(0.5)

    # 去重（按 id）
    seen = set()
    items = []
    for t in all_tx:
        tid = t.get("id") or f'{t.get("date")}-{t.get("description","")[:40]}'
        if tid in seen:
            continue
        seen.add(tid)
        person = t.get("person") or {}
        to_team = t.get("toTeam") or {}
        from_team = t.get("fromTeam") or {}
        cat = classify(t)
        items.append({
            "id": str(tid),
            "date": t.get("date"),
            "category": cat,
            "categoryCn": CAT_CN.get(cat, cat),
            "typeDesc": t.get("typeDesc", ""),
            "description": t.get("description", ""),
            "player": person.get("fullName"),
            "playerId": person.get("id"),
            "toTeam": to_team.get("name"),
            "fromTeam": from_team.get("name"),
        })

    items.sort(key=lambda x: x["date"] or "", reverse=True)

    # 汇总统计
    summary = {}
    for it in items:
        summary[it["category"]] = summary.get(it["category"], 0) + 1

    data = {
        "generatedAt": datetime.now().isoformat(),
        "season": SEASON,
        "total": len(items),
        "summary": summary,
        "recent": items[:60],
        "moves": [it for it in items if it["category"] in MOVE_CATS][:200],
        "trades": [it for it in items if it["category"] == "trade"],
        "all": items,
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT_FILE.exists():
        shutil.copy2(OUTPUT_FILE, OUTPUT_FILE.with_suffix(".json.bak"))
    OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] {OUTPUT_FILE}")
    print(f"     total={len(items)} summary={summary}")
    print("     最近5条:")
    for it in items[:5]:
        print(f"       {it['date']} [{it['categoryCn']}] {it['description'][:80]}")


if __name__ == "__main__":
    main()
