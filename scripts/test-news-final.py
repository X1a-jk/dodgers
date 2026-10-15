import requests, re, io, sys, subprocess, tempfile, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 前端 JS 语法检查
html_text = requests.get("http://localhost:8964/", timeout=10).text
scripts = re.findall(r"<script>(.*?)</script>", html_text, re.S)
print("script blocks:", len(scripts))
for i, s in enumerate(scripts):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(s)
        path = f.name
    r = subprocess.run(["node", "--check", path], capture_output=True, text=True)
    print(f"  block {i}: {'OK' if r.returncode == 0 else 'SYNTAX ERROR'}")
    if r.returncode != 0:
        print(r.stderr[:800])
    os.unlink(path)

# DN 时间修复验证
r = requests.post("http://localhost:8964/api/refresh?id=dn", timeout=40).json()
items = r["module"]["items"]
print("\nDN times:", [it["time"] for it in items[:3]])
