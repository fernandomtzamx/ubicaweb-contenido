#!/usr/bin/env python3
"""Aplica docs/sitio.yml: perfil del autor y nombres/descripciones de categorías."""
import importlib.util
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("publish", ROOT / "scripts" / "publish.py")
pub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)


def main():
    cfg = yaml.safe_load((ROOT / "docs" / "sitio.yml").read_text(encoding="utf-8"))
    wp = pub.WP(pub.env("WP_URL"), pub.env("WP_USER"), pub.env("WP_APP_PASSWORD"))
    wp.whoami()
    errors = 0

    autor = cfg.get("autor") or {}
    if autor:
        try:
            me = wp.req("POST", "users/me", json=autor)
            print(f"Autor actualizado: {me.get('name')}")
        except Exception as e:  # noqa: BLE001
            errors += 1
            print(f"ERROR autor: {e}")

    # Portada: página estática por slug (requiere rol administrador).
    if cfg.get("portada"):
        try:
            page = wp.find_by_slug("pages", cfg["portada"])
            if not page:
                raise RuntimeError(f"no existe la página '{cfg['portada']}'")
            wp.req("POST", "settings", json={"show_on_front": "page", "page_on_front": page["id"]})
            print(f"Portada: {cfg['portada']} (id {page['id']})")
        except Exception as e:  # noqa: BLE001
            errors += 1
            print(f"ERROR portada: {e}")

    # Página de entradas: 0 = ninguna (el listado del blog es una página propia).
    if "pagina_entradas" in cfg:
        try:
            wp.req("POST", "settings", json={"page_for_posts": int(cfg["pagina_entradas"])})
            print(f"Página de entradas: {cfg['pagina_entradas']}")
        except Exception as e:  # noqa: BLE001
            errors += 1
            print(f"ERROR página de entradas: {e}")

    # Menú: reemplaza los elementos del menú indicado y lo asigna a su ubicación.
    menu = cfg.get("menu")
    if menu:
        try:
            mid = int(menu["id"])
            if menu.get("ubicacion"):
                wp.req("POST", f"menus/{mid}", json={"locations": [menu["ubicacion"]]})
            viejos = wp.req("GET", "menu-items", params={"menus": mid, "per_page": 100, "context": "edit"})
            for it in viejos:
                wp.req("DELETE", f"menu-items/{it['id']}", params={"force": "true"})
            for i, it in enumerate(menu.get("items") or [], start=1):
                wp.req("POST", "menu-items", json={"title": it["titulo"], "url": it["url"], "menus": mid,
                                                   "menu_order": i, "status": "publish", "type": "custom"})
            print(f"Menú {mid}: {len(menu.get('items') or [])} elementos, ubicación {menu.get('ubicacion')}")
        except Exception as e:  # noqa: BLE001
            errors += 1
            print(f"ERROR menú: {e}")

    for c in cfg.get("categorias") or []:
        try:
            found = wp.req("GET", "categories", params={"slug": c["slug"]})
            payload = {"name": c["name"], "description": c.get("description", "")}
            if found:
                wp.req("POST", f"categories/{found[0]['id']}", json=payload)
                print(f"Categoría actualizada: {c['slug']} -> {c['name']}")
            else:
                wp.req("POST", "categories", json={**payload, "slug": c["slug"]})
                print(f"Categoría creada: {c['slug']} -> {c['name']}")
        except Exception as e:  # noqa: BLE001
            errors += 1
            print(f"ERROR categoría {c.get('slug')}: {e}")

    # Borrado a la papelera (recuperable desde wp-admin). Se confirma el slug antes de borrar.
    for b in cfg.get("borrar") or []:
        tipo = b.get("tipo", "pages")
        try:
            cur = wp.req("GET", f"{tipo}/{b['id']}", params={"context": "edit"})
        except Exception as e:  # noqa: BLE001
            print(f"Ya no existe {tipo}/{b['id']} ({b['slug']}): {str(e)[:80]}")
            continue
        if cur.get("status") == "trash":
            print(f"Ya en papelera: {tipo}/{b['id']} ({b['slug']})")
            continue
        slug = cur.get("slug") or cur.get("generated_slug", "")
        if not slug.startswith(b["slug"]):
            errors += 1
            print(f"ERROR {tipo}/{b['id']}: el slug es '{slug}', no '{b['slug']}'. No se borra.")
            continue
        try:
            # Los medios no tienen papelera en la API: requieren force y se borran definitivamente.
            wp.req("DELETE", f"{tipo}/{b['id']}", params={"force": "true"} if tipo == "media" else None)
            print(f"A la papelera: {tipo}/{b['id']} ({slug})")
        except Exception as e:  # noqa: BLE001
            errors += 1
            print(f"ERROR al borrar {tipo}/{b['id']} ({slug}): {e}")

    if errors:
        sys.exit(f"{errors} error(es)")


if __name__ == "__main__":
    main()
