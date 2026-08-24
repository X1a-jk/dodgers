#!/usr/bin/env python3
"""
带 no-cache 头的静态文件服务器，用于道奇数据门户。
避免浏览器缓存 index.html 和 dashboard-data.json。
"""
import http.server
import socketserver
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        # 简化日志输出
        print(f"[{self.address_string()}] {format % args}")


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), NoCacheHandler) as httpd:
        print(f"Serving at http://localhost:{PORT} (no-cache enabled)")
        httpd.serve_forever()
