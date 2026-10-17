# Inafuma Ibeben C.F.

Web del equipo para la liga municipal de fútbol 7 (Juegos Deportivos Municipales de Madrid, Latina, domingo mañana, grupo 3, temporada 2026/27).

Es una web estática: Vercel publica `index.html` tal cual, sin configuración.

## Qué se actualiza cada semana

- `data/resultados.json`: los resultados por partido (`"j01-6": [goles local, goles visitante]`) y la fecha de `actualizado`.
- `data/partidos.json`: solo si el Ayuntamiento cambia una hora o un campo.
- `data/plantilla.json`: jugadores (nombre en la camiseta, dorsal, portero, capitán 1/2/3) y `staff` (delegado).
- `data/cronicas.json`: una crónica por partido, con `partido` (id de `data/partidos.json`), `autor`, `titulo` y `texto`. Mientras esté vacío, la pestaña Crónicas muestra "Próximamente".

Otros datos: `data/equipos.json` (primera equipación de cada equipo del grupo) y `data/temporada-2025-26.json` (clasificación de la temporada pasada).

La clasificación se calcula sola a partir de los resultados.

## Calendario en PDF

`calendario-inafuma-ibeben.pdf` se descarga desde la pestaña Partidos. Si cambia una hora o un campo en `data/partidos.json`, se vuelve a generar con:

    python3 tools/calendario_pdf.py

(necesita `reportlab`; las tipografías están en `tools/fonts`).

## Juego (`juego/`)

`juego/index.html` es el juego de fútbol 7 por turnos y la pizarra de alineación. Es una página autónoma (las imágenes van dentro del propio archivo). La plantilla del juego está escrita en el propio archivo (`SQUAD`), así que si cambia la plantilla hay que actualizarla también ahí.
