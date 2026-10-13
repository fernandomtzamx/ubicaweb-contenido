#!/usr/bin/env python3
"""Exporta las entradas del blog (sin diccionario ni demo) a docs/originales/<slug>.md
como referencia para reescribirlas: título, categorías, extracto, SEO y texto plano.
Solo lee WordPress.
"""
import html
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "originales"
spec = importlib.util.spec_from_file_location("publish", ROOT / "scripts" / "publish.py")
pub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)


def texto(h):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h or "", flags=re.S | re.I)
    h = re.sub(r"<h([1-6])[^>]*>", lambda m: "\n\n" + "#" * int(m.group(1)) + " ", h)
    h = re.sub(r"</h[1-6]>", "\n\n", h)
    h = re.sub(r"<li[^>]*>", "\n- ", h)
    h = re.sub(r"</p>|<br\s*/?>", "\n\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = html.unescape(h)
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+", " ", h)).strip()


def main():
    wp = pub.WP(pub.env("WP_URL"), pub.env("WP_USER"), pub.env("WP_APP_PASSWORD"))
    wp.whoami()
    cats = {c["id"]: c["slug"] for c in wp.req("GET", "categories", params={"per_page": 100})}
    OUT.mkdir(parents=True, exist_ok=True)
    page, n = 1, 0
    while True:
        r = wp.s.get(f"{wp.api}/posts", timeout=60, params={"per_page": 100, "page": page, "status": "publish",
                                                            "context": "edit", "_embed": "wp:featuredmedia"})
        if r.status_code >= 400:
            break
        for p in r.json():
            slugs = [cats.get(c, str(c)) for c in p["categories"]]
            if "diccionario-seo-local" in slugs or "uncategorized" in slugs:
                continue
            seo = p.get("aioseo_head_json") or {}
            img = ""
            try:
                img = p["_embedded"]["wp:featuredmedia"][0]["source_url"]
            except (KeyError, IndexError, TypeError):
                pass
            meta = {"id": p["id"], "slug": p["slug"], "fecha": p["date"], "categorias": slugs,
                    "tags": p.get("tags", []), "featured_media": p.get("featured_media"), "imagen": img,
                    "titulo": p["title"]["raw"], "extracto": p["excerpt"]["raw"],
                    "seo_title": seo.get("title"), "seo_description": seo.get("description")}
            cuerpo = texto(p["content"]["raw"] or p["content"]["rendered"])
            (OUT / f"{p['slug']}.md").write_text(
                "```json\n" + json.dumps(meta, ensure_ascii=False, indent=1) + "\n```\n\n" + cuerpo + "\n",
                encoding="utf-8")
            n += 1
        if page >= int(r.headers.get("X-WP-TotalPages", 1)):
            break
        page += 1
    print(f"Exportadas: {n}")


if __name__ == "__main__":
    sys.exit(main())
