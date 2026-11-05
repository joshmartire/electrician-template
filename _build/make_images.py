#!/usr/bin/env python3
"""Generates logo, favicons and the default social-share image from the brand config.
Needs Pillow, fontTools and brotli:  pip install pillow fonttools brotli
Run after changing the business name or colours:  python3 _build/make_images.py"""
import json, os, io, math
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "site.config.json")))
IMG = os.path.join(ROOT, "assets", "img")
os.makedirs(IMG, exist_ok=True)
ACCENT_HEX = (CFG.get("accent") or "#ffc929").strip()
HEAT_HEX = (CFG.get("accent_alt") or "#5cc8ff").strip()
BG, TEXT, MUTED = (8, 9, 11), (242, 239, 233), (160, 156, 148)
hexrgb = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
ACCENT, HEAT = hexrgb(ACCENT_HEX), hexrgb(HEAT_HEX)
LOGO_FILE = (CFG.get("logo") or "").strip()

def font(name, size):
    f = TTFont(os.path.join(ROOT, "assets", "fonts", name))
    f.flavor = None
    buf = io.BytesIO(); f.save(buf); buf.seek(0)
    return ImageFont.truetype(buf, size)

def mark(draw, x, y, s, w=None):
    """Electric mark: a square plate with a bolt cut through it and two contact stubs."""
    k = s / 40
    P = lambda pts: [(x + px * k, y + py * k) for px, py in pts]
    draw.rounded_rectangle(P([(3, 3), (37, 37)]), radius=7 * k, outline=TEXT, width=max(1, round(3 * k)))
    draw.polygon(P([(22.5, 6), (11, 22.5), (19, 22.5), (16.5, 34), (29, 17), (20.5, 17)]), fill=ACCENT)
    draw.line(P([(1.5, 20), (8, 20)]), fill=HEAT, width=max(1, round(3 * k)))
    draw.line(P([(32, 20), (38.5, 20)]), fill=HEAT, width=max(1, round(3 * k)))

name = CFG["business_name"]
first, rest = name.split(" ")[0].upper(), " ".join(name.split(" ")[1:]).upper()

# favicon.svg
open(os.path.join(IMG, "favicon.svg"), "w").write(
 '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#08090b"/>'
 '<path d="M22.5 5L10 23h8.5L16 35l14-18.5h-9z" fill="' + ACCENT_HEX + '"/></svg>')

for size, fname in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")]:
    S = size * 4
    im = Image.new("RGB", (S, S), BG); d = ImageDraw.Draw(im)
    pad = S * 0.14
    mark(d, pad, pad, S - 2 * pad)
    im.resize((size, size), Image.LANCZOS).save(os.path.join(IMG, fname))

# logo.png (for schema): the client's logo when supplied, otherwise mark + wordmark on dark
W, H = 1200, 300
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
mark(d, 40, 40, 220)
d.text((300, 52), first, font=font("anton-latin-400-normal.woff2", 140), fill=TEXT)
d.text((306, 218), rest or CFG["short_tagline"].upper(), font=font("barlow-condensed-latin-600-normal.woff2", 44), fill=MUTED)
bbox = d.textbbox((300, 52), first, font=font("anton-latin-400-normal.woff2", 140))
sub = d.textbbox((306, 218), rest or CFG["short_tagline"].upper(), font=font("barlow-condensed-latin-600-normal.woff2", 44))
im = im.crop((0, 0, min(W, max(bbox[2], sub[2], 700) + 50), H))
if LOGO_FILE:
    src = Image.open(os.path.join(ROOT, LOGO_FILE.lstrip("/"))).convert("RGBA")
    src = src.crop(src.getchannel("A").getbbox() or (0, 0, src.width, src.height))
    if src.width > 1200:
        src = src.resize((1200, round(src.height * 1200 / src.width)), Image.LANCZOS)
    im = src
im.save(os.path.join(IMG, "logo.png"))

# og-default.png 1200x630: circuit traces running into a glowing node, with the headline
W, H = 1200, 630
im = Image.new("RGB", (W, H), BG)
glow = Image.new("RGB", (W, H), BG); g = ImageDraw.Draw(glow)
vx, vy = 960, 300
for i in range(80):
    t = i / 80
    r = 520 * (1 - t)
    g.ellipse([vx - r, vy - r * .8, vx + r, vy + r * .8], fill=tuple(int(BG[k] + (HEAT[k] - BG[k]) * 0.30 * t) for k in range(3)))
im = Image.blend(im, glow, 1.0); d = ImageDraw.Draw(im)
for i in range(16):
    y = 40 + i * 36
    mid = 640 + (i % 5) * 50
    col = tuple(int(BG[k] + (ACCENT[k] - BG[k]) * (0.25 + 0.5 * (i % 3 == 0))) for k in range(3))
    d.line([(560, y), (mid - 80, y), (mid - 40, y + (18 if i % 2 else -18)), (mid, y + (18 if i % 2 else -18)), (vx, vy + (i - 8) * 4)], fill=col, width=2)
    d.ellipse([mid - 5, y + (18 if i % 2 else -18) - 5, mid + 5, y + (18 if i % 2 else -18) + 5], fill=col)
d.ellipse([vx - 14, vy - 14, vx + 14, vy + 14], fill=(235, 248, 255))
d.rectangle([0, H - 12, W // 2, H], fill=ACCENT); d.rectangle([W // 2, H - 12, W, H], fill=HEAT)
mark(d, 70, 60, 90)
d.text((182, 70), first, font=font("anton-latin-400-normal.woff2", 64), fill=TEXT)
big = font("anton-latin-400-normal.woff2", 120)
d.text((70, 200), "WIRED RIGHT.", font=big, fill=TEXT)
d.text((70, 330), "POWERED", font=big, fill=TEXT)
w2 = d.textlength("POWERED ", font=big)
d.text((70 + w2, 330), "SAFE.", font=big, fill=ACCENT)
d.text((74, 540), f"ELECTRICIANS  ·  INSTANT ESTIMATE  ·  {CFG['region_label'].upper()}", font=font("barlow-condensed-latin-600-normal.woff2", 32), fill=MUTED)
im.save(os.path.join(IMG, "og-default.png"), optimize=True)
print("Images written to assets/img/")
