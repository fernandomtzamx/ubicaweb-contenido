---
title: "Páginas por sucursal: estructura, URL y contenido"
slug: paginas-por-sucursal-estructura-url-y-contenido-que-google-entiende
type: post
status: publish
date: 2026-11-10 08:00
excerpt: "Cómo armar una página por sucursal que Google entienda y no confunda con spam: la URL, el árbol del sitio, los datos obligatorios y el contenido que sí cambia."
categories: [seo-local-para-franquicias]
tags: [SEO local, páginas de sucursal, arquitectura web, URL, datos estructurados, franquicias]
portada_titulo: "Una página por sucursal que Google entienda"
portada_chips: "URL,H1,NAP,Schema"
featured_image: images/blog/paginas-por-sucursal-estructura-url-y-contenido-que-google-entiende.png
featured_alt: "Portada de UbicaWeb: páginas por sucursal, estructura, URL y contenido que Google entiende"
---

Abre el sitio de casi cualquier marca con 30 sucursales y busca la página de una en particular. Vas a encontrar una página "Sucursales" con 30 direcciones apiladas, un buscador de tiendas que carga un mapa y nada más, o 30 páginas idénticas donde solo cambia el nombre de la colonia. Ninguna le sirve a Google y la tercera se parece a lo que Google llama spam.

La página por sucursal es la pieza del sitio que más mueve el SEO local y la que menos atención recibe. Esto es lo que necesita para que Google la entienda y la ponga en el mapa.

<div class="pm-tldr" markdown="1">
**En 30 segundos:**

- Cada sucursal necesita **su propia URL indexable** dentro del sitio de la marca, no una pestaña ni un pin en un mapa.
- La estructura es un árbol: `/sucursales/ciudad/colonia/`, con enlaces de ida y de regreso.
- La página lleva nombre, dirección, teléfono y horario **idénticos a la ficha de Google**, más datos estructurados LocalBusiness.
- Lo que cambia entre sucursales tiene que ser real: servicios, fotos, reseñas, cómo llegar. Si solo cambia la ciudad, Google lo trata como página puerta.
</div>

[TOC]

## Por qué Google necesita una página por sucursal

La ficha de Google de cada sucursal tiene un campo "Sitio web" y los [lineamientos de Google](https://support.google.com/business/answer/3038177?hl=es-419) piden que esa URL presente la ubicación específica de la empresa, no una página genérica que redirija a otro lado. Si las 30 fichas apuntan a la home, Google recibe la misma señal 30 veces.

Esa página también pesa en el ranking. En la encuesta [Local Search Ranking Factors 2026](https://whitespark.ca/local-search-ranking-factors/) de Whitespark, donde 47 especialistas calificaron 187 factores, el NAP del sitio idéntico al de la ficha es el factor 15 del local pack, las palabras clave en el título de la página de destino el 17 y la relevancia geográfica del contenido el 18 (y el segundo en resultados orgánicos locales). Ninguno existe si la sucursal no tiene página.

Si todavía no sabes a dónde apunta cada ficha de tu red, empieza por la [auditoría de fichas por sucursal](/como-auditar-las-fichas-de-google-de-todas-tus-sucursales-en-una-tarde/).

## La estructura: un árbol, no una lista

Google describe las páginas puerta como "pages targeted at specific regions or cities that funnel users to one page" y también castiga las páginas sustancialmente similares que se parecen más a resultados de búsqueda que a una [jerarquía navegable](https://developers.google.com/search/docs/essentials/spam-policies). La defensa es justamente la jerarquía: que las páginas de sucursal vivan dentro de un árbol con sentido.

El árbol que funciona para una red mexicana tiene tres niveles:

1. **Índice de sucursales** (`/sucursales/`): lista todas las ciudades con enlace a cada una. Recibe el enlace del menú principal.
2. **Página por ciudad** (`/sucursales/monterrey/`): lista las sucursales de esa ciudad con dirección corta y enlace. Si solo hay una sucursal por ciudad, este nivel se omite.
3. **Página por sucursal** (`/sucursales/monterrey/san-pedro/`): la que va en la ficha de Google y en la campaña de Google Ads.

Cada nivel enlaza hacia abajo y hacia arriba, y las sucursales de una misma ciudad se enlazan entre sí. Whitespark pone el enlazado interno del sitio en el sexto lugar de los factores orgánicos locales; un árbol bien enlazado lo resuelve solo.

Lo que no funciona: el buscador de tiendas sin URL propia, los subdominios por sucursal y el dominio aparte de cada franquiciatario. Google, en voz de John Mueller, ya dijo que [un puñado de páginas por región está bien](https://www.searchenginejournal.com/googles-advice-for-targeting-multiple-locations-with-one-website/433846/), pero redirigir al visitante según su IP a páginas no indexables puede sacar la home de los resultados. Todo en un dominio, en un árbol, indexable, como explicamos en [gestión centralizada de sitios para franquicias](/beneficios-de-una-gestion-centralizada-de-sitios-web-para-franquicias/).

## La URL: corta, legible y estable

Google recomienda [palabras legibles en vez de identificadores largos](https://developers.google.com/search/docs/crawling-indexing/url-structure), guiones en vez de guiones bajos y el idioma de tu audiencia. Para una sucursal eso se traduce en una regla: ciudad y colonia o referencia local, en minúsculas, sin acentos, sin número de tienda.

| Sí | No |
| --- | --- |
| `/sucursales/guadalajara/providencia/` | `/sucursales/?id=0417` |
| `/sucursales/cdmx/polanco/` | `/sucursal_polanco_cdmx_tienda_12/` |
| `/sucursales/queretaro/juriquilla/` | `/ubicaciones/Querétaro/Juriquilla/` |

Dos decisiones se toman una sola vez desde la marca: dos sucursales en la misma colonia se distinguen por calle o plaza (`/polanco-masaryk/`), y la URL de una sucursal que cierra se redirige con 301 a la más cercana, nunca se deja en 404. Si cada franquiciatario decide su URL, en dos años tienes tres formatos y nadie sabe cuál es el oficial.

## El contenido: lo fijo y lo que cambia de verdad

Una página de sucursal tiene dos capas. La primera es la ficha técnica, igual en formato para toda la red y distinta en datos para cada local:

- **Nombre con la ciudad o colonia** en el H1 y en la etiqueta de título: "Marca Providencia, Guadalajara". No "Bienvenidos".
- **Dirección, teléfono y horario** escritos en el HTML, no solo en el mapa, y copiados letra por letra de la ficha de Google: ese es el [NAP](/nap/).
- **Botones de llamar, cómo llegar y WhatsApp**, mapa con el pin correcto y enlace a la ficha de Google de esa sucursal.

La segunda capa separa una página útil de una página puerta, y casi nadie la hace: contenido que solo es cierto para esa sucursal. Fotos reales de la fachada y el interior, los servicios que sí ofrece y los que no, referencias para llegar ("frente a la plaza, entrada por la calle lateral") y las reseñas de Google de esa unidad. Google llama abuso de contenido escalado a generar muchas páginas para manipular rankings y no para ayudar al usuario; 30 páginas con el mismo texto y la ciudad cambiada son eso.

La prueba práctica: si tapas el nombre de la ciudad, ¿alguien distinguiría la página de Providencia de la de Juriquilla? Si no, falta la segunda capa. Esta página es la misma "página de ubicación" de [las cinco páginas de un sitio de negocio local](/sitio-web-para-negocio-local-las-5-paginas-que-necesitas-y-nada-mas/) y la página de destino que piden las [campañas de Google Ads por sucursal](/google-ads-para-negocios-locales-campanas-por-sucursal/). Un trabajo, tres usos.

## Los datos estructurados: dile a Google qué es cada cosa

Google pide marcar cada ubicación como un [LocalBusiness](https://developers.google.com/webmasters/business-location-pages/schema.org-examples) con el subtipo más específico que exista (Restaurant, Dentist, AutoRepair), con nombre y dirección como obligatorios y, como recomendados, coordenadas con al menos cinco decimales, horario, teléfono con código de país y la URL de esa misma página. Es JSON-LD: una plantilla para toda la red que se llena con los datos de cada sucursal.

No es el factor que más pesa (Whitespark lo pone fuera de los primeros 100), pero convierte una página que Google lee en una que Google entiende: ese teléfono es de esa dirección y ese horario de ese local. Se valida con la prueba de resultados enriquecidos y cada URL de sucursal va en el sitemap.

## Qué controla la marca y qué llena la sucursal

En una red el problema no es diseñar una buena página de sucursal: es que las 30 queden igual de buenas y sigan así en dos años. Se resuelve repartiendo el trabajo:

- **La marca define** plantilla, formato de URL, campos obligatorios, datos estructurados y la regla de redirección cuando una sucursal cierra.
- **La sucursal entrega** fotos, horario real, servicios, referencias para llegar y nombre del responsable. Con un formulario, no con acceso al sitio.
- **Alguien revisa cada mes** que el NAP de la página siga igual al de la ficha, que los horarios especiales estén en las dos y que las fotos tengan menos de un año.

Es el mismo criterio de los [12 campos de la ficha de Google](/ficha-de-google-los-12-campos-que-mueven-el-ranking-local/): el estándar se escribe una vez desde la marca, y lo que se deja al criterio de cada local termina distinto en cada local. El resto del sistema está en la [guía de SEO local para franquicias](/la-guia-definitiva-del-seo-local-para-franquicias/).

<div class="pm-cta" markdown="1">
**Construimos la página de cada una de tus sucursales dentro del sitio de la marca: URL, plantilla, NAP alineado con la ficha, datos estructurados y revisión mensual.** Paquete Sitios, desde $499 MXN por sucursal al mes.

[Cotizar páginas por sucursal para mi red](/contacto/)
</div>
