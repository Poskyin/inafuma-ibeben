"""Genera calendario-inafuma-ibeben.pdf (una hoja A4) a partir de data/partidos.json y data/equipos.json.

Uso, desde la raíz del repositorio:  python3 tools/calendario_pdf.py
"""
import json, datetime, collections, pathlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "tools" / "fonts"
OUT = ROOT / "calendario-inafuma-ibeben.pdf"
TEAM = "Inafuma Ibeben"
WEB = "inafuma-ibeben.vercel.app"

for name, file in [("Black", "BigShoulders-Black.ttf"), ("Disp", "BigShoulders-ExtraBold.ttf"),
                   ("Body", "Outfit-Regular.ttf"), ("BodySB", "Outfit-SemiBold.ttf"), ("BodyB", "Outfit-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / file)))

ROSA = HexColor("#D81F80"); ROSA_INK = HexColor("#B0145F"); ROSA_SOFT = HexColor("#FBEAF2"); ROSA_ROW = HexColor("#FDF4F8")
ORO = HexColor("#D6AE57"); ORO_INK = HexColor("#9A7424"); ORO_LIGHT = HexColor("#F2CF7C")
INK = HexColor("#22141C"); MUTED = HexColor("#75626C"); LINE = HexColor("#EADFD9"); NIGHT = HexColor("#28041A")
CREAM = HexColor("#FFF8F1")
VENUE = {"Las Cruces": ROSA, "Aluche": ORO, "Gallur": HexColor("#173A82")}
VENUE_SUB = {"Las Cruces": "CDM Las Cruces", "Aluche": "Av. de las Águilas, 14", "Gallur": "CDM Gallur"}
DAYS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]

partidos = json.loads((ROOT / "data" / "partidos.json").read_text())
kits = json.loads((ROOT / "data" / "equipos.json").read_text()).get("equipos", {})
games = []
for p in partidos:
    if TEAM not in (p["local"], p["visitante"]):
        continue
    home = p["local"] == TEAM
    games.append(dict(j=p["jornada"], dt=datetime.date.fromisoformat(p["fecha"]), t=p["hora"], home=home,
                      opp=p["visitante"] if home else p["local"], site=p["sede"], field=str(p["campo"])))
games.sort(key=lambda g: g["j"])

W, H = A4
M = 26
c = canvas.Canvas(str(OUT), pagesize=A4)
c.setTitle("Inafuma Ibeben C.F. · Calendario 2026/27")
c.setAuthor("Inafuma Ibeben C.F.")


def text(x, y, s, font, size, color=INK, align="left", cs=0.0):
    w = pdfmetrics.stringWidth(s, font, size) + cs * max(len(s) - 1, 0)
    if align == "right": x -= w
    elif align == "center": x -= w / 2
    t = c.beginText(); t.setFont(font, size); t.setCharSpace(cs); t.setFillColor(color)
    t.setTextOrigin(x, y); t.textOut(s); c.drawText(t)
    return w


def swatch(x, y, team):
    """Small shirt + shorts icon of a team's first kit, bottom-left at (x, y)."""
    k = kits.get(team)
    if not k: return 0
    cols = [HexColor(v) for v in k.get("colores", [])] or [white]
    sw, sh, pw, ph = 12, 8.5, 8.5, 4
    c.saveState()
    p = c.beginPath(); p.roundRect(x, y + ph + 0.6, sw, sh, 1.6); c.clipPath(p, stroke=0, fill=0)
    if len(cols) > 1 and k.get("dibujo") == "franja":
        c.setFillColor(cols[0]); c.rect(x, y + ph + 0.6, sw, sh, stroke=0, fill=1)
        c.setFillColor(cols[1]); c.rect(x, y + ph + 0.6 + sh * 0.36, sw, sh * 0.28, stroke=0, fill=1)
    elif len(cols) > 1:
        for i in range(6):
            c.setFillColor(cols[i % 2]); c.rect(x + i * sw / 6, y + ph + 0.6, sw / 6 + 0.1, sh, stroke=0, fill=1)
    else:
        c.setFillColor(cols[0]); c.rect(x, y + ph + 0.6, sw, sh, stroke=0, fill=1)
    c.restoreState()
    c.setStrokeColor(HexColor("#B9A9B1")); c.setLineWidth(0.5)
    c.roundRect(x, y + ph + 0.6, sw, sh, 1.6, stroke=1, fill=0)
    c.setFillColor(HexColor(k.get("pantalonColor", "#FFFFFF")))
    c.rect(x + (sw - pw) / 2, y, pw, ph, stroke=1, fill=1)
    return sw


# ---------- Header: pink-and-gold marble, as on the shirt ----------
bh = 196
by = H - bh
c.saveState()
p = c.beginPath(); p.rect(0, by, W, bh); c.clipPath(p, stroke=0, fill=0)
iw = W; ih = iw * 760 / 1400
c.drawImage(str(ROOT / "img" / "marmol-rosa.jpg"), 0, by + bh / 2 - ih / 2, iw, ih)
c.setFillColor(NIGHT); c.setFillAlpha(0.34); c.rect(0, by, W, bh, stroke=0, fill=1)
c.restoreState()
c.setFillColor(ORO); c.rect(0, by - 4, W, 4, stroke=0, fill=1)

cs_ = 128
c.drawImage(str(ROOT / "img" / "escudo.png"), M + 6, by + (bh - cs_) / 2 + 4, cs_, cs_, mask="auto")
tx = M + cs_ + 30
text(tx, by + bh - 50, "JUEGOS DEPORTIVOS MUNICIPALES · TEMPORADA 2026/27", "BodySB", 8.5, ORO_LIGHT, cs=1.2)
w = text(tx - 1, by + bh - 102, "INAFUMA IBEBEN", "Black", 50, CREAM, cs=0.4)
text(tx - 1 + w + 8, by + bh - 102, "C.F.", "Black", 50, ORO_LIGHT, cs=0.4)
text(tx, by + bh - 122, "Fútbol 7 · Latina · Domingos por la mañana · Grupo 3", "Body", 10.5, CREAM)

nh = sum(g["home"] for g in games)
first = games[0]
chips = [f"{len(games)} PARTIDOS", f"{nh} EN CASA", f"{len(games) - nh} FUERA",
         f"DEBUT: {DAYS[first['dt'].weekday()].upper()} {first['dt'].day} {MONTHS[first['dt'].month - 1].upper()} · {first['t']}"]
x = tx; cy = by + 30
for ch in chips:
    cw = pdfmetrics.stringWidth(ch, "BodySB", 8) + 0.8 * (len(ch) - 1) + 18
    c.setStrokeColor(ORO_LIGHT); c.setLineWidth(0.9)
    c.roundRect(x, cy - 5.5, cw, 18, 9, stroke=1, fill=0)
    text(x + 9, cy, ch, "BodySB", 8, ORO_LIGHT, cs=0.8)
    x += cw + 6

# ---------- Fixture list ----------
cols = {"j": M + 16, "fecha": M + 38, "hora": M + 112, "cond": M + 160, "rival": M + 240, "campo": M + 412}
top = by - 4 - 22
for k, lab in [("fecha", "FECHA"), ("hora", "HORA"), ("cond", "CONDICIÓN"), ("rival", "RIVAL Y SU EQUIPACIÓN"), ("campo", "CAMPO")]:
    text(cols[k], top, lab, "BodySB", 7.5, MUTED, cs=1)
text(cols["j"], top, "J", "BodySB", 7.5, MUTED, align="center", cs=1)
c.setStrokeColor(ORO); c.setLineWidth(1.4); c.line(M, top - 7, W - M, top - 7)

footer_top = M + 84
breaks = sum(1 for a, b in zip(games, games[1:]) if a["dt"].month != b["dt"].month)
gap = 5
y = top - 7
rh = (y - footer_top - breaks * gap - 6) / len(games)
my_kit = (kits.get(TEAM) or {}).get("camiseta", "").lower()
for i, g in enumerate(games):
    if i and games[i - 1]["dt"].month != g["dt"].month:
        y -= gap
    y0 = y - rh; mid = y0 + rh / 2
    if i % 2 == 0:
        c.setFillColor(ROSA_ROW); c.rect(M, y0, W - 2 * M, rh, stroke=0, fill=1)
    text(cols["j"], mid - 5.5, str(g["j"]), "Disp", 17, ROSA, align="center")
    d = g["dt"]
    text(cols["fecha"], mid - 3.6, f"{DAYS[d.weekday()].capitalize()} {d.day} {MONTHS[d.month - 1]}", "Body", 10.5, INK)
    text(cols["hora"], mid - 4.6, g["t"], "Disp", 15.5, INK, cs=0.3)
    bw = 64
    if g["home"]:
        c.setFillColor(ROSA); c.roundRect(cols["cond"], mid - 7.5, bw, 15, 7.5, stroke=0, fill=1)
        text(cols["cond"] + bw / 2, mid - 2.9, "LOCAL", "BodyB", 8, white, align="center", cs=1.1)
    else:
        c.setStrokeColor(ORO); c.setLineWidth(1)
        c.roundRect(cols["cond"] + 0.5, mid - 7, bw - 1, 14, 7, stroke=1, fill=0)
        text(cols["cond"] + bw / 2, mid - 2.9, "VISITANTE", "BodyB", 8, ORO_INK, align="center", cs=1.1)
    sw = swatch(cols["rival"], mid - 7, g["opp"])
    nx = cols["rival"] + (sw + 7 if sw else 0)
    size = 11
    room = cols["campo"] - nx - 8
    clash = my_kit and (kits.get(g["opp"]) or {}).get("camiseta", "").lower() == my_kit
    tag = f"también de {my_kit}" if clash else ""
    tagw = pdfmetrics.stringWidth(tag, "BodySB", 7) + 10 if tag else 0
    while pdfmetrics.stringWidth(g["opp"], "BodySB", size) > room - tagw - 4 and size > 8:
        size -= 0.5
    nw = text(nx, mid - 3.8, g["opp"], "BodySB", size, INK)
    if tag:
        tx2 = nx + nw + 5
        c.setFillColor(ROSA_SOFT); c.roundRect(tx2, mid - 5.5, tagw, 11, 3, stroke=0, fill=1)
        text(tx2 + 5, mid - 2.4, tag, "BodySB", 7, ROSA_INK)
    c.setFillColor(VENUE.get(g["site"], MUTED)); c.circle(cols["campo"] + 4, mid, 3.6, stroke=0, fill=1)
    vw = text(cols["campo"] + 13, mid - 3.6, g["site"], "BodySB", 10.5, INK)
    text(cols["campo"] + 13 + vw, mid - 3.6, f"  ·  campo {g['field']}", "Body", 10, MUTED)
    y = y0
c.setStrokeColor(ORO); c.setLineWidth(1.4); c.line(M, y, W - M, y)

# ---------- Footer: venues and where to check changes ----------
cnt = collections.Counter(g["site"] for g in games)
fields = collections.defaultdict(set)
for g in games: fields[g["site"]].add(g["field"])
colw = (W - 2 * M) / 3
fy = M + 48
for k, site in enumerate(["Las Cruces", "Aluche", "Gallur"]):
    x = M + k * colw
    c.setFillColor(VENUE[site]); c.circle(x + 5, fy + 5.5, 5, stroke=0, fill=1)
    text(x + 16, fy, site.upper(), "Disp", 17, INK, cs=0.4)
    text(x + 16, fy - 14, f"{cnt[site]} partidos · campos {' y '.join(sorted(fields[site]))}", "Body", 9, MUTED)
    text(x + 16, fy - 25.5, VENUE_SUB[site], "Body", 9, MUTED)
today = datetime.date.today()
w = text(M, M, "Resultados y clasificación en ", "Body", 8.5, MUTED)
w += text(M + w, M, WEB, "BodySB", 8.5, ROSA_INK)
c.linkURL("https://" + WEB, (M + w - pdfmetrics.stringWidth(WEB, "BodySB", 8.5), M - 2, M + w, M + 9), relative=0)
text(W - M, M, f"Calendario oficial a {today.day} {MONTHS[today.month - 1]} {today.year} · cambios en deportesweb.madrid.es", "Body", 8.5, MUTED, align="right")

c.showPage()
c.save()
print("PDF:", OUT, "filas:", len(games), "alto fila:", round(rh, 1))
