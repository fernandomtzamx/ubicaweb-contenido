#!/usr/bin/env python3
"""Genera docs/calendario-editorial.md: dos entradas por semana (martes y jueves, 08:00)
desde la semana del 19 de octubre de 2026 hasta la última de diciembre de 2027.

Los temas rotan entre tres pilares: SEO local, marketing para franquicias y
marketing para negocios locales. Cada fila trae fecha, pilar, categoría de WordPress,
título propuesto (menos de 60 caracteres cuando se publique) y slug sugerido.
Uso: python scripts/calendario.py
"""
import datetime
import pathlib
import re
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "calendario-editorial.md"

SEO = "seo-local-para-franquicias"
MKT = "marketing-digital-para-franquicias"
WEB = "sitios-web-para-franquicias"
ADS = "publicidad-digital-para-franquicias"

SEO_LOCAL = [
    "Cómo auditar las fichas de Google de todas tus sucursales en una tarde",
    "Ficha de Google: los 12 campos que mueven el ranking local",
    "Páginas por sucursal: estructura, URL y contenido que Google entiende",
    "NAP consistente en una red de 50 sucursales: proceso paso a paso",
    "Categorías de la ficha de Google: cómo elegir la principal y las secundarias",
    "Fichas duplicadas y sucursales cerradas: cómo limpiar el mapa de tu marca",
    "Cómo pedir reseñas en una sucursal sin violar las reglas de Google",
    "Responder reseñas negativas: guion para gerentes de sucursal",
    "Local pack: qué es y cómo entrar en los tres primeros resultados",
    "Fotos en la ficha de Google: qué subir, cuántas y cada cuánto",
    "Google Posts para sucursales: calendario mensual que sí se cumple",
    "Preguntas y respuestas en Google Maps: contéstalas antes que un extraño",
    "Citaciones locales en México: directorios que sí valen la pena",
    "Apple Business Connect y Bing Places: las fichas que nadie reclama",
    "Palabras clave locales: cómo investigar 'cerca de mí' por ciudad",
    "Schema LocalBusiness para franquicias: datos estructurados por sucursal",
    "Cómo medir el SEO local: llamadas, rutas y clics por sucursal",
    "Suspensión de ficha de Google: por qué pasa y cómo recuperarla",
    "Áreas de servicio o dirección física: qué ficha usar y cuándo",
    "Horarios especiales y días festivos: el error que más llamadas pierde",
    "SEO local para franquicias de comida: menú, pedidos y reservas en la ficha",
    "SEO local para clínicas y consultorios con varias sedes",
    "SEO local para gimnasios y estudios con varias sucursales",
    "SEO local para escuelas y academias con varios planteles",
    "SEO local para talleres y servicios automotrices en red",
    "Reseñas falsas: cómo detectarlas y reportarlas en tu red",
    "Search Console por sucursal: cómo leer las búsquedas locales",
    "Nueva sucursal: checklist de SEO local antes de abrir",
    "Cierre o mudanza de sucursal: cómo avisarle a Google sin perder posición",
    "Atributos de la ficha: accesibilidad, pagos y servicios que filtran clientes",
    "Nombre de la ficha de Google: qué permite y qué te suspende",
    "Mensajes y llamadas desde la ficha: quién contesta en cada sucursal",
    "Enlaces locales: prensa, cámaras y alianzas por ciudad",
    "Contenido local en el sitio: eventos, equipo y barrio de cada sucursal",
    "Cómo comparar el SEO local de tus sucursales con la competencia",
    "SEO local y búsquedas por voz: cómo responde tu ficha a '¿dónde hay...?'",
    "Reseñas fuera de Google: Facebook, TripAdvisor y apps de pedidos",
    "Qué hacer cuando un franquiciatario se niega a ceder su ficha",
    "SEO local y respuestas con IA: cómo aparecen tus sucursales",
    "Productos y servicios en la ficha de Google: cómo cargarlos en red",
    "Reporte mensual de SEO local para la dirección: qué incluir",
    "SEO local en 2028: lo que cambia y lo que sigue igual",
]

FRANQUICIAS = [
    "Fondo de marketing en franquicias: cómo se calcula y cómo se reporta",
    "Marketing cooperativo: la marca pone la mitad, la sucursal la otra",
    "Plantillas de marketing para franquiciatarios: qué entregar y qué no",
    "Lanzamiento de una sucursal nueva: plan de marketing de 90 días",
    "Manual de marketing para franquicias: qué debe incluir",
    "Cómo convencer a un franquiciatario de invertir en marketing local",
    "Métricas de marketing por sucursal: el tablero que ve el director",
    "Marketing de temporada en franquicias: Buen Fin, Navidad y regreso a clases",
    "Promociones nacionales y locales: cómo convivir sin pelear",
    "Cómo captar franquiciatarios con marketing digital",
    "Página de 'abre tu franquicia': qué pide un candidato antes de llamar",
    "WhatsApp Business en franquicias: una cuenta por sucursal, un tono de marca",
    "Redes sociales en franquicias: cuenta central o cuentas locales",
    "Programa de lealtad en franquicias: cómo funciona en varias sucursales",
    "Email marketing por sucursal: segmentar sin romper la marca",
    "Contenido para franquicias: temas que atraen clientes y candidatos",
    "Cómo medir el ROI del marketing en una franquicia",
    "Agencia central o agencias locales: qué conviene a la red",
    "Marca consistente en 100 sucursales: control sin burocracia",
    "Qué hacer cuando una sucursal vende menos que las demás",
    "Encuestas de satisfacción por sucursal: preguntas que sí sirven",
    "Marketing para franquicias de servicios a domicilio",
    "Marketing para franquicias de salud y belleza",
    "Marketing para franquicias de educación",
    "Marketing para franquicias de comida rápida y cafeterías",
    "Branding local: cómo adaptar la marca a cada ciudad sin perderla",
    "Convención de franquiciatarios: cómo presentar el plan de marketing",
    "Presupuesto de marketing para una red de sucursales: cómo armarlo",
    "Marketing de referidos en franquicias: el cliente que trae clientes",
    "Cómo integrar a un franquiciatario nuevo al marketing de la marca",
    "Marketing para franquicias chicas: de 3 a 10 sucursales",
    "Marketing para franquicias grandes: más de 50 sucursales",
    "Influencers locales para franquicias: cómo y cuánto pagar",
    "Eventos en sucursal: cómo convertirlos en clientes recurrentes",
    "Relaciones públicas locales para franquicias",
    "Crisis en una sucursal: cómo responder sin dañar la marca",
    "Análisis de competencia local por sucursal",
    "Precios distintos por sucursal: cómo comunicarlos sin confundir",
    "Marketing automatizado para franquicias: qué automatizar primero",
    "Cómo auditar el marketing de tu franquicia en una semana",
    "Marketing para franquicias master: cuando la red es internacional",
    "Tendencias de marketing para franquicias en 2028",
]

NEGOCIOS_LOCALES = [
    (WEB, "Sitio web para negocio local: las 5 páginas que necesitas y nada más"),
    (ADS, "Google Ads para negocios locales: campañas por sucursal"),
    (MKT, "Marketing local para restaurantes con varias sucursales"),
    (WEB, "Cómo elegir dominio para una marca con varias sucursales"),
    (ADS, "Anuncios en Google Maps: cómo aparecer con el pin morado"),
    (MKT, "Cómo competir con cadenas grandes siendo un negocio local"),
    (WEB, "Página de contacto que convierte: mapa, WhatsApp y horario"),
    (ADS, "Meta Ads para negocios locales: radio, presupuesto y creativos"),
    (MKT, "Marketing para negocios locales con $5,000 al mes"),
    (WEB, "Sitio web para franquicias: WordPress o plataforma propia"),
    (ADS, "Cuánto invertir en Google Ads por sucursal: cómo calcularlo"),
    (MKT, "Marketing local para clínicas dentales"),
    (WEB, "Mantenimiento de sitio web para negocios locales: qué revisar cada mes"),
    (ADS, "Local Services Ads en México: qué son y cuándo convienen"),
    (MKT, "Google Business Profile o sitio web: necesitas los dos"),
    (WEB, "Core Web Vitals para sitios de negocios locales"),
    (ADS, "Remarketing para negocios locales: cómo hacerlo sin ser invasivo"),
    (MKT, "Marketing local para ferreterías y tiendas de materiales"),
    (WEB, "Landing pages locales para campañas de Google Ads"),
    (ADS, "Seguimiento de llamadas: saber qué anuncio trajo cada cliente"),
    (MKT, "Directorios locales de pago: cuáles valen y cuáles no"),
    (WEB, "Chat en el sitio de un negocio local: humano o bot"),
    (ADS, "Conversiones offline: medir ventas en mostrador desde anuncios"),
    (MKT, "Marketing local para lavanderías y servicios de barrio"),
    (WEB, "Páginas de ubicación con reseñas incrustadas: cómo y por qué"),
    (ADS, "Meta Ads o Google Ads para un negocio local: cuál primero"),
    (MKT, "Fotos y video para negocios locales: qué grabar con el celular"),
    (WEB, "Sitio web multilenguaje para franquicias en zonas turísticas"),
    (ADS, "Campañas de temporada para negocios locales: calendario anual"),
    (MKT, "Marketing local para escuelas de idiomas"),
    (WEB, "Accesibilidad web en sitios de negocios locales"),
    (ADS, "Anuncios en YouTube para negocios locales: cuándo tiene sentido"),
    (MKT, "Cómo leer Google Analytics si tienes varias sucursales"),
    (WEB, "Seguridad del sitio web: HTTPS, respaldos y actualizaciones"),
    (ADS, "TikTok para negocios locales: qué funciona en México"),
    (MKT, "Franquicia recién abierta: marketing local de los primeros 6 meses"),
    (WEB, "Cómo migrar el sitio de una franquicia sin perder posiciones"),
    (ADS, "Presupuesto anual de publicidad digital para un negocio local"),
    (MKT, "Página de empleo por sucursal: reclutar desde el sitio"),
    (WEB, "Qué incluir en la página de cada sucursal: ejemplos"),
    (ADS, "Tendencias en publicidad digital local para 2028"),
    (MKT, "Formularios que sí llegan: integrar el sitio con el CRM"),
]

PILAR = {SEO: "SEO local", MKT: "Marketing para franquicias", WEB: "Sitios web", ADS: "Publicidad digital"}


def slugify(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return t


def main():
    items = []
    for a, b, (cat, c) in zip(SEO_LOCAL, FRANQUICIAS, NEGOCIOS_LOCALES):
        items += [("SEO local", SEO, a), ("Marketing para franquicias", MKT, b),
                  ("Marketing para negocios locales", cat, c)]
    # Semana 1 (19 oct 2026): miércoles 21 (hoy) y viernes 23. Después: martes y jueves 08:00.
    slots = [datetime.date(2026, 10, 21), datetime.date(2026, 10, 23)]
    monday = datetime.date(2026, 10, 26)
    while monday <= datetime.date(2027, 12, 27):
        slots += [monday + datetime.timedelta(days=1), monday + datetime.timedelta(days=3)]
        monday += datetime.timedelta(days=7)
    assert len(items) >= len(slots), (len(items), len(slots))
    rows = []
    for n, (d, (pilar, cat, title)) in enumerate(zip(slots, items), 1):
        rows.append((n, d, pilar, cat, title, slugify(title)))

    lines = [
        "# Calendario editorial del blog: octubre 2026 a diciembre 2027",
        "",
        f"Generado con `scripts/calendario.py`. {len(rows)} entradas, dos por semana (martes y jueves a las 08:00, hora de Ciudad de México).",
        "",
        "## Reglas",
        "",
        "* Tres pilares que rotan: SEO local, marketing para franquicias y marketing para negocios locales (sitios web, publicidad digital, marketing).",
        "* Cada entrada va en `content/blog/<carpeta>/<slug>.md` con `date:` igual a la fecha de la tabla y `status: publish`; el workflow la programa.",
        "* Se escribe siguiendo `docs/guia-de-estilo.md`: tono business casual, español de México, nunca guion largo, sin cifras ni clientes inventados, cierre con llamado a la acción ligado a un servicio.",
        "* Mínimo 550 palabras, al menos dos fuentes enlazadas, portada con `scripts/portadas.py`, control con `scripts/lint.py`.",
        "* Los títulos son propuestas: al escribir se ajustan a menos de 60 caracteres y a lo que diga la investigación de palabras clave de ese mes.",
        "* Estado: ✅ publicada, 📝 en borrador, vacío pendiente.",
        "",
        "## Calendario",
        "",
        "| # | Fecha | Pilar | Categoría | Título propuesto | Slug | Estado |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for n, d, pilar, cat, title, slug in rows:
        estado = "✅" if n == 1 else ""
        lines.append(f"| {n} | {d.isoformat()} | {pilar} | {cat} | {title} | {slug} | {estado} |")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} entradas -> {OUT.relative_to(ROOT)}; última: {rows[-1][1]}")


if __name__ == "__main__":
    main()
