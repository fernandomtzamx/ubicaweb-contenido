#!/usr/bin/env python3
"""Arma las páginas de listado desde lo publicado en WordPress:

    /diccionario-seo-local/   índice A a Z de los términos

Los términos y sus nombres visibles salen de docs/diccionario.yml.
Se corre en la Action después de publicar, así los listados siempre están al día.
"""
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

def plano(t):
    return unicodedata.normalize("NFD", t).encode("ascii", "ignore").decode().upper()


def corto(texto, n):
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", texto or ""))).strip()
    t = re.sub(r"\s*(\[…\]|\[\.\.\.\]|…)$", "", t)
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


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
    posts = todas(wp)
    print(f"Entradas publicadas: {len(posts)}")
    nombres = yaml.safe_load((ROOT / "docs" / "diccionario.yml").read_text(encoding="utf-8")) or {}
    # /blog/ usa la plantilla de listado del tema (página de entradas); aquí solo el diccionario.
    publicar(wp, "diccionario-seo-local", "Diccionario de SEO local",
             "Los términos de SEO local explicados en corto: Google Maps, reseñas, NAP, Local Pack y más.",
             pagina_diccionario(posts, nombres))


if __name__ == "__main__":
    sys.exit(main())
