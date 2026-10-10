# Inafuma Ibeben C.F.

Web del equipo para la liga municipal de fútbol 7 (Juegos Deportivos Municipales de Madrid, Latina, domingo mañana, grupo 3, temporada 2026/27).

Es una web estática: Vercel publica `index.html` tal cual, sin configuración.

## Qué se actualiza cada semana

- `data/resultados.json`: los resultados por partido (`"j01-6": [goles local, goles visitante]`) y la fecha de `actualizado`.
- `data/partidos.json`: solo si el Ayuntamiento cambia una hora o un campo.
- `data/plantilla.json`: jugadores, nombre en la camiseta, dorsal y quién es portero.

Otros datos: `data/equipos.json` (primera equipación de cada equipo del grupo) y `data/temporada-2025-26.json` (clasificación de la temporada pasada).

La clasificación se calcula sola a partir de los resultados.
