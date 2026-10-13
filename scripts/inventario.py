#!/usr/bin/env python3
"""Inventario del sitio: contenido, estructura y SEO on-page de cada URL.

Solo lee; no cambia nada en WordPress. Escribe:
    docs/inventario/inventario.json   datos completos
    docs/inventario/inventario.md     resumen legible
"""
import html as htmllib
import importlib.util
import json
import pathlib
import re
import sys

import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "inventario"
spec = importlib.util.spec_from_file_location("publish", ROOT / "scripts" / "publish.py")
pub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)


def all_items(wp, endpoint, params=None):
    items, page = [], 1
    while True:
        r = wp.s.get(f"{wp.api}/{endpoint}", timeout=60,
                     params={"per_page": 100, "page": page, **(params or {})})
        if r.status_code == 400 and page > 1:
            break
        if r.status_code >= 400:
            print(f"Aviso: {endpoint} -> {r.status_code} {r.text[:150]}")
            break
        batch = r.json()
        items += batch
        if page >= int(r.headers.get("X-WP-TotalPages", 1)):
            break
        page += 1
    return items


def raw(wp, path):
    r = wp.s.get(wp.api.rsplit("/wp/v2", 1)[0] + "/" + path, timeout=60)
    if r.status_code >= 400:
        return {"error": f"{r.status_code} {r.text[:150]}"}
    return r.json()


def text_of(fragment):
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", fragment or ""))).strip()


def onpage(url):
    """Lee la URL pública como la vería Google."""
    try:
        r = requests.get(url, timeout=45, headers={"User-Agent": "Mozilla/5.0 (compatible; ubicaweb-inventario/1.0)"},
                         allow_redirects=True)
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:150]}
    h = r.text
    meta = lambda name: (re.search(rf'<meta[^>]+(?:name|property)=["\']{name}["\'][^>]*content=["\']([^"\']*)', h, re.I)
                         or re.search(rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]*(?:name|property)=["\']{name}["\']', h, re.I))
    m_desc, m_robots = meta("description"), meta("robots")
    canon = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', h, re.I)
    title = re.search(r"<title[^>]*>(.*?)</title>", h, re.I | re.S)
    body = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", h, flags=re.I | re.S)
    main = re.search(r"<main[^>]*>(.*?)</main>", body, re.I | re.S)
    words = len(text_of(main.group(1) if main else body).split())
    return {
        "http": r.status_code,
        "final_url": r.url,
        "title": text_of(title.group(1)) if title else "",
        "meta_description": htmllib.unescape(m_desc.group(1)) if m_desc else "",
        "robots": m_robots.group(1) if m_robots else "",
        "canonical": canon.group(1) if canon else "",
        "h1": [text_of(x) for x in re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.I | re.S)],
        "h2": [text_of(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", h, re.I | re.S)][:25],
        "words": words,
        "imgs_sin_alt": len(re.findall(r"<img(?![^>]*\balt=[\"'][^\"']+)[^>]*>", h, re.I)),
        "elementor": "elementor" in h,
        "forms": len(re.findall(r"<form\b", h, re.I)),
        "links_internos": sorted(set(re.findall(r'href=["\'](https?://(?:www\.)?ubicaweb\.com/[^"\'#?]*)', h, re.I)))[:120],
    }


def main():
    wp = pub.WP(pub.env("WP_URL"), pub.env("WP_USER"), pub.env("WP_APP_PASSWORD"))
    me = wp.whoami()
    print(f"Inventario como {me.get('username')} ({', '.join(me.get('roles', []))})")
    data = {"sitio": raw(wp, "")}
    data["sitio"] = {k: data["sitio"].get(k) for k in ("name", "description", "url", "home", "gmt_offset", "timezone_string")}
    data["settings"] = raw(wp, "wp/v2/settings")
    data["themes"] = [{"stylesheet": t.get("stylesheet"), "name": (t.get("name") or {}).get("raw"), "status": t.get("status"),
                       "version": t.get("version")} for t in (raw(wp, "wp/v2/themes") or []) if isinstance(t, dict)]
    pl = raw(wp, "wp/v2/plugins")
    data["plugins"] = [{"plugin": p.get("plugin"), "name": p.get("name"), "status": p.get("status"), "version": p.get("version")}
                       for p in pl] if isinstance(pl, list) else pl
    data["menus"] = []
    for m in all_items(wp, "menus", {"context": "edit"}):
        items = all_items(wp, "menu-items", {"menus": m["id"], "context": "edit"})
        data["menus"].append({"id": m["id"], "name": m.get("name"), "locations": m.get("locations"),
                              "items": [{"id": i["id"], "title": text_of((i.get("title") or {}).get("rendered")),
                                         "url": i.get("url"), "parent": i.get("parent"), "object": i.get("object"),
                                         "object_id": i.get("object_id")} for i in items]})
    data["categories"] = [{"id": c["id"], "slug": c["slug"], "name": c["name"], "count": c["count"],
                           "description": c.get("description", "")} for c in all_items(wp, "categories")]
    data["tags"] = [{"id": t["id"], "slug": t["slug"], "name": t["name"], "count": t["count"]} for t in all_items(wp, "tags")]
    cats = {c["id"]: c["slug"] for c in data["categories"]}

    data["contenido"] = []
    types = raw(wp, "wp/v2/types")
    endpoints = [(k, v.get("rest_base")) for k, v in (types or {}).items()
                 if isinstance(v, dict) and v.get("rest_base") and k not in
                 ("attachment", "nav_menu_item", "wp_block", "wp_template", "wp_template_part", "wp_navigation",
                  "wp_global_styles", "wp_font_family", "wp_font_face")]
    print("Tipos de contenido:", ", ".join(f"{k}->{b}" for k, b in endpoints))
    for kind, base in endpoints:
        for it in all_items(wp, base, {"status": "any", "context": "edit"}):
            content_raw = (it.get("content") or {}).get("raw", "") or ""
            row = {
                "tipo": kind, "id": it["id"], "slug": it.get("slug"), "status": it.get("status"),
                "titulo": text_of((it.get("title") or {}).get("raw") or (it.get("title") or {}).get("rendered")),
                "link": it.get("link"), "fecha": it.get("date"), "modificado": it.get("modified"),
                "parent": it.get("parent"), "template": it.get("template"),
                "categorias": [cats.get(c, c) for c in it.get("categories", [])],
                "tags": len(it.get("tags", [])),
                "extracto": text_of((it.get("excerpt") or {}).get("raw", ""))[:300],
                "palabras_editor": len(text_of(content_raw).split()),
                "featured_media": it.get("featured_media"),
                "elementor_meta": bool((it.get("meta") or {}).get("_elementor_edit_mode")) if isinstance(it.get("meta"), dict) else None,
                "aioseo": {k: v for k, v in (it.get("aioseo_head_json") or {}).items() if k in ("title", "description", "canonical_url", "robots")} if isinstance(it.get("aioseo_head_json"), dict) else None,
            }
            if it.get("status") == "publish" and it.get("link"):
                row["onpage"] = onpage(it["link"])
            data["contenido"].append(row)
            print(f"  {kind:12} {it['id']:>5} {it.get('status'):8} {it.get('slug')}")
    data["media_total"] = len(all_items(wp, "media", {"context": "edit", "_fields": "id"}))
    data["usuarios"] = [{"id": u["id"], "slug": u.get("slug"), "name": u.get("name"), "roles": u.get("roles")}
                        for u in all_items(wp, "users", {"context": "edit"})]

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "inventario.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = [f"# Inventario de {data['sitio'].get('name')}", "",
             f"Tema activo: {', '.join(t['name'] or t['stylesheet'] for t in data['themes'] if t['status'] == 'active') or '?'}",
             f"Medios: {data['media_total']}", "", "| tipo | id | estado | slug | título | palabras | h1 | title | meta desc |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in sorted(data["contenido"], key=lambda r: (r["tipo"], r["status"], r["slug"] or "")):
        op = r.get("onpage") or {}
        lines.append(f"| {r['tipo']} | {r['id']} | {r['status']} | {r['slug']} | {r['titulo'][:60]} | {op.get('words', r['palabras_editor'])} "
                     f"| {len(op.get('h1', []))} | {len(op.get('title', ''))} | {len(op.get('meta_description', ''))} |")
    (OUT / "inventario.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Inventario: {len(data['contenido'])} piezas, {len(data['menus'])} menús, "
          f"{len(data['plugins']) if isinstance(data['plugins'], list) else '?'} plugins")


if __name__ == "__main__":
    sys.exit(main())
