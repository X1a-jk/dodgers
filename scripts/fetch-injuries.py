#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
道奇伤病时间线数据抓取：从 transactions 接口解析伤病名单变动，
输出 D:\\baseball\\data\\injuries.json。

数据源逻辑：
- team_roster (40Man)：权威的当前 IL 名单与类型（D10/D15/D60）
- transactions：伤病名单变动历史（进 IL 日期、伤病描述、转移、回归）
最早回归日 = 进入当前名单类型的日期 + 天数（无官方预计回归数据，属推算值）
"""
import json
import re
import shutil
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from datetime import datetime, timedelta
from pathlib import Path

import statsapi

TEAM_ID = 119
SEASON = datetime.now().year
BASE_DIR = Path(r"D:\baseball")
REPORT_DIR = BASE_DIR / "report"
OUTPUT_FILE = BASE_DIR / "data" / "injuries.json"

STATUS_MAP = {"D10": "IL-10", "D15": "IL-15", "D60": "IL-60"}

RE_PLACED = re.compile(
    r"placed\s+(?:(?P<pos>[A-Z]{1,3})\s+)?(?P<name>.+?)\s+on the\s+"
    r"(?P<days>\d+)-day injured list"
    r"(?:\s+retroactive to\s+(?P<retro>[A-Za-z]+\s+\d{1,2},\s+\d{4}))?\.?\s*(?P<note>.*)$",
    re.S,
)
RE_TRANSFER = re.compile(
    r"transferred\s+(?:(?P<pos>[A-Z]{1,3})\s+)?(?P<name>.+?)\s+from the\s+"
    r"(?P<from>\d+)-day injured list to the\s+(?P<to>\d+)-day injured list\.?\s*(?P<note>.*)$",
    re.S,
)
RE_ACTIVATED = re.compile(
    r"activated\s+(?:(?P<pos>[A-Z]{1,3})\s+)?(?P<name>.+?)\s+from the\s+"
    r"(?P<days>\d+)-day injured list\.?\s*(?P<note>.*)$",
    re.S,
)


def run_with_timeout(func, timeout=45, default=None):
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func)
            return future.result(timeout=timeout)
    except TimeoutError:
        print(f"[WARN] Operation timed out after {timeout}s")
        return default
    except Exception as e:
        print(f"[WARN] Operation failed: {e}")
        return default


def slugify(name: str) -> str:
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_name = "".join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")


def report_url(name: str):
    slug = slugify(name)
    rel = f"report/{slug}/{slug}-scouting-report.html"
    return rel if (BASE_DIR / rel).exists() else None


def headshot_url(name: str):
    slug = slugify(name)
    rel = f"report/{slug}/headshot.jpg"
    return rel if (BASE_DIR / rel).exists() else None


def fetch_current_roster_il() -> dict:
    """当前 40 人名单上的 IL 球员 {pid: {name, pos, statusCode}}"""
    def _fetch():
        raw = statsapi.get(
            "team_roster",
            {"teamId": TEAM_ID, "rosterType": "40Man", "season": SEASON},
            request_kwargs={"timeout": 60},
        )
        out = {}
        for e in raw.get("roster", []):
            code = e.get("status", {}).get("code", "")
            if code in STATUS_MAP:
                pid = e["person"]["id"]
                out[pid] = {
                    "name": e["person"]["fullName"],
                    "pos": e.get("position", {}).get("abbreviation", ""),
                    "statusCode": code,
                }
        return out
    return run_with_timeout(_fetch, timeout=30, default={})


def fetch_il_transactions() -> list:
    """整季伤病名单变动事件"""
    def _fetch():
        raw = statsapi.get(
            "transactions",
            {
                "teamId": TEAM_ID,
                "startDate": f"{SEASON}-03-01",
                "endDate": datetime.now().strftime("%Y-%m-%d"),
            },
            request_kwargs={"timeout": 90},
        )
        events = []
        for t in raw.get("transactions", []):
            desc = t.get("description") or ""
            if "injured list" not in desc.lower():
                continue
            person = t.get("person") or {}
            date = t.get("effectiveDate") or t.get("date")
            base = {"date": date, "pid": person.get("id"), "name": person.get("fullName", "")}

            m = RE_PLACED.search(desc)
            if m:
                retro = m.group("retro")
                eff = None
                if retro:
                    try:
                        eff = datetime.strptime(retro, "%B %d, %Y").strftime("%Y-%m-%d")
                    except ValueError:
                        eff = None
                events.append({**base, "kind": "placed", "days": int(m.group("days")),
                               "pos": m.group("pos") or "", "note": (m.group("note") or "").strip(),
                               "effDate": eff or date})
                continue
            m = RE_TRANSFER.search(desc)
            if m:
                events.append({**base, "kind": "transfer", "days": int(m.group("to")),
                               "pos": m.group("pos") or "", "note": (m.group("note") or "").strip(),
                               "effDate": date})
                continue
            m = RE_ACTIVATED.search(desc)
            if m:
                events.append({**base, "kind": "activated", "days": int(m.group("days")),
                               "pos": m.group("pos") or "", "note": (m.group("note") or "").strip(),
                               "effDate": date})
        return events
    return run_with_timeout(_fetch, timeout=90, default=[])


def main():
    print("[INFO] Fetching roster + injury transactions...")
    roster_il = fetch_current_roster_il()
    events = fetch_il_transactions()
    print(f"[INFO] Current IL (roster): {len(roster_il)} | IL transactions this season: {len(events)}")
    if not roster_il and not events:
        print("[ERR] Both sources empty; keeping previous data if any.")
        sys.exit(1)

    today = datetime.now().date()

    # ---- 逐人推演当前状态 ----
    by_pid = {}
    for e in events:
        if e["pid"] is None:
            continue
        by_pid.setdefault(e["pid"], []).append(e)

    current = []
    total_days_lost = 0
    placements = 0
    covered = set()

    for pid, evs in by_pid.items():
        evs.sort(key=lambda x: x["date"])
        state = None       # (listDays, listStart, note, injury)
        placements_pid = []
        for e in evs:
            if e["kind"] in ("placed", "transfer"):
                placements += 1
                placements_pid.append(e)
                state = (e["days"], datetime.strptime(e["effDate"], "%Y-%m-%d").date(),
                         e["note"], e["pos"] or (state[3] if state else ""))
            elif e["kind"] == "activated":
                if placements_pid:
                    last = placements_pid[-1]
                    start = datetime.strptime(last["effDate"], "%Y-%m-%d").date()
                    total_days_lost += max(0, (today - start).days)
                    placements_pid = []
                state = None
        if state:
            covered.add(pid)

    # 当前 IL 明细（以 roster 为准，事件补充日期与伤病描述）
    for pid, info in roster_il.items():
        evs = sorted(by_pid.get(pid, []), key=lambda x: x["date"])
        list_days = int(info["statusCode"][1:])
        listed_date = None   # 当前名单类型的起算日（算最早回归）
        original_date = None  # 本次伤病首次进 IL 的日期（算累计缺阵）
        note = ""
        since_activation = []
        for e in reversed(evs):
            if e["kind"] == "activated":
                break
            since_activation.append(e)
        since_activation.reverse()
        for e in since_activation:
            if e["kind"] in ("placed", "transfer"):
                if original_date is None:
                    original_date = datetime.strptime(e["effDate"], "%Y-%m-%d").date()
                if e["days"] == list_days and listed_date is None:
                    listed_date = datetime.strptime(e["effDate"], "%Y-%m-%d").date()
                    note = e["note"].rstrip(".")
        ref_date = original_date or listed_date
        days_on_il = (today - ref_date).days if ref_date else None
        earliest = (listed_date + timedelta(days=list_days)).isoformat() if listed_date else None
        current.append({
            "id": pid,
            "name": info["name"],
            "pos": info["pos"],
            "listType": STATUS_MAP[info["statusCode"]],
            "injury": note,
            "listedDate": ref_date.isoformat() if ref_date else None,
            "daysOnIL": days_on_il,
            "earliestReturn": earliest,
            "reportUrl": report_url(info["name"]),
            "headshot": headshot_url(info["name"]),
        })

    # roster 说在 IL 但事务里找不到（极少见）→ 日期未知也列入
    # （上面循环已覆盖全部 roster_il，covered 仅用于统计事件侧）

    # 按进 IL 日期排序（未知日期排最后）
    current.sort(key=lambda x: (x["listedDate"] is None, x["listedDate"] or ""))

    # ---- 最近 45 天回归 ----
    cutoff = (today - timedelta(days=45)).isoformat()
    returns = []
    for e in events:
        if e["kind"] == "activated" and e["date"] >= cutoff:
            returns.append({
                "name": e["name"], "date": e["date"],
                "listType": f"IL-{e['days']}",
                "reportUrl": report_url(e["name"]),
            })
    returns.sort(key=lambda x: x["date"], reverse=True)

    data = {
        "generatedAt": datetime.now().isoformat(),
        "season": SEASON,
        "current": current,
        "recentReturns": returns,
        "seasonTotals": {
            "placements": placements,
            "daysLost": total_days_lost,
            "currentlyOnIL": len(current),
        },
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUTPUT_FILE.with_suffix(".tmp")
    if OUTPUT_FILE.exists():
        shutil.copy2(OUTPUT_FILE, OUTPUT_FILE.with_suffix(".json.bak"))
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(OUTPUT_FILE)
    print(f"[OK] Saved {OUTPUT_FILE}")
    print(f"     Current IL: {len(current)} | Recent returns (45d): {len(returns)} | "
          f"Season placements: {placements} | Days lost: {total_days_lost}")
    for c in current:
        print(f"     - {c['name']}: {c['listType']} since {c['listedDate']} ({c['injury'] or '伤情未知'})")
    sys.exit(0)


if __name__ == "__main__":
    main()
