#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news picture (1024x1024 PNG).

Fresh build for news-image-20261123. Everything is drawn with Pillow at
build time; the graded entrypoint (main.py) only copies entry.png.
Stories verified from CNN / WSJ / Reuters / AFP on 23 Nov 2026 (WIB).
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (246, 241, 230)
INK = (24, 24, 28)
CRIMSON = (127, 29, 29)
GOLD = (212, 160, 60)
NAVY = (16, 35, 63)
NAVY_LT = (30, 58, 95)
SLATE = (38, 48, 62)
STEEL = (52, 84, 112)
AMBER = (217, 119, 6)
ORANGE = (234, 88, 12)
WHITE = (250, 248, 243)
MUTED = (120, 116, 106)
CARD_BG = (255, 253, 247)
RULE = (196, 186, 168)


def font(name, size):
    base = "/usr/share/fonts/truetype/dejavu/"
    paths = {
        "bold": base + "DejaVuSans-Bold.ttf",
        "sans": base + "DejaVuSans.ttf",
        "serif": base + "DejaVuSerif-Bold.ttf",
    }
    return ImageFont.truetype(paths[name], size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def tag_chip(draw, xy, label, bg, fg=WHITE):
    f = font("bold", 15)
    w = int(draw.textlength(label, font=f)) + 18
    x, y = xy
    draw.rounded_rectangle([x, y, x + w, y + 24], radius=4, fill=bg)
    draw.text((x + 9, y + 4), label, font=f, fill=fg)
    return w


def masthead(draw):
    draw.rectangle([0, 0, W, 92], fill=CRIMSON)
    draw.rectangle([0, 92, W, 97], fill=GOLD)
    draw.text((14, 24), "THE WORLD IN ONE PICTURE",
              font=font("serif", 34), fill=WHITE)
    right = "MONDAY 23 NOVEMBER 2026"
    draw.text((W - 14 - draw.textlength(right, font=font("bold", 20)), 36),
              right, font=font("bold", 20), fill=GOLD)
    draw.text((14, 74), "make.fun  •  $100 USDC  •  top 50 share the pot",
              font=font("sans", 13), fill=(232, 200, 150))


def globe(draw, cx, cy, r):
    """Cracked amber globe: the planet under a failed climate deal."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 110, 138),
                 outline=(12, 40, 66), width=4)
    # land blobs
    draw.ellipse([cx - r + 18, cy - r + 26, cx - 10, cy - 6],
                 fill=(96, 150, 80))
    draw.ellipse([cx + 8, cy + 4, cx + r - 14, cy + r - 30],
                 fill=(96, 150, 80))
    draw.ellipse([cx - r + 30, cy + r - 52, cx + 6, cy + r - 12],
                 fill=(120, 160, 90))
    # cracks
    for pts in ([(cx - 60, cy - 90), (cx - 20, cy - 40), (cx - 46, cy + 10),
                 (cx - 6, cy + 60)],
                [(cx + 70, cy - 70), (cx + 30, cy - 10), (cx + 66, cy + 44),
                 (cx + 30, cy + 88)],
                [(cx - 90, cy + 20), (cx - 40, cy + 26), (cx - 66, cy + 66)]):
        draw.line(pts, fill=(20, 20, 20), width=4, joint="curve")
    # heat shimmer
    for i, yy in enumerate((cy - r - 26, cy - r - 12, cy - r + 2)):
        draw.arc([cx - 70 + i * 8, yy - 8, cx + 70 - i * 8, yy + 22],
                 start=200, end=340, fill=(240, 120, 40), width=4)


def pumpjack(draw, x, y, s, color):
    """Oil pumpjack silhouette."""
    draw.polygon([(x, y), (x + 18 * s, y - 34 * s), (x + 34 * s, y - 30 * s),
                  (x + 44 * s, y - 44 * s), (x + 60 * s, y - 40 * s),
                  (x + 60 * s, y - 30 * s), (x + 40 * s, y - 22 * s),
                  (x + 30 * s, y), ], fill=color)
    draw.line([(x + 52 * s, y - 36 * s), (x + 52 * s, y - 70 * s)],
              fill=color, width=3 * s)
    draw.line([(x + 52 * s, y - 70 * s), (x + 78 * s, y - 58 * s)],
              fill=color, width=3 * s)


def chairs(draw, x, y, n, color):
    for i in range(n):
        bx = x + i * 46
        draw.rectangle([bx, y, bx + 34, y + 26], outline=color, width=3)
        draw.rectangle([bx + 4, y - 16, bx + 30, y], outline=color, width=3)


def hero(draw):
    x0, y0, x1, y1 = 8, 104, 644, 660
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=NAVY)
    tag_chip(draw, (x0 + 16, y0 + 14), "ANTALYA  •  COP31", CRIMSON)
    draw.text((x0 + 16, y0 + 48), "COP31 COLLAPSES",
              font=font("bold", 56), fill=WHITE)
    draw.text((x0 + 16, y0 + 112),
              "No deal on fossil fuels — the longest",
              font=font("sans", 23), fill=(214, 224, 238))
    draw.text((x0 + 16, y0 + 140),
              "climate summit in history ends in failure.",
              font=font("sans", 23), fill=(214, 224, 238))
    # scene: globe centre-left, empty podium below it
    globe(draw, x0 + 160, y0 + 296, 95)
    # empty podium: no one left to gavel the deal through
    draw.polygon([(x0 + 380, y0 + 396), (x0 + 540, y0 + 396),
                  (x0 + 524, y0 + 330), (x0 + 396, y0 + 330)],
                 fill=(8, 18, 34))
    draw.rectangle([x0 + 396, y0 + 322, x0 + 524, y0 + 332], fill=(60, 75, 100))
    draw.line([(x0 + 460, y0 + 322), (x0 + 460, y0 + 296)], fill=(180, 180, 180),
              width=3)
    draw.ellipse([x0 + 452, y0 + 288, x0 + 468, y0 + 300], fill=(180, 180, 180))
    draw.text((x0 + 392, y0 + 404), "No gavel. No deal.",
              font=font("sans", 15), fill=(170, 185, 205))
    body = ("The EU, Britain and island states refused a pact that did not "
            "even mention fossil fuels. The first summit to fail since "
            "Copenhagen 2009.")
    lines = wrap(draw, body, font("sans", 17), x1 - x0 - 32)
    text_block(draw, (x0 + 16, y1 - 104), lines, font("sans", 17),
               (226, 232, 240), 23)
    draw.text((x0 + 16, y1 - 26), "CNN  •  WSJ  •  LE MONDE",
              font=font("bold", 13), fill=GOLD)


def smoke(draw, x, y, color=(150, 150, 150)):
    for dx, dy, r in ((0, 0, 11), (12, -12, 14), (24, -24, 15), (34, -36, 11)):
        draw.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r],
                     fill=color)


def mini_ship(draw, x, y, w):
    hull = [(x, y), (x + w, y), (x + w - 14, y + 26), (x + 14, y + 26)]
    draw.polygon(hull, fill=(70, 60, 52))
    for i in range(3):
        draw.rectangle([x + 16 + i * 34, y - 22, x + 44 + i * 34, y - 2],
                       fill=(150, 60, 50) if i % 2 else (60, 90, 120))
    draw.rectangle([x + w - 40, y - 40, x + w - 16, y - 22], fill=(200, 200, 200))
    smoke(draw, x + w - 34, y - 48, (140, 140, 140))


def side_card(draw, box, tag, tag_bg, headline, body, source, scene):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD_BG,
                           outline=RULE, width=1)
    tag_chip(draw, (x0 + 12, y0 + 12), tag, tag_bg)
    scene(draw, x0, y0)
    hl = wrap(draw, headline, font("bold", 25), x1 - x0 - 24)
    y = text_block(draw, (x0 + 12, y0 + 118), hl, font("bold", 25), INK, 30)
    bl = wrap(draw, body, font("sans", 16), x1 - x0 - 24)
    text_block(draw, (x0 + 12, y + 6), bl, font("sans", 16), (60, 60, 66), 21)
    draw.text((x0 + 12, y1 - 26), source, font=font("bold", 12), fill=MUTED)


def chapo_scene(draw, x0, y0):
    # prison bars + handcuffs
    for i in range(6):
        draw.rectangle([x0 + 210 + i * 22, y0 + 16, x0 + 216 + i * 22, y0 + 96],
                       fill=(90, 90, 96))
    draw.ellipse([x0 + 16, y0 + 52, x0 + 62, y0 + 98], outline=AMBER, width=6)
    draw.ellipse([x0 + 66, y0 + 52, x0 + 112, y0 + 98], outline=AMBER, width=6)
    draw.line([(x0 + 60, y0 + 74), (x0 + 68, y0 + 74)], fill=AMBER, width=6)


def bottom_card(draw, box, tag, tag_bg, headline, body, source, scene):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD_BG,
                           outline=RULE, width=1)
    tag_chip(draw, (x0 + 12, y0 + 12), tag, tag_bg)
    scene(draw, x0, y0)
    hl = wrap(draw, headline, font("bold", 22), x1 - x0 - 24)
    y = text_block(draw, (x0 + 12, y0 + 108), hl, font("bold", 22), INK, 26)
    bl = wrap(draw, body, font("sans", 15), x1 - x0 - 24)
    text_block(draw, (x0 + 12, y + 4), bl, font("sans", 15), (60, 60, 66), 20)
    draw.text((x0 + 12, y1 - 24), source, font=font("bold", 12), fill=MUTED)


def flame(draw, x, y, s):
    draw.polygon([(x, y), (x + 14 * s, y - 26 * s), (x + 8 * s, y - 12 * s),
                  (x + 26 * s, y - 40 * s), (x + 34 * s, y - 10 * s),
                  (x + 28 * s, y), ], fill=ORANGE)
    draw.polygon([(x + 8 * s, y), (x + 16 * s, y - 14 * s),
                  (x + 24 * s, y), ], fill=(250, 200, 60))


def fire_scene(draw, x0, y0):
    draw.rectangle([x0 + 210, y0 + 44, x0 + 306, y0 + 96], fill=(90, 90, 96))
    draw.polygon([(x0 + 204, y0 + 44), (x0 + 312, y0 + 44),
                  (x0 + 300, y0 + 26), (x0 + 216, y0 + 26)], fill=(60, 60, 66))
    flame(draw, x0 + 226, y0 + 26, 1)
    flame(draw, x0 + 268, y0 + 26, 1)


def drone_scene(draw, x0, y0):
    draw.rectangle([x0 + 216, y0 + 30, x0 + 252, y0 + 96], fill=(110, 110, 116))
    draw.rectangle([x0 + 258, y0 + 48, x0 + 288, y0 + 96], fill=(80, 80, 88))
    draw.ellipse([x0 + 292, y0 + 34, x0 + 306, y0 + 48], fill=(40, 40, 44))
    draw.line([(x0 + 288, y0 + 40), (x0 + 296, y0 + 40)], fill=(40, 40, 44),
              width=3)
    smoke(draw, x0 + 236, y0 + 62, (150, 150, 150))


def waves_scene(draw, x0, y0):
    for i, yy in enumerate((y0 + 58, y0 + 74, y0 + 90)):
        draw.arc([x0 + 210 + i * 6, yy - 10, x0 + 306 - i * 6, yy + 12],
                 start=180, end=360, fill=STEEL, width=4)
    draw.line([(x0 + 252, y0 + 20), (x0 + 262, y0 + 52)], fill=ORANGE, width=4)
    draw.polygon([(x0 + 262, y0 + 52), (x0 + 254, y0 + 58),
                  (x0 + 270, y0 + 58)], fill=ORANGE)


def ticker(draw):
    draw.rectangle([8, 920, 1016, 1008], fill=INK)
    draw.text((20, 930), "ALSO TODAY", font=font("bold", 16), fill=GOLD)
    items = ("Seoul minister quits over AI exam cheating  •  Nepal PM meets "
             "Modi in Delhi  •  UN keeps talking on killer robots  •  "
             "Alcaraz wins first ATP Finals crown  •  Delta glitch delays "
             "Thanksgiving flights")
    lines = wrap(draw, items, font("sans", 16), 996)
    text_block(draw, (20, 954), lines[:2], font("sans", 16), WHITE, 21)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    hero(d)
    side_card(d, (652, 104, 1016, 378), "MEXICO", SLATE,
              "FBI's most-wanted cartel boss captured",
              "El Chapo Isidro seized in a Sinaloa raid; 11 killed and a "
              "$5m reward ends a decade-long hunt.",
              "WSJ  •  CNN", chapo_scene)
    side_card(d, (652, 386, 1016, 660), "BALTIC SEA", STEEL,
              "Stricken Sparta II still smoulders",
              "Finnish, Estonian and Russian crews douse the drone-hit "
              "cargo ship; all 16 crew are safe.",
              "REUTERS", lambda dr, x, y: mini_ship(dr, x + 200, y + 78, 130))
    bottom_card(d, (8, 668, 336, 912), "INDONESIA", ORANGE,
                "24 bodies pulled from Java factory fire",
                "Dozens missing after the blaze at a Cikande candy plant; "
                "the search resumes on Monday.",
                "REUTERS", fire_scene)
    bottom_card(d, (348, 668, 676, 912), "UKRAINE", NAVY_LT,
                "14 missing after drone hits Kyiv flats",
                "A Russian drone strike on a residential building, "
                "Zelenskiy says.",
                "AFP", drone_scene)
    bottom_card(d, (688, 668, 1016, 912), "THE GULF", CRIMSON,
                "Iran–US war widens to Bahrain",
                "An Iranian strike wounds two in Bahrain; Saudi Arabia "
                "condemns the 'criminal' attacks.",
                "AFP", waves_scene)
    ticker(d)
    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
