#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Dodgers player scouting report dashboard.
- Fetch 40-man roster from MLB Stats API
- Download player headshots from MLB.com
- Generate a single index.html gallery page linking to individual reports
"""

import json
import os
import re
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

TEAM_ID = 119
SEASON = datetime.now().year
REPORT_ROOT = Path("D:/baseball/report")
SCRIPT_ROOT = Path("D:/baseball/scripts")
MLB_API_ROSTER = f"https://statsapi.mlb.com/api/v1/teams/{TEAM_ID}/roster?rosterType=40Man&season={SEASON}"

# MLB headshot URLs (will redirect to CDN). We save the resolved image locally.
HEADSHOT_URL_TEMPLATES = [
    "https://securea.mlb.com/mlb/images/players/head_shot/{player_id}.jpg",
    "https://content.mlb.com/images/headshots/current/60x60/{player_id}.png",
]

STATUS_META = {
    "A": {"label": "Active", "class": "status-active"},
    "RM": {"label": "Minors", "class": "status-minors"},
    "D10": {"label": "IL-10", "class": "status-il"},
    "D15": {"label": "IL-15", "class": "status-il"},
    "D60": {"label": "IL-60", "class": "status-il"},
}


def slugify(name: str) -> str:
    # Normalize accented Latin chars to ASCII before stripping non-ascii
    import unicodedata
    normalized = unicodedata.normalize('NFKD', name)
    ascii_name = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return re.sub(r"[^a-z0-9-]", "", ascii_name.lower().replace(" ", "-").replace("'", "").replace(".", ""))


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_headshot(player_id: int, dest_dir: Path) -> str:
    """Try MLB headshot sources; return local filename relative to report root or None."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    local_jpg = dest_dir / "headshot.jpg"
    local_png = dest_dir / "headshot.png"

    # Try high-res jpg
    if not local_jpg.exists():
        try:
            url = HEADSHOT_URL_TEMPLATES[0].format(player_id=player_id)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
                if len(data) > 500:
                    local_jpg.write_bytes(data)
        except Exception:
            pass

    # Fallback png
    if not local_jpg.exists() and not local_png.exists():
        try:
            url = HEADSHOT_URL_TEMPLATES[1].format(player_id=player_id)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
                if len(data) > 500:
                    local_png.write_bytes(data)
        except Exception:
            pass

    if local_jpg.exists():
        return "headshot.jpg"
    if local_png.exists():
        return "headshot.png"
    return None


def extract_report_summary(html_path: Path) -> dict:
    """Pull title/subtitle and a short blurb from existing HTML report."""
    summary = {"title": "", "subtitle": "", "blurb": ""}
    if not html_path.exists():
        return summary
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    if m:
        summary["title"] = m.group(1).replace(" 球探报告", "").strip()

    # Try to grab the scout summary paragraph
    m = re.search(r'<h2>\s*球探总评\s*</h2>\s*<p[^>]*>(.*?)</p>', text, re.S)
    if m:
        raw = re.sub(r"<[^>]+>", "", m.group(1))
        raw = re.sub(r"\s+", " ", raw)
        summary["blurb"] = raw.strip()[:200] + ("…" if len(raw) > 200 else "")
    m = re.search(r'<div class="header">.*?<p class="subtitle">(.*?)</p>', text, re.S)
    if m:
        summary["subtitle"] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
    # Fallback: first blockquote paragraph
    if not summary["blurb"]:
        m = re.search(r'<blockquote[^>]*>(.*?)</blockquote>', text, re.S)
        if m:
            raw = re.sub(r"<[^>]+>", "", m.group(1))
            raw = re.sub(r"\s+", " ", raw)
            summary["blurb"] = raw.strip()[:200] + ("…" if len(raw) > 200 else "")
    return summary


def fetch_player_stats(player_id: int) -> dict:
    """Fetch current season hitting/pitching stats for quick dashboard cards."""
    stats = {}
    try:
        url = f"https://statsapi.mlb.com/api/v1/people/{player_id}?hydrate=stats(group=[hitting,pitching],type=[season],season={SEASON})"
        data = fetch_json(url)
        person = data.get("people", [{}])[0]
        for group in person.get("stats", []):
            for split in group.get("splits", []):
                s = split.get("stat", {})
                if group["group"]["displayName"] == "Hitting":
                    stats.update({
                        "avg": s.get("avg", "-"),
                        "obp": s.get("obp", "-"),
                        "slg": s.get("slg", "-"),
                        "ops": s.get("ops", "-"),
                        "hr": s.get("homeRuns", "-"),
                        "rbi": s.get("rbi", "-"),
                    })
                elif group["group"]["displayName"] == "Pitching":
                    stats.update({
                        "era": s.get("era", "-"),
                        "whip": s.get("whip", "-"),
                        "w": s.get("wins", "-"),
                        "l": s.get("losses", "-"),
                        "so": s.get("strikeOuts", "-"),
                        "ip": s.get("inningsPitched", "-"),
                    })
    except Exception:
        pass
    return stats


def build_dashboard():
    roster_data = fetch_json(MLB_API_ROSTER)
    roster = roster_data.get("roster", [])

    players = []
    for entry in roster:
        person = entry.get("person", {})
        pid = person.get("id")
        name = person.get("fullName", "")
        pos = entry.get("position", {}).get("abbreviation", "")
        pos_type = entry.get("position", {}).get("type", "")
        status = entry.get("status", {}).get("code", "")
        jersey = entry.get("jerseyNumber", "")
        note = entry.get("note", "")

        slug = slugify(name)
        player_dir = REPORT_ROOT / slug
        html_report = player_dir / f"{slug}-scouting-report.html"
        report_exists = html_report.exists()

        # Download / locate headshot
        headshot_file = None
        if report_exists:
            headshot_file = download_headshot(pid, player_dir)

        summary = extract_report_summary(html_report) if report_exists else {}
        stats = fetch_player_stats(pid) if report_exists else {}

        # Determine role group
        role = pos
        if pos_type == "Pitcher":
            role_group = "Pitcher"
        elif pos_type == "Catcher":
            role_group = "Catcher"
        elif pos_type == "Infielder":
            role_group = "Infield"
        elif pos_type == "Outfielder":
            role_group = "Outfield"
        elif pos_type == "Two-Way Player":
            role_group = "Two-Way"
        else:
            role_group = "Other"

        players.append({
            "id": pid,
            "name": name,
            "slug": slug,
            "jersey": jersey,
            "position": pos,
            "role_group": role_group,
            "status": status,
            "status_label": STATUS_META.get(status, {}).get("label", status),
            "status_class": STATUS_META.get(status, {}).get("class", "status-other"),
            "report_exists": report_exists,
            "headshot": headshot_file,
            "note": note,
            "summary": summary,
            "stats": stats,
        })

    # Sort: active first, then by role group, then by jersey/name
    group_order = {"Pitcher": 0, "Catcher": 1, "Infield": 2, "Outfield": 3, "Two-Way": 4, "Other": 5}
    players.sort(key=lambda p: (
        0 if p["status"] == "A" else 1,
        group_order.get(p["role_group"], 9),
        p["name"],
    ))

    total = len(players)
    active = sum(1 for p in players if p["status"] == "A")
    il = sum(1 for p in players if p["status"].startswith("D"))
    minors = sum(1 for p in players if p["status"] == "RM")
    reports_ready = sum(1 for p in players if p["report_exists"])

    html = render_dashboard_html(players, total, active, il, minors, reports_ready)
    index_path = REPORT_ROOT / "index.html"
    index_path.write_text(html, encoding="utf-8")
    print(f"Dashboard written to: {index_path}")
    print(f"Players: {total} | Reports ready: {reports_ready} | Active: {active} | IL: {il} | Minors: {minors}")


def render_dashboard_html(players, total, active, il, minors, reports_ready):
    player_cards = []
    for p in players:
        headshot_path = f"{p['slug']}/{p['headshot']}" if p["headshot"] else ""
        headshot_html = (
            f'<img src="{headshot_path}" alt="{p["name"]}" loading="lazy">'
            if headshot_path
            else f'<div class="no-photo">{p["name"].split()[-1][:2]}</div>'
        )

        report_link = f"{p['slug']}/{p['slug']}-scouting-report.html" if p["report_exists"] else "#"
        card_disabled = "" if p["report_exists"] else "card-disabled"

        # Quick stats line - prefer scouting blurb if available
        if p["summary"].get("blurb"):
            stat_line = p["summary"]["blurb"]
        elif p["stats"].get("avg") and p["stats"]["avg"] != "-":
            stat_line = f"{p['stats'].get('avg', '-')}/{p['stats'].get('obp', '-')}/{p['stats'].get('slg', '-')} · {p['stats'].get('hr', '-')} HR · {p['stats'].get('rbi', '-')} RBI"
        elif p["stats"].get("era") and p["stats"]["era"] != "-":
            stat_line = f"ERA {p['stats'].get('era', '-')} · WHIP {p['stats'].get('whip', '-')} · {p['stats'].get('w', '-')}-{p['stats'].get('l', '-')} · {p['stats'].get('so', '-')} K"
        else:
            stat_line = p["summary"].get("subtitle") or ""

        jersey_html = f'<span class="jersey">#{p["jersey"]}</span>' if p["jersey"] else ""

        player_cards.append(f"""
        <article class="player-card {card_disabled}" data-group="{p['role_group']}" data-status="{p['status']}" data-name="{p['name'].lower()}">
            <a class="card-link" href="{report_link}" {"onclick=\"return false;\"" if not p["report_exists"] else ""}>
                <div class="photo-wrap">{headshot_html}</div>
                <div class="card-body">
                    <div class="card-top">
                        {jersey_html}
                        <span class="status {p['status_class']}">{p['status_label']}</span>
                    </div>
                    <h3>{p['name']}</h3>
                    <p class="position">{p['position']}</p>
                    <p class="stat-line">{stat_line}</p>
                </div>
            </a>
        </article>
        """)

    cards_html = "\n".join(player_cards)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Los Angeles Dodgers 2026 Player Reports</title>
    <style>
        :root {{
            --dodgers-blue: #005A9C;
            --dodgers-dark: #1a1a2e;
            --dodgers-light: #e0e0e0;
            --accent: #ff9800;
            --green: #4caf50;
            --red: #f44336;
            --gray: #90a4ae;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, var(--dodgers-dark) 0%, #16213e 50%, #0f3460 100%);
            color: var(--dodgers-light);
            min-height: 100vh;
        }}
        header {{
            background: linear-gradient(90deg, var(--dodgers-blue) 0%, #1a5490 100%);
            padding: 40px 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        header h1 {{ font-size: 2.6rem; margin-bottom: 8px; }}
        header p {{ opacity: 0.9; font-size: 1.1rem; }}
        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 25px;
        }}
        .stat-pill {{
            background: rgba(255,255,255,0.1);
            border-radius: 50px;
            padding: 10px 22px;
            font-size: 0.95rem;
        }}
        .stat-pill strong {{ font-size: 1.3rem; margin-right: 5px; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 30px 20px; }}
        .controls {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            justify-content: center;
            margin-bottom: 30px;
        }}
        .controls input, .controls select {{
            padding: 12px 16px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.07);
            color: #fff;
            font-size: 1rem;
            min-width: 220px;
        }}
        .controls input::placeholder {{ color: var(--gray); }}
        .controls select option {{ background: #1a1a2e; }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 22px;
        }}
        .player-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .player-card:hover {{ transform: translateY(-5px); box-shadow: 0 12px 30px rgba(0,0,0,0.4); }}
        .card-link {{ text-decoration: none; color: inherit; display: block; }}
        .card-disabled {{ opacity: 0.55; pointer-events: none; }}
        .photo-wrap {{
            height: 220px;
            background: linear-gradient(135deg, rgba(0,90,156,0.3) 0%, rgba(26,84,144,0.3) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}
        .photo-wrap img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center 30%;
        }}
        .no-photo {{
            font-size: 3rem;
            font-weight: bold;
            color: rgba(255,255,255,0.25);
            text-transform: uppercase;
        }}
        .card-body {{ padding: 18px; }}
        .card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .jersey {{
            background: var(--dodgers-blue);
            color: #fff;
            padding: 3px 10px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.85rem;
        }}
        .status {{
            font-size: 0.75rem;
            padding: 4px 10px;
            border-radius: 20px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .status-active {{ background: rgba(76,175,80,0.25); color: #81c784; }}
        .status-minors {{ background: rgba(144,164,174,0.25); color: #b0bec5; }}
        .status-il {{ background: rgba(244,67,54,0.25); color: #ef9a9a; }}
        .status-other {{ background: rgba(255,152,0,0.25); color: #ffcc80; }}
        .card-body h3 {{ font-size: 1.25rem; margin-bottom: 4px; color: #fff; }}
        .position {{
            color: var(--accent);
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 10px;
        }}
        .stat-line {{
            font-size: 0.85rem;
            color: var(--gray);
            line-height: 1.4;
            min-height: 36px;
        }}
        footer {{
            text-align: center;
            padding: 30px;
            color: var(--gray);
            font-size: 0.9rem;
        }}
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: var(--gray);
            display: none;
        }}
        @media (max-width: 600px) {{
            header h1 {{ font-size: 1.8rem; }}
            .grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>⚾ Los Angeles Dodgers</h1>
        <p>2026 Player Scouting Report Dashboard</p>
        <div class="stats-bar">
            <div class="stat-pill"><strong>{total}</strong> 40-Man Players</div>
            <div class="stat-pill"><strong>{active}</strong> Active</div>
            <div class="stat-pill"><strong>{il}</strong> Injured List</div>
            <div class="stat-pill"><strong>{minors}</strong> Minors</div>
            <div class="stat-pill"><strong>{reports_ready}</strong> Reports Ready</div>
        </div>
    </header>

    <div class="container">
        <div class="controls">
            <input type="text" id="search" placeholder="Search player name...">
            <select id="group-filter">
                <option value="">All Positions</option>
                <option value="Pitcher">Pitchers</option>
                <option value="Catcher">Catchers</option>
                <option value="Infield">Infielders</option>
                <option value="Outfield">Outfielders</option>
                <option value="Two-Way">Two-Way</option>
            </select>
            <select id="status-filter">
                <option value="">All Statuses</option>
                <option value="A">Active</option>
                <option value="D10">IL-10</option>
                <option value="D15">IL-15</option>
                <option value="D60">IL-60</option>
                <option value="RM">Minors</option>
            </select>
        </div>

        <div class="grid" id="grid">
            {cards_html}
        </div>
        <div class="empty-state" id="empty">No players match your filters.</div>
    </div>

    <footer>
        Generated {datetime.now().strftime("%Y-%m-%d %H:%M")} · Data from MLB Stats API · Headshots from MLB.com
    </footer>

    <script>
        const search = document.getElementById('search');
        const groupFilter = document.getElementById('group-filter');
        const statusFilter = document.getElementById('status-filter');
        const grid = document.getElementById('grid');
        const empty = document.getElementById('empty');
        const cards = Array.from(document.querySelectorAll('.player-card'));

        function filter() {{
            const term = search.value.toLowerCase();
            const group = groupFilter.value;
            const status = statusFilter.value;
            let visible = 0;

            cards.forEach(card => {{
                const nameMatch = card.dataset.name.includes(term);
                const groupMatch = !group || card.dataset.group === group;
                const statusMatch = !status || card.dataset.status === status;
                const show = nameMatch && groupMatch && statusMatch;
                card.style.display = show ? '' : 'none';
                if (show) visible++;
            }});

            empty.style.display = visible ? 'none' : 'block';
        }}

        search.addEventListener('input', filter);
        groupFilter.addEventListener('change', filter);
        statusFilter.addEventListener('change', filter);
    </script>
</body>
</html>
"""


if __name__ == "__main__":
    build_dashboard()
