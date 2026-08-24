import unicodedata, re

def slugify(name):
    normalized = unicodedata.normalize('NFKD', name)
    ascii_name = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return re.sub(r"[^a-z0-9-]", "", ascii_name.lower().replace(" ", "-").replace("'", "").replace(".", ""))

for name in ["Edwin Díaz", "Enrique Hernández", "Jonathan Hernández", "Teoscar Hernández", "Seth Halvorsen"]:
    print(name, '->', slugify(name))
