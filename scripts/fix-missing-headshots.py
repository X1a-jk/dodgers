#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
from pathlib import Path

REPORT_ROOT = Path("D:/baseball/report")

# Player name -> MLB player id
players = {
    "chayce-mcdermott": 681862,
    "edwin-diaz": 621242,
    "enrique-hernandez": 571771,
    "nick-frasso": 681885,
    "river-ryan": 686986,
    "teoscar-hernandez": 606192,
}

url_template = "https://securea.mlb.com/mlb/images/players/head_shot/{player_id}.jpg"

for slug, pid in players.items():
    dest = REPORT_ROOT / slug
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / "headshot.jpg"
    if out.exists():
        print(f"skip {slug}")
        continue
    try:
        url = url_template.format(player_id=pid)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
            if len(data) > 500:
                out.write_bytes(data)
                print(f"downloaded {slug}: {len(data)} bytes")
            else:
                print(f"empty {slug}")
    except Exception as e:
        print(f"failed {slug}: {e}")
