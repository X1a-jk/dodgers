import requests, re, io, sys, subprocess, tempfile, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

html_text = requests.get("http://localhost:8080/", timeout=10).text
for probe in ["openPalette", "palette-overlay", "PALETTE_PAGES", "Ctrl+K"]:
    print(f"contains {probe!r}:", probe in html_text)

scripts = re.findall(r"<script>(.*?)</script>", html_text, re.S)
for i, s in enumerate(scripts):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(s)
        path = f.name
    r = subprocess.run(["node", "--check", path], capture_output=True, text=True)
    print(f"script block {i}:", "OK" if r.returncode == 0 else "SYNTAX ERROR")
    if r.returncode != 0:
        print(r.stderr[:1500])
    os.unlink(path)
