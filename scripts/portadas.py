#!/usr/bin/env python3
"""Genera la portada de cada entrada de content/blog que no la tenga todavía.

Usa scripts/cover.py con la categoría como antetítulo. Campos opcionales del frontmatter:
    portada_titulo: texto corto para la portada (si no, el título)
    portada_chips:  "A,B,C" para el panel derecho
    portada_dato / portada_dato_texto: cifra grande y su explicación
Uso: python scripts/portadas.py [--todas]
"""
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
KICKER = {
    "sitios-web-para-franquicias": "SITIOS WEB",
    "seo-local-para-franquicias": "SEO LOCAL",
    "publicidad-digital-para-franquicias": "PUBLICIDAD DIGITAL",
    "marketing-digital-para-franquicias": "MARKETING PARA FRANQUICIAS",
    "operacion-de-franquicias": "OPERACIÓN Y TECNOLOGÍA",
    "franquicias-exitosas": "ABRIR UNA FRANQUICIA",
}


def main():
    todas = "--todas" in sys.argv
    for md in sorted((ROOT / "content" / "blog").rglob("*.md")):
        fm = yaml.safe_load(md.read_text(encoding="utf-8").split("---", 2)[1]) or {}
        img = fm.get("featured_image")
        if not img or ((ROOT / img).exists() and not todas):
            continue
        (ROOT / img).parent.mkdir(parents=True, exist_ok=True)
        cmd = [sys.executable, str(ROOT / "scripts" / "cover.py"), "--out", str(ROOT / img),
               "--kicker", KICKER.get((fm.get("categories") or [""])[0], "BLOG"),
               "--title", str(fm.get("portada_titulo") or fm["title"])]
        if fm.get("portada_dato"):
            cmd += ["--stat", str(fm["portada_dato"]), "--stat-label", str(fm.get("portada_dato_texto", ""))]
        elif fm.get("portada_chips"):
            cmd += ["--chips", str(fm["portada_chips"])]
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
