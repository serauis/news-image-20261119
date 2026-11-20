#!/usr/bin/env python3
"""v2: a dense newspaper front page for 19 Nov 2026, drawn in code (PIL).
Drawn at 2x and downscaled to 1024x1024 for smooth type.
Every story was reported on Thursday 19 November 2026 (sources in footer)."""
from PIL import Image, ImageDraw, ImageFont
import os

S = 2  # supersample
W = 1024 * S
img = Image.new("RGB", (W, W), (247, 242, 231))
d = ImageDraw.Draw(img)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

INK = (20, 32, 46)
RED = (179, 52, 31)
GREY = (90, 84, 70)
CARD = (255, 253, 246)
LINE = (205, 196, 172)

def F(path, px):
    return ImageFont.truetype(path, px * S)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def text_block(x, y, w, text, font, fill, leading):
    for ln in wrap(text, font, w):
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

M = 26 * S            # page margin
CW = W - 2 * M        # content width

# ---------- masthead ----------
f_kick = F(SANS_B, 14)
kick = "T H E   W O R L D   I N   O N E   D A Y"
kw = d.textlength(kick, font=f_kick)
d.text((M, 16 * S), kick, font=f_kick, fill=RED)
right = "21 STORIES · EVERY CONTINENT"
rw = d.textlength(right, font=f_kick)
d.text((W - M - rw, 16 * S), right, font=f_kick, fill=RED)
f_title = F(SERIF_B, 55)
title = "Thursday 19 November 2026"
tw = d.textlength(title, font=f_title)
d.text(((W - tw) / 2, 34 * S), title, font=f_title, fill=INK)
sub = "Trump, Xi and Putin share one table · The World Court finds genocide in Myanmar · COP31's draft drops fossil fuels"
f_sub = F(SANS_I, 14.5)
sw = d.textlength(sub, font=f_sub)
d.text(((W - sw) / 2, 104 * S), sub, font=f_sub, fill=(70, 62, 48))
d.line([M, 128 * S, W - M, 128 * S], fill=INK, width=2 * S)
d.line([M, 132 * S, W - M, 132 * S], fill=INK, width=1 * S)

# ---------- stats strip ----------
stats = [
    ("3", "presidents at one table"),
    ("9–6", "World Court vote: genocide"),
    ("$81bn", "Anthropic's record IPO raise"),
    ("13 yrs", "wait ends — GTA VI on sale"),
    ("109–0", "Denmark backs Greenland pact"),
    ("4.9%", "Australia's jobless rate"),
]
f_num = F(SANS_B, 21)
f_cap = F(SANS, 10.5)
cell = CW // 6
y0 = 140 * S
for i, (num, cap) in enumerate(stats):
    x = M + i * cell
    if i: d.line([x, y0 + 2 * S, x, y0 + 34 * S], fill=LINE, width=S)
    d.text((x + 7 * S, y0), num, font=f_num, fill=RED if i in (1, 2) else INK)
    text_block(x + 7 * S, y0 + 26 * S, cell - 12 * S, cap, f_cap, GREY, 12 * S)
d.line([M, 182 * S, W - M, 182 * S], fill=LINE, width=S)

# ---------- hero tiles ----------
heroes = [
    ((28, 84, 140), "1 · SHENZHEN — SUMMIT",
     "Trump, Xi and Putin hold first three-way summit",
     "The US, Chinese and Russian leaders met on APEC's last day in Shenzhen and issued a joint call on nuclear risk. Kyiv was not in the room. — Reuters, AP"),
    ((112, 44, 140), "2 · WORLDWIDE — GAMES",
     "GTA VI finally goes on sale around the world",
     "Rockstar's sequel unlocked at midnight local time — New Zealand first — 13 years after GTA V, its predecessor. On PS5 and Xbox Series X|S; no PC version yet. — Euronews"),
    ((24, 110, 70), "3 · NEW YORK — MARKETS",
     "Anthropic starts trading on Nasdaq as ANT",
     "Priced at $83, the largest IPO on record raised $81.3bn and values the Claude maker near $1.5tn — yet the S&P 500 still fell 2% as AI-bubble fears grew. — Dow Jones"),
]
f_cat = F(SANS_B, 11.5)
f_hh = F(SANS_B, 18.5)
f_deck = F(SANS, 12)
gap = 10 * S
tw3 = (CW - 2 * gap) // 3
hy = 192 * S
hh = 182 * S
for i, (color, cat, head, deck) in enumerate(heroes):
    x = M + i * (tw3 + gap)
    d.rectangle([x, hy, x + tw3, hy + hh], fill=CARD, outline=LINE, width=S)
    d.rectangle([x, hy, x + tw3, hy + 7 * S], fill=color)
    text_block(x + 9 * S, hy + 13 * S, tw3 - 18 * S, cat, f_cat, color, 14 * S)
    y = text_block(x + 9 * S, hy + 31 * S, tw3 - 18 * S, head, f_hh, INK, 22 * S)
    text_block(x + 9 * S, y + 4 * S, tw3 - 18 * S, deck, f_deck, (52, 48, 40), 15 * S)

# ---------- numbered tiles ----------
tiles = [
    ((150, 108, 30), "4 · THE HAGUE — LAW",
     "World Court rules on Rohingya genocide",
     "Judges ruled 9–6 that Myanmar committed genocide in 2017 — the first such ruling against a state. Rohingya refugees in Bangladesh cheered. — UN News"),
    ((140, 40, 40), "5 · CRIMEA — WAR",
     "Ukraine hits Crimean Bridge again",
     "A third strike in four days: the rail section was targeted overnight and traffic halted. Putin vowed a harsher response. — Euronews"),
    ((140, 40, 40), "6 · GAZA — WAR",
     "Israeli armour pushes into central Gaza",
     "Tanks moved toward Salah al-Din Street as five aid groups scored the peace plan's delivery at just 4 of 26 pledges. — Al Jazeera"),
    ((30, 110, 150), "7 · ODISHA, INDIA — STORM",
     "Cyclone Akvan nears India's east coast",
     "Red alert: thousands moved to safety in Odisha before landfall, expected Friday. Schools closed across coastal districts. — AP"),
    ((24, 110, 70), "8 · ANTALYA — CLIMATE",
     "COP31 draft drops fossil fuels",
     "The slimmed draft drops the fossil-fuel phase-out, and a $120bn adaptation-finance goal is still open as talks run to Friday. — AFP"),
    ((28, 84, 140), "9 · WASHINGTON — IRAN",
     "Senate rejects Iran war-powers curb",
     "The resolution that would have limited strikes on Iran failed 51–48, as Tehran warned it will not accept a war of attrition. — AP"),
]
f_th = F(SANS_B, 15)
f_td = F(SANS, 11.5)
ty = hy + hh + 10 * S
th = 128 * S
for r in range(2):
    for c in range(3):
        color, cat, head, deck = tiles[r * 3 + c]
        x = M + c * (tw3 + gap)
        y = ty + r * (th + gap)
        d.rectangle([x, y, x + tw3, y + th], fill=CARD, outline=LINE, width=S)
        d.rectangle([x, y, x + tw3, y + 6 * S], fill=color)
        text_block(x + 9 * S, y + 11 * S, tw3 - 18 * S, cat, f_cat, color, 13 * S)
        yy = text_block(x + 9 * S, y + 27 * S, tw3 - 18 * S, head, f_th, INK, 18 * S)
        text_block(x + 9 * S, yy + 3 * S, tw3 - 18 * S, deck, f_td, (52, 48, 40), 14 * S)

# ---------- also on thursday ----------
ay = ty + 2 * th + gap + 8 * S
f_ah = F(SANS_B, 14)
d.text((M, ay), "ALSO ON THURSDAY 19 NOVEMBER", font=f_ah, fill=RED)
d.line([M, ay + 20 * S, W - M, ay + 20 * S], fill=LINE, width=S)
also = [
    ("SEOUL —", "551,864 sit Korea's Suneung college exam; flights paused nationwide for the listening test."),
    ("BOGOTÁ —", "Colombia's unions hold a national strike against the economic-rescue tax bill."),
    ("CANBERRA —", "Jobless rate jumps to 4.9%, a five-year high; economists warn of a recession risk."),
    ("JAKARTA —", "Indonesia's parliament passes the asset-forfeiture law, 18 years in the making."),
    ("SENEGAL —", "Dozens missing after a migrant boat capsizes off the coast near Yenne."),
    ("YONGBYON —", "IAEA says North Korea is expanding its uranium enrichment facility."),
    ("LONDON —", "Gold falls to a 14-month low as bets on higher interest rates grow."),
    ("FLORIDA —", "Floods shut South Florida schools for a second day after 15 inches of rain."),
    ("DEEP SPACE —", "Voyager 1 reaches one light-day from Earth, 48 years after its launch."),
    ("PORT-AU-PRINCE —", "Haitian police kill 34 gang members in a raid on the capital."),
    ("MOGADISHU —", "Somalia expels the UAE ambassador in a diplomatic row."),
    ("ROME —", "Author and journalist Corrado Augias dies at 91."),
]
f_lead = F(SANS_B, 11)
f_item = F(SANS, 11)
colw = (CW - gap) // 2
iy = ay + 28 * S
for i, (lead, body) in enumerate(also):
    x = M + (i // 6) * (colw + gap)
    y = iy + (i % 6) * 34 * S
    d.text((x, y), "▪ " + lead, font=f_lead, fill=INK)
    lw = d.textlength("▪ " + lead + " ", font=f_lead)
    lines = wrap(body, f_item, colw - lw)
    d.text((x + lw, y), lines[0], font=f_item, fill=(52, 48, 40))
    for j, ln in enumerate(lines[1:], 1):
        d.text((x, y + j * 13.5 * S), ln, font=f_item, fill=(52, 48, 40))

# ---------- footer ----------
fy = 962 * S
d.line([M, fy - 8 * S, W - M, fy - 8 * S], fill=INK, width=S)
f_foot = F(SANS, 10.5)
text_block(M, fy, CW, "DATE CHECK — every story on this page happened, or was first reported, on Thursday 19 November 2026, in some time zone. Claims are attributed, not stated as fact.", f_foot, GREY, 13 * S)
text_block(M, fy + 15 * S, CW, "Sources: BBC, Reuters, AP, AFP, Al Jazeera, UN News, Euronews, ABC, Xinhua, Dow Jones. Page drawn in code.", f_foot, GREY, 13 * S)

img = img.resize((1024, 1024), Image.LANCZOS)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry2.png")
img.save(out, "PNG", optimize=True)
print(out, os.path.getsize(out), "bytes")
