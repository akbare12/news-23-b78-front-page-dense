#!/usr/bin/env python3
"""news-23 b78 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
Deterministic PIL render, 1024x1024, entry.png next to this file."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FD, "DejaVuSerif.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, font, fill, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def chip(d, x, y, label, color):
    # small rounded chip, returns width used
    font = f(SANS_B, 8)
    w = int(d.textlength(label, font=font)) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=color)
    d.text((x + w / 2, y + 6.5), label, font=font, fill="white", anchor="mm")
    return w


def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 52], fill="black")
    text(d, (12, 26), "THE WORLD TODAY", f(SERIF_B, 40), "white", "lm")
    text(d, (W - 12, 27), "MONDAY 23 NOVEMBER 2026", f(SANS_B, 16), "#e8b93b", "rm")

    # ---------- kicker ----------
    d.rectangle([0, 52, W, 74], fill="#a3121f")
    text(d, (W // 2, 63), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
         f(SANS_B, 15), "white", "mm")

    # ---------- number strip: 2 rows x 5 ----------
    strip = [
        [("-3.3%", "KOSPI", "#c8102e"), ("5.3", "US-CHINA POWER GAP", "#1f4e9c"),
         ("11,762", "EBOLA CASES, DRC", "#1e7a34"), ("10T won", "SEOUL STABILISATION FUND", "#8a6d00"),
         ("2%", "BILLIONAIRE TAX IN PARIS", "#7a3fa0")],
        [("$450M", "SKUBAL DEAL", "#1f4e9c"), ("165", "RUSSIAN MISSILES/WEEK", "#c8102e"),
         ("12,000", "CLEARED IN MANCHESTER", "#1e7a34"), ("264 kg", "EXPLOSIVES SEIZED", "#8a6d00"),
         ("$107.3B", "ANTHROPIC IPO", "#7a3fa0")],
    ]
    col_w = W // 5
    for r, row in enumerate(strip):
        y0 = 74 + r * 28
        for c, (val, lab, col) in enumerate(row):
            x = c * col_w + 10
            text(d, (x, y0 + 1), val, f(SANS_B, 18), col)
            text(d, (x, y0 + 19), lab, f(SANS, 8), "#555555")

    # ---------- region bar ----------
    regions = [("ASIA-PACIFIC 7", "#1f4e9c", 165), ("AMERICAS 8", "#a3121f", 165),
               ("MIDDLE EAST 6", "#b8860b", 165), ("EUROPE 5", "#0f7a6e", 165),
               ("AFRICA 3", "#5b2d8e", 165), ("WORLD 2", "#333333", 199)]
    x = 0
    for name, col, w in regions:
        d.rectangle([x, 132, x + w, 152], fill=col)
        text(d, (x + 8, 142), name, f(SANS_B, 11), "white", "lm")
        x += w

    # ---------- UTC strip ----------
    text(d, (10, 160), "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
         f(SANS, 10), "#444444")
    text(d, (W - 10, 160), "~ APPROX", f(SANS, 10), "#888888", "ra")

    # ---------- heroes ----------
    hy = 168
    hw = 332
    gap = 14
    heroes = [
        ("KOSPI 4,708.54  \u00b7  -161 PTS", "AI ROUT HITS ASIA",
         "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
         "KOREA EXCHANGE"),
        ("UN  \u00b7  BRIDGETOWN", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
         "UNITED NATIONS"),
        ("ASIA POWER INDEX 2026", "US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
         "LOWY INSTITUTE"),
    ]
    for i, (src, head, body, srcname) in enumerate(heroes):
        x0 = 10 + i * (hw + gap)
        x1 = x0 + hw
        # scene
        if i == 0:
            d.rectangle([x0, hy, x1, hy + 112], fill="#0d1b3e")
            # lit buildings
            import random
            rnd = random.Random(78)
            bx = x0 + 8
            while bx < x1 - 30:
                bw = rnd.randint(18, 30)
                bh = rnd.randint(30, 60)
                d.rectangle([bx, hy + 112 - bh, bx + bw, hy + 112], fill="#16294f")
                for wy in range(hy + 112 - bh + 6, hy + 106, 9):
                    for wx in range(bx + 4, bx + bw - 3, 7):
                        if rnd.random() < 0.55:
                            d.rectangle([wx, wy, wx + 3, wy + 4], fill="#ffd94a")
                bx += bw + 4
            # orange chart line (kept in lower half, clear of the -3.3% label)
            pts = [(x0 + 12, hy + 82), (x0 + 60, hy + 72), (x0 + 110, hy + 80),
                   (x0 + 160, hy + 62), (x0 + 210, hy + 68), (x0 + 260, hy + 54),
                   (x0 + 310, hy + 60)]
            d.line(pts, fill="#ff7a1a", width=3)
            for px, py in pts:
                d.ellipse([px - 3, py - 3, px + 3, py + 3], fill="white", outline="#ff7a1a")
            text(d, (x0 + 10, hy + 6), "-3.3%", f(SANS_B, 24), "#ff4d4d")
        elif i == 1:
            d.rectangle([x0, hy, x1, hy + 112], fill="#0f6a5c")
            lines = wrap(d, "150 DELEGATES BACK A RISK FRAMEWORK", f(SANS_B, 21), 200)
            yy = hy + 14
            for ln in lines:
                text(d, (x0 + 10, yy), ln, f(SANS_B, 21), "#ffd94a")
                yy += 24
            # globe
            cx, cy, r = x1 - 52, hy + 56, 36
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#bfe8df", outline="white", width=2)
            d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline="#0f6a5c", width=1)
            d.line([cx - r, cy, cx + r, cy], fill="#0f6a5c", width=1)
            d.line([cx - r + 8, cy - r // 2, cx + r - 8, cy - r // 2], fill="#0f6a5c", width=1)
            d.line([cx - r + 8, cy + r // 2, cx + r - 8, cy + r // 2], fill="#0f6a5c", width=1)
        else:
            d.rectangle([x0, hy, x1, hy + 112], fill="#f7f1dd")
            text(d, (x0 + 10, hy + 6), "NARROWEST SINCE 2018", f(SANS_B, 10), "#555555")
            text(d, (x1 - 10, hy + 6), "GAP 5.3", f(SANS_B, 10), "#c8102e", "ra")
            bars = [("78.9", "US", "#1f3a6e", 62, "white"), ("73.6", "CHINA", "#c8102e", 58, "white"),
                    ("40.5", "INDIA", "#c9a227", 32, "black")]
            bw_, bar_top, bar_bot = 62, hy + 42, hy + 104
            bx = x0 + 34
            for val, lab, col, hgt, labcol in bars:
                text(d, (bx + bw_ // 2, bar_top - 20), val, f(SANS_B, 16), "black", "ma")
                d.rectangle([bx, bar_bot - hgt, bx + bw_, bar_bot], fill=col)
                text(d, (bx + bw_ // 2, bar_bot - 13), lab, f(SANS_B, 10), labcol, "ma")
                bx += bw_ + 34
        # source strip under scene
        d.rectangle([x0, hy + 112, x1, hy + 126], fill="black")
        text(d, (x0 + 8, hy + 119), src, f(SANS_B, 10), "white", "lm")
        # headline (2 lines max, serif bold)
        hl = wrap(d, head, f(SERIF_B, 19), hw - 8)
        yy = hy + 134
        for ln in hl[:2]:
            text(d, (x0 + 2, yy), ln, f(SERIF_B, 19), "black")
            yy += 23
        # body (2 lines)
        bl = wrap(d, body, f(SANS, 11), hw - 8)
        yy = hy + 182
        for ln in bl[:2]:
            text(d, (x0 + 2, yy), ln, f(SANS, 11), "#222222")
            yy += 14
        # chip row on its own line
        text(d, (x0 + 2, hy + 212), srcname, f(SANS, 9), "#666666")
        chip(d, x1 - 62, hy + 208, "REPORTED", "#1f4e9c")

    # ---------- MORE OF THE DAY bar ----------
    d.rectangle([0, 402, W, 420], fill="black")
    text(d, (10, 411), "MORE OF THE DAY  \u2014  10 STORIES", f(SANS_B, 13), "white", "lm")

    # ---------- cards: 2 rows x 5 ----------
    cards = [
        ("AMERICAS", "#1f4e9c", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED", "#1f4e9c"),
        ("FBI", "#27408b", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", "#1f4e9c"),
        ("WHITE HOUSE", "#8a6d00", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", "#1f4e9c"),
        ("MARKETS", "#0f7a6e", "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED", "#1f4e9c"),
        ("SPORT", "#a3121f", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", "#1f4e9c"),
        ("SPORT", "#a3121f", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED", "#1f4e9c"),
        ("LEGAL", "#5b2d8e", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED", "#1f4e9c"),
        ("TECH", "#1f4e9c", "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED", "#1f4e9c"),
        ("EUROPE", "#0f7a6e", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM", "#c8102e"),
        ("SPACE", "#5b2d8e", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", "#c8102e"),
    ]
    cw = 198
    for idx, (cat, catcol, head, body, src, chip_lab, chip_col) in enumerate(cards):
        r, c = divmod(idx, 5)
        x0 = 10 + c * (cw + 6)
        y0 = 426 + r * 88
        d.rectangle([x0, y0, x0 + cw, y0 + 14], fill=catcol)
        text(d, (x0 + 6, y0 + 7), cat, f(SANS_B, 9), "white", "lm")
        text(d, (x0 + cw - 4, y0 + 7), str(idx + 1), f(SANS_B, 9), "white", "rm")
        hl = wrap(d, head, f(SANS_B, 12), cw - 6)
        yy = y0 + 18
        for ln in hl[:2]:
            text(d, (x0 + 2, yy), ln, f(SANS_B, 12), "black")
            yy += 15
        text(d, (x0 + 2, y0 + 52), body, f(SANS, 10), "#333333")
        text(d, (x0 + 2, y0 + 72), src, f(SANS, 9), "#666666")
        chip(d, x0 + cw - 62, y0 + 68, chip_lab, chip_col)

    # ---------- map + ALSO ----------
    my = 602
    d.rectangle([0, my, W, my + 18], fill="black")
    text(d, (10, my + 9), "WHERE IT HAPPENED", f(SANS_B, 12), "white", "lm")
    text(d, (352, my + 9), "ALSO ON MONDAY", f(SANS_B, 12), "white", "lm")
    map_x0, map_y0, map_x1, map_y1 = 10, my + 24, 340, 884
    d.rectangle([map_x0, map_y0, map_x1, map_y1], outline="black", width=1)
    # stylised land blobs (light green)
    d.polygon([(22, 650), (60, 638), (110, 640), (128, 668), (120, 720), (96, 780),
               (70, 800), (44, 770), (28, 720), (18, 680)], fill="#cfe8c0")
    d.polygon([(160, 640), (220, 632), (290, 636), (330, 652), (322, 700), (280, 716),
               (220, 712), (180, 690), (158, 664)], fill="#cfe8c0")
    d.polygon([(196, 730), (250, 726), (272, 750), (258, 800), (224, 828), (198, 792),
               (188, 758)], fill="#cfe8c0")
    d.ellipse([292, 836, 332, 862], fill="#cfe8c0")
    pins = [(300, 662, "1"), (95, 798, "2"), (315, 648, "3"), (105, 698, "4"),
            (116, 678, "5"), (246, 660, "6"), (90, 720, "7"), (54, 736, "8"),
            (74, 760, "9"), (84, 784, "10"), (230, 648, "11"), (210, 640, "12"),
            (266, 644, "13")]
    for px, py, num in pins:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill="#c8102e", outline="white", width=1)
        d.text((px, py), num, font=f(SANS_B, 8), fill="white", anchor="mm")
    text(d, (16, 838), "Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", f(SANS, 9), "black")
    text(d, (16, 849), "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF", f(SANS, 9), "black")
    text(d, (16, 860), "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow", f(SANS, 9), "black")

    also = [
        "Paris: 100+ back 2% billionaire tax", "Manchester: 12,000 cleared",
        "Zelenskyy: 165 missiles in a week", "COP31: the day after pact rejected",
        "Benghazi: UN demands port probe [CLAIM]", "Israel unity talks resume",
        "Gaza: two killed in Israeli strike", "West Bank settler attacks",
        "Iran war: no deal in sight", "Lebanon seizes 264 kg explosives",
        "Bahrain: strike hits plant, 2 hurt", "Sudan: defences down drones [CLAIM]",
        "DRC: fighting traps Ebola teams", "Bangladesh: Hasina jailed if she returns",
        "Seoul minister quits in exam row", "SK Telecom -7.3% as hype cools",
        "China eases margin rules", "Seoul readies 10T-won fund",
    ]
    yy = map_y0 + 6
    for i, item in enumerate(also):
        num = 14 + i
        col = "#c8102e" if "[CLAIM]" in item else "black"
        item = item.replace(" [CLAIM]", "")
        text(d, (352, yy), f"{num}. {item}", f(SANS, 12), "black")
        if col != "black":
            w = d.textlength(f"{num}. {item}", font=f(SANS, 12))
            text(d, (352 + w + 4, yy), "[CLAIM]", f(SANS_B, 10), "#c8102e")
        yy += 14

    # ---------- DATE CHECK ----------
    dy = 892
    d.rectangle([10, dy, W - 10, dy + 56], outline="#c8102e", width=2)
    text(d, (18, dy + 8), "DATE CHECK", f(SANS_B, 13), "#c8102e")
    text(d, (W - 18, dy + 8), "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY",
         f(SANS_B, 9), "#c8102e", "ra")
    text(d, (18, dy + 26), "LEFT OUT \u2014 NOT 23 NOV: Dems 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo (22 Nov) \u00b7 EU\u2013Indonesia (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar (19 Nov)",
         f(SANS, 10), "black")
    text(d, (18, dy + 42), "NOT YET \u2014 Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
         f(SANS, 10), "black")

    # ---------- footer ----------
    d.rectangle([0, 956, W, H], fill="black")
    text(d, (10, 962), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
         f(SANS, 10), "#cccccc")
    text(d, (10, 977), "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.",
         f(SANS, 10), "#cccccc")
    text(d, (10, 991), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
         f(SANS, 10), "#cccccc")
    text(d, (W // 2, 1014), "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
         f(SANS_B, 11), "#e8b93b", "mm")

    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
