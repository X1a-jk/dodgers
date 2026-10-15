#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
带 no-cache 头的静态文件服务器，用于道奇数据门户。
避免浏览器缓存 index.html 和 dashboard-data.json。

扩展：新闻中心实时刷新 API
- POST /api/news/refresh?id=mlb|dn|athletic|x  重新抓取对应新闻源
- GET  /api/news/status                        各源缓存状态
"""
import http.server
import json
import os
import socketserver
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

# 让 portal/ 里的 server.py 能找到 D:\baseball\news\news_fetch.py
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)
import news.news_fetch as nf  # noqa: E402


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        from urllib.parse import urlparse, parse_qs
        p = urlparse(self.path)
        if p.path == "/api/news/refresh":
            mid = parse_qs(p.query).get("id", [""])[0]
            if mid not in nf.MODULES:
                self._send_json({"ok": False, "error": "未知模块"}, 400)
                return
            ok, data, err = nf.refresh(mid)
            if ok:
                self._send_json({"ok": True, "module": data})
            else:
                self._send_json({"ok": False, "error": err,
                                 "module": data or {"module": mid, "items": []}})
        else:
            self._send_json({"error": "not found"}, 404)

    def do_GET(self):
        from urllib.parse import urlparse
        p = urlparse(self.path)
        if p.path == "/api/news/status":
            mods = {}
            for mid in nf.MODULES:
                c = nf.read_cache(mid)
                mods[mid] = {"updated": (c or {}).get("updated"),
                             "count": len((c or {}).get("items") or [])}
            self._send_json({"modules": mods})
            return
        super().do_GET()


class ThreadingServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    with ThreadingServer(("", PORT), NoCacheHandler) as httpd:
        print(f"Serving at http://localhost:{PORT} (no-cache + news API enabled)")
        httpd.serve_forever()
