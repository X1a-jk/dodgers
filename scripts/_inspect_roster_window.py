#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""摸清 9/14~9/18 道奇 40 人名单当前状态 + 区间 transactions"""
import json
import requests

API = "https://statsapi.mlb.com/api/v1"
HEADERS = {"User-Agent": "Mozilla/5.0 (roster-backfill)"}

def get(path, params=None):
    r = requests.get(API + path, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

# 1. 当前 40 人名单
j = get("/teams/119/roster", {"rosterType": "40Man", "season": 2026})
roster = j.get("roster", [])
print(f"=== 当前40人名单 ({len(roster)}人) ===")
for p in sorted(roster, key=lambda x: x["person"]["fullName"]):
    st = p["status"]["description"]
    if st == "Reassigned to Minors":
        st = "小联盟"
    print(f'{p["person"]["fullName"]:28s} #{p.get("jerseyNumber",""):>3s} {st}')

# 2. 区间 transactions
tx = get("/transactions", {"teamId": 119, "startDate": "2026-09-14", "endDate": "2026-09-19"})
txs = tx.get("transactions", [])
print(f"\n=== Transactions 2026-09-14 ~ 09-19 ({len(txs)}条) ===")
for t in txs:
    person = (t.get("person") or {}).get("fullName", "?")
    print(f'{t.get("date")} [{t.get("typeCode")}] {t.get("typeDesc")} :: {person} :: {t.get("description","")[:110]}')
