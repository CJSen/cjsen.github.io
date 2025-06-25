import os
from datetime import datetime

SITE_URL = "https://chjs.dpdns.org"  # 修改为你的站点地址
docs_dir = os.path.join(os.path.dirname(__file__), "../docs")
post_dir = os.path.join(docs_dir, "post")
sitemap_path = os.path.join(docs_dir, "sitemap.xml")


def get_lastmod(filepath):
    t = os.path.getmtime(filepath)
    return datetime.utcfromtimestamp(t).strftime("%Y-%m-%dT%H:%M:%SZ")


def url_entry(loc, lastmod=None):
    entry = f"  <url>\n    <loc>{loc}</loc>"
    if lastmod:
        entry += f"\n    <lastmod>{lastmod}</lastmod>"
    entry += "\n  </url>"
    return entry


def main():
    urls = []
    # 主页
    urls.append(
        url_entry(f"{SITE_URL}/", get_lastmod(os.path.join(docs_dir, "index.html")))
    )
    # 其他页面
    for page in ["about.html", "link.html", "tag.html"]:
        page_path = os.path.join(docs_dir, page)
        if os.path.exists(page_path):
            urls.append(url_entry(f"{SITE_URL}/{page}", get_lastmod(page_path)))
    # 博客文章
    if os.path.exists(post_dir):
        for fname in os.listdir(post_dir):
            if fname.endswith(".html"):
                fpath = os.path.join(post_dir, fname)
                urls.append(url_entry(f"{SITE_URL}/post/{fname}", get_lastmod(fpath)))
    # 生成 sitemap.xml
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(u + "\n")
        f.write("</urlset>\n")
    print(f"sitemap.xml generated at {sitemap_path}")


if __name__ == "__main__":
    main()
