#!/usr/bin/env python3
"""Composite the day's headlines onto the generated base illustration.
Base art: media-generation-base-0-*.png (2x2 editorial panels + blank masthead).
Output: entry.png at exactly 1024x1024, <= 1 MiB (the bounty's limits)."""
from PIL import Image, ImageDraw, ImageFont
import glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
base_path = sorted(glob.glob(os.path.join(HERE, "media-generation-base-0-*.png")))[0]
img = Image.open(base_path).convert("RGB").resize((1024, 1024), Image.LANCZOS)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
if not os.path.exists(SANS_B):
    SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

d = ImageDraw.Draw(img, "RGBA")
INK = (26, 35, 50)

def centered(text, font, y, fill):
    w = d.textlength(text, font=font)
    d.text(((1024 - w) / 2, y), text, font=font, fill=fill)

# Masthead (blank box approx x 53..971, y 46..223)
centered("THE WORLD IN ONE DAY", ImageFont.truetype(SERIF_B, 47), 82, INK)
centered("THURSDAY · 19 NOVEMBER 2026", ImageFont.truetype(SANS_B, 23), 152, (120, 40, 30))

# Headline bars at each panel's foot.
panels = [  # (x0, y0, x1, y1) at 1024 scale
    (40, 246, 501, 596),    # top-left: ICJ / Rohingya
    (523, 246, 984, 596),   # top-right: summit
    (40, 612, 501, 975),    # bottom-left: markets / AI IPO
    (523, 612, 984, 975),   # bottom-right: Crimean Bridge
]
headlines = [
    ("MYANMAR GUILTY OF GENOCIDE", "World Court rules on the Rohingya — a first against a state"),
    ("TRUMP · XI · PUTIN MEET", "First three-way summit, in Shenzhen"),
    ("RECORD $81B AI IPO", "Anthropic debuts — markets still slide 2%"),
    ("CRIMEAN BRIDGE HIT AGAIN", "Ukraine's 3rd strike in four days"),
]
BAR_H = 66
for (x0, y0, x1, y1), (h1, h2) in zip(panels, headlines):
    d.rectangle([x0, y1 - BAR_H, x1, y1], fill=(10, 14, 22, 190))
    fh = ImageFont.truetype(SANS_B, 21)
    while d.textlength(h1, font=fh) > (x1 - x0 - 20) and fh.size > 13:
        fh = ImageFont.truetype(SANS_B, fh.size - 1)
    d.text((x0 + 10, y1 - BAR_H + 7), h1, font=fh, fill=(255, 255, 255))
    fs = ImageFont.truetype(SANS, 15)
    while d.textlength(h2, font=fs) > (x1 - x0 - 20) and fs.size > 10:
        fs = ImageFont.truetype(SANS, fs.size - 1)
    d.text((x0 + 10, y1 - BAR_H + 36), h2, font=fs, fill=(238, 230, 205))

out = os.path.join(HERE, "entry.png")
img.save(out, "PNG", optimize=True)
print(out, img.size, os.path.getsize(out), "bytes")
