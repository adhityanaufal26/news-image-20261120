#!/usr/bin/env python3
"""Draw the 20 November 2026 front page (1024x1024, deterministic)."""
from PIL import Image, ImageDraw, ImageFont
import math
import os

W = H = 1024
CREAM = (250, 246, 233)
INK = (26, 26, 26)
RED = (178, 34, 34)
NAVY = (27, 42, 74)
TEAL = (14, 116, 144)
GOLD = (184, 134, 11)
GREY = (90, 90, 90)
LIGHT = (255, 255, 252)
PALE = (238, 232, 214)

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FD, "DejaVuSerif.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_O = os.path.join(FD, "DejaVuSans.ttf")


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrap(d, xy, text, font, fill, maxw, leading=1.15, max_lines=99):
    x, y = xy
    lh = int(font.size * leading)
    for ln in wrap(d, text, font, maxw)[:max_lines]:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def badge(d, x, y, n, fill=RED):
    r = 11
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=fill)
    f = F(SANS_B, 13)
    s = str(n)
    tw = d.textlength(s, font=f)
    d.text((x + r - tw / 2, y + 3), s, font=f, fill=(255, 255, 255))
    return x + 2 * r + 5


def spiral(d, cx, cy, R, col):
    pts = []
    for i in range(0, 361, 6):
        t = math.radians(i)
        r = R * i / 360.0
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    d.line(pts, fill=col, width=4)
    pts2 = [(cx + (R * i / 360.0) * math.cos(math.radians(i) + 2.2),
             cy + (R * i / 360.0) * math.sin(math.radians(i) + 2.2)) for i in range(0, 361, 6)]
    d.line(pts2, fill=col, width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=col)


def pin(d, x, y, n):
    d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=RED, outline=(255, 255, 255), width=2)
    f = F(SANS_B, 10)
    s = str(n)
    tw = d.textlength(s, font=f)
    d.text((x - tw / 2, y - 6), s, font=f, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 14
    # --- masthead ---
    d.text((M, 8), "THE DAY IN ONE PICTURE  •  WORLD NEWS FRONT PAGE", font=F(SANS_B, 11), fill=GREY)
    d.text((W - M - d.textlength("32 STORIES • 1 DAY", font=F(SANS_B, 11)), 8), "32 STORIES • 1 DAY", font=F(SANS_B, 11), fill=GREY)
    d.text((M, 24), "Friday 20 November 2026", font=F(SERIF_B, 46), fill=INK)
    d.rectangle([M, 78, W - M, 81], fill=RED)
    sub = "Cyclone Akvan hits Odisha  •  Trump defers Iran to 2027  •  Riyadh tower hit, tanker mined in Hormuz"
    d.text((M, 85), sub, font=F(SANS_B, 14), fill=RED)
    d.rectangle([M, 104, W - M, 105], fill=INK)

    # --- UTC timeline ---
    y = 110
    d.text((M, y), "FRIDAY IN UTC", font=F(SANS_B, 11), fill=NAVY)
    tl = [("01:27", "Tanker mined\nE. of Hormuz"), ("03:06", "Trump defers\nIran (Reuters)"),
          ("03:17", "Call for Gaza\naid access"), ("04:07", "Kyiv ballistic\nstrikes"),
          ("04:22", "Genoa drones\nshut airport"), ("~06:30", "Akvan landfall\n(noon IST)"),
          ("Evening", "Trump WH press\nconference")]
    tw = (W - 2 * M) / len(tl)
    for i, (t, lab) in enumerate(tl):
        x = M + i * tw
        d.ellipse([x + tw / 2 - 4, y + 18, x + tw / 2 + 4, y + 26], fill=RED)
        f = F(SANS_B, 12)
        d.text((x + tw / 2 - d.textlength(t, font=f) / 2, y + 28), t, font=f, fill=INK)
        ly = y + 44
        for ln in lab.split("\n"):
            f2 = F(SANS, 9)
            d.text((x + tw / 2 - d.textlength(ln, font=f2) / 2, ly), ln, font=f2, fill=GREY)
            ly += 11
    d.line([M, y + 22, W - M, y + 22], fill=(180, 175, 160), width=1)

    # --- region strip ---
    y = 182
    regions = [("EUROPE 7", (37, 99, 235)), ("AMERICAS 7", (220, 38, 38)), ("ASIA-PACIFIC 9", (217, 119, 6)),
               ("MIDEAST 5", (5, 150, 105)), ("AFRICA 0*", (107, 114, 128)), ("OCEANIA 2", (124, 58, 237)), ("WORLD 2", (27, 42, 74))]
    rw = (W - 2 * M) / len(regions)
    for i, (lab, col) in enumerate(regions):
        x = M + i * rw
        d.rectangle([x + 1, y, x + rw - 2, y + 18], fill=col)
        f = F(SANS_B, 10)
        d.text((x + rw / 2 - d.textlength(lab, font=f) / 2, y + 4), lab, font=f, fill=(255, 255, 255))

    # --- day in numbers ---
    y = 204
    d.text((M, y), "THE DAY IN NUMBERS", font=F(SANS_B, 11), fill=NAVY)
    nums = [("300,000", "evacuated for Akvan"), ("423", "rescue teams deployed"),
            ("51–48", "Senate vote on war powers"), ("$48.3bn", "Iran war cost so far"),
            ("113*", "Nicholls, NZ v India"), ("$1.8bn", "GTA VI sales"),
            ("5,248 pts", "Taiwan 3-day fall"), ("1 light-day", "Voyager 1 from Earth")]
    nw = (W - 2 * M) / 8
    for i, (big, lab) in enumerate(nums):
        x = M + i * nw
        d.rectangle([x + 2, y + 16, x + nw - 3, y + 52], fill=PALE, outline=(200, 192, 165))
        f = F(SANS_B, 13)
        d.text((x + nw / 2 - d.textlength(big, font=f) / 2, y + 20), big, font=f, fill=INK)
        f2 = F(SANS, 8)
        ly = y + 37
        for ln in wrap(d, lab, f2, nw - 8):
            d.text((x + nw / 2 - d.textlength(ln, font=f2) / 2, ly), ln, font=f2, fill=GREY)
            ly += 9

    # --- lead cards ---
    y0, lh = 262, 200
    cw = (W - 2 * M - 12) / 3
    leads = [
        (1, "ASIA-PACIFIC · WEATHER — ODISHA, INDIA", "Cyclone Akvan crosses the coast",
         "Severe storm lands near Gopalpur ~noon Fri. Winds 90–100 km/h, gusting 110. ~300,000 evacuated to 9,341 shelters; 423 rescue teams; 69 trains cancelled; schools shut.",
         "Source: IMD / The Hindu"),
        (2, "AMERICAS · POLITICS — WASHINGTON", "Trump defers Iran: “see after Jan 1”",
         "No rush on Iran decision; will decide in 2027 (Reuters Fri 03:06 UTC). Senate 51–48 rejects curbing war powers overnight. Pentagon: war cost past $48.3bn.",
         "Source: Reuters / AP"),
        (3, "MIDEAST · WAR — RIYADH & HORMUZ", "Riyadh tower hit; tanker mined",
         "Houthis CLAIM strikes on 4 Saudi targets; Riyadh landmark tower damaged, no injuries reported (Saudi confirms damage). Tanker mined + on fire E. of Hormuz 01:27 UTC.",
         "Source: Saudi stmt / Reuters — Houthi part = CLAIM"),
    ]
    for i, (n, kick, head, body, src) in enumerate(leads):
        x = M + i * (cw + 6)
        d.rectangle([x, y0, x + cw, y0 + lh], fill=LIGHT, outline=(170, 162, 140))
        # illustration band
        ix0, iy0, ix1, iy1 = x + 6, y0 + 6, x + cw - 6, y0 + 78
        if i == 0:
            d.rectangle([ix0, iy0, ix1, iy1], fill=(219, 234, 254))
            d.polygon([(ix0 + 120, iy1), (ix0 + 180, iy0 + 34), (ix0 + 250, iy0 + 44), (ix1, iy1)], fill=(254, 215, 170))
            spiral(d, ix0 + 62, iy0 + 36, 27, (37, 99, 235))
            for k in range(3):
                wx = ix0 + 16 + k * 30
                d.arc([wx, iy1 - 15, wx + 22, iy1 - 2], 180, 360, fill=(37, 99, 235), width=2)
            d.text((ix0 + 150, iy0 + 6), "GOPALPUR", font=F(SANS_B, 9), fill=NAVY)
            d.text((ix0 + 150, iy0 + 18), "coast →", font=F(SANS, 9), fill=GREY)
        elif i == 1:
            d.rectangle([ix0, iy0, ix1, iy1], fill=(254, 243, 199))
            for k, bh in enumerate([30, 44, 36, 52, 40, 34]):
                bx = ix0 + 150 + k * 26
                d.rectangle([bx, iy1 - bh, bx + 20, iy1], fill=(120, 113, 108))
            d.rectangle([ix0 + 8, iy0 + 8, ix0 + 78, iy0 + 62], fill=(255, 255, 255), outline=RED, width=2)
            d.text((ix0 + 16, iy0 + 12), "JAN 1", font=F(SANS_B, 16), fill=RED)
            d.text((ix0 + 16, iy0 + 32), "2027", font=F(SANS_B, 13), fill=INK)
            d.text((ix0 + 16, iy0 + 48), "we'll see", font=F(SANS_O, 10), fill=GREY)
        else:
            d.rectangle([ix0, iy0, ix1, iy1], fill=(255, 237, 213))
            d.polygon([(ix0 + 60, iy1), (ix0 + 78, iy0 + 10), (ix0 + 96, iy1)], fill=(120, 113, 108))
            d.polygon([(ix0 + 110, iy1), (ix0 + 126, iy0 + 20), (ix0 + 142, iy1)], fill=(87, 83, 78))
            for k in range(4):
                sx = ix0 + 72 + k * 8
                d.ellipse([sx, iy0 + 2 + k * 4, sx + 14, iy0 + 14 + k * 4], outline=(90, 90, 90))
            pts = [(ix0 + 200 + j * 14, iy1 - 40 + int(18 * math.sin(j / 3.0))) for j in range(7)]
            d.line(pts, fill=RED, width=3)
            d.polygon([pts[-1], (pts[-1][0] - 12, pts[-1][1] - 5), (pts[-1][0] - 10, pts[-1][1] + 6)], fill=RED)
            d.rectangle([ix0 + 190, iy1 - 12, ix0 + 280, iy1 - 4], fill=(27, 42, 74))
        yy = y0 + 84
        nx = badge(d, x + 8, yy, n)
        d.text((nx, yy + 3), kick, font=F(SANS_B, 8), fill=TEAL)
        yy += 26
        yy = draw_wrap(d, (x + 8, yy), head, F(SANS_B, 15), INK, cw - 16, 1.12, 2)
        yy += 2
        yy = draw_wrap(d, (x + 8, yy), body, F(SANS, 10), INK, cw - 16, 1.18, 5)
        d.text((x + 8, y0 + lh - 16), src, font=F(SANS_O, 8), fill=GREY)

    # --- mid cards 4-13 ---
    y0 = 468
    mids = [
        (4, "Shenzhen Outlook adopted", "APEC backs trade/data/AI text; trilateral declaration Fri. Trump back for WH press conf."),
        (5, "Kyiv: ~20 ballistic missiles", "Bridges hit; energy + logistics targeted 04:07–06:07 UTC. Minor damage near Dutch embassy."),
        (6, "Europe–Russia talks “soon”", "Merz: new talks incl. Europe. Putin invites European reps to Moscow; Kyiv at table."),
        (7, "Gaza aid call; Israel taps Eisenkot", "4 nations demand unrestricted aid to flooded Gaza. Herzog taps ex-army chief, bypassing Netanyahu."),
        (8, "Anthropic +17% on debut", "After record $81.3bn IPO at $83. Taiwan unveils 5 stabilisers; S. Korea exports pass $1tn."),
        (9, "Voyager 1: one light-day out", "NASA confirms milestone. Japan's Hayabusa2 engine trouble ends asteroid-landing plan."),
        (10, "Nicholls 113* — NZ 243/5", "1st Test day 1 v India, Wellington. India beat Malaysia at Hong Kong Open badminton."),
        (11, "Fiji declares disaster", "National state of disaster over El Niño drought + water shortages."),
        (12, "Yongbyon plant expanding", "IAEA/UN watchdog reports N. Korea uranium enrichment plant growing."),
        (13, "Genoa drones; Paris protests", "Airport shut 4h overnight (04:22 UTC). France: 4th weekend of cost-of-living protests."),
    ]
    mw = (W - 2 * M - 16) / 5
    mh = 74
    for i, (n, head, body) in enumerate(mids):
        col, row = i % 5, i // 5
        x = M + col * (mw + 4)
        y = y0 + row * (mh + 4)
        d.rectangle([x, y, x + mw, y + mh], fill=LIGHT, outline=(170, 162, 140))
        nx = badge(d, x + 5, y + 5, n, fill=NAVY)
        yy = draw_wrap(d, (x + 5, y + 29), head, F(SANS_B, 10), INK, mw - 10, 1.1, 2)
        draw_wrap(d, (x + 5, yy + 1), body, F(SANS, 8), (55, 55, 55), mw - 10, 1.15, 4)

    # --- map ---
    y0 = 624
    d.text((M, y0), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=NAVY)
    d.text((W - M - d.textlength("Positions approximate.", font=F(SANS_O, 9)), y0 + 2), "Positions approximate.", font=F(SANS_O, 9), fill=GREY)
    mx0, my0, mx1, my1 = M, y0 + 17, W - M, y0 + 125
    d.rectangle([mx0, my0, mx1, my1], fill=(219, 234, 254), outline=(150, 170, 200))
    MWd, MHd = mx1 - mx0, my1 - my0

    def P(lon, lat):
        return (mx0 + (lon + 180) / 360.0 * MWd, my0 + (75 - lat) / 125.0 * MHd)

    land = (245, 222, 179)
    edge = (146, 120, 70)
    na = [P(-165, 68), P(-140, 70), P(-125, 72), P(-110, 68), P(-95, 70), P(-85, 66), P(-80, 62), P(-78, 58), P(-70, 45), P(-70, 42), P(-74, 39), P(-76, 35), P(-80, 32), P(-81, 26), P(-84, 30), P(-89, 30), P(-94, 29), P(-97, 26), P(-97, 22), P(-95, 18), P(-90, 15), P(-83, 9), P(-79, 9), P(-83, 15), P(-88, 16), P(-92, 15), P(-97, 16), P(-102, 18), P(-105, 20), P(-110, 23), P(-114, 29), P(-117, 33), P(-122, 37), P(-124, 43), P(-124, 48), P(-130, 55), P(-145, 60), P(-158, 58), P(-165, 60)]
    sa = [P(-79, 9), P(-75, 11), P(-71, 12), P(-64, 10), P(-58, 8), P(-52, 5), P(-50, 0), P(-44, -2), P(-37, -5), P(-35, -8), P(-37, -12), P(-39, -16), P(-41, -22), P(-46, -25), P(-50, -29), P(-53, -33), P(-57, -36), P(-58, -39), P(-62, -40), P(-63, -43), P(-65, -46), P(-67, -49), P(-68, -52), P(-68, -54), P(-70, -54), P(-72, -51), P(-74, -48), P(-74, -44), P(-73, -40), P(-72, -35), P(-71, -30), P(-70, -24), P(-70, -19), P(-73, -16), P(-76, -14), P(-78, -9), P(-80, -4), P(-80, 1), P(-77, 4), P(-77, 7)]
    eu = [P(-9, 43), P(-9, 37), P(-2, 37), P(3, 42), P(7, 44), P(10, 44), P(12, 46), P(14, 45), P(19, 42), P(23, 40), P(23, 37), P(26, 38), P(27, 37), P(30, 36), P(36, 36), P(36, 41), P(30, 41), P(28, 41), P(23, 40), P(19, 42), P(14, 45), P(10, 44), P(8, 44), P(3, 43), P(-1, 44), P(-2, 49), P(0, 51), P(5, 53), P(8, 55), P(8, 57), P(10, 59), P(5, 59), P(5, 61), P(10, 64), P(14, 67), P(18, 69), P(25, 71), P(31, 70), P(40, 68), P(45, 68), P(50, 69), P(60, 69), P(40, 65), P(30, 60), P(28, 55), P(24, 58), P(21, 55), P(18, 56), P(12, 54), P(8, 54), P(3, 51), P(-1, 50), P(-4, 48), P(-2, 44)]
    af = [P(-6, 35), P(-2, 35), P(10, 37), P(11, 34), P(20, 32), P(30, 31), P(32, 31), P(34, 28), P(35, 24), P(37, 22), P(38, 20), P(40, 15), P(43, 12), P(48, 11), P(51, 12), P(51, 10), P(48, 5), P(42, -1), P(40, -6), P(39, -10), P(40, -15), P(36, -20), P(33, -26), P(31, -29), P(28, -33), P(25, -34), P(20, -35), P(17, -32), P(15, -27), P(12, -18), P(13, -12), P(12, -6), P(9, -1), P(9, 4), P(4, 6), P(-2, 5), P(-8, 5), P(-13, 8), P(-17, 12), P(-17, 15), P(-16, 20), P(-15, 25), P(-13, 28), P(-10, 31), P(-6, 35)]
    asia = [P(36, 36), P(36, 41), P(40, 43), P(48, 42), P(50, 44), P(50, 47), P(48, 50), P(52, 52), P(55, 51), P(58, 51), P(60, 52), P(65, 50), P(70, 50), P(75, 50), P(80, 50), P(85, 50), P(90, 50), P(95, 50), P(100, 50), P(105, 50), P(110, 50), P(115, 50), P(120, 50), P(125, 50), P(130, 50), P(135, 48), P(140, 50), P(142, 52), P(145, 55), P(150, 60), P(155, 62), P(160, 65), P(165, 68), P(170, 68), P(175, 68), P(178, 66), P(178, 64), P(170, 66), P(160, 60), P(156, 52), P(150, 45), P(145, 40), P(142, 35), P(140, 36), P(135, 34), P(130, 32), P(122, 31), P(120, 26), P(115, 23), P(110, 20), P(108, 15), P(106, 9), P(103, 5), P(100, 6), P(98, 10), P(97, 15), P(92, 16), P(91, 22), P(89, 22), P(86, 20), P(82, 16), P(80, 13), P(77, 8), P(73, 16), P(72, 20), P(70, 22), P(66, 25), P(61, 25), P(57, 26), P(52, 26), P(50, 29), P(48, 30), P(50, 26), P(52, 24), P(55, 24), P(58, 23), P(59, 22), P(55, 17), P(48, 14), P(43, 12), P(42, 15), P(39, 21), P(35, 28), P(34, 31), P(36, 36)]
    aus = [P(113, -22), P(114, -28), P(115, -34), P(118, -35), P(124, -33), P(130, -32), P(133, -32), P(136, -35), P(138, -35), P(140, -38), P(145, -38), P(150, -37), P(153, -30), P(153, -27), P(151, -24), P(149, -20), P(146, -19), P(145, -15), P(142, -11), P(142, -17), P(141, -17), P(140, -18), P(136, -15), P(135, -12), P(132, -11), P(130, -12), P(126, -14), P(122, -17), P(118, -20), P(113, -22)]
    for poly in [na, sa, eu, af, asia, aus]:
        d.polygon(poly, fill=land, outline=edge)
    pins = [(1, 85.3, 19.4), (2, -77.0, 38.9), (3, 46.7, 24.6), (4, 114.0, 22.5), (5, 30.5, 50.4),
            (6, 13.4, 52.5), (7, 34.3, 31.4), (8, -122.4, 37.8), (9, 130.0, 31.0), (10, 174.8, -41.3),
            (11, 178.0, -17.7), (12, 125.8, 39.8), (13, 8.9, 44.4)]
    for n, lon, lat in pins:
        x, y = P(lon, lat)
        pin(d, x, y, n)

    # --- briefs ---
    y0 = 754
    d.text((M, y0), "ALSO ON FRIDAY 20 NOVEMBER", font=F(SANS_B, 12), fill=NAVY)
    briefs = [
        "Washington — US & Venezuela restore military cooperation (Hegseth).",
        "Washington — State Dept 53-p. report on $12bn Venezuelan oil revenue.",
        "Seoul — Top court overturns ex-PM Han Duck-soo conviction.",
        "Mumbai — Sensex +1.21%, Nifty +1.14% on Friday.",
        "Markets — Oil flat: Hormuz disruption offsets oversupply.",
        "Los Angeles — GTA VI sales pass $1.8bn.",
        "Sacramento — California AG probes Nvidia over China AI chips.",
        "Washington — White House cyber director ousted amid tech outages.",
        "Washington — US loses measles elimination status as cases surge.",
        "Andromeda — Astronomers capture star swallowing companion (7-year watch).",
        "New Delhi — Modi inaugurates FICCI centenary convention.",
        "New Delhi — Justice Varma: resignation is not admission of guilt.",
        "Kerch — Crimean Bridge rail traffic disrupted (Kyiv CLAIM).",
        "Antalya — COP31 final day: 194 nations chase deal; draft $120bn/yr.",
        "Asia — Women's Asian Hockey Champions Trophy begins.",
        "Worldwide — World Children's Day marked worldwide.",
        "Shenzhen — Trump warns APEC strict AI rules would stifle development.",
        "Shenzhen — Takaichi dodges “Taiwan contingency” question.",
        "Bekaa — Israel strikes Hezbollah missile facility (overnight).",
    ]
    colw = (W - 2 * M - 12) / 2
    f = F(SANS, 9)
    for i, b in enumerate(briefs):
        col, row = i // 10, i % 10
        x = M + col * (colw + 12)
        y = y0 + 16 + row * 11
        d.text((x, y), f"{14 + i}.", font=F(SANS_B, 9), fill=RED)
        d.text((x + 26, y), b, font=f, fill=INK)

    # --- date check + footer ---
    y0 = 886
    d.rectangle([M, y0, W - M, y0 + 92], outline=RED, width=2)
    d.text((M + 8, y0 + 5), "DATE CHECK — LEFT OUT ON PURPOSE (first reported Thu 19 Nov or earlier)", font=F(SANS_B, 10), fill=RED)
    lines = [
        "ICJ Rohingya ruling 9–6 (19 Nov)  •  Trump–Xi–Putin meeting itself (19 Nov)  •  Anthropic IPO pricing $83 (18 Nov)",
        "Denmark Greenland–US pact (19 Nov)  •  Trump pardon of Pete Rose (19 Nov)  •  APEC meeting itself (Thu — Fri = declaration only)",
        "Every story here happened or was first reported on Friday 20 November 2026, in some time zone. Disputed claims are attributed, not stated as fact.",
    ]
    yy = y0 + 22
    for ln in lines:
        d.text((M + 8, yy), ln, font=F(SANS, 9), fill=INK)
        yy += 13
    d.text((M, 996), "Sources: Reuters, AP, AFP, BBC, The Hindu, IMD, IAEA, NASA. Original drawings.  •  *Africa: no qualifying Friday story in this selection.",
           font=F(SANS_O, 9), fill=GREY)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print(out, os.path.getsize(out))


if __name__ == "__main__":
    main()
