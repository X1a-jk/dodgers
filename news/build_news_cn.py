# -*- coding: utf-8 -*-
"""Rebuild D:\\baseball\\news\\news-cn.json from cache files."""
import json
from datetime import datetime, timezone

BASE = r"D:\baseball\news"

# (title_cn, [topics], top) keyed by url
META = {
    # ---- mlb ----
    "https://www.mlb.com/news/shohei-ohtani-hopes-to-shake-off-rust-heading-into-2026-postseason":
        ("大谷翔平盼摆脱锈迹迎接 2026 季后赛", ["injury", "game"], True),
    "https://www.mlb.com/news/dave-roberts-ties-record-for-100-win-seasons-as-manager":
        ("戴夫·罗伯茨追平教头百胜赛季纪录", ["game", "offfield"], True),
    "https://www.mlb.com/news/dodgers-2026-postseason-faq":
        ("道奇 2026 季后赛 FAQ", ["game"], True),
    "https://www.mlb.com/news/fill-out-your-postseason-bracket-2026":
        ("填写季后赛预测对阵表，冲击 1 万美元奖金", ["offfield"], False),
    "https://www.mlb.com/news/mlb-postseason-power-rankings-for-2026-wild-card-series":
        ("外卡系列赛在即，MLB 季后赛实力排名出炉", ["game"], False),
    "https://www.mlb.com/news/solve-today-s-dodgers-trivia-puzzle":
        ("道奇每日 trivia 竞猜", ["offfield"], False),
    "https://www.mlb.com/news/blake-snell-solid-in-final-regular-season-tuneup-following-groin-injury":
        ("斯内尔腹股沟伤愈，常规赛收官热身表现稳健", ["injury", "game"], True),
    "https://www.mlb.com/news/dodgers-injuries-and-roster-moves":
        ("道奇伤病与阵容变动汇总", ["injury", "roster"], False),
    "https://www.mlb.com/news/dodgers-top-30-prospects-list-139354450":
        ("道奇农场 Top 30 新秀榜单", ["farm"], False),
    "https://www.mlb.com/news/dodgers-triple-a-affiliate-oklahoma-city-wins-2026-national-championship":
        ("道奇 3A 附属球队夺得 2026 全国锦标赛冠军", ["farm"], True),
    "https://www.mlb.com/news/blake-treinen-out-for-2026-postseason-with-shoulder-injury":
        ("特雷宁肩伤赛季报销，无缘 2026 季后赛", ["injury", "roster"], True),
    "https://www.mlb.com/news/tarik-skubal-throws-seven-scoreless-as-dodgers-shut-out-giants":
        ("斯库巴尔七局无失分，道奇完封巨人", ["game"], False),
    "https://www.mlb.com/news/dodgers-secure-first-round-bye-for-2026-postseason":
        ("道奇锁定 2026 季后赛首轮轮空", ["game"], True),
    "https://www.mlb.com/news/dodgers-prospect-james-tibbs-iii-records-100-rbi-walks-runs-season":
        ("詹姆斯·蒂布斯三世在 3A 打出历史级赛季", ["farm"], False),
    "https://www.mlb.com/news/dalton-rushing-activation-sept-25":
        ("道尔顿·拉欣从伤病名单激活", ["injury", "roster"], False),
    "https://www.mlb.com/news/greatest-pitcher-debate-justin-verlander-max-scherzer-clayton-kershaw-zack-greinke":
        ("历史最强投手之争：韦兰德、谢泽尔、克肖还是格雷恩基", ["offfield"], False),
    "https://www.mlb.com/news/most-popular-mlb-players-jerseys-for-2026-season":
        ("2026 赛季 MLB 球衣销量榜出炉", ["offfield"], False),
    "https://www.mlb.com/news/dodgers-set-new-franchise-record-for-attendance-in-2026":
        ("道奇 2026 年上座数刷新队史纪录", ["offfield"], True),
    "https://www.mlb.com/news/will-smith-is-dodgers-nominee-for-roberto-clemente-award":
        ("威尔·史密斯获选道奇 Roberto Clemente 奖提名人", ["offfield"], False),
    "https://www.mlb.com/news/dodgers-triple-a-affiliate-oklahoma-city-wins-2026-pacific-coast-league-title":
        ("道奇 3A 俄克拉荷马城夺得 2026 太平洋海岸联盟冠军", ["farm"], True),
    # ---- dn ----
    "https://dodgersnation.com/miguel-rojas-gets-emotional-in-what-could-be-final-regular-season-game/2026/09/27/":
        ("罗哈斯动情落泪，或迎常规赛谢幕战", ["roster", "offfield"], True),
    "https://dodgersnation.com/dodgers-late-inning-surge-brings-them-100th-win-of-season/2026/09/27/":
        ("道奇后段发力，拿下赛季第 100 胜", ["game"], True),
    "https://dodgersnation.com/edgardo-henriquez-trending-in-right-direction-for-nlds-roster/2026/09/27/":
        ("恩里克斯伤势恢复向好，有望赶上 NLDS 名单", ["injury", "roster"], True),
    "https://dodgersnation.com/josue-de-paula-to-join-team-during-bye-with-roster-decision-looming/2026/09/27/":
        ("德保拉轮空期加入球队，名单抉择在即", ["roster", "farm"], True),
    "https://dodgersnation.com/dodgers-gear-up-for-postseason-with-full-strength-lineup/2026/09/27/":
        ("道奇以完整先发阵容备战季后赛", ["roster", "game"], True),
    "https://dodgersnation.com/comets-win-1st-triple-a-national-championship-in-extra-innings-thriller/2026/09/27/":
        ("彗星座加局鏖战夺队史首座 3A 全国锦标赛", ["farm"], True),
    "https://dodgersnation.com/3-dodgers-players-who-could-replace-blake-treinen-on-postseason-roster/2026/09/27/":
        ("三位道奇球员有望顶替特雷宁进入季后赛名单", ["roster"], True),
    "https://dodgersnation.com/blake-treinen-suffers-season-ending-injury-during-giants-warm-up/2026/09/26/":
        ("特雷宁热身时遭遇赛季终结伤病", ["injury"], True),
    "https://dodgersnation.com/kike-hernandez-shows-october-form-vs-giants-for-99th-win/2026/09/26/":
        ("基克·埃尔南德斯对巨人打出十月状态，助道奇取第 99 胜", ["game"], False),
    "https://dodgersnation.com/former-dodgers-pitcher-kirby-yates-retires-after-12-year-mlb-career/2026/09/26/":
        ("前道奇投手柯比·耶茨 12 年大联盟生涯后退役", ["offfield"], False),
    "https://dodgersnation.com/dodgers-lineup-vs-giants-freddie-freeman-sits-miguel-rojas-returns/2026/09/26/":
        ("道奇对巨人先发阵容：弗里曼轮休，罗哈斯回归", ["roster", "game"], False),
    "https://dodgersnation.com/roki-sasakis-dodgers-bullpen-transformation-continues-with-dominant-outing/2026/09/25/":
        ("佐佐木朗希牛棚转型持续进化，再投统治级表现", ["roster", "game"], True),
    # ---- athletic ----
    "https://www.nytimes.com/athletic/7638819/2026/09/28/mlb-wild-card-series-staff-predictions-2026/":
        ("2026 外卡系列赛专家预测出炉", ["game"], False),
    "https://www.nytimes.com/athletic/7638511/2026/09/28/mlb-playoffs-salary-cap-competitive-balance/":
        ("季后赛格局引发工资帽与竞争力平衡之争", ["offfield"], False),
    "https://www.nytimes.com/athletic/7637579/2026/09/27/dodgers-100-wins-postseason-roster/":
        ("道奇 100 胜与季后赛名单展望", ["game", "roster"], True),
    "https://www.nytimes.com/athletic/7632764/2026/09/27/mlb-postseason-2026-power-rankings/":
        ("MLB 2026 季后赛实力排名", ["game"], False),
    "https://www.nytimes.com/athletic/7635435/2026/09/27/mlb-postseason-bracket-stats-best-worst/":
        ("MLB 季后赛对阵表数据盘点：最好与最坏", ["game"], False),
    "https://www.nytimes.com/athletic/7633797/2026/09/26/dodgers-health-blake-snell-shohei-ohtani/":
        ("道奇健康报告：斯内尔与大谷的伤情进展", ["injury"], True),
    "https://www.nytimes.com/athletic/7626065/2026/09/25/mlb-playoff-rankings-offense/":
        ("MLB 季后赛进攻实力排名", ["game"], False),
    "https://www.nytimes.com/athletic/7623345/2026/09/24/dodgers-first-round-bye-clinched/":
        ("道奇锁定首轮轮空", ["game"], True),
}

DIGEST = [
    "道奇后段发力拿下赛季第 100 胜，戴夫·罗伯茨追平教头百胜赛季纪录，并锁定首轮轮空全力备战国联分区赛。",
    "终结者布莱克·特雷宁肩伤赛季报销确定无缘季后赛，顶替人选浮出水面，佐佐木朗希牛棚转型渐入佳境、恩里克斯恢复向好。",
    "健康报告：大谷翔平坦言需要摆脱锈迹，斯内尔腹股沟伤愈后收官热身稳健，道奇以完整先发阵容迎接季后赛。",
    "名单博弈：德保拉轮空期报到接受最后考察，拉欣从伤病名单激活，罗哈斯动情落泪或迎常规赛谢幕战。",
    "农场报喜：3A 俄克拉荷马城彗星座加局鏖战夺得队史首座全国锦标赛冠军，蒂布斯三世打出历史级赛季。",
    "场外双纪录：道奇 2026 上座数刷新队史纪录，威尔·史密斯获选 Roberto Clemente 奖球队提名人。",
]

def link(src, url):
    return {"source": src, "url": url}

TOP = [
    {
        "title_cn": "道奇拿下赛季第 100 胜，罗伯茨追平教头百胜纪录",
        "title_en": "Dodgers’ Late-Inning Surge Brings Them 100th Win of Season",
        "sources": ["dn", "mlb", "athletic"],
        "time": "2026-09-27T15:03:46+00:00",
        "links": [
            link("dn", "https://dodgersnation.com/dodgers-late-inning-surge-brings-them-100th-win-of-season/2026/09/27/"),
            link("mlb", "https://www.mlb.com/news/dave-roberts-ties-record-for-100-win-seasons-as-manager"),
            link("mlb", "https://www.mlb.com/news/dodgers-2026-postseason-faq"),
            link("athletic", "https://www.nytimes.com/athletic/7637579/2026/09/27/dodgers-100-wins-postseason-roster/"),
        ],
    },
    {
        "title_cn": "终结者特雷宁肩伤赛季报销，牛棚重组人选浮出水面",
        "title_en": "Blake Treinen out for 2026 postseason with shoulder injury",
        "sources": ["mlb", "dn"],
        "time": "2026-09-27T00:39:05+00:00",
        "links": [
            link("mlb", "https://www.mlb.com/news/blake-treinen-out-for-2026-postseason-with-shoulder-injury"),
            link("dn", "https://dodgersnation.com/blake-treinen-suffers-season-ending-injury-during-giants-warm-up/2026/09/26/"),
            link("dn", "https://dodgersnation.com/3-dodgers-players-who-could-replace-blake-treinen-on-postseason-roster/2026/09/27/"),
            link("dn", "https://dodgersnation.com/roki-sasakis-dodgers-bullpen-transformation-continues-with-dominant-outing/2026/09/25/"),
        ],
    },
    {
        "title_cn": "道奇健康报告：大谷找状态、斯内尔伤愈热身稳健",
        "title_en": "Dodgers Health Blake Snell Shohei Ohtani",
        "sources": ["mlb", "athletic"],
        "time": "2026-09-27T23:35:00+00:00",
        "links": [
            link("mlb", "https://www.mlb.com/news/shohei-ohtani-hopes-to-shake-off-rust-heading-into-2026-postseason"),
            link("mlb", "https://www.mlb.com/news/blake-snell-solid-in-final-regular-season-tuneup-following-groin-injury"),
            link("athletic", "https://www.nytimes.com/athletic/7633797/2026/09/26/dodgers-health-blake-snell-shohei-ohtani/"),
        ],
    },
    {
        "title_cn": "季后赛名单最后拼图：恩里克斯伤愈向好、德保拉轮空期报到、罗哈斯或迎谢幕战",
        "title_en": "Dodgers Gear Up for Postseason With Full Strength Lineup",
        "sources": ["dn", "mlb"],
        "time": "2026-09-27T10:32:09+00:00",
        "links": [
            link("dn", "https://dodgersnation.com/dodgers-gear-up-for-postseason-with-full-strength-lineup/2026/09/27/"),
            link("dn", "https://dodgersnation.com/edgardo-henriquez-trending-in-right-direction-for-nlds-roster/2026/09/27/"),
            link("dn", "https://dodgersnation.com/josue-de-paula-to-join-team-during-bye-with-roster-decision-looming/2026/09/27/"),
            link("dn", "https://dodgersnation.com/miguel-rojas-gets-emotional-in-what-could-be-final-regular-season-game/2026/09/27/"),
            link("mlb", "https://www.mlb.com/news/dodgers-injuries-and-roster-moves"),
        ],
    },
    {
        "title_cn": "3A 俄克拉荷马城彗星座夺得队史首座全国锦标赛冠军",
        "title_en": "Dodgers affiliate wins 2026 Triple-A National Championship",
        "sources": ["mlb", "dn"],
        "time": "2026-09-27T07:48:00+00:00",
        "links": [
            link("mlb", "https://www.mlb.com/news/dodgers-triple-a-affiliate-oklahoma-city-wins-2026-national-championship"),
            link("mlb", "https://www.mlb.com/news/dodgers-triple-a-affiliate-oklahoma-city-wins-2026-pacific-coast-league-title"),
            link("dn", "https://dodgersnation.com/comets-win-1st-triple-a-national-championship-in-extra-innings-thriller/2026/09/27/"),
        ],
    },
    {
        "title_cn": "季后赛预览：实力排名、对阵预测与阵容数据盘点齐发",
        "title_en": "MLB Playoff Power Rankings ahead of Wild Card Series",
        "sources": ["mlb", "athletic"],
        "time": "2026-09-28T04:00:00+00:00",
        "links": [
            link("mlb", "https://www.mlb.com/news/mlb-postseason-power-rankings-for-2026-wild-card-series"),
            link("athletic", "https://www.nytimes.com/athletic/7632764/2026/09/27/mlb-postseason-2026-power-rankings/"),
            link("athletic", "https://www.nytimes.com/athletic/7638819/2026/09/28/mlb-wild-card-series-staff-predictions-2026/"),
            link("athletic", "https://www.nytimes.com/athletic/7635435/2026/09/27/mlb-postseason-bracket-stats-best-worst/"),
        ],
    },
]

items = []
for src in ("mlb", "dn", "athletic"):
    with open(rf"{BASE}\cache\{src}.json", encoding="utf-8") as f:
        cache = json.load(f)
    for it in cache["items"]:
        url = it["url"]
        if url not in META:
            raise SystemExit(f"MISSING META: {url}")
        cn, topics, top = META[url]
        entry = {
            "title_cn": cn,
            "title_en": it["title"],
            "url": url,
            "source": src,
            "time": it["time"],
            "topics": topics,
        }
        if top:
            entry["top"] = True
        items.append(entry)

out = {
    "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
    "digest": DIGEST,
    "top": TOP,
    "items": items,
}

with open(rf"{BASE}\news-cn.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

# ---- validation ----
allowed = {"mlb", "dn", "athletic"}
topics_allowed = {"injury", "roster", "farm", "game", "offfield"}
with open(rf"{BASE}\news-cn.json", encoding="utf-8") as f:
    data = json.load(f)
assert data["digest"] and 4 <= len(data["digest"]) <= 6, "digest bad"
assert 3 <= len(data["top"]) <= 6, "top count bad"
assert all(i["source"] in allowed for i in data["items"]), "bad source"
assert all(1 <= len(i["topics"]) <= 3 and set(i["topics"]) <= topics_allowed for i in data["items"]), "bad topics"
total = sum(len(json.load(open(rf"{BASE}\cache\{s}.json", encoding="utf-8"))["items"]) for s in ("mlb", "dn", "athletic"))
assert len(data["items"]) == total, f"count mismatch: {len(data['items'])} vs {total}"
for t in data["top"]:
    assert t["sources"] and all(l["source"] in t["sources"] for l in t["links"]), "top sources/links mismatch"
print(f"OK generated={data['generated']} items={len(data['items'])} top={len(data['top'])} digest={len(data['digest'])}")
