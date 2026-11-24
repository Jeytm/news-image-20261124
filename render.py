#!/usr/bin/env python3
"""Render the news poster for Tuesday 24 November 2026.

Deterministic: fixed seed, no network, no clock. Writes entry.png
(1024x1024) in the same directory. Run: python3 render.py
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
RED = (179, 32, 44)
GOLD = (201, 162, 39)
MUTED = (90, 88, 80)
RULE = (180, 172, 150)
CARD_BG = (255, 252, 245)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
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


def para(draw, x, y, text, fnt, color, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def scene_fire(d, x, y, w, h):
    """Factory fire: dusk sky, smoking chimneys, flame, building."""
    d.rectangle([x, y, x + w, y + h], fill=(52, 44, 48))
    d.rectangle([x, y + h - 46, x + w, y + h], fill=(94, 52, 34))
    d.rectangle([x + 18, y + h - 96, x + w - 90, y + h], fill=(28, 24, 26))
    d.rectangle([x + w - 84, y + h - 128, x + w - 58, y + h], fill=(28, 24, 26))
    for i in range(4):
        wx = x + 34 + i * 34
        d.rectangle([wx, y + h - 82, wx + 18, y + h - 62], fill=(240, 170, 60))
    for cx, s in ((x + 60, 46), (x + 120, 60), (x + 190, 40)):
        d.polygon([(cx - s // 2, y + h - 46), (cx, y + h - 46 - s),
                   (cx + s // 2, y + h - 46)], fill=(232, 116, 28))
        d.polygon([(cx - s // 4, y + h - 46), (cx, y + h - 46 - s // 2),
                   (cx + s // 4, y + h - 46)], fill=(245, 196, 66))
    for cx, cy, r in ((x + 70, y + 34, 26), (x + 120, y + 18, 32),
                      (x + 175, y + 40, 24), (x + 215, y + 16, 28)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(110, 104, 102))
        d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                  fill=(140, 132, 128))


def scene_ship(d, x, y, w, h):
    """Cargo ship ablaze on a grey sea."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 205, 210))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(64, 96, 122))
    d.polygon([(x + 14, y + h - 52), (x + w - 14, y + h - 52),
               (x + w - 34, y + h - 26), (x + 34, y + h - 26)],
              fill=(40, 44, 52))
    for i, c in enumerate(((176, 62, 40), (52, 96, 130), (196, 120, 44))):
        d.rectangle([x + 34 + i * 42, y + h - 84, x + 70 + i * 42, y + h - 54],
                    fill=c)
    d.polygon([(x + w - 70, y + h - 52), (x + w - 46, y + 18),
               (x + w - 22, y + h - 52)], fill=(232, 116, 28))
    d.polygon([(x + w - 58, y + h - 52), (x + w - 46, y + 44),
               (x + w - 34, y + h - 52)], fill=(245, 196, 66))
    d.ellipse([x + w - 78, y + 2, x + w - 14, y + 34], fill=(120, 116, 112))
    for i in range(5):
        wx = x + 8 + i * 46
        d.arc([wx, y + h - 18, wx + 34, y + h + 2], 180, 360, fill=(240, 244, 246))


def scene_globe(d, x, y, w, h):
    """Divided globe: half sun, half cloud — COP31 ends split."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 222))
    cx, cy = x + w // 2, y + h // 2 + 2
    r = min(52, h // 2 - 6)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(72, 122, 158))
    d.ellipse([cx - r, cy - r, cx, cy + r], fill=(52, 92, 128))
    d.ellipse([cx - r + 8, cy - r + 12, cx - 6, cy - 2], fill=(96, 150, 96))
    d.ellipse([cx + 4, cy + 4, cx + r - 8, cy + r - 10], fill=(96, 150, 96))
    d.line([cx, cy - r, cx, cy + r], fill=(220, 230, 235))
    d.ellipse([x + w - 52, y + 8, x + w - 14, y + 46], fill=(232, 176, 44))
    d.ellipse([x + 8, y + 10, x + 52, y + 38], fill=(245, 245, 240))
    d.ellipse([x + 24, y + 4, x + 68, y + 32], fill=(245, 245, 240))


def scene_train(d, x, y, w, h):
    """New express train on rails, two flags above."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 196))
    d.line([x + 26, y + 6, x + 26, y + 30], fill=(60, 60, 60), width=3)
    d.polygon([(x + 26, y + 6), (x + 58, y + 13), (x + 26, y + 22)],
              fill=(255, 153, 51))
    d.line([x + w - 26, y + 6, x + w - 26, y + 30], fill=(60, 60, 60), width=3)
    d.polygon([(x + w - 26, y + 6), (x + w - 58, y + 13), (x + w - 26, y + 22)],
              fill=(220, 20, 60))
    top = y + 34
    bot = y + h - 22
    d.rounded_rectangle([x + 14, top, x + w - 14, bot], radius=10,
                        fill=(20, 60, 110))
    d.rounded_rectangle([x + 14, top, x + w - 14, top + 14], radius=10,
                        fill=(240, 240, 238))
    wy = top + 20
    for i in range(4):
        wx = x + 28 + i * 44
        d.rectangle([wx, wy, wx + 28, wy + 14], fill=(180, 220, 240))
    d.line([x, y + h - 12, x + w, y + h - 12], fill=(60, 60, 60), width=3)
    d.line([x, y + h - 5, x + w, y + h - 5], fill=(60, 60, 60), width=3)


def scene_sport(d, x, y, w, h):
    """Checkered flag and gold trophy."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 28))
    fx, fy, fs = x + 14, y + 10, 15
    for r in range(4):
        for c in range(6):
            col = (245, 245, 240) if (r + c) % 2 == 0 else (20, 20, 20)
            d.rectangle([fx + c * fs, fy + r * fs,
                         fx + (c + 1) * fs, fy + (r + 1) * fs], fill=col)
    d.line([fx, fy, fx, fy + 4 * fs + 22], fill=(180, 180, 180), width=3)
    tx = x + w - 88
    d.ellipse([tx, y + 22, tx + 52, y + 74], fill=(212, 175, 55))
    d.rectangle([tx + 17, y + 72, tx + 35, y + 86], fill=(212, 175, 55))
    d.rectangle([tx + 6, y + 84, tx + 46, y + 92], fill=(212, 175, 55))
    d.arc([tx - 14, y + 26, tx + 12, y + 56], 90, 270, fill=(212, 175, 55), width=5)
    d.arc([tx + 40, y + 26, tx + 66, y + 56], 270, 90, fill=(212, 175, 55), width=5)
    d.ellipse([x + 20, y + h - 30, x + 48, y + h - 4], fill=(190, 220, 60))
    d.arc([x + 20, y + h - 30, x + 48, y + h - 4], 300, 60,
          fill=(250, 250, 250), width=2)


def scene_chart(d, x, y, w, h):
    """Falling market bars with a red arrow."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 222))
    base = y + h - 12
    vals = [52, 44, 48, 36, 28, 18]
    bw = 24
    for i, v in enumerate(vals):
        bx = x + 14 + i * 36
        col = (179, 32, 44) if i >= 3 else (90, 96, 100)
        d.rectangle([bx, base - v, bx + bw, base], fill=col)
    d.text((x + 12, y + 4), "-1,484", font=font(SANS_B, 22), fill=RED)
    d.line([x + 108, base - 56, x + w - 12, base - 16], fill=(179, 32, 44), width=4)
    d.polygon([(x + w - 12, base - 16), (x + w - 32, base - 20),
               (x + w - 22, base - 2)], fill=(179, 32, 44))


def card(d, x, y, w, h, kicker, kcolor, scene, scene_h, headline, body,
         hsize=28, bsize=18):
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=CARD_BG,
                        outline=RULE, width=1)
    d.text((x + 14, y + 10), kicker, font=font(SANS_B, 17), fill=kcolor)
    sy = y + 36
    scene(d, x + 14, sy, w - 28, scene_h)
    hy = sy + scene_h + 10
    y2 = para(d, x + 14, hy, headline, font(SERIF_B, hsize), INK, w - 28,
              hsize + 5)
    para(d, x + 14, y2 + 4, body, font(SANS, bsize), (52, 50, 46), w - 28,
         bsize + 6)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---- masthead ----
    d.rectangle([M, M, W - M, M + 96], fill=NAVY)
    d.text((W // 2, M + 14), "THE WORLD IN ONE DAY",
           font=font(SERIF_B, 56), fill=(250, 248, 242), anchor="ma")
    d.text((W // 2, M + 70), "TUESDAY, 24 NOVEMBER 2026",
           font=font(SANS_B, 20), fill=(212, 175, 55), anchor="ma")
    d.line([M, M + 108, W - M, M + 108], fill=GOLD, width=3)

    # ---- lead story ----
    ly = M + 120
    lh = 276
    d.text((M, ly), "INDONESIA  •  LEAD STORY", font=font(SANS_B, 18), fill=RED)
    scene_fire(d, M, ly + 28, 420, 180)
    hx = M + 440
    hw = W - M - hx
    y = para(d, hx, ly + 24,
             "Fire at candy factory in Banten kills at least 24",
             font(SERIF_B, 40), INK, hw, 46)
    para(d, hx, y + 8,
         "Blaze sweeps through the plant east of Jakarta; around 30 workers still missing as rescuers search the ruins. It is the day's deadliest single event.",
         font(SANS, 21), (52, 50, 46), hw, 28)
    d.line([M, ly + lh - 8, W - M, ly + lh - 8], fill=RULE, width=2)

    # ---- middle row: two cards ----
    my = ly + lh + 8
    mh = 252
    cw = (W - 2 * M - 16) // 2
    card(d, M, my, cw, mh, "UKRAINE WAR", (30, 70, 120), scene_ship, 96,
         "Kyiv region hit as war grinds on",
         "Russian strike kills several in the Kyiv region. In the Baltic, cargo ship Sparta II burns in the Gulf of Finland after a drone attack.")
    card(d, M + cw + 16, my, cw, mh, "CLIMATE  •  COP31", (40, 110, 70),
         scene_globe, 96, "COP31 ends divided in Antalya",
         "Climate talks close with no agreement on stronger language to phase out fossil fuels.")
    d.line([M, my + mh + 10, W - M, my + mh + 10], fill=RULE, width=2)

    # ---- bottom row: three cards ----
    by = my + mh + 22
    bh = 252
    bw = (W - 2 * M - 32) // 3
    card(d, M, by, bw, bh, "INDIA – NEPAL", (150, 90, 20), scene_train, 92,
         "New rail link opens",
         "Modi and Nepal's PM flag off the Saryu–Kamala Express.",
         hsize=25)
    card(d, M + bw + 16, by, bw, bh, "SPORT", (120, 90, 10), scene_sport, 92,
         "Verstappen takes Vegas",
         "Verstappen wins Vegas; Alcaraz takes ATP Finals; Pant hits 128.",
         hsize=25)
    card(d, M + 2 * (bw + 16), by, bw, bh, "MARKETS", RED, scene_chart, 92,
         "Sensex slides 1,484",
         "Indian stocks fall sharply; the SpiceJet crisis deepens.",
         hsize=25)

    # ---- footer ----
    fy = by + bh + 14
    d.line([M, fy, W - M, fy], fill=GOLD, width=3)
    d.text((W // 2, fy + 10),
           "24 NOVEMBER 2026  •  THE DAY'S WORLD NEWS IN ONE IMAGE",
           font=font(SANS_B, 16), fill=MUTED, anchor="ma")

    # ---- deterministic grain to enrich the file ----
    rnd = random.Random(20261124)
    px = img.load()
    for yy in range(H):
        for xx in range(W):
            if rnd.random() < 0.15:
                n = rnd.randint(-2, 2)
                r, g, b = px[xx, yy]
                px[xx, yy] = (max(0, min(255, r + n)),
                              max(0, min(255, g + n)),
                              max(0, min(255, b + n)))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
