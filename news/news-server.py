#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dodgers 社媒与新闻聚合 — 独立页面服务（已整合进门户，本服务保留备用）
门户版:  python portal/server.py  → http://localhost:8080 → 「新闻中心」

用法:  python news-server.py [端口]   (默认 8964)
"""
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import news_fetch as nf

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8964


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _html(self, text):
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        p = urlparse(self.path).path
        if p in ("/", "/index.html"):
            self._html(INDEX_HTML)
        elif p == "/api/all":
            mods = {}
            for mid in nf.MODULES:
                mods[mid] = nf.read_cache(mid) or {
                    "module": mid, "label": nf.LABELS[mid],
                    "updated": None, "items": [], "never": True}
            self._json({"modules": mods})
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        p = urlparse(self.path)
        if p.path == "/api/refresh":
            mid = parse_qs(p.query).get("id", [""])[0]
            if mid not in nf.MODULES:
                self._json({"ok": False, "error": "未知模块"}, 400)
                return
            ok, data, err = nf.refresh(mid)
            if ok:
                self._json({"ok": True, "module": data})
            else:
                self._json({"ok": False, "error": err,
                            "module": data or {"module": mid, "items": []}})
        else:
            self._json({"error": "not found"}, 404)


INDEX_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>⚾ Dodgers 社媒与新闻聚合</title>
<style>
:root{
  --bg:#0d1117; --card:#161b22; --card2:#1c2330; --line:#2b3442;
  --txt:#e6edf3; --sub:#8b98a9; --blue:#1d6fd1; --blue2:#3b8bff;
  --red:#ef3e42; --green:#3fb950; --yellow:#d29922; --gray:#6e7681;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--txt);font-family:"Segoe UI",system-ui,"Microsoft YaHei",sans-serif;min-height:100vh;padding:18px}
.wrap{max-width:1200px;margin:0 auto}
header{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin-bottom:16px}
header h1{font-size:20px;font-weight:700;letter-spacing:.5px}
header h1 .la{color:var(--blue2)}
.btn{background:var(--blue);color:#fff;border:none;border-radius:8px;padding:8px 14px;font-size:13px;cursor:pointer;transition:.15s}
.btn:hover{background:var(--blue2)}
.btn:disabled{opacity:.5;cursor:wait}
.btn.ghost{background:var(--card2);border:1px solid var(--line)}
.btn.ghost:hover{border-color:var(--blue)}
select{background:var(--card2);color:var(--txt);border:1px solid var(--line);border-radius:8px;padding:7px 10px;font-size:13px}
.global-status{font-size:12px;color:var(--sub);margin-left:auto}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;display:flex;flex-direction:column;overflow:hidden}
.card-head{display:flex;align-items:center;gap:8px;padding:12px 14px;border-bottom:1px solid var(--line);background:var(--card2)}
.card-head .dot{width:8px;height:8px;border-radius:50%;flex:none}
.dot.green{background:var(--green)} .dot.yellow{background:var(--yellow)}
.dot.gray{background:var(--gray)} .dot.red{background:var(--red)}
.card-head h2{font-size:14px;font-weight:600;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card-head .time{font-size:11px;color:var(--sub);white-space:nowrap}
.icon-btn{background:none;border:1px solid var(--line);border-radius:6px;color:var(--sub);width:28px;height:28px;cursor:pointer;font-size:14px;flex:none;transition:.15s}
.icon-btn:hover{color:var(--blue2);border-color:var(--blue)}
.icon-btn.spin{animation:spin 1s linear infinite;color:var(--blue2)}
@keyframes spin{to{transform:rotate(360deg)}}
.card-body{padding:8px 0;overflow-y:auto;max-height:560px;flex:1}
.item{display:flex;gap:10px;padding:9px 14px;border-bottom:1px solid #21262e;align-items:baseline}
.item:last-child{border-bottom:none}
.item:hover{background:#1a2029}
.item .t{font-size:13px;line-height:1.45;flex:1}
.item .t a{color:var(--txt);text-decoration:none}
.item .t a:hover{color:var(--blue2);text-decoration:underline}
.item .meta{font-size:11px;color:var(--sub);white-space:nowrap}
.badge{font-size:10px;padding:1px 6px;border-radius:4px;margin-right:6px;vertical-align:1px}
.b-mlb{background:#00326333;color:#7fb3ff;border:1px solid #00326388}
.b-dn{background:#ef3e4222;color:#ff9a9c;border:1px solid #ef3e4255}
.b-athletic{background:#d29d4b22;color:#e8c07a;border:1px solid #d29d4b55}
.empty,.error{padding:24px 14px;text-align:center;color:var(--sub);font-size:13px;line-height:1.7}
.error{color:#ff9a9c}
.x-hint{padding:10px 14px 0;font-size:11px;color:var(--sub)}
#x-widget{padding:8px 10px}
footer{margin-top:14px;font-size:11px;color:var(--gray);text-align:center;line-height:1.8}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>⚾ <span class="la">Dodgers</span> 社媒与新闻聚合</h1>
    <button class="btn" id="refresh-all">⟳ 全部刷新</button>
    <label style="font-size:12px;color:var(--sub)">自动刷新
      <select id="auto">
        <option value="0">关闭</option>
        <option value="180">3 分钟</option>
        <option value="600">10 分钟</option>
        <option value="1800">30 分钟</option>
      </select>
    </label>
    <span class="global-status" id="gstatus"></span>
  </header>
  <div class="grid" id="grid"></div>
  <footer>
    数据源：MLB.com 官方 API · Dodgers Nation · The Athletic · X 官方组件（浏览器直连）<br>
    每个模块独立缓存，刷新只重抓对应模块；接口故障时自动保留上次内容。
  </footer>
</div>

<script>
const MODS = [
  {id:'mlb',      name:'MLB.com 道奇新闻', badge:'b-mlb',      badgeTxt:'MLB'},
  {id:'dn',       name:'Dodgers Nation',   badge:'b-dn',       badgeTxt:'DN'},
  {id:'athletic', name:'The Athletic',     badge:'b-athletic', badgeTxt:'ATH'},
  {id:'x',        name:'Dodgers 官方 X',   badge:'',           badgeTxt:''},
];

const grid = document.getElementById('grid');
const cards = {};

function el(tag, cls, text){ const e=document.createElement(tag); if(cls)e.className=cls; if(text!=null)e.textContent=text; return e; }

function relTime(iso){
  if(!iso) return '—';
  const d = new Date(iso), diff = (Date.now() - d.getTime())/1000;
  if(diff < 60) return '刚刚';
  if(diff < 3600) return Math.floor(diff/60) + ' 分钟前';
  if(diff < 86400) return Math.floor(diff/3600) + ' 小时前';
  return Math.floor(diff/86400) + ' 天前';
}

function dotClass(updated){
  if(!updated) return 'gray';
  const diff = (Date.now() - new Date(updated).getTime())/1000;
  if(diff < 600) return 'green';
  if(diff < 3600) return 'yellow';
  return 'gray';
}

MODS.forEach(m=>{
  const card = el('div','card');
  const head = el('div','card-head');
  const dot = el('span','dot gray');
  const h2 = el('h2','',m.name);
  const time = el('span','time','—');
  const btn = el('button','icon-btn','⟳'); btn.title='单独刷新此模块';
  head.append(dot,h2,time,btn);
  const body = el('div','card-body');
  body.append(el('div','empty','尚未加载，点击 ⟳ 刷新'));
  card.append(head,body);
  grid.append(card);
  cards[m.id] = {el:card, dotEl:dot, timeEl:time, bodyEl:body, btnEl:btn, def:m};
  btn.addEventListener('click', ()=>refreshOne(m.id));
});

function renderList(mid, data){
  const c = cards[mid], body = c.bodyEl;
  body.innerHTML = '';
  if(!data.items || !data.items.length){
    body.append(el('div','empty','暂无内容，点击 ⟳ 刷新试试'));
    return;
  }
  data.items.forEach(it=>{
    const row = el('div','item');
    const t = el('div','t');
    if(c.def.badge) t.append(el('span','badge '+c.def.badge, c.def.badgeTxt));
    const a = el('a','',it.title||'(无标题)');
    a.href = it.url; a.target = '_blank'; a.rel = 'noopener';
    t.append(a);
    row.append(t, el('span','meta', relTime(it.time)));
    body.append(row);
  });
}

function renderX(){
  const c = cards['x'], body = c.bodyEl;
  body.innerHTML = '';
  body.append(el('div','x-hint','X 由浏览器直连 x.com 加载，若无法显示多为网络问题，点 ⟳ 重试'));
  const box = el('div',''); box.id = 'x-widget';
  body.append(box);
  const a = el('a','twitter-timeline','Posts by @Dodgers');
  a.href = 'https://x.com/Dodgers';
  a.setAttribute('data-height','560');
  a.setAttribute('data-theme','dark');
  a.setAttribute('data-chrome','noheader nofooter transparent noscrollbar');
  box.append(a);
  if(window.twttr && twttr.widgets){ twttr.widgets.load(box); }
  c.timeEl.textContent = '刚刚';
  c.dotEl.className = 'dot green';
}

function applyData(mid, data){
  const c = cards[mid];
  if(mid === 'x'){ renderX(); return; }
  renderList(mid, data);
  c.timeEl.textContent = data.updated ? relTime(data.updated) : '—';
  c.dotEl.className = 'dot ' + dotClass(data.updated);
}

function setLoading(mid, on){
  const c = cards[mid];
  c.btnEl.disabled = on;
  c.btnEl.classList.toggle('spin', on);
}

function flashError(mid, msg){
  const c = cards[mid];
  c.dotEl.className = 'dot red';
  const old = c.bodyEl.querySelector('.error');
  if(old) old.remove();
  const err = el('div','error','⚠ 刷新失败：' + msg + '（以下为上次缓存内容）');
  c.bodyEl.prepend(err);
}

async function refreshOne(mid){
  setLoading(mid, true);
  const ctrl = new AbortController();
  const timer = setTimeout(()=>ctrl.abort(), 25000);
  try{
    const r = await fetch('/api/refresh?id='+mid, {method:'POST', signal:ctrl.signal});
    const j = await r.json();
    if(j.ok){
      if(mid === 'x'){ renderX(); }
      else if(j.module){ applyData(mid, j.module); }
    } else {
      if(j.module && j.module.items && j.module.items.length){ applyData(mid, j.module); }
      flashError(mid, j.error || '网络错误');
    }
  }catch(e){
    flashError(mid, e.name==='AbortError' ? '请求超时' : '无法连接本地服务');
  }finally{
    clearTimeout(timer);
    setLoading(mid, false);
  }
}

async function loadAll(){
  try{
    const r = await fetch('/api/all');
    const j = await r.json();
    MODS.forEach(m=>{
      const d = j.modules[m.id];
      if(d && d.items && d.items.length){ applyData(m.id, d); }
      else if(m.id==='x'){ renderX(); }
      else { cards[m.id].bodyEl.innerHTML=''; cards[m.id].bodyEl.append(el('div','empty','点击 ⟳ 获取最新内容')); }
    });
    document.getElementById('gstatus').textContent = '缓存加载于 ' + new Date().toLocaleTimeString('zh-CN');
  }catch(e){
    document.getElementById('gstatus').textContent = '⚠ 本地服务未响应';
  }
}

document.getElementById('refresh-all').addEventListener('click', async function(){
  this.disabled = true;
  for(const m of MODS){ await refreshOne(m.id); await new Promise(r=>setTimeout(r,400)); }
  this.disabled = false;
});

let autoTimer = null;
document.getElementById('auto').addEventListener('change', function(){
  if(autoTimer){ clearInterval(autoTimer); autoTimer=null; }
  const sec = parseInt(this.value);
  if(sec > 0){
    autoTimer = setInterval(()=>{ document.getElementById('refresh-all').click(); }, sec*1000);
  }
});

window.twttr = (function(d,s,id){
  var js, fjs = d.getElementsByTagName(s)[0], t = window.twttr || {};
  if(d.getElementById(id)) return t;
  js = d.createElement(s); js.id = id; js.async = true;
  js.src = 'https://platform.twitter.com/widgets.js';
  js.onload = function(){ if(cards['x']) renderX(); };
  fjs.parentNode.insertBefore(js, fjs);
  t._e = []; t.ready = function(f){ t._e.push(f); };
  return t;
}(document,'script','twitter-wjs'));

loadAll();
</script>
</body>
</html>
"""


def main():
    threading.Thread(target=nf.warm, daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Dodgers news aggregator -> http://localhost:{PORT}  (Ctrl+C stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()
