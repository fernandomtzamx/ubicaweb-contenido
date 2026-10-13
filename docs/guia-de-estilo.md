# Guía de estilo de UbicaWeb

## Qué vendemos y a quién

UbicaWeb vende sitios web, SEO local y publicidad digital a **franquicias y negocios con varias ubicaciones**. El lector ideal es quien decide el marketing de la red: director de marketing de la marca, dueño de la franquicia o gerente de expansión. No es el franquiciatario que busca abrir su primer local.

Cada pieza debe acercar a ese lector a una conversación comercial. Si un tema atrae tráfico pero no a ese comprador (por ejemplo, "cómo subir de nivel en Local Guides"), se reorienta al problema de negocio o se deja de priorizar.

## Voz: business casual

Referencia de tono: businesscasualcopywriting.com/blog. Se toma el espíritu, nunca su texto.

* Conversacional, con autoridad. Como un operador que ya vio demasiados sitios aburridos.
* Directo: frases cortas, verbos concretos, segunda persona con "tú".
* Ligeramente irreverente cuando aclara el punto; nunca chistes forzados.
* Nombra el statu quo: la hoja de cálculo, las 40 fichas de Google sin dueño, la agencia local de cada franquiciatario, el sitio que nadie actualiza.
* Dolor, resultado, objeción y prueba en cada página de venta.
* Nada de "soluciones integrales", "transformación digital", "innovador", "de clase mundial", "potencia", "revoluciona".
* Nunca inventar cifras, clientes, testimonios ni casos. Si falta la prueba, se marca como pendiente.

## Reglas de formato

* Nunca usar guion largo ni guion medio. Usar dos puntos, comas o punto y seguido.
* Español de México, "tú".
* Títulos de menos de 60 caracteres; meta descripción de 140 a 160.
* Un solo H1 por página.
* Todo enlace externo con `rel="nofollow"` (lo aplica `publish.py`).
* Cada entrada termina con un llamado a la acción ligado a un servicio, no con "contáctanos".

## Identidad visual

| Elemento | Valor |
| --- | --- |
| Verde de marca (logo) | `#108139` |
| Verde claro de apoyo | `#C7E0CD` |
| Fondo beige | `#F5F0E6` |
| Beige de paneles | `#EAE2D2` |
| Texto | `#1C2B22` |
| Texto secundario | `#607066` |
| Tipografía | Sans serif (Inter en portadas; la del tema en el sitio) |

## Imágenes y fotografía

* Fotografía limpia, clara, fotorrealista, de estudio: fondos lisos o beige, luz suave, sin ruido visual.
* Temas: personas reales trabajando (equipo de marketing, dueño en su local), pantallas con mapas y fichas, fachadas de sucursales genéricas.
* Prohibido: logotipos de terceros, marcas reales de franquicias sin permiso, texto incrustado en la foto, collages, estética de stock genérico con apretón de manos.
* Portadas de blog: `scripts/cover.py` (tipográficas, 1200x630) mientras no haya fotografía; texto alternativo descriptivo siempre.
