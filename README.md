# Inafuma Ibeben C.F.

Web del equipo para la liga municipal de fútbol 7 (Juegos Deportivos Municipales de Madrid, Latina, domingo mañana, grupo 3, temporada 2026/27).

Es una web estática: Vercel publica `index.html` tal cual, sin configuración.

## Qué se actualiza cada semana

- `data/resultados.json`: los resultados por partido (`"j01-6": [goles local, goles visitante]`) y la fecha de `actualizado`.
- `data/partidos.json`: solo si el Ayuntamiento cambia una hora o un campo.
- `data/plantilla.json`: nombres en la camiseta y dorsales cuando estén confirmados.

La clasificación se calcula sola a partir de los resultados.
