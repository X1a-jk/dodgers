# -*- coding: utf-8 -*-
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'D:\baseball\news'
OLD = json.load(open(BASE + r'\news-cn.json', encoding='utf-8'))
old_by_url = {it['url']: it for it in OLD['items']}

NEW_T = {
 'https://www.mlb.com/news/charles-davalan-eduardo-quintero-emil-morales-excel-with-dodgers-high-a-affiliate':
   ('Charles Davalan、Eduardo Quintero、Emil Morales 在高阶1A有出色表现', ['farm'], False),
 'https://dodgersnation.com/2-dodgers-players-have-zero-chance-of-making-postseason-roster/2026/09/11/':
   ('DN 点名两名道奇球员进季后赛名单“毫无机会”', ['roster','game'], False),
 'https://dodgersnation.com/25-years-later-how-the-dodgers-and-baseball-responded-to-9-11/2026/09/11/':
   ('25 年后回看：道奇与棒球界当年如何回应 9/11 事件', ['offfield'], False),
 'https://dodgersnation.com/things-to-do-in-la-sept-11-13-la-card-show-at-dodger-stadium-joe-kelly-in-charity-golf-tourney/2026/09/11/':
   ('本周末洛杉矶活动：道奇球场卡展、Joe Kelly 慈善高尔夫赛', ['offfield'], False),
 'https://www.nytimes.com/athletic/7582397/2026/09/11/shohei-ohtani-injured-dodgers-decisions/':
   ('大谷伤情罗生门谁该负责？Athletic：人人都有份', ['injury','offfield'], True),
}

# top=true for items belonging to top groups
FORCE_TOP = {
 'https://www.mlb.com/news/emmet-sheehan-strikes-out-10-as-dodgers-win-5th-straight',
 'https://www.mlb.com/news/tarik-skubal-starts-for-dodgers-vs-reds-on-sept-8',
 'https://dodgersnation.com/its-time-for-the-dodgers-to-hand-the-closer-role-to-their-biggest-breakout-star/2026/09/10/',
 'https://dodgersnation.com/dodgers-magic-number-drops-again-as-first-round-bye-comes-into-focus/2026/09/09/',
 'https://www.mlb.com/news/dodgers-storylines-ahead-of-postseason-with-shohei-ohtani-josue-de-paula-freddie-freeman',
}
FORCE_NOT_TOP = {
 'https://dodgersnation.com/5-things-dodgers-fans-need-to-know-about-top-prospect-josue-de-paula/2026/09/10/',
}

items = []
for src in ['mlb','dn','athletic']:
    cache = json.load(open(BASE + rf'\cache\{src}.json', encoding='utf-8'))
    for it in cache['items']:
        url = it['url']
        if url in NEW_T:
            cn, topics, top = NEW_T[url]
        elif url in old_by_url:
            o = old_by_url[url]
            cn, topics, top = o['title_cn'], o['topics'], o.get('top', False)
        else:
            raise SystemExit('missing translation: ' + url)
        if url in FORCE_TOP: top = True
        if url in FORCE_NOT_TOP: top = False
        entry = {'title_cn': cn, 'title_en': it['title'], 'url': url,
                 'source': src, 'time': it['time'], 'topics': topics}
        if top: entry['top'] = True
        items.append(entry)

digest = [
 '大谷翔平因膝伤与二头肌伤正式进入伤病名单、本赛季不再登板；Athletic 发文追问责任归属，直言球队、经纪人与球员三方都有份，伤情罗生门持续发酵。',
 '头号新秀 Josue De Paula 上调大联盟，球队公布其在季后赛冲刺阶段的重要角色，首秀表现备受期待。',
 '道奇以 7 连胜收官主场赛程，稳居国联 2 号种子，魔术数字持续下降，首轮轮空越来越近。',
 'Edwin Díaz 在 3A 完成第三次复健登板、状态回升，DN 喊话应尽快敲定终结者人选。',
 'DN 点名两名球员进入季后赛名单“毫无机会”；Freddie Freeman 因右膝酸痛缺阵，伤病名单压力不减。',
 '场外声音：Skubal 休赛季或被要价 5 亿美元历史级合同；9·11 二十五周年，回看道奇与棒球界的回应。',
]

top = [
 {'title_cn':'大谷翔平进入伤病名单：膝伤+二头肌伤，本赛季不再投球',
  'title_en':'Shohei Ohtani placed on injured list with knee, biceps injuries',
  'sources':['mlb','dn','athletic'],
  'time':'2026-09-10T06:28:00+00:00',
  'links':[
   {'source':'mlb','url':'https://www.mlb.com/news/shohei-ohtani-out-of-lineup-again-vs-reds'},
   {'source':'dn','url':'https://dodgersnation.com/dodgers-to-put-shohei-ohtani-on-injured-list-as-injury-concerns-worsen/2026/09/09/'},
   {'source':'athletic','url':'https://www.nytimes.com/athletic/7580811/2026/09/10/shohei-ohtani-dodgers-injured-list/'}]},
 {'title_cn':'大谷伤情罗生门：Athletic 称球队、经纪人、球员都有责任',
  'title_en':"Who's to blame in the Shohei Ohtani injury saga? Everyone",
  'sources':['athletic','dn'],
  'time':'2026-09-11T12:00:00+00:00',
  'links':[
   {'source':'athletic','url':'https://www.nytimes.com/athletic/7582397/2026/09/11/shohei-ohtani-injured-dodgers-decisions/'},
   {'source':'dn','url':'https://dodgersnation.com/mlb-reporter-questions-shohei-ohtanis-injury-communication-with-dodgers/2026/09/10/'},
   {'source':'athletic','url':'https://www.nytimes.com/athletic/7580876/2026/09/10/dodgers-shohei-ohtani-josue-de-paula/'}]},
 {'title_cn':'头号新秀 Josue De Paula 上调大联盟，球队公布其重要角色',
  'title_en':'Dodgers calling up top prospect Josue De Paula',
  'sources':['mlb','dn','athletic'],
  'time':'2026-09-10T06:52:00+00:00',
  'links':[
   {'source':'mlb','url':'https://www.mlb.com/news/josue-de-paula-top-prospect-called-up-dodgers'},
   {'source':'dn','url':'https://dodgersnation.com/dodgers-reveal-major-role-for-josue-de-paula-after-historic-promotion/2026/09/10/'},
   {'source':'athletic','url':'https://www.nytimes.com/athletic/7580666/2026/09/10/dodgers-josue-de-paula-call-up-prospect/'}]},
 {'title_cn':'7 连胜收官主场赛程，2 号种子+首轮轮空在望',
  'title_en':'Dodgers End Homestand With 7 Consecutive Wins, Hold Firm Grip on No. 2 Seed',
  'sources':['dn','mlb'],
  'time':'2026-09-09T21:42:22+00:00',
  'links':[
   {'source':'dn','url':'https://dodgersnation.com/dodgers-end-homestand-with-7-consecutive-wins-hold-firm-grip-on-no-2-seed/2026/09/09/'},
   {'source':'dn','url':'https://dodgersnation.com/dodgers-magic-number-drops-again-as-first-round-bye-comes-into-focus/2026/09/09/'},
   {'source':'mlb','url':'https://www.mlb.com/news/emmet-sheehan-strikes-out-10-as-dodgers-win-5th-straight'}]},
 {'title_cn':'Edwin Díaz 3A 复健进展顺利，终结者角色归属引热议',
  'title_en':'Edwin Díaz makes third rehab appearance at Triple-A',
  'sources':['mlb','dn'],
  'time':'2026-09-11T02:35:23+00:00',
  'links':[
   {'source':'mlb','url':'https://www.mlb.com/news/edwin-diaz-makes-third-rehab-appearance-at-triple-a'},
   {'source':'dn','url':'https://dodgersnation.com/its-time-for-the-dodgers-to-hand-the-closer-role-to-their-biggest-breakout-star/2026/09/10/'}]},
 {'title_cn':'Skubal 休赛季或被要价 5 亿美元历史级合同',
  'title_en':'Tarik Skubal Could Command Historic $500 Million Deal in Dodgers Free Agency',
  'sources':['dn','mlb'],
  'time':'2026-09-10T14:34:09+00:00',
  'links':[
   {'source':'dn','url':'https://dodgersnation.com/tarik-skubal-could-command-historic-500-million-deal-in-dodgers-free-agency/2026/09/10/'},
   {'source':'mlb','url':'https://www.mlb.com/news/tarik-skubal-starts-for-dodgers-vs-reds-on-sept-8'}]},
]

out = {'generated':'2026-09-11T18:55:00+00:00','digest':digest,'top':top,'items':items}
with open(BASE + r'\news-cn.json','w',encoding='utf-8') as f:
    json.dump(out,f,ensure_ascii=False,indent=1)
print('items:',len(items))
