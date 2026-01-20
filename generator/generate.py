import json
import os
import re


BASE_DIR = os.path.dirname(__file__)
TEMPLATE_PATH = os.path.join(BASE_DIR, "template.html")
HOME_TEMPLATE_PATH = os.path.join(BASE_DIR, "template_home.html")
PRODUCTS_PATH = os.path.join(BASE_DIR, "products.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "docs", "p")
OUTPUT_DIR_HOME = os.path.join(BASE_DIR, "..", "docs")
PRODUCTS_EXPORT_PATH = os.path.join(OUTPUT_DIR_HOME, "products.json")


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_text(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def render_template(template, data):
    html = template
    for key, value in data.items():
        html = html.replace(f"{{{{{key}}}}}", value)
    return html


def build_slug(title):
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s]", "", slug)
    slug = re.sub(r"\s+", "-", slug).strip("-")
    return slug


def build_description(product):
    parts = []
    if product.get("status1"):
        parts.append(f"*{product['status1']}*<br>")
    if product.get("status2"):
        parts.append(f"*{product['status2']}*<br>")
    if product.get("review"):
        parts.append(f"*Review : {product['review']}*<br>")
    parts.append(f" <p>{product['description']}</p>")
    return "".join(parts)


def render_product_page(template, product):
    title = product["title"].title()
    html = render_template(
        template,
        {
            "TITLE": title,
            "DESCRIPTION": product["description"],
            "IMAGE": product["image"],
            "AFFILIATE_URL": product["affiliate_url"],
        },
    )
    slug = build_slug(title)
    return slug, html


def build_home_links(products, slugs):
    items = []
    for product, slug in zip(products, slugs):
        description = build_description(product)
        items.append(
            f" <li>{description}<a href='/produk-pilihan/p/{slug}.html'>"
            f"https://bagusprasojo.github.io/produk-pilihan/p/{slug}.html"
            f"</a><hr></li>"
        )
    return f"<ul>{''.join(items)} </ul>"


def generate():
    template = read_text(TEMPLATE_PATH)
    products = read_json(PRODUCTS_PATH)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    slugs = []
    for product in products:
        slug, html = render_product_page(template, product)
        slugs.append(slug)
        output_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
        write_text(output_path, html)
        print(f"Generated: {slug}.html")

    link_list = build_home_links(products, slugs)
    template_home = read_text(HOME_TEMPLATE_PATH)
    html = template_home.replace("{{DAFTAR_LINK}}", link_list)
    output_path = os.path.join(OUTPUT_DIR_HOME, "link.html")
    write_text(output_path, html)
    write_json(PRODUCTS_EXPORT_PATH, products)


if __name__ == "__main__":
    generate()
