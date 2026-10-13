# UbicaWeb: contenido y pipeline de publicación

Repositorio fuente del blog de [ubicaweb.com](https://www.ubicaweb.com). Cada archivo Markdown en `content/` se publica en WordPress mediante la API REST cuando llega a `main`.

## Cómo funciona

1. Los agentes escriben o actualizan un archivo en `content/<pilar>/<slug>.md`.
2. Al hacer push a `main`, la GitHub Action `Publicar en WordPress` publica solo los archivos nuevos o modificados.
3. Si ya existe una entrada con el mismo `slug`, se actualiza; nunca se duplica.
4. Cada corrida deja su log en `registro/ultima-publicacion.log`, para revisar errores sin capturas.

## Frontmatter

```yaml
---
title: "Título de la entrada"
slug: titulo-de-la-entrada
type: post            # post | page
status: draft         # draft | publish | pending | private
date: 2026-10-20 08:00   # opcional, hora de Ciudad de México; con publish la programa
excerpt: "Descripción corta para listados y buscadores."
featured_image: images/titulo-de-la-entrada.png   # opcional
categories: [seo-local]
tags: [franquicias, google-business-profile]
---
```

## Secretos requeridos (Settings > Secrets and variables > Actions)

| Secreto | Valor |
| --- | --- |
| `WP_URL` | `https://www.ubicaweb.com` |
| `WP_USER` | `aiagent` |
| `WP_APP_PASSWORD` | contraseña de aplicación de ese usuario |

## Autenticación en el servidor

Si WordPress responde `401 rest_not_logged_in` aunque la contraseña sea correcta, el servidor está borrando el encabezado `Authorization`. Sube `wordpress/mu-plugins/agente-auth.php` a `wp-content/mu-plugins/` (se activa solo). El script manda la credencial también en `X-Agente-Auth`, que es la que lee el mu-plugin.

## Probar la conexión

Actions > Publicar en WordPress > Run workflow > `check`.

## Herramientas

* `scripts/lint.py archivo.md`: control de calidad antes de publicar (frontmatter, guiones largos, extensión, portada, enlaces internos).
* `scripts/cover.py`: portadas de 1200x630. Ajusta colores y marca a la identidad de UbicaWeb.
* `scripts/site_setup.py`: aplica `docs/sitio.yml` (categorías, autor, limpieza) con el modo `setup`.

## Uso local

```bash
pip install -r requirements.txt
export WP_URL=https://www.ubicaweb.com WP_USER=aiagent WP_APP_PASSWORD=...
python scripts/publish.py --check
python scripts/publish.py content/pruebas/prueba-conexion.md
```
