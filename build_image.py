#!/usr/bin/env python3
"""Draw entry.png: a cream newspaper front page summing up Friday 20 November 2026.

1024x1024, deterministic (fixed coordinates, no randomness, no timestamps).
Original Pillow drawings only. Run: python3 build_image.py
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W = H = 1024
M = 16                      # page margin
CW = W - 2 * M              # content width = 992

CREAM = (247, 243, 232)
BOX_BG = (252, 250, 244)
INK = (26, 24, 20)
RED = (176, 42, 30)
GREY = (92, 88, 80)
RULE = (70, 66, 58)
OCEAN = (212, 225, 232)
LAND = (198, 180, 142)
LAND_EDGE = (118, 100, 68)
SEA_BLUE = (70, 110, 150)
FLAME = (232, 110, 30)
FLAME2 = (245, 170, 40)
SMOKE = (120, 118, 112)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(draw, text, font):
    return draw.textlength(text, font=font)


def fit_font(draw, text, path, max_w, size, min_size=8):
    """Shrink font until text fits max_w."""
    while size > min_size and tw(draw, text, F(path, size)) > max_w:
        size -= 1
    return F(path, size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(draw, trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, text, font, fill, max_w, leading, max_lines=None):
    lines = wrap(draw, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def centered(draw, cx, y, text, font, fill):
    draw.text((cx - tw(draw, text, font) / 2, y), text, font=font, fill=fill)


def hrule(draw, y, x0=M, x1=W - M, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def badge(draw, cx, cy, r, num):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f = F(SANS_B, 11 if num < 10 else 9)
    s = str(num)
    draw.text((cx - tw(draw, s, f) / 2, cy - 6), s, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- drawings

def draw_cyclone(draw, x, y, w, h):
    """Spiral storm crossing a coastline. Box top-left (x, y)."""
    draw.rectangle([x, y, x + w, y + h], fill=OCEAN, outline=RULE, width=1)
    # landmass on the right, coast curving down
    coast = [(x + w * 0.62, y), (x + w * 0.55, y + h * 0.3), (x + w * 0.60, y + h * 0.55),
             (x + w * 0.52, y + h * 0.8), (x + w * 0.58, y + h)]
    land = coast + [(x + w, y + h), (x + w, y)]
    draw.polygon(land, fill=LAND)
    draw.line(coast, fill=LAND_EDGE, width=2)
    # spiral centred on the coast
    cx, cy = x + w * 0.56, y + h * 0.48
    pts = []
    turns = 3.2
    steps = 220
    for i in range(steps + 1):
        t = i / steps
        ang = t * turns * 2 * math.pi
        r = 4 + t * (min(w, h) * 0.52)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.82))
    draw.line(pts, fill=SEA_BLUE, width=4)
    draw.ellipse([cx - 6, cy - 5, cx + 6, cy + 5], fill=CREAM, outline=SEA_BLUE, width=2)
    # rain streaks over land
    for i in range(7):
        rx = x + w * 0.68 + i * w * 0.042
        ry = y + h * 0.18 + (i % 3) * h * 0.22
        draw.line([(rx, ry), (rx - 7, ry + 13)], fill=SEA_BLUE, width=2)
    f = F(SANS_B, 8)
    draw.text((x + 6, y + h - 13), "BAY OF BENGAL", font=f, fill=SEA_BLUE)
    draw.text((x + w * 0.66, y + 5), "ODISHA", font=f, fill=LAND_EDGE)
    draw.ellipse([cx - 2, cy + 14, cx + 2, cy + 18], fill=RED)
    draw.text((cx + 5, cy + 11), "Gopalpur", font=F(SANS, 8), fill=INK)


def draw_calendar_chart(draw, x, y, w, h):
    """JAN 1 2027 calendar card + rising cost bars."""
    draw.rectangle([x, y, x + w, y + h], fill=BOX_BG, outline=RULE, width=1)
    # calendar card
    cx0, cy0, cw, ch = x + 14, y + 6, 104, h - 12
    draw.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], fill=(255, 255, 255), outline=INK, width=2)
    draw.rectangle([cx0, cy0, cx0 + cw, cy0 + 18], fill=RED)
    centered(draw, cx0 + cw / 2, cy0 + 3, "JANUARY", F(SANS_B, 11), (255, 255, 255))
    centered(draw, cx0 + cw / 2, cy0 + 19, "1", F(SERIF_B, 28), INK)
    centered(draw, cx0 + cw / 2, cy0 + ch - 15, "2027", F(SANS_B, 12), INK)
    # bar chart
    bx0, by1 = x + 140, y + h - 16
    bw, gap = 26, 10
    heights = [16, 26, 38, 52]
    for i, bh in enumerate(heights):
        bx = bx0 + i * (bw + gap)
        draw.rectangle([bx, by1 - bh, bx + bw, by1], fill=RED if i == 3 else (150, 145, 135))
    draw.line([(bx0 - 6, by1), (bx0 + 4 * (bw + gap), by1)], fill=INK, width=2)
    draw.text((bx0, y + 8), "IRAN WAR COST", font=F(SANS_B, 9), fill=INK)
    draw.text((bx0, y + 20), "past $48.3bn", font=F(SANS_B, 11), fill=RED)
    draw.text((bx0, by1 + 3), "decision deferred to 2027", font=F(SANS, 8), fill=GREY)


def _tower(draw, x, base, w, h, damaged=False):
    top = base - h
    draw.rectangle([x, top, x + w, base], fill=(205, 200, 190), outline=INK, width=2)
    cols, rows = 4, max(4, h // 10)
    for c in range(cols):
        for r in range(rows):
            wx = x + 5 + c * ((w - 10) // cols)
            wy = top + 5 + r * ((h - 10) // rows)
            fill = (240, 225, 170) if (c + r) % 3 else (120, 135, 150)
            if damaged and 1 <= r <= 3:
                fill = (40, 38, 36)
            draw.rectangle([wx, wy, wx + 6, wy + 6], fill=fill)
    if damaged:
        draw.rectangle([x + 3, top + 20, x + w - 3, top + 36], fill=(60, 55, 50))
        fx, fy = x + w / 2, top + 22
        draw.polygon([(fx - 8, fy), (fx, fy - 14), (fx + 8, fy)], fill=FLAME)
        draw.polygon([(fx - 4, fy), (fx, fy - 8), (fx + 4, fy)], fill=FLAME2)
        for sx, sy, sr in [(fx + 4, top + 3, 5), (fx + 13, top + 1, 6), (fx + 23, top - 1, 7)]:
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SMOKE)


def draw_towers_tanker(draw, x, y, w, h):
    """Rectangular towers (one damaged) + burning tanker."""
    draw.rectangle([x, y, x + w, y + h], fill=(235, 232, 224), outline=RULE, width=1)
    base = y + h - 12
    _tower(draw, x + 12, base, 42, 46)
    _tower(draw, x + 62, base, 52, 58, damaged=True)
    _tower(draw, x + 122, base, 38, 40)
    draw.line([(x + 4, base), (x + w - 4, base)], fill=INK, width=2)
    # tanker on the right
    tx0, tx1, deck = x + 172, x + w - 8, base - 16
    draw.polygon([(tx0, deck), (tx1, deck), (tx1 - 10, base), (tx0 + 8, base)], fill=(90, 60, 50), outline=INK)
    draw.rectangle([tx0, deck - 4, tx1, deck], fill=(60, 55, 50))
    draw.rectangle([tx1 - 26, deck - 18, tx1 - 6, deck - 4], fill=(220, 216, 208), outline=INK)
    for i in range(3):
        draw.rectangle([tx1 - 23 + i * 6, deck - 15, tx1 - 19 + i * 6, deck - 10], fill=(120, 135, 150))
    fx = tx0 + 22
    draw.polygon([(fx - 9, deck - 4), (fx, deck - 24), (fx + 9, deck - 4)], fill=FLAME)
    draw.polygon([(fx - 5, deck - 4), (fx, deck - 15), (fx + 5, deck - 4)], fill=FLAME2)
    draw.ellipse([fx + 2, deck - 36, fx + 16, deck - 24], fill=SMOKE)
    # waves
    pts = []
    for i in range(41):
        wx = tx0 - 4 + i * ((tx1 - tx0 + 8) / 40)
        pts.append((wx, base + 5 + 2.5 * math.sin(i * 0.9)))
    draw.line(pts, fill=SEA_BLUE, width=2)
    draw.text((x + 10, y + 4), "RIYADH", font=F(SANS_B, 8), fill=GREY)
    draw.text((tx0 + 30, y + 4), "HORMUZ", font=F(SANS_B, 8), fill=GREY)


# ---------------------------------------------------------------- world map

def _poly(draw, pts, mx, my, mw, mh):
    xy = [(mx + (lon + 180) / 360 * mw, my + (75 - lat) / 130 * mh) for lon, lat in pts]
    draw.polygon(xy, fill=LAND, outline=LAND_EDGE, width=1)


def draw_map(draw, x, y, w, h):
    """Simplified world map, lon -180..180, lat 75..-55. Returns pin projector."""
    draw.rectangle([x, y, x + w, y + h], fill=OCEAN, outline=RULE, width=1)
    mx, my, mw, mh = x + 4, y + 4, w - 8, h - 8

    north_america = [(-168, 66), (-158, 71), (-140, 70), (-128, 70), (-115, 69), (-100, 69),
                     (-90, 69), (-82, 66), (-78, 62), (-72, 58), (-65, 50), (-56, 47), (-60, 45),
                     (-68, 44), (-70, 42), (-74, 40), (-76, 36), (-79, 33), (-81, 31), (-80, 26),
                     (-84, 30), (-89, 30), (-94, 29), (-97, 26), (-97, 22), (-94, 18), (-90, 21),
                     (-87, 21), (-88, 16), (-83, 9), (-79, 9), (-82, 8), (-86, 12), (-92, 15),
                     (-96, 16), (-102, 18), (-105, 20), (-110, 23), (-114, 29), (-117, 33),
                     (-122, 37), (-124, 42), (-124, 47), (-128, 51), (-133, 56), (-140, 60),
                     (-152, 59), (-158, 56), (-162, 58), (-165, 60), (-168, 66)]
    south_america = [(-79, 9), (-72, 12), (-64, 10), (-55, 6), (-50, 0), (-44, -3), (-35, -8),
                     (-39, -13), (-40, -21), (-48, -26), (-52, -33), (-58, -39), (-62, -41),
                     (-65, -45), (-67, -50), (-68, -54), (-71, -54), (-73, -50), (-73, -44),
                     (-73, -37), (-71, -30), (-70, -20), (-70, -18), (-75, -15), (-77, -12),
                     (-80, -5), (-81, 1), (-79, 9)]
    eurasia = [(-9, 43), (-2, 44), (0, 46), (-5, 48), (-2, 50), (2, 51), (5, 53), (8, 55),
               (8, 57), (12, 56), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (28, 66),
               (32, 70), (45, 68), (60, 69), (75, 72), (90, 75), (105, 77), (120, 73),
               (135, 72), (150, 70), (165, 69), (178, 66), (178, 62), (162, 60), (158, 52),
               (150, 45), (142, 42), (140, 38), (135, 35), (129, 33), (122, 31), (120, 26),
               (113, 22), (108, 18), (107, 12), (104, 8), (100, 6), (98, 10), (97, 15),
               (93, 20), (90, 22), (88, 21), (86, 20), (82, 16), (80, 13), (77, 8),
               (75, 12), (72, 19), (70, 21), (66, 25), (61, 25), (57, 26), (52, 26),
               (50, 29), (48, 30), (50, 26), (54, 24), (56, 24), (59, 22), (55, 17),
               (52, 15), (45, 12), (43, 12), (42, 15), (39, 21), (36, 28), (34, 31),
               (36, 36), (30, 36), (27, 37), (23, 36), (19, 40), (15, 38), (16, 40),
               (12, 44), (8, 44), (3, 43), (0, 39), (-2, 37), (-6, 36), (-9, 37), (-9, 43)]
    africa = [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (34, 28),
              (35, 24), (37, 22), (39, 20), (41, 16), (43, 12), (48, 11), (51, 12), (51, 10),
              (48, 5), (42, -2), (40, -10), (39, -18), (36, -22), (35, -26), (32, -29),
              (27, -33), (20, -35), (18, -33), (16, -29), (14, -23), (12, -18), (13, -12),
              (12, -6), (9, -1), (9, 4), (6, 4), (3, 6), (-2, 5), (-8, 5), (-13, 8),
              (-17, 15), (-17, 21), (-16, 24), (-13, 28), (-9, 31), (-6, 35)]
    australia = [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (130, -32),
                 (133, -32), (136, -35), (138, -35), (140, -38), (145, -38), (147, -38),
                 (150, -37), (153, -30), (153, -27), (151, -24), (149, -20), (146, -19),
                 (145, -15), (142, -11), (142, -14), (141, -17), (139, -17), (136, -15),
                 (135, -12), (132, -11), (129, -14), (126, -14), (122, -17), (117, -20), (113, -22)]
    greenland = [(-58, 64), (-52, 60), (-44, 60), (-42, 62), (-40, 66), (-32, 68), (-22, 70),
                 (-20, 76), (-28, 80), (-45, 80), (-58, 76), (-60, 70), (-58, 64)]
    uk = [(-5, 50), (-3, 53), (-5, 55), (-6, 57), (-3, 58), (-2, 57), (-1, 54), (1, 52), (1, 51), (-3, 50), (-5, 50)]
    japan = [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (141, 44), (143, 44),
             (141, 42), (140, 38), (138, 35), (134, 34), (131, 33), (130, 31)]
    indonesia = [(95, 5), (100, 0), (104, -3), (106, -6), (110, -7), (114, -8), (119, -9),
                 (120, -10), (114, -10), (108, -8), (103, -5), (99, -1), (95, 3), (95, 5)]
    nz_north = [(173, -35), (176, -37), (178, -38), (177, -39), (175, -40), (174, -41), (173, -39), (173, -35)]
    nz_south = [(172, -41), (174, -42), (173, -44), (171, -45), (168, -46), (167, -46), (168, -44), (171, -42), (172, -41)]
    madagascar = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (45, -25), (44, -22), (44, -18), (44, -16)]

    for poly in (north_america, south_america, eurasia, africa, australia, greenland,
                 uk, japan, indonesia, nz_north, nz_south, madagascar):
        _poly(draw, poly, mx, my, mw, mh)
    # Fiji: tiny island dot so pin 11 sits on land
    fx = mx + (177.5 + 180) / 360 * mw
    fy = my + (75 - (-17.7)) / 130 * mh
    draw.ellipse([fx - 4, fy - 3, fx + 4, fy + 3], fill=LAND, outline=LAND_EDGE, width=1)

    def pin(lon, lat):
        return (mx + (lon + 180) / 360 * mw, my + (75 - lat) / 130 * mh)

    pins = {1: (84.8, 19.3), 2: (-77, 38.9), 3: (46.7, 24.6), 4: (114.1, 22.5),
            5: (30.5, 50.4), 6: (14, 52), 7: (34.3, 31.5), 8: (-122.4, 37.8),
            9: (168, 64), 10: (174.8, -41.3), 11: (177.5, -17.7), 12: (125.8, 39.8),
            13: (2.3, 48.9), 14: (13.2, -8.8)}
    for num, (lon, lat) in pins.items():
        px, py = pin(lon, lat)
        r = 6.5
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
        f = F(SANS_B, 8 if num < 10 else 7)
        s = str(num)
        draw.text((px - tw(draw, s, f) / 2, py - 4), s, font=f, fill=(255, 255, 255))
    # Voyager label at the top-right edge (the one edge pin allowed)
    vx, vy = pin(168, 64)
    draw.text((vx - 96, vy - 5), "VOYAGER 1", font=F(SANS_B, 7), fill=INK)
    draw.line([(vx - 40, vy), (vx - 9, vy)], fill=INK, width=1)
    return pin


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # top line
    d.text((M, 10), "THE DAY IN ONE PICTURE  •  WORLD NEWS FRONT PAGE", font=F(SANS, 11), fill=INK)
    rt = "33 STORIES  •  1 DAY"
    d.text((W - M - tw(d, rt, F(SANS_B, 11)), 10), rt, font=F(SANS_B, 11), fill=RED)
    hrule(d, 28, width=2)

    # masthead
    centered(d, W / 2, 36, "Friday 20 November 2026", F(SERIF_B, 54), INK)
    hrule(d, 98, width=2)
    hrule(d, 102, width=1)

    # red subhead
    sub = "Cyclone Akvan hits Odisha  •  Trump defers Iran to 2027  •  Riyadh tower hit, tanker mined in Hormuz"
    centered(d, W / 2, 108, sub, fit_font(d, sub, SANS_B, CW, 15), RED)
    hrule(d, 130)

    # timeline
    d.text((M, 136), "FRIDAY IN UTC", font=F(SANS_B, 11), fill=INK)
    slots = [("01:27", "Tanker mined E. of Hormuz"),
             ("~02:30", "Akvan crosses near Gopalpur"),
             ("03:06", "Trump defers Iran (Reuters)"),
             ("03:17", "Call for Gaza aid access"),
             ("04:07", "Kyiv ballistic strikes"),
             ("04:22", "Genoa drones shut airport"),
             ("Evening", "Trump WH press conference")]
    colw = CW / 7
    for i, (t, label) in enumerate(slots):
        x = M + i * colw
        d.text((x + 5, 152), t, font=F(SANS_B, 11), fill=RED)
        block(d, x + 5, 166, label, F(SANS, 9), INK, colw - 10, 11, max_lines=3)
        if i:
            d.line([(x, 150), (x, 198)], fill=(190, 185, 172), width=1)
    hrule(d, 202)

    # region strip
    regions = [("EUROPE", 5), ("AMERICAS", 8), ("ASIA-PACIFIC", 10), ("MIDEAST", 3),
               ("AFRICA", 1), ("OCEANIA", 2), ("WORLD", 4)]
    rw = CW / 7
    for i, (name, n) in enumerate(regions):
        x = M + i * rw
        d.rectangle([x + 2, 208, x + rw - 2, 234], outline=RULE, width=1)
        label = f"{name}  {n}"
        centered(d, x + rw / 2, 214, label, fit_font(d, label, SANS_B, rw - 10, 12), INK)
    # numbers
    d.text((M, 242), "THE DAY IN NUMBERS", font=F(SANS_B, 11), fill=INK)
    numbers = [("300,000", "evacuated for Akvan"), ("423", "rescue teams deployed"),
               ("51–48", "Senate vote on war powers"), ("$48.3bn", "Iran war cost so far"),
               ("113*", "Nicholls, NZ v India"), ("$1.8bn", "GTA VI sales"),
               ("5,248 pts", "Taiwan 3-day fall"), ("1 light-day", "Voyager 1 from Earth")]
    nw = CW / 8
    for i, (num, label) in enumerate(numbers):
        cx = M + i * nw + nw / 2
        centered(d, cx, 258, num, fit_font(d, num, SERIF_B, nw - 8, 20), RED)
        lines = wrap(d, label, F(SANS, 8.5), nw - 10)
        yy = 282
        for ln in lines[:2]:
            centered(d, cx, yy, ln, F(SANS, 8.5), INK)
            yy += 10
    hrule(d, 306)

    # leads
    leads = [
        (1, "ASIA-PACIFIC • WEATHER — ODISHA, INDIA", "Cyclone Akvan crosses the coast",
         "Severe storm crossed near Gopalpur Friday morning, winds 70–80 km/h gusting 90. "
         "About 300,000 evacuated to 9,341 shelters; 423 rescue teams; 69 trains cancelled; schools shut.",
         "Source: IMD / The Hindu", draw_cyclone),
        (2, "AMERICAS • POLITICS — WASHINGTON", "Trump defers Iran: see after Jan 1",
         "No rush on an Iran decision — Trump says he will decide in 2027 (Reuters, Fri 03:06 UTC). "
         "Senate 51–48 rejects curbing war powers overnight; Pentagon puts war cost past $48.3bn.",
         "Source: Reuters / AP", draw_calendar_chart),
        (3, "MIDEAST • WAR — RIYADH & HORMUZ", "Riyadh tower hit; tanker mined",
         "Houthi CLAIM: strikes on 4 Saudi targets; Riyadh landmark tower damaged — Saudi confirms "
         "damage. Tanker mined and on fire east of Hormuz, 01:27 UTC (IRGC claim).",
         "Source: Saudi stmt / Reuters", draw_towers_tanker),
    ]
    colw3 = CW / 3
    ly = 314
    for i, (num, kicker, head, body, src, art) in enumerate(leads):
        x = M + i * colw3
        badge(d, x + 12, ly + 10, 10, num)
        d.text((x + 28, ly + 3), kicker, font=fit_font(d, kicker, SANS_B, colw3 - 34, 10), fill=RED)
        hy = block(d, x + 4, ly + 22, head, F(SERIF_B, 20), INK, colw3 - 10, 24, max_lines=2)
        art(d, x + 4, ly + 74, colw3 - 12, 78)
        by = block(d, x + 4, ly + 158, body, F(SANS, 9.5), INK, colw3 - 10, 12, max_lines=4)
        d.text((x + 4, by + 1), src, font=F(SANS, 8.5), fill=GREY)
        if i:
            d.line([(x - 2, ly), (x - 2, ly + 210)], fill=(190, 185, 172), width=1)
    hrule(d, 528)

    # mid cards 4-14
    mids = [
        (4, "Shenzhen Outlook adopted", "APEC backs trade, data and AI text; trilateral declaration Friday. Trump returns for White House press conference."),
        (5, "Kyiv: ~20 ballistic missiles", "Bridges hit; energy and logistics targeted 04:07–06:07 UTC. Minor damage near Dutch embassy."),
        (6, "Europe–Russia talks “soon”", "Merz: new talks including Europe. Putin invites European representatives to Moscow; Kyiv at the table."),
        (7, "Gaza aid call; Israel taps Eisenkot", "Four nations demand unrestricted aid to flooded Gaza. Herzog taps ex-army chief, bypassing Netanyahu."),
        (8, "Anthropic +17% on debut", "After record $81.3bn IPO priced at $83 (18 Nov). Taiwan unveils 5 stabilizers; S. Korea exports pass $1tn."),
        (9, "Voyager 1: one light-day out", "NASA confirms the milestone. Japan’s Hayabusa2 engine trouble ends its asteroid-landing plan."),
        (10, "Nicholls 113*", "NZ 243/5, 1st Test day 1 v India, Wellington. India beat Malaysia at Hong Kong Open badminton."),
        (11, "Fiji declares disaster", "National state of disaster over El Niño drought and water shortages."),
        (12, "Yongbyon plant expanding", "IAEA/UN watchdog reports North Korea’s uranium enrichment plant is growing."),
        (13, "Genoa drones; Paris protests", "Airport shut 4h overnight (04:22 UTC). France: 4th weekend of cost-of-living protests."),
        (14, "Angola buys into De Beers", "Luanda to pay ~$180m for 10% of De Beers, Endiama CEO said Friday (Reuters). First gold refinery opens, 25 kg/day."),
    ]
    my0, cardh = 536, 48
    for idx, (num, head, deck) in enumerate(mids):
        cx = M + (idx % 3) * colw3
        cy = my0 + (idx // 3) * cardh
        badge(d, cx + 10, cy + 9, 8, num)
        hy = block(d, cx + 23, cy, head, F(SERIF_B, 14.5), INK, colw3 - 30, 17, max_lines=2)
        block(d, cx + 23, max(hy, cy + 18), deck, F(SANS, 8.8), INK, colw3 - 30, 11, max_lines=2)
    # 12th cell: navigation note
    nx, ny = M + 2 * colw3, my0 + 3 * cardh
    d.rectangle([nx + 4, ny + 2, nx + colw3 - 8, ny + cardh - 6], outline=RED, width=1)
    block(d, nx + 12, ny + 8, "Continued below: 19 more briefs, stories 15–33, plus where it all happened.",
          F(SANS_B, 9), RED, colw3 - 26, 12, max_lines=3)
    hrule(d, 734)

    # map (left) + briefs (right)
    d.text((M, 740), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=INK)
    draw_map(d, M, 756, 440, 180)
    d.text((M + 6, 920), "Positions approximate.", font=F(SANS, 8), fill=INK)

    bx = 468
    d.text((bx, 740), "ALSO ON FRIDAY 20 NOVEMBER", font=F(SANS_B, 11), fill=INK)
    briefs = [
        "15. Washington — US & Venezuela restore military cooperation (Hegseth).",
        "16. Washington — State Dept 53-p. report on $12bn Venezuelan oil revenue.",
        "17. Seoul — Top court overturns ex-PM Han Duck-soo conviction.",
        "18. Mumbai — Sensex +1.21%, Nifty +1.14% on Friday.",
        "19. Markets — Oil flat: Hormuz disruption offsets oversupply.",
        "20. Los Angeles — GTA VI sales pass $1.8bn.",
        "21. Sacramento — California AG probes Nvidia over China AI chips.",
        "22. Washington — White House cyber director ousted amid tech outages.",
        "23. Washington — US loses measles elimination status as cases surge.",
        "24. Andromeda — Astronomers capture star swallowing companion (7-year watch).",
        "25. New Delhi — Modi inaugurates FICCI centenary convention.",
        "26. New Delhi — Justice Varma: resignation is not admission of guilt.",
        "27. Kerch — Crimean Bridge rail traffic disrupted (Kyiv CLAIM).",
        "28. Antalya — COP31 final day: 194 nations chase deal; draft $120bn/yr.",
        "29. Asia — Women’s Asian Hockey Champions Trophy begins.",
        "30. Worldwide — World Children’s Day marked worldwide.",
        "31. Shenzhen — Trump warns APEC strict AI rules would stifle development.",
        "32. Shenzhen — Takaichi dodges “Taiwan contingency” question.",
        "33. Bekaa — Israel strikes Hezbollah missile facility (overnight).",
    ]
    bcolw = (W - M - bx) / 2
    for j, text in enumerate(briefs):
        col = 0 if j < 10 else 1
        row = j if j < 10 else j - 10
        x = bx + col * bcolw
        y = 758 + row * 18.5
        block(d, x + 4, y, text, F(SANS, 8.5), INK, bcolw - 10, 9.2, max_lines=2)
    d.line([(bx + bcolw, 756), (bx + bcolw, 936)], fill=(190, 185, 172), width=1)

    # date check box + sources footer
    d.rectangle([M, 948, W - M, 1002], outline=RED, width=2)
    d.text((M + 8, 952), "DATE CHECK — LEFT OUT ON PURPOSE (first reported Thu 19 Nov or earlier)",
           font=F(SANS_B, 10), fill=RED)
    left_out = ("ICJ Rohingya ruling 9–6 (19 Nov)  •  Trump–Xi–Putin meeting itself (19 Nov)  •  "
                "Anthropic IPO pricing $83 (18 Nov)  •  Denmark Greenland–US pact (19 Nov)  •  "
                "Trump pardon of Pete Rose (19 Nov)  •  APEC meeting itself (Thu — Fri = declaration only)")
    block(d, M + 8, 966, left_out, F(SANS, 8.5), INK, CW - 16, 10.5, max_lines=2)
    d.text((M + 8, 989), "Every story here happened or was first reported on Friday 20 November 2026, in some time zone. "
                         "Disputed claims are attributed, not stated as fact.",
           font=F(SANS, 8.5), fill=GREY)
    centered(d, W / 2, 1007, "Sources: Reuters, AP, AFP, BBC, The Hindu, IMD, IAEA, NASA.  Original drawings.",
             F(SANS, 9), GREY)
    img.save(OUT, "PNG")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
