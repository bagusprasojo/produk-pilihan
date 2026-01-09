import json
import os
import re


BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "docs", "p")
OUTPUT_DIR_HOME = os.path.join(BASE_DIR, "..", "docs")

with open(os.path.join(BASE_DIR, "template.html"), encoding="utf-8") as f:
    template = f.read()

with open(os.path.join(BASE_DIR, "products.json"), encoding="utf-8") as f:
    products = json.load(f)

os.makedirs(OUTPUT_DIR, exist_ok=True)

link = "<ul>"
for p in products:
    title = p["title"]
    title = title.title()

    html = template
    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{DESCRIPTION}}", p["description"])
    html = html.replace("{{IMAGE}}", p["image"])
    html = html.replace("{{AFFILIATE_URL}}", p["affiliate_url"])

    
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug).strip('-')


    output_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
    # print(output_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✔ Generated: {slug}.html")
    description = ""
    if p.get("status1"):
        description += f"*{p['status1']}*<br>"

    if p.get("status2"):
        description += f"*{p['status2']}*<br>"

    if p.get("review"):
        description += f"*Review : {p['review']}*<br>"

    description = f"{description} <p>{p['description']}</p>"    

    # print(description)

    link = f"{link} <li>{description}<a href='/produk-pilihan/p/{slug}.html'>https://bagusprasojo.github.io/produk-pilihan/p/{slug}.html</a><hr></li>"

link = f"{link} </ul>"
with open(os.path.join(BASE_DIR, "template_home.html"), encoding="utf-8") as f:
    template_home = f.read()

html = template_home
html = html.replace("{{DAFTAR_LINK}}", link)
output_path = os.path.join(OUTPUT_DIR_HOME, "index.html")
with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    

