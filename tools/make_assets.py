"""Genera los GIFs/PNG pixelados de la interfaz (estilo web 2000) en static/ui/.
Uso:  python tools/make_assets.py      (necesita Pillow)"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "ui")
os.makedirs(OUT, exist_ok=True)

# Paleta fija (el índice 0 es el transparente)
PAL = [(0, 0, 0), (255, 255, 255), (201, 160, 255), (120, 255, 255), (255, 95, 210),
       (170, 255, 68), (10, 90, 26), (0, 0, 0), (255, 230, 60), (122, 44, 255),
       (255, 46, 59), (40, 10, 70), (150, 150, 170), (16, 16, 80), (5, 2, 12), (255, 140, 40)]
T, WHITE, LILAC, CYAN, PINK, LIME, DGREEN, BLACK, YELLOW, PURPLE, RED, DPURPLE, GRAY, NAVY, BG, ORANGE = range(16)


def new(w, h, bg=T):
    im = Image.new("P", (w, h), bg)
    flat = [c for rgb in PAL for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    return im


def save(frames, name, duration, transparent=True):
    kw = dict(save_all=True, append_images=frames[1:], duration=duration, loop=0, disposal=2)
    if transparent:
        kw["transparency"] = 0
    frames[0].save(os.path.join(OUT, name), **kw)


def stars():                      # fondo: campo de estrellas que titila (tile 192x192)
    rnd = random.Random(7)
    pts = [(rnd.randrange(192), rnd.randrange(192), rnd.choice([WHITE, LILAC, CYAN, PINK]),
            rnd.random(), rnd.random() < 0.25) for _ in range(75)]
    frames = []
    for f in range(8):
        im = new(192, 192, BG)
        d = ImageDraw.Draw(im)
        for x, y, col, ph, big in pts:
            t = (math.sin(2 * math.pi * (f / 8 + ph)) + 1) / 2
            if t > 0.75:
                d.point((x, y), col)
                if big:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        d.point(((x + dx) % 192, (y + dy) % 192), col)
            elif t > 0.35:
                d.point((x, y), LILAC if big else GRAY)
        frames.append(im)
    save(frames, "bg_stars.gif", 150, transparent=False)


def sparkle():                    # estrellita de 4 puntas
    frames = []
    for i, L in enumerate([1, 3, 6, 9, 6, 3]):
        im = new(24, 24)
        d = ImageDraw.Draw(im)
        col = [CYAN, PINK, LIME, LILAC, YELLOW, WHITE][i]
        d.line((12 - L, 12, 12 + L, 12), fill=col)
        d.line((12, 12 - L, 12, 12 + L), fill=col)
        d.rectangle((11, 11, 13, 13), fill=WHITE)
        if L > 4:
            for dx, dy in ((-3, -3), (3, -3), (-3, 3), (3, 3)):
                d.point((12 + dx, 12 + dy), col)
        frames.append(im)
    save(frames, "sparkle.gif", 120)


def eye():                        # ojo que mira alrededor y parpadea (uncanny)
    seq = [(0, 14), (-8, 14), (-8, 14), (0, 14), (8, 14), (8, 14), (0, 14), (0, 3), (0, 1), (0, 3), (0, 14), (0, 14)]
    durs = [500, 300, 500, 300, 300, 600, 400, 60, 90, 60, 700, 900]
    frames = []
    for dx, h in seq:
        im = new(48, 30)
        d = ImageDraw.Draw(im)
        d.ellipse((2, 15 - h, 45, 15 + h), fill=WHITE, outline=DPURPLE)
        if h > 6:
            for a, b in ((6, 12), (40, 12), (9, 18), (38, 19)):    # venitas
                d.line((a, b, a + (6 if a < 24 else -6), 15), fill=RED)
            d.ellipse((24 + dx - 9, 15 - 9, 24 + dx + 9, 15 + 9), fill=LIME, outline=DGREEN)
            d.rectangle((24 + dx - 1, 15 - 8, 24 + dx + 1, 15 + 8), fill=BLACK)
            d.point((24 + dx - 5, 15 - 5), WHITE)
        else:
            d.line((2, 15, 45, 15), fill=PURPLE)
        frames.append(im)
    save(frames, "eye.gif", durs)


def hazard():                     # cinta "under construction" que se desplaza
    frames = []
    for s in range(0, 16, 2):
        im = new(64, 16, BLACK)
        px = im.load()
        for x in range(64):
            for y in range(16):
                px[x, y] = YELLOW if ((x + y + s) // 8) % 2 == 0 else BLACK
        frames.append(im)
    save(frames, "hazard.gif", 80, transparent=False)


def jelly():                      # medusa onírica que flota
    frames = []
    for f in range(8):
        ph = 2 * math.pi * f / 8
        dy = round(3 * math.sin(ph))
        im = new(64, 84)
        d = ImageDraw.Draw(im)
        for i in range(5):                                     # tentáculos
            bx = 14 + i * 9
            for yy in range(0, 38, 2):
                x = bx + round(3 * math.sin(yy / 5 + ph + i))
                d.rectangle((x, 34 + dy + yy, x + 1, 35 + dy + yy), fill=PINK if (yy // 4) % 2 else LILAC)
        d.pieslice((6, 6 + dy, 58, 62 + dy), 180, 360, fill=LILAC, outline=PURPLE)
        d.pieslice((14, 12 + dy, 50, 48 + dy), 180, 360, fill=PINK)
        d.ellipse((18, 14 + dy, 26, 18 + dy), fill=WHITE)
        for x in range(8, 58, 8):
            d.ellipse((x - 3, 31 + dy, x + 3, 37 + dy), fill=LILAC, outline=PURPLE)
        frames.append(im)
    save(frames, "jelly.gif", 130)


def heart():
    rows = ["01100110", "11111111", "11111111", "11111111", "01111110", "00111100", "00011000"]
    frames = []
    for col, k in ((RED, 2), (PINK, 3), (RED, 2), (WHITE, 2)):
        im = new(8 * 3, 7 * 3)
        d = ImageDraw.Draw(im)
        for y, r in enumerate(rows):
            for x, c in enumerate(r):
                if c == "1":
                    d.rectangle((x * 3, y * 3, x * 3 + 2, y * 3 + 2), fill=col)
        frames.append(im)
    save(frames, "heart.gif", 300)


def cursor():                     # cursor pixelado (flecha lima con borde negro)
    im = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(1, 1), (1, 15), (5, 11), (8, 18), (11, 17), (8, 10), (14, 10)], fill=(170, 255, 68, 255), outline=(0, 0, 0, 255))
    d.rectangle((13, 2, 15, 4), fill=(255, 95, 210, 255))
    im.save(os.path.join(OUT, "cursor.png"))


def button88(name, lines, c1, c2, txt=WHITE):     # botones 88x31 animados
    font = ImageFont.load_default()
    frames = []
    for f in range(4):
        im = new(88, 31, c1)
        d = ImageDraw.Draw(im)
        for x in range(-31, 88, 8):                              # franjas que corren
            d.polygon([(x + f * 2, 31), (x + 4 + f * 2, 31), (x + 35 + f * 2, 0), (x + 31 + f * 2, 0)], fill=c2)
        d.rectangle((0, 0, 87, 30), outline=[WHITE, LIME, PINK, CYAN][f])
        d.rectangle((1, 1, 86, 29), outline=BLACK)
        y0 = 15 - 6 * len(lines) // 1 + (2 if len(lines) == 1 else 0)
        for i, ln in enumerate(lines):
            w = d.textlength(ln, font=font)
            col = YELLOW if (f % 2 and i == 0) else txt
            for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, 1)):   # contorno para legibilidad
                d.text(((88 - w) / 2 + ox, y0 + i * 12 + oy), ln, font=font, fill=BLACK)
            d.text(((88 - w) / 2, y0 + i * 12), ln, font=font, fill=col)
        frames.append(im)
    save(frames, name, 200, transparent=False)


if __name__ == "__main__":
    stars(); sparkle(); eye(); hazard(); jelly(); heart(); cursor()
    button88("btn_tansi.gif", ["TANSI", "VISUAL STUDIO"], DPURPLE, PURPLE)
    button88("btn_wokwi.gif", ["ESP32", "+ WOKWI"], DGREEN, LIME, txt=BLACK)
    button88("btn_mqtt.gif", ["MQTT", "POWERED"], NAVY, CYAN)
    button88("btn_music.gif", ["LOUD MUSIC", "140 BPM"], DPURPLE, PINK)
    button88("btn_chrome.gif", ["BEST VIEWED", "IN CHROME"], BLACK, DGREEN)
    button88("btn_vj.gif", ["VJ MODE", "ON"], RED, ORANGE)
    print("assets en", os.path.abspath(OUT))
