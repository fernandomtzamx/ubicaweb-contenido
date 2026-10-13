#!/usr/bin/env python3
"""Arma las páginas de listado desde lo publicado en WordPress:

    /blog/                    entradas agrupadas por tema, con portada
    /diccionario-seo-local/   índice A a Z de los términos

Solo muestra lo que se conserva según docs/mapa-del-sitio.csv (lo que se fusiona o se borra no aparece).
Se corre en la Action después de publicar, así los listados siempre están al día.
"""
import csv
import html
import importlib.util
import pathlib
import re
import sys
import unicodedata

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("publish", ROOT / "scripts" / "publish.py")
pub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)

# Temas del blog en orden de aparición: (ancla, título, descripción, slugs de categoría actuales)
GRUPOS = [
    ("sitios-web", "Sitios web", "Cómo debe verse y funcionar el sitio de una marca con muchas sucursales.",
     ["sitios-web-para-franquicias"]),
    ("seo-local", "SEO local y reseñas", "Aparecer en Google Maps cuando alguien busca cerca de tu sucursal.",
     ["seo-local-para-franquicias"]),
    ("publicidad", "Publicidad digital", "Anuncios en Google y Meta que llevan gente a cada ubicación.",
     ["publicidad-digital-para-franquicias"]),
    ("marketing", "Marketing para franquicias", "Planes, estrategia y presupuesto de marketing para la red.",
     ["marketing-digital-para-franquicias"]),
    ("operacion", "Operación y tecnología", "Herramientas y procesos para administrar la red sin perder el control.",
     ["herramienas-digitales-para-franquicias", "transformacion-digital-para-franquicias"]),
    ("franquicias", "Abrir y hacer crecer una franquicia", "Regalías, registro, inversión y lo básico del modelo.",
     ["franquicias-exitosas"]),
]


def plano(t):
    return unicodedata.normalize("NFD", t).encode("ascii", "ignore").decode().upper()


def corto(texto, n):
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", texto or ""))).strip()
    t = re.sub(r"\s*(\[…\]|\[\.\.\.\]|…)$", "", t)
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


def conservadas():
    fuera = set()
    for r in csv.DictReader(open(ROOT / "docs" / "mapa-del-sitio.csv", encoding="utf-8")):
        if r["accion"].startswith(("Fusionar", "Borrar")) and r["url_actual"].startswith("/"):
            fuera.add(r["url_actual"].strip("/"))
    return fuera


def todas(wp):
    posts, page = [], 1
    while True:
        r = wp.s.get(f"{wp.api}/posts", timeout=60, params={
            "per_page": 100, "page": page, "status": "publish", "_embed": "wp:featuredmedia",
            "_fields": "id,slug,link,title,excerpt,categories,_links,_embedded"})
        if r.status_code >= 400:
            break
        posts += r.json()
        if page >= int(r.headers.get("X-WP-TotalPages", 1)):
            break
        page += 1
    return posts


def imagen(p):
    try:
        m = p["_embedded"]["wp:featuredmedia"][0]
        tam = m.get("media_details", {}).get("sizes", {})
        for k in ("medium_large", "large", "medium"):
            if k in tam:
                return tam[k]["source_url"]
        return m.get("source_url", "")
    except (KeyError, IndexError, TypeError):
        return ""


def pagina_blog(posts, cats, fuera):
    grupos = {g[0]: [] for g in GRUPOS}
    for p in posts:
        if p["slug"] in fuera:
            continue
        slugs = {cats.get(c, "") for c in p["categories"]}
        for ancla, _, _, cs in GRUPOS:
            if slugs & set(cs):
                grupos[ancla].append(p)
                break
    total = sum(len(v) for v in grupos.values())
    nav = "".join(f'<a href="#{a}">{t}</a>' for a, t, _, _ in GRUPOS if grupos[a])
    bloques = []
    for ancla, titulo, desc, _ in GRUPOS:
        if not grupos[ancla]:
            continue
        cards = []
        for p in sorted(grupos[ancla], key=lambda p: p["title"]["rendered"].lower()):
            t = html.unescape(p["title"]["rendered"]).rstrip(".")
            img = imagen(p)
            img_tag = f'<img src="{img}" alt="" loading="lazy">' if img else ""
            cards.append(f'<a class="uw-post" href="{p["link"]}">{img_tag}<div><b>{html.escape(t)}</b></div></a>')
        bloques.append(f'<div class="uw-grupo" id="{ancla}"><h2>{titulo}</h2><p class="uw-grupo-desc">{desc}</p>'
                       f'<div class="uw-posts">{"".join(cards)}</div></div>')
    return f"""<div class="uw">
<section class="uw-sec"><span class="uw-kicker">Blog</span>
<h1 class="uw-titulo-listado">Marketing para franquicias, sin relleno.</h1>
<p class="uw-sub">{total} guías sobre cómo hacer que cada sucursal aparezca, se vea bien y reciba clientes. Elige un tema.</p>
<nav class="uw-nav">{nav}</nav></section>
<section class="uw-sec uw-sec--blanco">{"".join(bloques)}</section>
{CTA}
</div>"""


def pagina_diccionario(posts, nombres):
    por_slug = {p["slug"]: p for p in posts}
    terminos = []
    for slug, nombre in nombres.items():
        p = por_slug.get(slug)
        if p:
            terminos.append((nombre, p))
        else:
            print(f"Aviso: término sin entrada publicada: {slug}")
    terminos.sort(key=lambda x: plano(x[0]))
    letras = {}
    for nombre, p in terminos:
        letras.setdefault(plano(nombre)[0], []).append((nombre, p))
    nav = "".join(f'<a href="#letra-{l.lower()}">{l}</a>' for l in letras)
    bloques = []
    for l, items in letras.items():
        links = "".join(f'<a href="{p["link"]}"><b>{html.escape(n)}</b></a>' for n, p in items)
        bloques.append(f'<div class="uw-letra-bloque" id="letra-{l.lower()}"><span>{l}</span>'
                       f'<div class="uw-terminos">{links}</div></div>')
    return f"""<div class="uw">
<section class="uw-sec"><span class="uw-kicker">Diccionario de SEO local</span>
<h1 class="uw-titulo-listado">Los términos de SEO local, explicados para quien tiene que tomar decisiones.</h1>
<p class="uw-sub">{len(terminos)} conceptos que vas a escuchar cuando hablemos de Google Maps, reseñas y búsquedas cerca de mí. Sin tecnicismos de más.</p>
<nav class="uw-letras">{nav}</nav></section>
<section class="uw-sec uw-sec--blanco">{"".join(bloques)}</section>
{CTA}
</div>"""


CTA = """<section class="uw-final"><h2>¿Prefieres que lo hagamos nosotros?</h2>
<p>Sitios por sucursal, anuncios en Google y Meta, y fichas de Google bien atendidas. Desde $499 MXN al mes por ubicación.</p>
<a class="uw-btn" href="/contacto/">Cotizar mi red de sucursales</a></section>"""

EXTRA_CSS = ".uw .uw-terminos{grid-template-columns:repeat(3,1fr)}.uw .uw-terminos a b{font-weight:600}.uw .uw-titulo-listado{font-size:44px;line-height:1.1;font-weight:800;max-width:860px;margin-bottom:16px}" \
            "@media (max-width:900px){.uw .uw-titulo-listado{font-size:30px}.uw .uw-terminos{grid-template-columns:1fr}}"


def publicar(wp, slug, titulo, excerpt, cuerpo):
    css = (ROOT / "scripts" / "landing.css").read_text(encoding="utf-8") + EXTRA_CSS
    contenido = pub.render_landing(f"<style>\n{css}</style>\n{cuerpo}")
    page = wp.find_by_slug("pages", slug)
    payload = {"title": titulo, "content": contenido, "excerpt": excerpt, "status": "publish",
               "comment_status": "closed", "ping_status": "closed"}
    if page:
        res = wp.req("POST", f"pages/{page['id']}", json=payload)
    else:
        res = wp.req("POST", "pages", json={**payload, "slug": slug})
    print(f"Listado {slug}: id={res['id']} {res['link']}")


def main():
    wp = pub.WP(pub.env("WP_URL"), pub.env("WP_USER"), pub.env("WP_APP_PASSWORD"))
    wp.whoami()
    cats = {c["id"]: c["slug"] for c in wp.req("GET", "categories", params={"per_page": 100})}
    posts = todas(wp)
    print(f"Entradas publicadas: {len(posts)}")
    fuera = conservadas()
    nombres = yaml.safe_load((ROOT / "docs" / "diccionario.yml").read_text(encoding="utf-8")) or {}
    publicar(wp, "blog", "Blog de marketing para franquicias",
             "Guías sobre sitios web, SEO local y publicidad digital para franquicias y negocios con varias sucursales.",
             pagina_blog(posts, cats, fuera))
    publicar(wp, "diccionario-seo-local", "Diccionario de SEO local",
             "Los términos de SEO local explicados en corto: Google Maps, reseñas, NAP, Local Pack y más.",
             pagina_diccionario(posts, nombres))


if __name__ == "__main__":
    sys.exit(main())
