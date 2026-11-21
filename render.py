#!/usr/bin/env python3
"""Render the news-image-20261121 front page: 40 stories from Saturday 21 Nov 2026.

Classic newspaper grammar: cream serif masthead, stat strip under the masthead,
region bar, 3 large hero scenes, 10 vignettes in two rows of 5, dotted world map
with numbered pins at the bottom, numbered briefs 14-40, date-check footer.
Everything is drawn with PIL primitives; no external assets, no network, no
randomness, so the output bytes are identical on every run.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MX = 22                      # side margin
CW = W - 2 * MX              # content width: 980

CREAM = (246, 240, 224)
INK = (22, 35, 63)
RED = (166, 28, 28)
RED_DK = (140, 20, 20)
GREY = (107, 107, 96)
LINE = (180, 172, 150)
NAVY_SKY = (14, 26, 51)
GOLD = (212, 175, 55)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FD, name), size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
try:
    SERIF_I = font("DejaVuSerif-Italic.ttf", 16)
except OSError:
    SERIF_I = font("DejaVuSerif.ttf", 16)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in s.split(" "):
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, s, f, max_w, fill, leading=None):
    lines = wrap(draw, s, f, max_w)
    lh = leading or int(f.size * 1.22)
    for i, ln in enumerate(lines):
        draw.text((x, y + i * lh), ln, font=f, fill=fill)
    return y + len(lines) * lh


def starburst(draw, cx, cy, r, color, spikes=12):
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)


def dotted_arc(draw, p0, p1, p2, color, step=0.06, r=2):
    """Dotted quadratic bezier from p0 via control p1 to p2."""
    t = 0.0
    while t <= 1.0:
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
        t += step


def skyline(draw, x0, y_base, widths, heights, win_c=(255, 215, 94)):
    """Dark buildings with lit windows; widths/heights are fixed lists."""
    x = x0
    for w, h in zip(widths, heights):
        draw.rectangle([x, y_base - h, x + w, y_base], fill=(8, 14, 28))
        for wy in range(y_base - h + 6, y_base - 4, 11):
            for wx in range(x + 4, x + w - 4, 10):
                if (wx * 7 + wy * 13) % 5 < 3:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=win_c)
        x += w + 3


def badge(draw, x, y, n, r=11):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=1)
    f = SANS_B(13 if n < 10 else 11)
    tw = text_w(draw, str(n), f)
    draw.text((x - tw / 2, y - f.size / 2 - 1), str(n), font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- scenes: heroes
def scene_cop31(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(207, 232, 216))
    # globe
    gx, gy, gr = x + 82, y + 62, 46
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(59, 123, 191))
    draw.ellipse([gx - 30, gy - 28, gx - 2, gy - 2], fill=(96, 176, 96))
    draw.ellipse([gx + 4, gy + 6, gx + 30, gy + 30], fill=(96, 176, 96))
    draw.ellipse([gx - 12, gy + 18, gx + 12, gy + 34], fill=(96, 176, 96))
    draw.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 340, fill=(255, 255, 255), width=1)
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(255, 255, 255), width=1)
    # thermometer
    tx = x + 252
    draw.rectangle([tx - 7, y + 14, tx + 7, y + 88], fill=(255, 255, 255), outline=(120, 120, 120))
    draw.rectangle([tx - 4, y + 46, tx + 4, y + 88], fill=(200, 30, 30))
    draw.ellipse([tx - 13, y + 84, tx + 13, y + 110], fill=(200, 30, 30))
    draw.ellipse([tx - 13, y + 84, tx + 13, y + 110], outline=(120, 120, 120))
    # tags
    draw.rectangle([x + 196, y + 6, x + 314, y + 22], fill=RED)
    f = SANS_B(9)
    draw.text((x + 202, y + 8), "1.5°C LIMIT PASSED", font=f, fill=(255, 255, 255))
    draw.rectangle([x + 8, y + 104, x + 158, y + 122], fill=(255, 255, 255))
    draw.text((x + 14, y + 107), "3RD DRAFT DUE SAT AM", font=SANS_B(9), fill=INK)


def scene_kyiv(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY_SKY)
    for sx, sy in [(30, 14), (90, 8), (150, 18), (230, 10), (290, 20), (60, 26), (180, 6)]:
        draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(255, 255, 255))
    draw.ellipse([x + 278, y + 12, x + 302, y + 36], fill=(238, 232, 200))
    dotted_arc(draw, (x + 20, y + 118), (x + 90, y + 30), (x + 150, y + 52),
               (255, 140, 26), step=0.05)
    dotted_arc(draw, (x + 300, y + 118), (x + 240, y + 40), (x + 190, y + 66),
               (255, 140, 26), step=0.05)
    starburst(draw, x + 150, y + 52, 17, (255, 140, 26))
    starburst(draw, x + 150, y + 52, 8, (255, 215, 94))
    starburst(draw, x + 190, y + 66, 12, (255, 140, 26))
    starburst(draw, x + 190, y + 66, 6, (255, 215, 94))
    skyline(draw, x + 6, y + h, [34, 26, 44, 30, 38, 28, 40, 26],
            [58, 74, 50, 80, 62, 70, 54, 66])


def scene_riyadh(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(16, 30, 58))
    for sx, sy in [(40, 12), (120, 8), (200, 16), (260, 10), (80, 22), (170, 6)]:
        draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(255, 255, 255))
    draw.ellipse([x + 282, y + 10, x + 304, y + 32], fill=(238, 232, 200))
    draw.ellipse([x + 288, y + 8, x + 306, y + 28], fill=(16, 30, 58))
    # gold towers
    draw.rectangle([x + 14, y + 62, x + 44, y + h], fill=(176, 141, 79))
    draw.polygon([(x + 60, y + h), (x + 60, y + 40), (x + 74, y + 22),
                  (x + 88, y + 40), (x + 88, y + h)], fill=(201, 164, 92))
    draw.rectangle([x + 100, y + 74, x + 138, y + h], fill=(176, 141, 79))
    draw.rectangle([x + 150, y + 52, x + 186, y + h], fill=(201, 164, 92))
    draw.rectangle([x + 198, y + 80, x + 232, y + h], fill=(176, 141, 79))
    draw.rectangle([x + 244, y + 66, x + 282, y + h], fill=(201, 164, 92))
    for wx in range(x + 20, x + 276, 12):
        for wy in range(y + 70, y + h - 6, 12):
            if (wx * 5 + wy * 11) % 7 < 3:
                draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 215, 94))
    dotted_arc(draw, (x + 40, y + 126), (x + 110, y + 30), (x + 165, y + 48),
               (255, 140, 26), step=0.045)
    dotted_arc(draw, (x + 290, y + 126), (x + 220, y + 34), (x + 175, y + 52),
               (255, 140, 26), step=0.045)
    starburst(draw, x + 168, y + 50, 15, (255, 140, 26))
    starburst(draw, x + 168, y + 50, 7, (255, 215, 94))


# ---------------------------------------------------------------- scenes: vignettes (188 x 52)
def scene_mercury(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(13, 27, 46))
    for sx, sy in [(8, 8), (60, 6), (120, 10), (170, 6), (150, 40), (20, 42)]:
        draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(255, 255, 255))
    draw.ellipse([x + 12, y + 10, x + 44, y + 42], fill=(154, 154, 154))
    draw.ellipse([x + 20, y + 18, x + 26, y + 24], fill=(110, 110, 110))
    draw.ellipse([x + 30, y + 28, x + 35, y + 33], fill=(110, 110, 110))
    draw.ellipse([x + 28, y + 14, x + 32, y + 18], fill=(110, 110, 110))
    draw.rectangle([x + 74, y + 22, x + 92, y + 28], fill=(43, 88, 164))   # panel
    draw.rectangle([x + 96, y + 20, x + 122, y + 30], fill=(240, 240, 240))  # body
    draw.rectangle([x + 126, y + 22, x + 144, y + 28], fill=(43, 88, 164))  # panel
    draw.polygon([(x + 96, y + 30), (x + 122, y + 30), (x + 109, y + 42)], fill=(255, 140, 26))


def scene_warsaw(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h // 2], fill=(255, 255, 255))
    draw.rectangle([x, y + h // 2, x + w, y + h], fill=(200, 30, 46))
    # plane silhouette, side profile, nose right
    draw.polygon([(x + 60, y + 24), (x + 128, y + 24), (x + 140, y + 28),
                  (x + 128, y + 32), (x + 60, y + 32)], fill=(22, 35, 63))
    draw.polygon([(x + 66, y + 24), (x + 74, y + 10), (x + 82, y + 24)], fill=(22, 35, 63))
    draw.polygon([(x + 92, y + 32), (x + 104, y + 44), (x + 112, y + 32)], fill=(22, 35, 63))


def scene_quake(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(233, 224, 200))
    # mountains
    draw.polygon([(x + 6, y + h), (x + 60, y + 8), (x + 104, y + h)], fill=(122, 94, 66))
    draw.polygon([(x + 70, y + h), (x + 130, y + 2), (x + 182, y + h)], fill=(96, 74, 52))
    draw.polygon([(x + 52, y + 16), (x + 60, y + 8), (x + 68, y + 16)], fill=(255, 255, 255))
    draw.polygon([(x + 122, y + 10), (x + 130, y + 2), (x + 138, y + 10)], fill=(255, 255, 255))
    # seismograph zigzag
    pts = [(x + 8, y + 34), (x + 22, y + 34), (x + 28, y + 22), (x + 36, y + 44),
           (x + 44, y + 18), (x + 52, y + 46), (x + 60, y + 26), (x + 68, y + 40),
           (x + 78, y + 30), (x + 92, y + 36), (x + 106, y + 30), (x + 120, y + 42),
           (x + 132, y + 30), (x + 146, y + 36), (x + 160, y + 30), (x + 180, y + 34)]
    draw.line(pts, fill=(200, 30, 30), width=3)
    # small house
    draw.rectangle([x + 150, y + 38, x + 172, y + 50], fill=(176, 141, 79))
    draw.polygon([(x + 148, y + 38), (x + 161, y + 28), (x + 174, y + 38)],
                 fill=(166, 28, 28))


def scene_davao(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(168, 205, 232))
    draw.ellipse([x + 160, y + 4, x + 178, y + 22], fill=(255, 244, 200))
    # runway
    draw.rectangle([x, y + 40, x + w, y + h], fill=(60, 60, 60))
    for dx in range(8, 180, 24):
        draw.rectangle([x + dx, y + 45, x + dx + 12, y + 47], fill=(255, 255, 255))
    # plane side profile, nose right, on the runway
    draw.polygon([(x + 40, y + 26), (x + 140, y + 26), (x + 154, y + 30),
                  (x + 140, y + 34), (x + 40, y + 34)], fill=(255, 255, 255))
    draw.polygon([(x + 48, y + 26), (x + 58, y + 12), (x + 66, y + 26)], fill=(255, 255, 255))
    draw.polygon([(x + 78, y + 34), (x + 92, y + 44), (x + 100, y + 34)], fill=(255, 255, 255))
    draw.polygon([(x + 128, y + 30), (x + 146, y + 30), (x + 146, y + 38),
                  (x + 132, y + 38)], fill=(200, 30, 30))
    for wx in (56, 76, 96, 116):
        draw.rectangle([x + wx, y + 29, x + wx + 8, y + 32], fill=(43, 88, 164))


def scene_boat(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(27, 90, 140))
    # waves
    for wy in (10, 26, 42):
        for wx in range(4, 184, 16):
            draw.arc([x + wx, y + wy, x + wx + 14, y + wy + 10], 180, 360,
                     fill=(255, 255, 255), width=2)
    # capsized hull, keel up
    draw.pieslice([x + 56, y + 8, x + 132, y + 44], 0, 180, fill=(122, 84, 40))
    draw.rectangle([x + 56, y + 24, x + 132, y + 30], fill=(90, 60, 28))
    # people in the water
    for px, py in [(40, 34), (150, 38), (160, 28)]:
        draw.ellipse([x + px, y + py, x + px + 8, y + py + 8], fill=(255, 200, 150))
    # rescue ring
    draw.ellipse([x + 18, y + 16, x + 34, y + 32], outline=(255, 255, 255), width=3)


def scene_rahul(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(46, 125, 50))
    draw.rectangle([x + 70, y, x + 118, y + h], fill=(210, 180, 140))   # pitch
    # stumps
    for sx in (86, 94, 102):
        draw.line([x + sx, y + 8, x + sx, y + 22], fill=(255, 255, 255), width=3)
    draw.line([x + 86, y + 8, x + 102, y + 8], fill=(255, 255, 255), width=2)
    # bat
    draw.polygon([(x + 128, y + 14), (x + 140, y + 14), (x + 136, y + 40),
                  (x + 126, y + 40)], fill=(176, 141, 79))
    draw.line([x + 132, y + 40, x + 138, y + 50], fill=(176, 141, 79), width=4)
    # red ball + motion dots
    draw.ellipse([x + 152, y + 30, x + 162, y + 40], fill=(200, 30, 30))
    for dx in (168, 174):
        draw.ellipse([x + dx, y + 33, x + dx + 3, y + 36], fill=(255, 255, 255))
    draw.text((x + 10, y + 34), "124*", font=SANS_B(16), fill=(255, 255, 255))


def scene_trump(draw, x, y, w, h):
    # US flag, left half
    for i in range(7):
        draw.rectangle([x, y + i * 8, x + 92, y + i * 8 + 8],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([x, y, x + 40, y + 28], fill=(43, 88, 164))
    for sx in (8, 20, 32):
        for sy in (6, 16):
            draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    # Russian tricolor, right half
    draw.rectangle([x + 96, y, x + w, y + 18], fill=(255, 255, 255))
    draw.rectangle([x + 96, y + 18, x + w, y + 35], fill=(43, 88, 164))
    draw.rectangle([x + 96, y + 35, x + w, y + h], fill=(200, 30, 30))
    # handshake star between the flags
    starburst(draw, x + 94, y + 26, 8, (255, 215, 94))


def scene_youth(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(246, 240, 224))
    # crowd of heads + placards
    heads = [(16, 34, (200, 30, 30)), (44, 30, (43, 88, 164)), (72, 36, (30, 132, 73)),
             (100, 30, (212, 175, 55)), (128, 34, (166, 28, 28)), (156, 30, (108, 52, 131))]
    for hx, hy, c in heads:
        draw.ellipse([x + hx, y + hy, x + hx + 12, y + hy + 12], fill=c)
        draw.rectangle([x + hx + 1, y + hy + 12, x + hx + 11, y + h], fill=c)
    # placards on sticks
    for px, py, c in [(26, 6, (200, 30, 30)), (82, 4, (43, 88, 164)),
                      (138, 6, (30, 132, 73))]:
        draw.line([x + px + 10, y + py + 12, x + px + 10, y + 30], fill=(60, 60, 60), width=2)
        draw.rectangle([x + px, y + py, x + px + 34, y + py + 14], fill=(255, 255, 255),
                       outline=c, width=2)
        draw.line([x + px + 5, y + py + 5, x + px + 29, y + py + 5], fill=c, width=2)
        draw.line([x + px + 5, y + py + 9, x + px + 29, y + py + 9], fill=c, width=2)


def scene_chips(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(20, 90, 50))
    for lx in (10, 40, 150):
        draw.line([x + lx, y + 6, x + lx, y + h - 6], fill=(60, 160, 100), width=2)
    draw.line([x + 6, y + 40, x + w - 6, y + 40], fill=(60, 160, 100), width=2)
    draw.rectangle([x + 72, y + 12, x + 112, y + 40], fill=(16, 40, 26))
    draw.rectangle([x + 82, y + 20, x + 102, y + 32], fill=(34, 197, 94))
    for px in range(76, 110, 8):
        draw.rectangle([x + px, y + 8, x + px + 4, y + 12], fill=(212, 175, 55))
        draw.rectangle([x + px, y + 40, x + px + 4, y + 44], fill=(212, 175, 55))
    draw.line([x + 122, y + 26, x + 156, y + 26], fill=(255, 255, 255), width=3)
    draw.polygon([(x + 156, y + 21), (x + 166, y + 26), (x + 156, y + 31)], fill=(255, 255, 255))
    draw.rectangle([x + 168, y + 8, x + 184, y + 20], fill=(222, 41, 16))
    draw.text((x + 171, y + 10), "*", font=SANS_B(9), fill=(255, 215, 0))


def scene_vegas(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 40))
    for i in range(12):
        c = (255, 255, 255) if i % 2 == 0 else (10, 10, 10)
        draw.rectangle([x + 8 + i * 14, y + 4, x + 22 + i * 14, y + 16], fill=c)
    for sx in (20, 34, 150, 164):
        draw.line([x + sx, y + 34, x + sx + 12, y + 34], fill=(255, 255, 255), width=2)
    draw.polygon([(x + 48, y + 30), (x + 140, y + 30), (x + 152, y + 40),
                  (x + 40, y + 40)], fill=(220, 40, 40))
    draw.polygon([(x + 96, y + 30), (x + 118, y + 22), (x + 128, y + 30)], fill=(220, 40, 40))
    for wx in (58, 128):
        draw.ellipse([x + wx, y + 38, x + wx + 12, y + 50], fill=(10, 10, 10),
                     outline=(180, 180, 180))


# ---------------------------------------------------------------- world map
# Rough continent outlines in (lon, lat); drawn as a dot grid, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66), (-80, 73),
     (-70, 62), (-55, 52), (-60, 47), (-70, 42), (-75, 35), (-80, 26), (-84, 30),
     (-90, 21), (-97, 16), (-94, 17), (-87, 13), (-83, 9), (-79, 9), (-85, 11),
     (-92, 14), (-97, 16), (-105, 20), (-110, 24), (-117, 33), (-125, 40),
     (-124, 48), (-135, 58), (-150, 60), (-165, 60)],
    [(-55, 60), (-45, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 74), (-30, 76),
     (-45, 76), (-58, 74), (-58, 70)],
    [(-79, 9), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-44, -3), (-35, -8),
     (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -50), (-74, -54),
     (-73, -40), (-72, -30), (-70, -18), (-77, -12), (-81, -6), (-80, 0)],
    [(-6, 35), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12), (51, 11),
     (48, 2), (40, -10), (35, -18), (32, -29), (26, -34), (19, -35), (15, -27),
     (12, -18), (9, -1), (9, 4), (-8, 5), (-15, 11), (-17, 15), (-16, 20),
     (-15, 25), (-10, 30)],
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-5, 48), (0, 50), (3, 53), (8, 57),
     (10, 59), (5, 60), (5, 62), (12, 64), (18, 69), (25, 71), (30, 70), (40, 68),
     (50, 69), (55, 68), (60, 66), (55, 60), (50, 55), (45, 50), (40, 47),
     (35, 45), (30, 46), (28, 44), (23, 40), (26, 38), (23, 36), (19, 40),
     (15, 44), (12, 44), (8, 44), (3, 43), (0, 39), (-2, 37), (-6, 36)],
    [(30, 70), (40, 68), (50, 69), (60, 66), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
     (170, 67), (178, 65), (170, 60), (162, 56), (158, 52), (150, 59), (142, 55),
     (140, 45), (135, 43), (130, 42), (127, 40), (122, 38), (120, 32), (122, 28),
     (118, 25), (110, 20), (108, 18), (105, 10), (103, 8), (100, 7), (98, 10),
     (95, 16), (92, 21), (89, 22), (86, 20), (82, 17), (80, 13), (77, 8),
     (75, 12), (73, 16), (70, 20), (66, 25), (62, 25), (58, 26), (55, 26),
     (52, 28), (50, 29), (48, 30), (50, 26), (54, 24), (57, 22), (59, 22),
     (55, 17), (52, 15), (48, 14), (44, 13), (43, 12), (40, 15), (38, 18),
     (35, 28), (35, 36), (30, 36), (27, 37), (30, 40), (28, 41), (30, 46),
     (35, 45), (40, 47), (45, 50), (50, 55), (55, 60), (60, 66)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10), (125, -8),
     (130, -3), (135, -4), (140, -8), (147, -9), (142, -8), (136, -6), (131, -1)],
]


def point_in_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xin = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xin:
                inside = not inside
        j = i
    return inside


def on_land(lon, lat):
    return any(point_in_poly(lon, lat, p) for p in CONTINENTS)


# (story, lon, lat, badge dx, badge dy) — badges offset so Europe pins don't collide
PINS = [
    (1, 30.7, 36.9, 12, -12),    # Antalya
    (2, 33.4, 47.9, 14, 10),     # Kryvyi Rih
    (3, 46.7, 24.7, 12, 8),      # Riyadh
    (4, -75.2, -11.2, 12, -10),  # Junin, Peru
    (6, 21.0, 52.2, -16, -12),   # Warsaw
    (7, 125.6, 7.1, 12, 6),      # Davao
    (8, 6.2, 4.9, -12, 10),      # Bayelsa, Nigeria
    (9, 174.8, -41.3, 12, -12),  # Wellington
    (10, -115.1, 36.2, -10, 12), # Las Vegas
    (11, -77.0, 38.9, -12, -12), # Washington (Trump-Putin)
    (12, 13.4, 52.5, 10, -14),   # Berlin (youth march)
    (13, -77.0, 38.9, 14, 10),   # Washington (AI chips)
]


# ---------------------------------------------------------------- content
HEROES = [
    dict(n=1, scene=scene_cop31, tag="ANTALYA, TÜRKIYE · CLIMATE",
         label="COP31: NO DEAL",
         head="COP31 runs into overtime with no deal",
         body="Talks pass their Friday deadline with no agreement; a third draft is due "
              "Saturday morning as nearly 200 countries stay split over fossil fuels.",
         src="Reuters · UN News"),
    dict(n=2, scene=scene_kyiv, tag="KRYVYI RIH, UKRAINE · WAR",
         label="KRYVYI RIH: STRIKES",
         head="Russian strikes kill 12, wound 82 in a day",
         body="A double-tap strike on Kryvyi Rih kills a boy of 7 and a paramedic and "
              "injures 42, four of them children, as the barrage hits cities across Ukraine.",
         src="Kyiv Independent · AP"),
    dict(n=3, scene=scene_riyadh, tag="RIYADH, SAUDI ARABIA · CONFLICT",
         label="RIYADH: INTERCEPTS",
         head="Coalition downs three Houthi missiles over Riyadh",
         body="Air defences destroy three ballistic missiles fired at the capital early on "
              "Saturday; the coalition hits six Houthi workshops in Sanaa.",
         src="Reuters · AFP"),
]

VIGNETTES = [
    dict(n=4, scene=scene_quake, tag="JUNÍN, PERU · QUAKE · USGS",
         head="Magnitude 6.7 quake hits Peru",
         body="Struck at 00:09 UTC, 108 km deep; felt in Lima, no deaths reported.",
         src="USGS · IGP"),
    dict(n=5, scene=scene_mercury, tag="MERCURY · SPACE · ESA",
         head="BepiColombo reaches Mercury after eight years",
         body="Fires thrusters at 19:24 CET to be caught by Mercury's gravity.",
         src="ESA"),
    dict(n=6, scene=scene_warsaw, tag="WARSAW, POLAND · NATO · AP",
         head="Rutte in Warsaw as Poland seeks NATO help",
         body="NATO chief visits after Friday's landings; Warsaw wants more support.",
         src="AP"),
    dict(n=7, scene=scene_davao, tag="DAVAO · AVIATION · CAAP",
         head="Jet lands safely; all 146 safe",
         body="Air Niugini 767 diverts after engine fire warning; no injuries.",
         src="CAAP · AP"),
    dict(n=8, scene=scene_boat, tag="BAYELSA · DISASTER · Police",
         head="Funeral boat capsizes; four dead",
         body="Police confirm four dead, 24 rescued; search for more goes on.",
         src="Police · Reuters"),
    dict(n=9, scene=scene_rahul, tag="WELLINGTON · CRICKET · AFP",
         head="Rahul hits century as India fight back",
         body="Unbeaten 124 at tea; India 344 for 2, replying to 368.",
         src="AFP · Scorecard"),
    dict(n=10, scene=scene_vegas, tag="LAS VEGAS · FORMULA 1 · F1",
         head="Russell fastest in final practice",
         body="1:34.041 in the last dry session; clashes with Verstappen.",
         src="F1 · Reuters"),
    dict(n=11, scene=scene_trump, tag="WASHINGTON · TALKS · Reuters",
         head="Trump upbeat on Putin talks",
         body="Sees a 'real good chance' of a Ukraine deal after talks in China.",
         src="Reuters"),
    dict(n=12, scene=scene_youth, tag="EUROPE · PROTEST · AFP",
         head="Youth march across Europe",
         body="Rallies in about 400 cities over living costs and rearmament.",
         src="AFP"),
    dict(n=13, scene=scene_chips, tag="WASHINGTON · TECH · House panel",
         head="US clears ~900,000 AI chips for China",
         body="Washington approved the sale of close to 900,000 AI chips to China.",
         src="House panel"),
]

# (number, city, one-line brief) — 14..40
BRIEFS = [
    (14, "NEW YORK", "Wall Street enters correction; S&P −3.6%."),
    (15, "NEW DELHI", "Modi opens SCO dialogue forum."),
    (16, "WASHINGTON", "Trump: Iran wants a deal."),
    (17, "LOS ANGELES", "Jury convicts Palisades Fire starter."),
    (18, "TOKYO", "Frosty APEC greeting for Takaichi."),
    (19, "OTTAWA", "World can no longer count on US leadership."),
    (20, "JOHANNESBURG", "ANC scrambles after worst result since 1994."),
    (21, "COPENHAGEN", "Denmark charges two over Russian murder plot."),
    (22, "MEXICO", "Caravan of about 300 migrants crosses in."),
    (23, "BRUSSELS", "Rare EU-UK summit; Burnham seeks Brexit fix."),
    (24, "PODGORICA", "Montenegro rejects land deal with Croatia."),
    (25, "KABUL", "UN warns ISIS-K is gaining drones."),
    (26, "NEW DELHI", "India launches first H5N1 vaccine."),
    (27, "WASHINGTON", "Second judge blocks Trump's triumphal arch."),
    (28, "BRASILIA", "Indigenous land bill advances; Raoni visit."),
    (29, "BAGHDAD", "Pipeline chief arrested over illicit oil trade."),
    (30, "HORMUZ", "Iran claims waters 500 km beyond strait."),
    (31, "CALIFORNIA", "California subpoenas Nvidia."),
    (32, "WASHINGTON", "US floats NATO membership for Ukraine."),
    (33, "THE HAGUE", "Myanmar, China call ICJ ruling 'unjust'."),
    (34, "ODISHA", "After Akvan: relief under way; no deaths."),
    (35, "MELBOURNE", "Australia v England open T20 series tonight."),
    (36, "SUMY", "HIMARS wipes out 20 Russian commanders."),
    (37, "PERTH", "Starc takes 7/58 as Ashes opens; England 172."),
    (38, "TURIN", "Medvedev meets Zverev in tonight's semi."),
    (39, "WASHINGTON", "Pentagon: US Iran engagement cost $48.3bn."),
    (40, "LONDON", "Britain hits Moscow with cyberattacks."),
]

STATS = [
    ("0", "climate deal agreed at COP31"),
    ("12", "killed in Ukraine strikes in a day"),
    ("42", "injured in the Kryvyi Rih strike"),
    ("3", "missiles downed over Riyadh"),
    ("6.7", "Peru quake magnitude"),
    ("146", "safe after Davao jet landing"),
]

REGIONS = [
    ("EUROPE", 11, (31, 78, 121)),
    ("ASIA", 6, (176, 58, 46)),
    ("MIDDLE EAST", 3, (183, 149, 11)),
    ("AFRICA", 2, (30, 132, 73)),
    ("AMERICAS", 14, (108, 52, 131)),
    ("OCEANIA", 3, (17, 122, 101)),
    ("GLOBAL", 1, (93, 109, 126)),
]

DATE_CHECK = (
    "Russian missiles land in Poland — Fri 20 Nov · Kyiv's bridges hit — Fri 20 Nov · "
    "Cyclone Akvan landfall — Fri 20 Nov · Bayer's $7.25bn Roundup settlement — Fri 20 Nov · "
    "Anthropic's $81.3bn IPO — Thu 19 Nov · Asia's AI sell-off — Fri 20 Nov · "
    "ICJ Myanmar ruling — Fri 20 Nov · UK–EU 'reset' deal — Fri 20 Nov · "
    "Shenzhen declaration — Thu 19 Nov · Mongolia's president quits — Fri 20 Nov"
)


def draw_rich_wrapped(draw, x, y, lead, lead_font, body, body_font, max_w, leading):
    """Draw 'lead' in lead_font + 'body' in body_font, word-wrapped; return bottom y."""
    words = []
    for w in lead.split(" "):
        words.append((w, lead_font))
    for w in body.split(" "):
        words.append((w, body_font))
    lines, cur, cur_w = [], [], 0
    space_w = text_w(draw, " ", body_font)
    for w, f in words:
        ww = text_w(draw, w, f)
        add = ww if not cur else ww + space_w
        if cur_w + add <= max_w or not cur:
            cur.append((w, f))
            cur_w += add
        else:
            lines.append(cur)
            cur = [(w, f)]
            cur_w = ww
    if cur:
        lines.append(cur)
    for i, ln in enumerate(lines):
        cx = x
        for w, f in ln:
            draw.text((cx, y + i * leading), w, font=f, fill=INK)
            cx += text_w(draw, w, f) + space_w
    return y + len(lines) * leading


def render():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    report = {}

    # ---- kicker
    y = 10
    d.text((MX, y), "THE WORLD IN ONE DAY", font=SANS_B(15), fill=RED)
    right = "40 STORIES · 7 REGIONS · EVERY ONE DATED"
    d.text((W - MX - text_w(d, right, SANS_B(11)), y + 3), right, font=SANS_B(11), fill=GREY)
    d.line([MX, 32, W - MX, 32], fill=INK, width=2)

    # ---- masthead
    title = "Saturday 21 November 2026"
    tf = SERIF_B(50)
    d.text(((W - text_w(d, title, tf)) / 2, 36), title, font=tf, fill=INK)
    sub = "Climate summit runs past its deadline · Five missiles shot down over Saudi Arabia · Strong quake shakes Peru"
    sf = SERIF_B(16)
    d.text(((W - text_w(d, sub, sf)) / 2, 94), sub, font=sf, fill=RED)
    d.line([MX, 112, W - MX, 112], fill=INK, width=1)

    # ---- stat strip: 6 big numbers
    y0 = 118
    cell = CW / 6
    for i, (num, label) in enumerate(STATS):
        cx = MX + i * cell
        nf = SERIF_B(28)
        d.text((cx + (cell - text_w(d, num, nf)) / 2, y0), num, font=nf, fill=INK)
        draw_wrapped(d, cx + 8, y0 + 32, label, SANS(9.5), cell - 16, GREY,
                     leading=11)
        if i:
            d.line([cx, y0 + 2, cx, y0 + 50], fill=LINE, width=1)
    d.line([MX, 176, W - MX, 176], fill=INK, width=1)
    report["stats_bottom"] = 176

    # ---- region bar (widths proportional to counts, floored at label width)
    y0 = 180
    total = sum(c for _, c, _ in REGIONS)
    lf = SANS_B(10)
    floors = [text_w(d, "%s %d" % (name, count), lf) + 12
              for name, count, _ in REGIONS]
    widths = [max(CW * count / total, f) for (_, count, _), f in zip(REGIONS, floors)]
    over = sum(widths) - CW
    while over > 0.5:
        slack = [max(0.0, w - f) for w, f in zip(widths, floors)]
        tot = sum(slack)
        if tot <= 0:
            break
        for i in range(len(widths)):
            cut = min(slack[i], over * slack[i] / tot)
            widths[i] -= cut
            over -= cut
    widths[-1] += CW - sum(widths)
    rx = MX
    for (name, count, color), rw in zip(REGIONS, widths):
        d.rectangle([rx, y0, rx + rw - 1, y0 + 22], fill=color)
        label = "%s %d" % (name, count)
        d.text((rx + (rw - text_w(d, label, lf)) / 2, y0 + 5), label, font=lf,
               fill=(255, 255, 255))
        rx += rw
    report["regions_bottom"] = y0 + 22

    # ---- heroes: 3 panels
    y0 = 208
    hw = 320
    hg = 124
    for i, hero in enumerate(HEROES):
        hx = MX + i * (hw + 10)
        hero["scene"](d, hx, y0, hw, hg)
        badge(d, hx + 16, y0 + 16, hero["n"])
        # red label bar under the scene
        d.rectangle([hx, y0 + hg, hx + hw, y0 + hg + 20], fill=RED)
        lab = "%d · %s" % (hero["n"], hero["tag"])
        d.text((hx + 6, y0 + hg + 4), lab, font=SANS_B(9), fill=(255, 255, 255))
        ty = y0 + hg + 26
        ty = draw_wrapped(d, hx, ty, hero["head"], SERIF_B(19), hw, INK, leading=21)
        ty = draw_wrapped(d, hx, ty + 3, hero["body"], SANS(11.5), hw, INK, leading=13.5)
        d.text((hx, ty + 3), "— " + hero["src"], font=SANS(9), fill=GREY)
        report["hero_%d_bottom" % hero["n"]] = ty + 15
    hero_bottom = max(report["hero_%d_bottom" % n] for n in (1, 2, 3))

    # ---- vignettes: two rows of five
    d.line([MX, hero_bottom + 6, W - MX, hero_bottom + 6], fill=LINE, width=1)
    vw = 188
    vg = 48
    vy = hero_bottom + 12
    for row in range(2):
        row_top = vy + row * 130
        for col in range(5):
            v = VIGNETTES[row * 5 + col]
            vx = MX + col * (vw + 10)
            v["scene"](d, vx, row_top, vw, vg)
            badge(d, vx + 14, row_top + 13, v["n"], r=10)
            ty = row_top + vg + 5
            d.text((vx, ty), v["tag"], font=SANS_B(9), fill=RED)
            ty = draw_wrapped(d, vx, ty + 12, v["head"], SERIF_B(12.5), vw, INK,
                              leading=14.5)
            ty = draw_wrapped(d, vx, ty + 2, v["body"], SANS(9.5), vw, INK, leading=11.5)
            d.text((vx, ty + 1), "— " + v["src"], font=SANS(8.5), fill=GREY)
        report["vig_row_%d_bottom" % row] = row_top + 125
    vig_bottom = vy + 130 + 125

    # ---- bottom headers
    y0 = int(vig_bottom + 4)
    d.text((MX, y0), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
    d.text((MX + 340, y0), "ALSO ON SATURDAY 21 NOVEMBER — 27 MORE STORIES",
           font=SANS_B(12), fill=INK)
    d.line([MX, y0 + 18, W - MX, y0 + 18], fill=INK, width=1)
    report["bottom_header"] = y0 + 18

    # ---- dotted world map (left) + briefs (right)
    map_x, map_y, map_w, map_h = MX, y0 + 24, 330, 150
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(220, 232, 240))
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], outline=LINE, width=1)
    lon0, lon1, lat0, lat1 = -168, 192, -58, 84
    dot_step = 6
    for gy in range(map_y + 4, map_y + map_h - 14, dot_step):
        lat = lat1 - (gy - map_y) / (map_h - 18) * (lat1 - lat0)
        for gx in range(map_x + 4, map_x + map_w - 4, dot_step):
            lon = lon0 + (gx - map_x) / map_w * (lon1 - lon0)
            if on_land(lon, lat):
                d.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6], fill=(51, 80, 122))
    pin_font = SANS_B(8)
    for n, lon, lat, dx, dy in PINS:
        px = map_x + (lon - lon0) / (lon1 - lon0) * map_w
        py = map_y + (lat1 - lat) / (lat1 - lat0) * (map_h - 18)
        bx, by = px + dx, py + dy
        d.line([px, py, bx, by], fill=RED, width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        d.ellipse([bx - 6.5, by - 6.5, bx + 6.5, by + 6.5], fill=RED,
                  outline=(255, 255, 255), width=1)
        tw = text_w(d, str(n), pin_font)
        d.text((bx - tw / 2, by - 4.5), str(n), font=pin_font, fill=(255, 255, 255))
    note = "Pins 1–13 mark the drawn stories. No. 5 is in space: Mercury."
    d.text((map_x + 6, map_y + map_h - 12), note, font=SANS(8.5), fill=GREY)

    # briefs: two columns, rows sized by the taller side
    bx0, bx1 = MX + 340, W - MX
    col_w = (bx1 - bx0 - 10) / 2
    rows = [(BRIEFS[i], BRIEFS[i + 14] if i + 14 < len(BRIEFS) else None)
            for i in range(14)]
    by = map_y
    lead_f, body_f = SANS_B(9), SANS(9)
    for left, right in rows:
        h_left = 0
        if left is not None:
            n, city, body = left
            h_left = len(wrap(d, "%d %s — %s" % (n, city, body),
                              body_f, col_w)) * 11
        h_right = 0
        if right is not None:
            n, city, body = right
            h_right = len(wrap(d, "%d %s — %s" % (n, city, body),
                               body_f, col_w)) * 11
        rh = max(h_left, h_right)
        if left is not None:
            n, city, body = left
            draw_rich_wrapped(d, bx0, by, "%d %s —" % (n, city), lead_f,
                              body, body_f, col_w, 11)
        if right is not None:
            n, city, body = right
            draw_rich_wrapped(d, bx0 + col_w + 10, by, "%d %s —" % (n, city),
                              lead_f, body, body_f, col_w, 11)
        by += rh + 1
    report["briefs_bottom"] = by
    report["map_bottom"] = map_y + map_h

    # ---- date check box
    y0 = max(by, map_y + map_h) + 8
    d.rectangle([MX, y0, W - MX, y0 + 46], outline=RED, width=2)
    d.text((MX + 8, y0 + 5), "DATE CHECK — WHAT WE LEFT OUT",
           font=SANS_B(11), fill=RED)
    draw_wrapped(d, MX + 8, y0 + 20, "✕ " + DATE_CHECK.replace(" · ", "  ✕ "),
                 SANS(9), CW - 16, INK, leading=11)
    report["datecheck_bottom"] = y0 + 46

    # ---- footer
    foot = ("Every story here happened, or was first reported, on Saturday 21 November 2026 "
            "in at least one time zone. Sources named beside each story. "
            "Original drawings, not photographs.")
    ff = SANS(8.5)
    d.text(((W - text_w(d, foot, ff)) / 2, y0 + 52), foot, font=ff, fill=GREY)
    report["footer_bottom"] = y0 + 64
    return img, report


def main():
    img, report = render()
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    size = os.path.getsize(out)
    print("wrote %s (%d bytes)" % (out, size))
    for k, v in report.items():
        print("layout %-18s %d" % (k, v))
    assert size <= 1048576, "entry.png over 1 MiB"
    assert report["footer_bottom"] <= 1024, "layout overflows 1024px"


if __name__ == "__main__":
    main()
