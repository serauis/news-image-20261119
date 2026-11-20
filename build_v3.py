#!/usr/bin/env python3
"""v3: front page WITH pictures — crops from the v1 base art + a 3x2 sprite
sheet, composed in code with 30 stories of Thursday 19 November 2026."""
from PIL import Image, ImageDraw, ImageFont
import glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
S = 2
W = 1024 * S
img = Image.new("RGB", (W, W), (247, 242, 231))
d = ImageDraw.Draw(img)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
INK = (20, 32, 46); RED = (179, 52, 31); GREY = (90, 84, 70)
CARD = (255, 253, 246); LINE = (205, 196, 172)

def F(p, px): return ImageFont.truetype(p, int(px * S))
def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines
def block(x, y, w, text, font, fill, leading):
    for ln in wrap(text, font, w):
        d.text((x, y), ln, font=font, fill=fill); y += leading
    return y

def crop_frac(im, fx0, fy0, fx1, fy1):
    w, h = im.size
    return im.crop((int(w * fx0), int(h * fy0), int(w * fx1), int(h * fy1)))
def fill(im, tw, th):
    tw, th = int(tw), int(th)
    r = max(tw / im.width, th / im.height)
    im2 = im.resize((int(im.width * r + 0.5), int(im.height * r + 0.5)), Image.LANCZOS)
    x = (im2.width - tw) // 2; y = (im2.height - th) // 2
    return im2.crop((x, y, x + tw, y + th))

base = Image.open(sorted(glob.glob(os.path.join(HERE, "media-generation-base-0-*.png")))[0]).convert("RGB")
sheet = Image.open(sorted(glob.glob(os.path.join(HERE, "media-generation-sheet-0-*.png")))[0]).convert("RGB")
ART = {
    "icj":     crop_frac(base, 0.045, 0.245, 0.484, 0.577),
    "summit":  crop_frac(base, 0.516, 0.245, 0.956, 0.577),
    "markets": crop_frac(base, 0.045, 0.603, 0.484, 0.947),
    "bridge":  crop_frac(base, 0.516, 0.603, 0.956, 0.947),
}
sw, sh = sheet.size
def cell(c, r):
    return sheet.crop((int(sw * (c / 3 + 0.010)), int(sh * (r / 2 + 0.014)),
                       int(sw * ((c + 1) / 3 - 0.010)), int(sh * ((r + 1) / 2 - 0.014))))
ART.update({"gta": cell(0, 0), "gaza": cell(1, 0), "cyclone": cell(2, 0),
            "cop31": cell(0, 1), "senate": cell(1, 1), "exam": cell(2, 1)})

M = 26 * S; CW = W - 2 * M; gap = 10 * S
# ---------- masthead ----------
f_kick = F(SANS_B, 13)
d.text((M, 14 * S), "T H E   W O R L D   I N   O N E   D A Y", font=f_kick, fill=RED)
r = "30 STORIES · EVERY CONTINENT"
d.text((W - M - d.textlength(r, font=f_kick), 14 * S), r, font=f_kick, fill=RED)
f_title = F(SERIF_B, 47)
t = "Thursday 19 November 2026"
d.text(((W - d.textlength(t, font=f_title)) / 2, 30 * S), t, font=f_title, fill=INK)
f_sub = F(SANS_I, 13.5)
sub = "Trump, Xi and Putin share one table · The World Court finds genocide in Myanmar · GTA VI unlocks worldwide"
d.text(((W - d.textlength(sub, font=f_sub)) / 2, 88 * S), sub, font=f_sub, fill=(70, 62, 48))
d.line([M, 110 * S, W - M, 110 * S], fill=INK, width=2 * S)
d.line([M, 114 * S, W - M, 114 * S], fill=INK, width=S)
# ---------- stats ----------
stats = [("3", "presidents, one table"), ("9–6", "World Court: genocide"),
         ("$81bn", "Anthropic record IPO"), ("13 yrs", "wait for GTA VI ends"),
         ("109–0", "Denmark–Greenland pact"), ("4.9%", "Australia jobless rate")]
f_num = F(SANS_B, 19); f_cap = F(SANS, 10)
cellw = CW // 6
for i, (n, c) in enumerate(stats):
    x = M + i * cellw
    if i: d.line([x, 124 * S, x, 152 * S], fill=LINE, width=S)
    d.text((x + 6 * S, 122 * S), n, font=f_num, fill=RED if i in (1, 2) else INK)
    d.text((x + 6 * S, 146 * S), c, font=f_cap, fill=GREY)
d.line([M, 160 * S, W - M, 160 * S], fill=LINE, width=S)
# ---------- heroes ----------
heroes = [
    ("summit", (28, 84, 140), "1 · SHENZHEN — SUMMIT", "Trump, Xi and Putin hold first three-way summit",
     "The US, Chinese and Russian leaders met on APEC's last day and issued a joint call on nuclear risk. Kyiv was not in the room. — Reuters, AP"),
    ("icj", (150, 108, 30), "2 · THE HAGUE — LAW", "World Court: Myanmar committed genocide",
     "Judges ruled 9–6 that Myanmar committed genocide against the Rohingya in 2017 — the first such ruling against a state. — UN News, BBC"),
    ("markets", (24, 110, 70), "3 · NEW YORK — MARKETS", "Anthropic's record IPO — yet Wall Street slides",
     "ANT priced at $83 in the largest IPO ever ($81.3bn raised), but the S&P 500 fell 2% and the Nikkei 4.7% on AI-bubble fears. — Dow Jones"),
]
f_cat = F(SANS_B, 11); f_hh = F(SANS_B, 16.5); f_deck = F(SANS, 11.5)
tw3 = (CW - 2 * gap) // 3; hy = 168 * S; hh = 216 * S
for i, (art, color, cat, head, deck) in enumerate(heroes):
    x = M + i * (tw3 + gap)
    d.rectangle([x, hy, x + tw3, hy + hh], fill=CARD, outline=LINE, width=S)
    img.paste(fill(ART[art], tw3, 100 * S), (x, hy))
    d.rectangle([x, hy + 100 * S, x + tw3, hy + 106 * S], fill=color)
    block(x + 9 * S, hy + 112 * S, tw3 - 18 * S, cat, f_cat, color, 13 * S)
    y = block(x + 9 * S, hy + 128 * S, tw3 - 18 * S, head, f_hh, INK, 20 * S)
    block(x + 9 * S, y + 3 * S, tw3 - 18 * S, deck, f_deck, (52, 48, 40), 14.5 * S)
# ---------- grid tiles with thumbs ----------
tiles = [
    ("gta", (112, 44, 140), "4 · WORLDWIDE — GAMES", "GTA VI finally goes on sale",
     "Rockstar's sequel unlocked at midnight local time — New Zealand first — 13 years after GTA V. PS5 and Xbox only; no PC yet."),
    ("bridge", (140, 40, 40), "5 · CRIMEA — WAR", "Ukraine hits Crimean Bridge again",
     "A third strike in four days: the rail section was hit overnight, traffic halted. Putin vowed a harsher response. — Euronews"),
    ("gaza", (140, 40, 40), "6 · GAZA — WAR", "Israeli armour pushes into central Gaza",
     "Tanks moved toward Salah al-Din Street as aid groups scored the peace plan at just 4 of 26 pledges kept. — Al Jazeera"),
    ("cyclone", (30, 110, 150), "7 · ODISHA — STORM", "Cyclone Akvan nears India's coast",
     "Red alert: thousands moved to safety in Odisha before landfall, expected Friday. Schools shut along the coast. — AP"),
    ("cop31", (24, 110, 70), "8 · ANTALYA — CLIMATE", "COP31 draft drops fossil fuels",
     "The slimmed draft drops the phase-out pledge; a $120bn adaptation goal is still open as talks run to Friday. — AFP"),
    ("senate", (28, 84, 140), "9 · WASHINGTON — IRAN", "Senate rejects Iran war-powers curb",
     "The bid to limit strikes on Iran failed 51–48, as Tehran warned it will not accept a war of attrition. — AP"),
]
f_th = F(SANS_B, 13.5); f_td = F(SANS, 10.5)
ty = hy + hh + gap; th = 118 * S
for r in range(2):
    for c in range(3):
        art, color, cat, head, deck = tiles[r * 3 + c]
        x = M + c * (tw3 + gap); y = ty + r * (th + gap)
        d.rectangle([x, y, x + tw3, y + th], fill=CARD, outline=LINE, width=S)
        img.paste(fill(ART[art], 96 * S, th), (x, y))
        tx = x + 104 * S
        block(tx, y + 7 * S, tw3 - 112 * S, cat, f_cat, color, 12 * S)
        yy = block(tx, y + 22 * S, tw3 - 112 * S, head, f_th, INK, 16.5 * S)
        block(tx, yy + 2 * S, tw3 - 112 * S, deck, f_td, (52, 48, 40), 13 * S)
# ---------- also ----------
ay = ty + 2 * th + gap + 6 * S
d.text((M, ay), "ALSO ON THURSDAY 19 NOVEMBER", font=F(SANS_B, 13), fill=RED)
d.line([M, ay + 19 * S, W - M, ay + 19 * S], fill=LINE, width=S)
also = [
    ("SEOUL —", "551,864 sit Korea's Suneung exam; flights paused for the listening test."),
    ("BOGOTÁ —", "Colombia's unions strike nationwide over the rescue tax bill."),
    ("CANBERRA —", "Jobless rate jumps to 4.9%, a five-year high."),
    ("JAKARTA —", "Parliament passes the asset-forfeiture law, 18 years on."),
    ("SENEGAL —", "Dozens missing after a migrant boat capsizes off Yenne."),
    ("YONGBYON —", "IAEA: North Korea is expanding its uranium plant."),
    ("LONDON —", "Gold falls to a 14-month low on rate-rise bets."),
    ("FLORIDA —", "Floods shut South Florida schools a second day."),
    ("DEEP SPACE —", "Voyager 1 reaches one light-day from Earth."),
    ("PORT-AU-PRINCE —", "Police kill 34 gang members in a capital raid."),
    ("MOGADISHU —", "Somalia expels the UAE ambassador."),
    ("ROME —", "Author Corrado Augias dies at 91."),
    ("SHENZHEN —", "APEC adopts the Shenzhen Outlook on trade and AI."),
    ("WASHINGTON —", "US loses its measles elimination status."),
    ("ODESA —", "Russian strike kills four, injures at least 13."),
    ("LATIN AMERICA —", "Hegseth tours the region on an anti-narcotics push."),
    ("PAKISTAN —", "Army says 22 militants killed in Khyber raids."),
    ("BELGRADE —", "Cupic elected speaker of Serbia's new parliament."),
    ("ULAANBAATAR —", "Parliament accepts President Khurelsukh's resignation."),
    ("CRETE —", "Frontex patrols step up amid migrant arrivals from Libya."),
    ("MEXICO CITY —", "EU–Mexico deal to remove 95% of farm tariffs."),
]
f_lead = F(SANS_B, 10); f_item = F(SANS, 10)
colw = (CW - 2 * gap) // 3; iy = ay + 26 * S
for i, (lead, body) in enumerate(also):
    x = M + (i // 7) * (colw + gap); y = iy + (i % 7) * 37 * S
    d.text((x, y), "▪ " + lead, font=f_lead, fill=INK)
    lw = d.textlength("▪ " + lead + " ", font=f_lead)
    lines = wrap(body, f_item, colw - lw)
    d.text((x + lw, y), lines[0], font=f_item, fill=(52, 48, 40))
    for j, ln in enumerate(lines[1:], 1):
        d.text((x, y + j * 12.5 * S), ln, font=f_item, fill=(52, 48, 40))
# ---------- footer ----------
fy = 972 * S
d.line([M, fy - 6 * S, W - M, fy - 6 * S], fill=INK, width=S)
f_foot = F(SANS, 10)
block(M, fy, CW, "DATE CHECK — every story on this page happened, or was first reported, on Thursday 19 November 2026, in some time zone. Claims are attributed, not stated as fact.", f_foot, GREY, 12.5 * S)
block(M, fy + 14 * S, CW, "Sources: BBC, Reuters, AP, AFP, Al Jazeera, UN News, Euronews, ABC, Xinhua, Dow Jones. Pictures: original illustrations. Page drawn in code.", f_foot, GREY, 12.5 * S)

img = img.resize((1024, 1024), Image.LANCZOS)
out = os.path.join(HERE, "entry3.png")
img.save(out, "PNG", optimize=True)
print(out, os.path.getsize(out), "bytes")
