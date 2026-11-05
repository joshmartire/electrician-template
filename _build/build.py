#!/usr/bin/env python3
"""
Electrician Website Template — static site generator.

Usage:  python3 _build/build.py
Reads:  _build/site.config.json, _build/content_*.py, _build/pages.py, _build/electric_art.py
Writes: the published site into the repository root (HTML pages, sitemap.xml, robots.txt, 404.html).

Per-client settings in site.config.json control the services offered ("services"), the brand colours
("accent", "accent_alt"), the logo ("logo"), the licence number ("licence_number"), the client's own work photos
("photos"; see _build/photos.py), the opening animation ("intro", "intro_scope"), the house wired as you scroll at
the top of the home page ("house_scene"), emergency wording ("emergency") and the instant electrical estimate's
pricing ("estimator").

Shared components (header, footer, CTA, schema, metadata) live in this file, so a change here updates
every page on the next build. Folders starting with "_" are never published.
"""
import json, os, re, html, posixpath, sys, math
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content_services import SERVICES as ALL_SERVICES
from content_cities import CITIES
from content_costs import COSTS, ASK
import pages as P
import photos as PH
import electric_art as EA

CFG = json.load(open(os.path.join(HERE, "site.config.json"), encoding="utf-8"))
ALL_SVC = {s["slug"]: s for s in ALL_SERVICES}
# ---- services the client offers (config "services"; empty = all). Removing a slug drops its pages, menu and footer
# links, related-service links, sitemap entries, form options and its estimate job. Links to it inside other
# services' text become plain text and are listed in _build/removed-service-mentions.txt so those sentences can be
# reworded.
_wanted = CFG.get("services") or [s["slug"] for s in ALL_SERVICES]
_unknown = [x for x in _wanted if x not in ALL_SVC]
if _unknown:
    sys.exit(f"site.config.json: unknown service slug(s) {_unknown}. Valid: {[s['slug'] for s in ALL_SERVICES]}")
SERVICES = [s for s in ALL_SERVICES if s["slug"] in _wanted]
if not SERVICES:
    sys.exit("site.config.json: services is empty. List at least one service slug.")
SVC = {s["slug"]: s for s in SERVICES}
ALL_OFFERED = len(SERVICES) == len(ALL_SERVICES)
REMOVED_MENTIONS = {}
CITY = {c["slug"]: c for c in CITIES}
CATS = [
    ("power", "Power & Panels", "Panel upgrades, EV chargers, generators and surge protection: the capacity and backup a modern home needs."),
    ("wiring", "Wiring & Lighting", "Rewiring, knob and tube, pot lights, outlets, renovations and hot tubs, done to code and inspected."),
    ("repair", "Repair, Safety & Commercial", "Troubleshooting, emergencies, safety inspections and electrical for businesses."),
]
CATS = [c for c in CATS if any(s["cat"] == c[0] for s in SERVICES)]

EST = dict(CFG.get("estimator") or {})
EST_ON = bool(EST.get("enabled", True))
if EST_ON:
    jobs = []
    for j in EST.get("jobs", []):
        if j.get("service") and j["service"] not in SVC:
            continue
        j = dict(j)
        j["inputs"] = [i for i in j.get("inputs", []) if not i.get("service") or i["service"] in SVC]
        jobs.append(j)
    EST["jobs"] = jobs
    if not jobs:
        EST_ON = False
    elif EST.get("default_job") not in [j["id"] for j in jobs]:
        EST["default_job"] = jobs[0]["id"]
INTRO_ON = bool(CFG.get("intro", True))
INTRO_SCOPE = CFG.get("intro_scope", "all")
HOUSE_ON = bool(CFG.get("house_scene", True))   # the house wired circuit by circuit at the top of the home page
EMERG = bool(CFG.get("emergency", True)) and "emergency-electrician" in SVC
ESA = CFG.get("inspection_short") or "ESA"
LICENCE = (CFG.get("licence_number") or "").strip()

def and_join(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]

def related_of(s):
    return [r for r in s["related"] if r in SVC]

# ---- brand colours (config "accent" + "accent_alt", #rrggbb). Derived shades keep every text/background pair at WCAG AA.
def _rgb(h):
    h = h.lstrip("#"); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
def _lum(h):
    v = [x / 255 for x in _rgb(h)]
    v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
def _mix(h, other, t):
    a, b = _rgb(h), _rgb(other); return "#%02x%02x%02x" % tuple(round(x + (y - x) * t) for x, y in zip(a, b))
def _darken_until(h, bg, target=4.5):
    t = 0.0
    while contrast(_mix(h, "#000000", t), bg) < target and t < 1:
        t += 0.02
    return _mix(h, "#000000", min(t, 1))

BG = "#08090b"
INK = "#120e00"   # dark text used on accent buttons and the CTA band
def _colour(key, default):
    v = (CFG.get(key) or default).strip()
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", v):
        sys.exit(f"site.config.json: {key} must be a #rrggbb colour (got {v!r}).")
    if contrast(v, BG) < 4.5 or contrast(INK, v) < 4.5:
        sys.exit(f"site.config.json: {key} {v} is too dark: it is used as text on the dark page and behind dark button text "
                 f"({contrast(v, BG):.1f}:1, needs 4.5:1). Pick a brighter version of the brand colour.")
    return v
ACCENT = _colour("accent", "#ffc929")
ALT = _colour("accent_alt", "#5cc8ff")
ACCENT_2 = _mix(ACCENT, "#ffffff", 0.3)
ACCENT_ON_PAPER = _darken_until(ACCENT, "#ecebe6")
ALT_ON_PAPER = _darken_until(ALT, "#ecebe6")

# ---- logo
LOGO_FILE = (CFG.get("logo") or "").strip()
if LOGO_FILE and not os.path.isfile(os.path.join(ROOT, LOGO_FILE.lstrip("/"))):
    sys.exit(f"site.config.json: logo file not found: {LOGO_FILE}")
LOGO_W, LOGO_H = 160, 44

def prep_logo():
    global LOGO_W, LOGO_H
    out = os.path.join(ROOT, "assets", "img", "client-logo.webp")
    if not LOGO_FILE:
        if os.path.exists(out): os.remove(out)
        return
    from PIL import Image
    im = Image.open(os.path.join(ROOT, LOGO_FILE.lstrip("/"))).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox() or (0, 0, im.width, im.height))
    if im.height > 240:
        im = im.resize((round(im.width * 240 / im.height), 240), Image.LANCZOS)
    im.save(out, "WEBP", quality=92, method=6)
    LOGO_W = max(1, round(im.width * LOGO_H / im.height))

PHOTOS = PH.load(CFG, ROOT, set(ALL_SVC), "site.config.json")
PHOTO_CLASSES = {"section": "section section--tight", "head": "sec-head", "kicker": "eyebrow", "h2": "display h-lg", "lead": "lead", "group_title": True}

BIZ = CFG["business_name"]
DOMAIN = CFG["domain"].rstrip("/")
BASE = CFG.get("base_path", "/")
PHONE = CFG["phone_display"]
TEL = CFG["phone_e164"]
CTA = CFG["cta_label"]
CITY_NAMES = [c["name"] for c in CITIES]

def city_list_text():
    return and_join(CITY_NAMES)

# ------------------------------------------------------------------ icons
UI = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
 "chev": '<path d="M6 9l6 6 6-6"/>',
 "plus": '<path d="M12 5v14M5 12h14"/>',
 "pin": '<path d="M12 22s7-6.4 7-12a7 7 0 0 0-14 0c0 5.6 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
 "check": '<path d="M4 12l5 5L20 6"/>',
 "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 "calc": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M8 6h8v4H8zM8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/>',
 "shield": '<path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
 "heat": '<path d="M14 14.8V4a2 2 0 0 0-4 0v10.8a4 4 0 1 0 4 0z"/><path d="M12 9v7"/>',
 "flicker": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.6 1 2.5h6c0-.9.2-1.7 1-2.5A6 6 0 0 0 12 3z"/><path d="M2 8l2 1M22 8l-2 1M5 2l1.5 1.5M19 2l-1.5 1.5"/>',
 "trip": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M10 7h4v6h-4z"/><path d="M12 16v2"/>',
 "smell": '<path d="M8 21c-2-3 2-5 0-9s2-6 0-9M12 21c-2-3 2-5 0-9s2-6 0-9M16 21c-2-3 2-5 0-9s2-6 0-9"/>',
 "old": '<rect x="4" y="3" width="16" height="18" rx="3"/><path d="M9 9v3M15 9v3M10 16a2 2 0 0 0 4 0"/>',
 "spark": '<path d="M12 2v4M12 18v4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M2 12h4M18 12h4M4.9 19.1l2.8-2.8M16.3 7.7l2.8-2.8"/>',
}
SVC_ICONS = {
 "panel": ['M5 2h14v20H5z', 'M8 5h8v3H8z', 'M8 11h3M13 11h3M8 14h3M13 14h3M8 17h3M13 17h3'],
 "ev": ['M3 17v-4l2-5h10l3 5h2v4h-2', 'M7 17h6', 'M5 17a2 2 0 1 0 4 0a2 2 0 1 0-4 0', 'M13 17a2 2 0 1 0 4 0a2 2 0 1 0-4 0', 'M11 3l-2 3h3l-2 3'],
 "generator": ['M3 8h18v11H3z', 'M6 19v2M18 19v2', 'M6 11h7M6 14h7', 'M16 11v5', 'M18 4l-2 3h3l-2 3'],
 "surge": ['M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10z', 'M13 6l-3 6h4l-3 6'],
 "wire": ['M2 7h5c3 0 3 10 6 10h9', 'M2 12h4c3 0 4-7 7-7h9', 'M2 17h6c2 0 3-5 6-5h8'],
 "knob": ['M2 6h20M2 14h20', 'M6 6a2 2 0 1 0 0 .01', 'M6 4.5v3M6 12.5v3M18 4.5v3M18 12.5v3', 'M10 10h4v8h-4z'],
 "potlight": ['M3 4h18', 'M8 4v2h8V4', 'M9 6l-4 14M15 6l4 14', 'M12 9v3M12 15v1'],
 "outlet": ['M5 2h14a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z', 'M9 8v3M15 8v3', 'M10 16a2 2 0 0 0 4 0'],
 "reno": ['M3 21V10l9-7 9 7v11', 'M9 21v-6h6v6', 'M14 9l-2 3h3l-2 3'],
 "hottub": ['M3 12h18v8H3z', 'M3 15h18', 'M8 9c-1-1.5 1-2.5 0-4M12 9c-1-1.5 1-2.5 0-4M16 9c-1-1.5 1-2.5 0-4'],
 "repair": ['M14.7 6.3a4 4 0 0 0-5.4 5l-6.5 6.5a1.6 1.6 0 0 0 2.3 2.3l6.5-6.5a4 4 0 0 0 5-5.4l-2.4 2.4-2.1-.4-.4-2.1z'],
 "bolt": ['M13 2L4 14h7l-1 8 9-12h-7z'],
 "inspect": ['M10 3a7 7 0 1 0 0 14a7 7 0 1 0 0-14', 'M21 21l-6-6', 'M7 10l2 2 4-4'],
 "commercial": ['M3 21V8l6-4v4l6-4v4l6-4v17z', 'M7 13h2M11 13h2M15 13h2M7 17h2M11 17h2M15 17h2'],
 "doc": ['M6 2h9l4 4v16H6z', 'M14 2v5h5', 'M9 12h7M9 16h7'],
 "home": ['M3 11l9-8 9 8', 'M5 9.5V21h14V9.5', 'M10 21v-6h4v6'],
 "calc": ['M5 2h14v20H5z', 'M8 5h8v4H8z', 'M8 13h.01M12 13h.01M16 13h.01M8 17h.01M12 17h.01M16 17h.01'],
}

def ui(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{UI[name]}</svg>'

def sicon(key, cls="svc-card__icon"):
    paths = "".join(f'<path pathLength="1" d="{d}"/>' for d in SVC_ICONS[key])
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{paths}</svg>'

# brand mark: a bolt cut through a square plate
LOGO_MARK = ('<svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true" focusable="false">'
             '<rect x="3" y="3" width="34" height="34" rx="7" fill="none" stroke="currentColor" stroke-width="3"/>'
             '<path d="M22.5 6L11 22.5h8L16.5 34 29 17h-8.5z" fill="var(--accent)"/>'
             '<path d="M3 20h5M32 20h5" stroke="var(--alt)" stroke-width="3" stroke-linecap="round"/></svg>')

# ------------------------------------------------------------------ opening animation: "power up"
# A breaker panel fades in out of the dark, its breakers flip on one by one with their lights coming on, the main
# breaker throws with a flash, sparks and a jolt, the business name flickers on like a tube light, then the light
# floods the screen and the page appears. Timings live in main.css (OPENING ANIMATION); main.js only starts it,
# lets a tap or key skip it, and removes it at the end.
INTRO_BREAKERS = 12

def _sparks(x_pct, y_pct, delay_ms, n=14, seed=1):
    out = ""
    for i in range(n):
        a = math.radians((i * 137.5 + seed * 53) % 360)
        d = 50 + ((i * 71 + seed * 29) % 130)
        out += (f'<i style="left:{x_pct}%;top:{y_pct}%;--dx:{math.cos(a) * d:.0f}px;--dy:{math.sin(a) * d:.0f}px;'
                f'--dl:{delay_ms + (i % 4) * 14}ms"></i>')
    return out

def intro_markup():
    brks = "".join(f'<span class="ib__b" style="--i:{i}"><i></i></span>' for i in range(INTRO_BREAKERS))
    words = BIZ.split(" ")
    name = html.escape(words[0]) + (f' <span>{html.escape(" ".join(words[1:]))}</span>' if len(words) > 1 else "")
    return f'''<div class="intro" aria-hidden="true">
<div class="intro__stage">
<div class="intro__grid"></div>
<div class="ib"><div class="ib__main"><span class="ib__lever"></span><b>Main</b></div><div class="ib__rows">{brks}</div></div>
<div class="intro__sparks">{_sparks(50, 30, 1580)}</div>
<div class="intro__brand"><p class="intro__name">{name}</p>
<div class="intro__meta"><span>{html.escape(CFG["region_label"])}</span><i></i><span>Powering up</span></div></div>
<div class="intro__flash"></div>
</div></div>'''

# ------------------------------------------------------------------ url helpers
def url_of(path):
    if path == "index.html":
        return DOMAIN + "/"
    if path.endswith("/index.html"):
        return DOMAIN + "/" + path[:-len("index.html")]
    return DOMAIN + "/" + path

def href(from_path, to_path):
    from_dir = posixpath.dirname(from_path)
    if to_path.endswith("index.html"):
        target_dir = posixpath.dirname(to_path)
        rel = posixpath.relpath(target_dir or ".", from_dir or ".")
        return "./" if rel == "." else rel + "/"
    return posixpath.relpath(to_path, from_dir or ".")

def asset(from_path, a):
    return posixpath.relpath("assets/" + a, posixpath.dirname(from_path) or ".")

_VER = {}
def vasset(from_path, a):
    """Asset URL with a content hash (?v=...), so browsers fetch the new file as soon as it changes after a deploy."""
    if a not in _VER:
        import hashlib
        _VER[a] = hashlib.md5(open(os.path.join(ROOT, "assets", a), "rb").read()).hexdigest()[:8]
    return asset(from_path, a) + "?v=" + _VER[a]

PATH = {
 "home": "index.html",
 "services": "services/index.html",
 "areas": "service-areas/index.html",
 "about": "about/index.html",
 "faq": "faq/index.html",
 "contact": "contact/index.html",
 "estimate": "electrical-estimate/index.html",
 "thanks": "thank-you/index.html",
 "privacy": "privacy-policy.html",
 "terms": "terms-and-conditions.html",
 "cookies": "cookie-policy.html",
}
def svc_path(slug): return f"services/{slug}/index.html"
def svc_city_path(slug, city): return f"services/{slug}/{city}/index.html"
def city_path(city): return f"service-areas/{city}/index.html"
def quote_path():
    """Where 'get a price' buttons go: the instant estimate when it's on, else the contact form."""
    return PATH["estimate"] if EST_ON else PATH["contact"]

def expand(text, here):
    """Replace {biz}/{phone}/{esa} tokens and [[slug|anchor]] links."""
    text = text.replace("{biz}", html.escape(BIZ)).replace("{phone}", html.escape(PHONE)).replace("{esa}", html.escape(ESA))
    def link(m):
        key, anchor = m.group(1), m.group(2)
        if key == "estimate" and not EST_ON: target = PATH["contact"]
        elif key.startswith("area:"): target = city_path(key[5:])
        elif key in PATH: target = PATH[key]
        elif key in SVC: target = svc_path(key)
        elif key in ALL_SVC:
            start = max(text.rfind(". ", 0, m.start()), text.rfind(">", 0, m.start())) + 1
            ends = [i for i in (text.find(". ", m.end()), text.find("<", m.end())) if i != -1]
            sentence = re.sub(r"\[\[[a-z0-9:\-]+\|([^\]]+)\]\]", r"\1", text[start:(min(ends) + 1 if ends else len(text))]).strip().rstrip("<").strip()
            REMOVED_MENTIONS.setdefault(sentence, set()).add(ALL_SVC[key]["name"])
            return anchor
        else: raise SystemExit(f"Unknown link target [[{key}]]")
        return f'<a href="{href(here, target)}">{anchor}</a>'
    return re.sub(r"\[\[([a-z0-9:\-]+)\|([^\]]+)\]\]", link, text)

# ------------------------------------------------------------------ shared components
def nav_html(here, active):
    def a(key, label):
        cur = ' aria-current="page"' if active == key else ""
        return f'<li class="nav__item"><a class="nav__link" href="{href(here, PATH[key])}"{cur}>{label}</a></li>'
    cols = ""
    for cat, label, _ in CATS:
        items = "".join(f'<li><a href="{href(here, svc_path(s["slug"]))}">{sicon(s["icon"], "")}{s["name"]}</a></li>' for s in SERVICES if s["cat"] == cat)
        cols += f'<div><p class="mega__title">{label}</p><ul>{items}</ul></div>'
    cols += f'<div class="mega__all"><span class="muted">{len(SERVICES)} services across {city_list_text()}</span><a class="link-arrow" href="{href(here, PATH["services"])}">All services {ui("arrow")}</a></div>'
    areas = "".join(f'<li><a href="{href(here, city_path(c["slug"]))}">{ui("pin")}{c["name"]}, {CFG["province"]}</a></li>' for c in CITIES)
    areas += f'<li><a href="{href(here, PATH["areas"])}">{ui("arrow")}All service areas</a></li>'
    svc_cur = ' aria-current="page"' if active == "services" else ""
    area_cur = ' aria-current="page"' if active == "areas" else ""
    est = ""
    if EST_ON:
        cur = ' aria-current="page"' if active == "estimate" else ""
        est = f'<li class="nav__item"><a class="nav__link nav__link--est" href="{href(here, PATH["estimate"])}"{cur}><i aria-hidden="true"></i>Instant Estimate</a></li>'
    return f'''<nav class="nav" aria-label="Main">
<ul class="nav__list">
<li class="nav__item" data-dropdown><button class="nav__link" type="button" aria-expanded="false" aria-controls="mega-services"{svc_cur}>Services {ui("chev")}</button>
<div class="mega mega--{len(CATS)}" id="mega-services">{cols}</div></li>
<li class="nav__item" data-dropdown><button class="nav__link" type="button" aria-expanded="false" aria-controls="mega-areas"{area_cur}>Service Areas {ui("chev")}</button>
<div class="mega mega--small" id="mega-areas"><div><p class="mega__title">Where we work</p><ul>{areas}</ul></div></div></li>
{est}{a("about", "About")}{a("faq", "FAQ")}{a("contact", "Contact")}
</ul>
<div class="nav__cta"><a class="nav__phone" href="tel:{TEL}">{ui("phone")}<span>{PHONE}</span><span class="visually-hidden"> (call us)</span></a>
<a class="btn btn--primary btn--sm" href="{href(here, PATH["contact"])}">{CTA}</a></div>
</nav>'''

def mobile_nav_html(here):
    groups = ""
    for cat, label, _ in CATS:
        items = "".join(f'<li><a href="{href(here, svc_path(s["slug"]))}">{s["name"]}</a></li>' for s in SERVICES if s["cat"] == cat)
        groups += f'<li><p class="mobile-nav__group">{label}</p><ul>{items}</ul></li>'
    groups += f'<li><a href="{href(here, PATH["services"])}">All services →</a></li>'
    areas = "".join(f'<li><a href="{href(here, city_path(c["slug"]))}">{c["name"]}</a></li>' for c in CITIES)
    est = f'<li><a class="mobile-nav__est" href="{href(here, PATH["estimate"])}">Instant Estimate</a></li>' if EST_ON else ""
    return f'''<div class="mobile-nav" id="mobile-nav">
<ul>
<li><a href="{href(here, PATH["home"])}">Home</a></li>
{est}
<li><details><summary>Services {ui("plus")}</summary><ul>{groups}</ul></details></li>
<li><details><summary>Service Areas {ui("plus")}</summary><ul>{areas}<li><a href="{href(here, PATH["areas"])}">All service areas →</a></li></ul></details></li>
<li><a href="{href(here, PATH["about"])}">About</a></li>
<li><a href="{href(here, PATH["faq"])}">FAQ</a></li>
<li><a href="{href(here, PATH["contact"])}">Contact</a></li>
</ul>
<div class="mobile-nav__cta"><a class="btn btn--primary" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a><a class="btn btn--ghost" href="tel:{TEL}">{ui("phone")} Call {PHONE}</a></div>
</div>'''

def brand_inner(here):
    if LOGO_FILE:
        return f'<img class="brand__logo" src="{asset(here, "img/client-logo.webp")}" alt="{html.escape(BIZ)}" width="{LOGO_W}" height="{LOGO_H}" decoding="async">'
    return f'{LOGO_MARK}<span class="brand__name">{html.escape(BIZ.split(" ")[0])} <small>{html.escape(" ".join(BIZ.split(" ")[1:]) or CFG["short_tagline"])}</small></span>'

def header_html(here, active):
    return f'''<div class="progress" aria-hidden="true"></div>
<header class="site-header">
<div class="wrap">
<a class="brand" href="{href(here, PATH["home"])}" aria-label="{html.escape(BIZ)} home">{brand_inner(here)}</a>
{nav_html(here, active)}
<button class="burger" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
</div>
</header>
{mobile_nav_html(here)}'''

def hours_text():
    return [f'{h["label"]}: {fmt_time(h["open"])}–{fmt_time(h["close"])}' for h in CFG.get("hours") or []]

def fmt_time(t):
    hh, mm = map(int, t.split(":"))
    suf = "a.m." if hh < 12 else "p.m."
    h12 = hh % 12 or 12
    return f"{h12}:{mm:02d} {suf}" if mm else f"{h12} {suf}"

def cta_band(here, title="Wired right. The first time.", text=None):
    text = text or ("See a ballpark for your job in about a minute, or book a visit for a written, itemized quote." if EST_ON
                    else "Book a visit and we'll give you a written, itemized quote before any work begins.")
    second = (f'<a class="btn btn--ghost" href="{href(here, PATH["estimate"])}">{ui("calc")} Instant estimate</a>' if EST_ON
              else f'<a class="btn btn--ghost" href="tel:{TEL}">{ui("phone")} {PHONE}</a>')
    return f'''<section class="cta-band" aria-labelledby="cta-title">
<div class="cta-band__flow" aria-hidden="true"></div>
<div class="wrap">
<div><h2 class="display" id="cta-title" data-reveal="rise">{title}</h2><p data-reveal="up">{text}</p></div>
<div class="btn-row" data-reveal="up"><a class="btn btn--primary" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a>{second}<a class="cta-band__tel" href="tel:{TEL}">or call {PHONE}</a></div>
</div>
</section>'''

def footer_html(here):
    cols = ""
    for cat, label, _ in CATS:
        items = "".join(f'<li><a href="{href(here, svc_path(s["slug"]))}">{s["name"]}</a></li>' for s in SERVICES if s["cat"] == cat)
        cols += f'<div class="footer__col"><h2>{label}</h2><ul>{items}</ul></div>'
    areas = "".join(f'<li><a href="{href(here, city_path(c["slug"]))}">{c["name"]}</a></li>' for c in CITIES)
    company = (f'<li><a href="{href(here, PATH["about"])}">About</a></li>'
               + (f'<li><a href="{href(here, PATH["estimate"])}">Instant Electrical Estimate</a></li>' if EST_ON else "")
               + f'<li><a href="{href(here, PATH["services"])}">All Services</a></li>'
               f'<li><a href="{href(here, PATH["areas"])}">Service Areas</a></li><li><a href="{href(here, PATH["faq"])}">FAQ</a></li><li><a href="{href(here, PATH["contact"])}">Contact</a></li>')
    hours = "<br>".join(hours_text())
    links = [("Google Business Profile", CFG.get("google_business_profile_url"))] + [(p.get("name"), p.get("url")) for p in CFG.get("social_profiles", [])]
    links = [(n, u) for n, u in links if u]
    profiles = ("<li><span>Find us</span>" + " · ".join(f'<a href="{html.escape(u)}" rel="noopener">{html.escape(n)}</a>' for n, u in links) + "</li>") if links else ""
    lic = f'<li><span>Licence</span>{html.escape(ESA)} LEC #{html.escape(LICENCE)}</li>' if LICENCE else ""
    return f'''<footer class="site-footer">
<div class="wrap">
<div class="footer__grid footer__grid--{len(CATS)}">
<div class="footer__brand">
<a class="brand" href="{href(here, PATH["home"])}" aria-label="{html.escape(BIZ)} home">{brand_inner(here)}</a>
<p>Electrical services for homes and businesses in {city_list_text()}, {CFG["province"]}: panels, EV chargers, wiring, lighting and repairs.</p>
<ul class="footer__contact">
<li><span>Call</span><a href="tel:{TEL}">{PHONE}</a></li>
<li><span>Email</span><a href="mailto:{CFG["email"]}">{CFG["email"]}</a></li>
<li><span>Hours</span>{hours}</li>
{lic}
{profiles}
</ul>
</div>
{cols}
<div class="footer__col"><h2>Service Areas</h2><ul>{areas}</ul><h2 class="mt-2">Company</h2><ul>{company}</ul></div>
</div>
<div class="footer__bottom">
<p>© {date.today().year} {html.escape(CFG["legal_name"])}. All rights reserved.</p>
<ul><li><a href="{href(here, PATH["privacy"])}">Privacy Policy</a></li><li><a href="{href(here, PATH["terms"])}">Terms &amp; Conditions</a></li><li><a href="{href(here, PATH["cookies"])}">Cookie Policy</a></li></ul>
</div>
</div>
</footer>
<div class="callbar"><a class="btn btn--ghost" href="tel:{TEL}">{ui("phone")} Call</a><a class="btn btn--primary" href="{href(here, quote_path())}">{"Instant Estimate" if EST_ON else CTA}</a></div>'''

def crumbs_html(here, trail):
    items = []
    for label, p in trail:
        items.append(f'<li><span aria-current="page">{label}</span></li>' if p is None else f'<li><a href="{href(here, p)}">{label}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'

def crumbs_schema(trail, here):
    lst = [{"@type": "ListItem", "position": i, "name": html.unescape(re.sub("<[^>]+>", "", label)), "item": url_of(p if p else here)} for i, (label, p) in enumerate(trail, 1)]
    return {"@type": "BreadcrumbList", "itemListElement": lst}

def business_ref():
    return {"@type": "Electrician", "@id": DOMAIN + "/#business", "name": BIZ, "url": DOMAIN + "/", "telephone": TEL}

def business_entity():
    e = {
        "@type": "Electrician",
        "@id": DOMAIN + "/#business",
        "name": BIZ,
        "description": f"Electrical contractor for homes and businesses in {city_list_text()}, {CFG['province']}: panel upgrades, EV chargers, rewiring, lighting, generators, repairs and inspections.",
        "url": DOMAIN + "/",
        "logo": DOMAIN + "/assets/img/logo.png",
        "image": DOMAIN + "/assets/img/og-default.png",
        "telephone": TEL,
        "email": CFG["email"],
        "areaServed": [{"@type": "City", "name": f'{c["name"]}, {CFG["province"]}'} for c in CITIES],
        "knowsAbout": [s["name"] for s in SERVICES],
    }
    if CFG.get("legal_name") and CFG["legal_name"] != BIZ:
        e["legalName"] = CFG["legal_name"]
    a = CFG.get("address")
    if a:
        e["address"] = {"@type": "PostalAddress", "streetAddress": a["street"], "addressLocality": a["city"], "addressRegion": a["region"], "postalCode": a["postal"], "addressCountry": CFG["country"]}
    if CFG.get("hours"):
        e["openingHoursSpecification"] = [{"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"], "opens": h["open"], "closes": h["close"]} for h in CFG["hours"]]
    same = [u for u in [CFG.get("google_business_profile_url")] + [p.get("url") for p in CFG.get("social_profiles", [])] if u]
    if same:
        e["sameAs"] = same
    return e

PAGES = []

def demo_bar():
    if not CFG.get("demo_mode"):
        return ""
    return ('<aside class="demo-bar" aria-label="Website demo notice">Website demo: the business name, phone, email, service areas and estimate pricing on this site are '
            'samples, not a real company.</aside>')

def page(path, *, title, desc, body, active=None, crumbs=None, schema=None, noindex=False, og_type="website", head_extra="", scripts_extra="", body_class=""):
    full_title = title if BIZ in title else f"{title} | {BIZ}"
    if len(full_title) > 65 and BIZ not in title:
        full_title = title
    robots = "noindex, follow" if (noindex or CFG.get("demo_mode")) else "index, follow"
    graph = list(schema or [])
    if crumbs:
        graph.append(crumbs_schema(crumbs, path))
    ld = ""
    if graph:
        ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"
    canonical = url_of(path) if path != "404.html" else DOMAIN + "/404.html"
    verify = f'<meta name="google-site-verification" content="{html.escape(CFG["google_site_verification"])}">' if CFG.get("google_site_verification") else ""
    # Opening animation: plays on whichever indexable page a visitor opens first in a browser session (e.g. a service
    # page from Google), then never again that session. Skipped when the URL has a #hash, for reduced motion, on the
    # 404 and thank-you pages, and everywhere when config "intro" is false ("intro_scope": "home" = home page only).
    intro_here = INTRO_ON and not noindex and (INTRO_SCOPE == "all" or path == "index.html")
    if intro_here:
        boot = ('<script>(function(d){d.className=d.className.replace("no-js","js");try{if(sessionStorage.getItem("el-intro")||location.hash.length>1||'
                'matchMedia("(prefers-reduced-motion: reduce)").matches)d.className+=" no-intro"}catch(e){d.className+=" no-intro"}})(document.documentElement)</script>')
    else:
        boot = '<script>document.documentElement.className=document.documentElement.className.replace("no-js","js");</script>'
    html_cls = "no-js" + (" has-demo" if CFG.get("demo_mode") else "") + ("" if intro_here else " no-intro")
    defs = EA.defs_svg() if ('class="house"' in body or 'class="ja ' in body or "hero-lines" in body) else ""
    out = f'''<!doctype html>
<html lang="en-CA" class="{html_cls}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
{verify}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{html.escape(BIZ)}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(BIZ)} — electricians in {html.escape(CFG["region_label"])}">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{BG}">
<link rel="icon" href="{asset(path, "img/favicon.svg")}" type="image/svg+xml">
<link rel="icon" href="{asset(path, "img/favicon-32.png")}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{asset(path, "img/apple-touch-icon.png")}">
<link rel="preload" href="{asset(path, "fonts/anton-latin-400-normal.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{asset(path, "fonts/barlow-latin-400-normal.woff2")}" as="font" type="font/woff2" crossorigin>
{head_extra}
<link rel="stylesheet" href="{vasset(path, "css/main.css")}">
<style>:root{{--accent:{ACCENT};--accent-2:{ACCENT_2};--accent-paper:{ACCENT_ON_PAPER};--alt:{ALT};--alt-paper:{ALT_ON_PAPER}}}</style>
{boot}
{ld}
</head>
<body{f' class="{body_class}"' if body_class else ""}>
<a class="skip-link" href="#main">Skip to content</a>
{defs}
{demo_bar()}
{intro_markup() if intro_here else ""}
{header_html(path, active)}
<main id="main">
{body}
</main>
{footer_html(path)}
<script src="{vasset(path, "js/main.js")}" defer></script>
{scripts_extra}
</body>
</html>
'''
    out = re.sub(r"\n{2,}", "\n", out)
    dest = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(dest) or ROOT, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(out)
    PAGES.append({"path": path, "url": canonical if path != "404.html" else None, "title": full_title, "noindex": noindex})

def page_hero(here, *, eyebrow, h1, lead, crumbs, ctas=True, mark_icon=None, est_cta=True, compact=False):
    mark = sicon(mark_icon, "page-hero__mark") if mark_icon else ""
    btns = ""
    if ctas:
        second = (f'<a class="btn btn--ghost" href="{href(here, PATH["estimate"])}">{ui("calc")} Instant estimate</a>' if (EST_ON and est_cta)
                  else f'<a class="btn btn--ghost" href="tel:{TEL}">{ui("phone")} {PHONE}</a>')
        btns = f'<div class="btn-row intro-fade" style="--d:500ms"><a class="btn btn--primary" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a>{second}</div>'
    return f'''<section class="page-hero{" page-hero--compact" if compact else ""}">
<div class="page-hero__flow" aria-hidden="true"></div>
<div class="wrap">
<div class="intro-fade">{crumbs_html(here, crumbs)}</div>
<p class="eyebrow intro-fade" style="--d:100ms">{eyebrow}</p>
<h1 class="display" data-split>{h1}</h1>
<p class="lead intro-fade" style="--d:350ms">{lead}</p>
{btns}
</div>
{mark}
</section>'''

def svc_card(here, s, n, heading="h3", target=None):
    t = target or svc_path(s["slug"])
    return (f'<a class="svc-card svc-card--{s["cat"]}" href="{href(here, t)}" data-reveal="up"><div class="svc-card__top">{sicon(s["icon"])}<span class="svc-card__no">{n:02d}</span></div>'
            f'<{heading}>{s["name"]}</{heading}><p>{s["short"]}</p><span class="svc-card__go">View service {ui("arrow")}</span></a>')

def faq_html(faqs):
    return '<div class="faq">' + "".join(
        f'<details><summary>{html.escape(q)}<i aria-hidden="true"></i></summary><div class="faq__a"><p>{html.escape(a)}</p></div></details>' for q, a in faqs) + "</div>"

def est_card(here):
    if not EST_ON:
        return ""
    return f'''<div class="aside-card aside-card--est" data-reveal="up"><p class="mono accent">Instant estimate</p><h2>Price your job</h2><p>EV chargers, panel upgrades, pot lights, generators and more. Pick the job, answer a few questions and see a ballpark in about a minute.</p>
<a class="btn btn--ghost" href="{href(here, PATH["estimate"])}">{ui("calc")} Start my estimate</a></div>'''

def emerg_card(here):
    if not EMERG:
        return ""
    return (f'<div class="aside-card aside-card--emerg" data-reveal="up"><p class="mono">{ui("bolt")} Urgent?</p><h2>Call now</h2>'
            f'<p>{html.escape(CFG.get("emergency_note") or "Sparks, burning smell or no power? Call now.")}</p><a class="btn btn--primary" href="tel:{TEL}">{ui("phone")} {PHONE}</a></div>')

def aside_html(here, s=None, city=None):
    hours = "<br>".join(hours_text())
    quote = f'''<div class="aside-card aside-card--accent" data-reveal="up"><h2>Get a quote</h2><p>Tell us about the job and we'll book a visit and give you a written, itemized quote.</p>
<a class="btn btn--primary" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a><a class="btn btn--ghost" href="tel:{TEL}">{ui("phone")} {PHONE}</a></div>'''
    blocks = [quote, est_card(here)]
    if s:
        rel = "".join(f'<li><a href="{href(here, svc_path(r) if not city else svc_city_path(r, city["slug"]))}">{SVC[r]["name"]}{" in " + city["name"] if city else ""}{ui("arrow")}</a></li>' for r in related_of(s))
        if rel:
            blocks.append(f'<div class="aside-card" data-reveal="up"><h2>Related services</h2><ul class="aside-list">{rel}</ul></div>')
        cl = "".join(f'<li><a href="{href(here, svc_city_path(s["slug"], c["slug"]))}"{" aria-current=\"page\"" if city and c["slug"] == city["slug"] else ""}>{s["name"]} in {c["name"]}{ui("arrow")}</a></li>' for c in CITIES)
        blocks.append(f'<div class="aside-card" data-reveal="up"><h2>Service areas</h2><ul class="aside-list">{cl}</ul></div>')
    blocks.append(emerg_card(here))
    blocks.append(f'<div class="aside-card" data-reveal="up"><h2>Hours</h2><p class="muted" style="margin:0">{hours}<br>{CFG.get("hours_note","")}</p></div>')
    return '<aside class="aside" aria-label="Electrical help">' + "".join(b for b in blocks if b) + "</aside>"

# ------------------------------------------------------------------ pages
def lower_name(s):
    """Service name for use mid-sentence, in lower case (keeps EV and similar acronyms)."""
    return re.sub(r"\bev\b", "EV", s["name"].lower())

def who_for(s):
    return "businesses and property managers" if s["cat"] == "repair" and s["slug"] == "commercial-electrical" else "homeowners"

def build_service(s):
    here = svc_path(s["slug"])
    cat_label = dict((c, l) for c, l, _ in CATS)[s["cat"]]
    crumbs = [("Home", PATH["home"]), ("Services", PATH["services"]), (s["name"], None)]
    cities = "".join(f'<a class="chip" href="{href(here, svc_city_path(s["slug"], c["slug"]))}">{ui("pin")}{s["name"]} in {c["name"]}</a>' for c in CITIES)
    content = f'''{page_hero(here, eyebrow=cat_label, h1=s["h1"], lead=s["lead"], crumbs=crumbs, mark_icon=s["icon"])}
<section class="section section--tight">
<div class="wrap article">
<div class="prose" data-reveal="up">
{expand(s["body"], here)}
<h2>What affects the cost of {lower_name(s)}</h2>
{COSTS[s["slug"]]}
<h2>{s["name"]} questions</h2>
{faq_html(s["faqs"])}
<h2>Where we offer {lower_name(s)}</h2>
<p>We provide {lower_name(s)} for {who_for(s)} in {city_list_text()}. See what to expect in your area:</p>
<div class="chips">{cities}</div>
</div>
{aside_html(here, s)}
</div>
</section>
{PH.gallery(PH.for_service(PHOTOS, s["slug"]), lambda x: asset(here, x[len("/assets/"):]), f"{s['name']}: our work", kicker="Our work", limit=3, classes=PHOTO_CLASSES)}
{cta_band(here)}'''
    schema = [{
        "@type": "Service", "@id": url_of(here) + "#service", "name": s["name"], "serviceType": s["name"],
        "description": s["desc"], "url": url_of(here), "provider": business_ref(),
        "areaServed": [{"@type": "City", "name": f'{c["name"]}, {CFG["province"]}'} for c in CITIES],
    }]
    page(here, title=s["title"], desc=s["desc"], body=content, active="services", crumbs=crumbs, schema=schema)

def build_service_city(s, c):
    here = svc_city_path(s["slug"], c["slug"])
    crumbs = [("Home", PATH["home"]), ("Services", PATH["services"]), (s["name"], svc_path(s["slug"])), (c["name"], None)]
    labels = re.findall(r"<li><strong>([^<]+)</strong>", s["body"])
    included = "".join(f"<li>{l}</li>" for l in labels)
    audience = "businesses" if s["slug"] == "commercial-electrical" else "homes"
    others = [x for x in CITIES if x["slug"] != c["slug"]]
    other_links = " and ".join(f'<a href="{href(here, svc_city_path(s["slug"], o["slug"]))}">{lower_name(s)} in {o["name"]}</a>' for o in others)
    rel_links = ", ".join(f'<a href="{href(here, svc_city_path(r, c["slug"]))}">{lower_name(SVC[r])}</a>' for r in related_of(s))
    rel_sentence = (f"People planning {lower_name(s)} in {c['name']} often look at related work too, including {rel_links}. " if rel_links else "")
    est_ok = EST_ON and any(j.get("service") == s["slug"] for j in EST["jobs"])
    est_line = (f' Want a ballpark first? Try the <a href="{href(here, PATH["estimate"])}">instant electrical estimate</a>.' if est_ok else "")
    body = f'''<h2>{s["name"]} for {c["name"]} {audience}</h2>
<p>{c["short"]} {s["cities"][c["slug"]]}</p>
<h2>What's included</h2>
<p>{s["short"]} Depending on your property, the work can include:</p>
<ul>{included}</ul>
<p>Full details, how the work runs and common questions are on our main <a href="{href(here, svc_path(s["slug"]))}">{lower_name(s)} page</a>.{est_line}</p>
<h2>Local conditions in {c["name"]}</h2>
<p>{c["cat"][s["cat"]]}</p>
<h2>Questions to ask before you hire</h2>
<p>Whoever you hire for {lower_name(s)} in {c["name"]}, get clear answers to these before signing:</p>
<ul>{"".join(f"<li>{q}</li>" for q in ASK[s["slug"]])}</ul>
<h2>Permits and inspections</h2>
<p>{c["permits"]}</p>
<h2>More from {html.escape(BIZ)} in {c["name"]}</h2>
<p>{rel_sentence}We also provide {other_links}. See every service we offer on our <a href="{href(here, city_path(c["slug"]))}">{c["name"]} service area page</a>.</p>'''
    content = f'''{page_hero(here, eyebrow=f'{c["name"]}, {CFG["province"]}', h1=f'{s["name"]} in {c["name"]}', lead=f'{s["name"]} for {c["name"]} {audience}: priced in writing, permitted, and done to pass inspection the first time.', crumbs=crumbs, mark_icon=s["icon"])}
<section class="section section--tight">
<div class="wrap article">
<div class="prose" data-reveal="up">{expand(body, here)}</div>
{aside_html(here, s, c)}
</div>
</section>
{cta_band(here, title=f"{s['name']} in {c['name']}? Let's talk.")}'''
    desc = f'{s["name"]} in {c["name"]}, {CFG["province"]}: {s["short"][0].lower() + s["short"][1:]}'
    desc = re.sub(r"\bev\b", "EV", desc)
    if len(desc) > 158:
        desc = desc[:155].rsplit(" ", 1)[0].rstrip(",") + "…"
    schema = [{
        "@type": "Service", "@id": url_of(here) + "#service", "name": f'{s["name"]} in {c["name"]}, {CFG["province"]}',
        "serviceType": s["name"], "url": url_of(here), "provider": business_ref(),
        "areaServed": {"@type": "City", "name": f'{c["name"]}, {CFG["province"]}'},
    }]
    page(here, title=f'{s["name"]} in {c["name"]}, {CFG["province"]}', desc=desc, body=content, active="services", crumbs=crumbs, schema=schema)

def svc_groups(here, heading="h3", city=None, head_tag="h2"):
    groups, n = "", 0
    for i, (cat, label, blurb) in enumerate(CATS, 1):
        cards = ""
        for s in SERVICES:
            if s["cat"] == cat:
                n += 1
                cards += svc_card(here, s, n, heading=heading, target=svc_city_path(s["slug"], city["slug"]) if city else None)
        title = f"{label} in {city['name']}" if city else label
        text = city["cat"][cat] if city else blurb
        groups += (f'<div class="svc-group svc-group--{cat}"><div class="svc-group__head" data-reveal="up"><span class="svc-group__num">0{i}</span><div><{head_tag} class="display h-md">{title}</{head_tag}>'
                   f'<p class="muted" style="margin:6px 0 0">{text}</p></div></div><div class="svc-grid" data-stagger>{cards}</div></div>')
    return groups

def build_services_hub():
    here = PATH["services"]
    crumbs = [("Home", PATH["home"]), ("Services", None)]
    content = f'''{page_hero(here, eyebrow="What we do", h1="Electrical Services", lead=f"{len(SERVICES)} electrical service{'s' if len(SERVICES) != 1 else ''} for homes and businesses in {city_list_text()}, from panel upgrades and EV chargers to rewiring, lighting, repairs and inspections.", crumbs=crumbs, mark_icon="panel")}
<section class="section section--tight"><div class="wrap">{svc_groups(here)}</div></section>
{cta_band(here)}'''
    items = [{"@type": "ListItem", "position": i, "url": url_of(svc_path(s["slug"])), "name": s["name"]} for i, s in enumerate(SERVICES, 1)]
    names = [lower_name(x) for x in SERVICES]
    desc = f"Electrical services in {city_list_text()}, {CFG['province']}: " + (", ".join(names[:5]) + " and more." if len(names) > 5 else and_join(names) + ".")
    if len(desc) > 158:
        desc = f"Electrical services in {city_list_text()}, {CFG['province']}: " + ", ".join(names[:3]) + " and more."
    page(here, title="Electrical Services", desc=desc, body=content, active="services", crumbs=crumbs, schema=[{"@type": "ItemList", "itemListElement": items}])

def build_city_hub(c):
    here = city_path(c["slug"])
    crumbs = [("Home", PATH["home"]), ("Service Areas", PATH["areas"]), (c["name"], None)]
    hub = "".join(f"<p>{p}</p>" for p in c["hub"])
    others = " · ".join(f'<a href="{href(here, city_path(o["slug"]))}">{o["name"]}</a>' for o in CITIES if o["slug"] != c["slug"])
    content = f'''{page_hero(here, eyebrow=f'Service area · {c["region"]}', h1=f'Electrician in {c["name"]}, {CFG["province"]}', lead=c["intro"], crumbs=crumbs, mark_icon="home")}
<section class="section section--tight"><div class="wrap">
<div class="hub-intro prose"><div data-reveal="up">{hub}</div><div data-reveal="up"><h2 class="h-sm" style="margin-top:0">Permits and inspections in {c["name"]}</h2><p>{c["permits"]}</p><p>Also serving: {others}</p></div></div>
{svc_groups(here, city=c)}
</div></section>
{cta_band(here, title=f"An electrician in {c['name']}? We're close by.")}'''
    page(here, title=c["title"], desc=c["desc"], body=content, active="areas", crumbs=crumbs)

def build_areas_hub():
    here = PATH["areas"]
    crumbs = [("Home", PATH["home"]), ("Service Areas", None)]
    cards = "".join(f'''<a class="area-card" href="{href(here, city_path(c["slug"]))}" data-reveal="up"><span class="area-card__no" aria-hidden="true">0{i}</span><div><h2>{c["name"]}</h2><p>{c["intro"]}</p><span class="svc-card__go">{len(SERVICES)} service{"s" if len(SERVICES) != 1 else ""} in {c["name"]} {ui("arrow")}</span></div></a>''' for i, c in enumerate(CITIES, 1))
    content = f'''{page_hero(here, eyebrow=CFG["region_label"], h1="Service Areas", lead=f"We do electrical work for homes and businesses in {city_list_text()}. Each area page covers local housing, wiring, permits and every service we offer there.", crumbs=crumbs, mark_icon="home")}
<section class="section section--tight"><div class="wrap"><div class="areas" data-stagger>{cards}</div>
<div class="prose mt-3" data-reveal="up"><p>Just outside these communities? <a href="{href(here, PATH["contact"])}">Contact us</a> with your address and what you need, and we'll let you know whether we can help.</p></div></div></section>
{cta_band(here)}'''
    page(here, title=f"Service Areas: {city_list_text()}", desc=f"Electrician serving {city_list_text()}, {CFG['province']}: local housing and wiring, permits and every electrical service we offer in your area.", body=content, active="areas", crumbs=crumbs)

def hero_picker(here):
    """Job picker in the hero card. A plain GET form to the estimate page, so it works without JavaScript."""
    if not EST_ON:
        return ""
    default = EST.get("default_job")
    opts = "".join(f'''<label class="pick"><input type="radio" name="job" value="{j["id"]}"{" checked" if j["id"] == default else ""}><span class="pick__box">{sicon(j.get("icon", "bolt"), "pick__icon")}<b>{html.escape(j["label"])}</b></span></label>''' for j in EST["jobs"])
    return f'''<form class="picker" action="{href(here, PATH["estimate"])}" method="get" aria-label="Instant electrical estimate">
<fieldset><legend class="picker__label">What do you need?</legend><div class="picker__grid">{opts}</div></fieldset>
<button class="btn btn--primary picker__go" type="submit"><span>Price my job</span>{ui("arrow")}</button>
</form>'''

def signs_html(p):
    items = "".join(f'<li class="sign" data-reveal="up"><span class="sign__ic">{ui(ic)}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for ic, t, d in p["signs"])
    call = (f'<a class="btn btn--primary" href="tel:{TEL}">{ui("phone")} Call {PHONE}</a>' if EMERG
            else f'<a class="btn btn--primary" href="{href(PATH["home"], PATH["contact"])}">Book a visit {ui("arrow")}</a>')
    insp = (f'<a class="btn btn--ghost" href="{href(PATH["home"], svc_path("electrical-inspections"))}">{ui("shield")} Book an inspection</a>' if "electrical-inspections" in SVC else "")
    return f'''<section class="section signs" aria-labelledby="signs-title">
<div class="signs__bg" aria-hidden="true"></div>
<div class="wrap">
<div class="sec-head"><div><p class="eyebrow">Know the warning signs</p><h2 class="display h-xl" id="signs-title" data-reveal="rise">Don't ignore<br><span class="outline">the flicker.</span></h2></div>
<p class="lead" data-reveal="up">Most electrical fires give a warning first. If anything on this list sounds familiar, have it checked before it becomes an emergency.</p></div>
<ol class="signs__list" data-stagger>{items}</ol>
<div class="signs__cta" data-reveal="up"><p><strong>Smoke or fire?</strong> Get out and call 911. <strong>Sparks, burning smell or partial power loss?</strong> Turn off the circuit if it's safe, then call us.</p><div class="btn-row">{call}{insp}</div></div>
</div></section>'''

def build_home():
    here = PATH["home"]
    p = P.home(CFG, CITIES, SERVICES, ALL_OFFERED)
    areas = "".join(f'<a href="{href(here, city_path(c["slug"]))}">{c["name"]}</a>' for c in CITIES)
    marquee_items = "".join(f'<span class="marquee__item">{s["name"]}</span>{ui("bolt", "marquee__star marquee__star--" + ("alt" if i % 2 else "acc"))}' for i, s in enumerate(SERVICES))
    feats = "".join(f'<div class="feature" data-reveal="up"><p class="feature__no" aria-hidden="true">0{i+1}</p><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(p["features"]))
    procs = "".join(f'<li class="proc" data-reveal="up"><span class="proc__no" aria-hidden="true">0{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(p["process"] if EST_ON else p["process"][1:]))
    area_cards = "".join(f'''<a class="area-card" href="{href(here, city_path(c["slug"]))}" data-reveal="up"><span class="area-card__no" aria-hidden="true">0{i}</span><div><h3>{c["name"]}</h3><p>{c["short"]}</p><span class="svc-card__go">Electrician in {c["name"]} {ui("arrow")}</span></div></a>''' for i, c in enumerate(CITIES, 1))
    foot = "".join(f'<div data-reveal="up"><h3>{t}</h3><p>{d}</p></div>' for t, d in p["statement_points"])
    tags = "".join(f'<li>{ui("check")}{t}</li>' for t in p["tags"])
    if EST_ON:
        hero_side = f'''<div class="hero__est intro-fade" style="--d:450ms">
<div class="hero__est-head"><span class="hero__live"><i></i>Instant estimate</span><span class="mono muted">About 60 seconds</span></div>
<p class="hero__est-title">Price your job<br><span class="accent">before anyone visits.</span></p>
{hero_picker(here)}
<ul class="hero__est-steps"><li><b>01</b>Job</li><li><b>02</b>Details</li><li><b>03</b>Price</li></ul>
</div>'''
        rows = [(j["label"], j.get("hint", "")) for j in EST["jobs"]]
        est_section = f'''<section class="section est-teaser" aria-labelledby="est-title">
<div class="wrap est-teaser__grid">
<div><p class="eyebrow">Instant electrical estimate</p><h2 class="display h-xl" id="est-title" data-reveal="rise">Know the number<br><span class="outline">before the visit.</span></h2>
<p class="lead mt-1" data-reveal="up">No waiting on a callback to find out whether the job fits your budget. Pick the job, answer a few quick questions and see a ballpark price right away.</p>
<ol class="est-teaser__steps" data-stagger><li data-reveal="up"><b>01</b><span><strong>Pick the job.</strong> {html.escape(and_join([j["label"] for j in EST["jobs"]]))}.</span></li>
<li data-reveal="up"><b>02</b><span><strong>Add the details.</strong> Distances, quantities, your panel and the options you want.</span></li>
<li data-reveal="up"><b>03</b><span><strong>See the range.</strong> {"The ESA permit and inspection are included, and the" if EST.get("permit_included") else "The"} price updates as you go.</span></li></ol>
<div class="btn-row mt-2" data-reveal="up"><a class="btn btn--primary" href="{href(here, PATH["estimate"])}">{ui("calc")} Get my instant estimate</a></div>
<p class="fine mt-1" data-reveal="up">A ballpark, not a quote. Your written price is confirmed after a site visit.</p></div>
<div class="est-teaser__art" data-reveal="scale">{EA.panel_svg(rows, "Illustration of a breaker panel schedule listing the jobs the instant estimate can price")}</div>
</div></section>'''
    else:
        hero_side = (f'<div class="hero__est hero__est--plain intro-fade" style="--d:450ms"><p class="hero__est-title">Lost power?<br><span class="accent">Something sparking?</span></p>'
                     f'<p class="hero__est-text">Call and we\'ll tell you what to do right now.</p><a class="btn btn--primary" href="tel:{TEL}">{ui("phone")} {PHONE}</a></div>')
        est_section = ""
    h = p["house"]
    circuits = [c for c in h["circuits"]]
    media = EA.house_svg("Illustration of a house in cross-section at night, with its service, panel, rooms, garage EV charger and backyard lit up by working circuits") if HOUSE_ON else EA.hero_lines_svg()
    hud = ""
    msgs = ""
    if HOUSE_ON:
        brk = "".join(f'<li data-c="{cid}"><i></i></li>' for cid, _, _ in circuits)
        hud = (f'<div class="house__hud" aria-hidden="true"><div class="house__hud-top"><span class="house__count"><b>00</b> / {len(circuits):02d}</span><span class="house__load"><b>000</b> A</span></div>'
               f'<p class="house__name">Power off</p><p class="house__detail">Scroll to wire the house</p><i class="house__meter"><b></b></i><ol class="house__brk">{brk}</ol></div>')
        msgs = "".join(f'<div class="hmsg" data-msg="{i}"><p class="hmsg__k">{html.escape(a)}</p><p class="hmsg__s">{html.escape(b)}</p></div>' for i, (a, b) in enumerate(h["messages"]))
        msgs += f'<div class="hmsg hmsg--final" data-msg="final"><p class="hmsg__k">{html.escape(h["final"][0])}</p><p class="hmsg__s">{html.escape(h["final"][1])}</p></div>'
        msgs = f'<div class="house__msgs" aria-hidden="true">{msgs}</div>'
    data = json.dumps([{"id": cid, "n": name, "d": det} for cid, name, det in circuits]).replace('"', "&quot;")
    emerg = (f'<p class="hero__emerg intro-fade" style="--d:1000ms"><a href="tel:{TEL}">{ui("bolt")}<span>{html.escape(CFG.get("emergency_note") or "")}</span><b>{PHONE}</b></a></p>' if EMERG else "")
    content = f'''<section class="hero{" house" if HOUSE_ON else ""}" aria-labelledby="hero-title"{f' data-house data-circuits="{data}"' if HOUSE_ON else ""}>
<div class="house__pin">
<div class="hero__media" aria-hidden="true"><div class="hero__glow"></div>{media}<div class="hero__shade"></div></div>
{hud}{msgs}
<div class="wrap hero__grid">
<div class="hero__copy">
<h1 id="hero-title"><span class="eyebrow intro-fade" style="--d:0ms">{p["eyebrow"]}</span><span class="display hero__title" data-split style="--base-delay:150ms"><span class="line">Wired right.</span> <span class="line">Powered <span class="hl">safe.</span></span></span></h1>
<p class="lead intro-fade" style="--d:650ms">{p["lead"]}</p>
<div class="btn-row intro-fade" style="--d:800ms"><a class="btn btn--primary" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a><a class="btn btn--ghost" href="tel:{TEL}">{ui("phone")} {PHONE}</a></div>
<p class="hero__areas intro-fade" style="--d:950ms"><span>Serving</span>{areas}</p>
{emerg}
</div>
{hero_side}
</div>
<ul class="hero__tags intro-fade" style="--d:1100ms">{tags}</ul>
<div class="scroll-cue" aria-hidden="true"><span>{"Scroll to power up" if HOUSE_ON else "Scroll"}</span><i></i></div>
</div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee__track"><div class="marquee__group">{marquee_items}</div><div class="marquee__group">{marquee_items}</div></div></div>
<section class="section statement" aria-labelledby="statement-title">
<div class="wrap">
<h2 class="eyebrow" id="statement-title">{p["statement_eyebrow"]}</h2>
<p class="fill-text" data-fill>{p["statement"]}</p>
<div class="statement__foot" data-stagger>{foot}</div>
</div>
</section>
<section class="section" aria-labelledby="services-title">
<div class="wrap">
<div class="sec-head"><div><p class="eyebrow">What we do</p><h2 class="display h-xl" id="services-title" data-reveal="rise">Panels. Power.<br><span class="outline">Done right.</span></h2></div><p class="lead" data-reveal="up">{p["services_lead"]}</p></div>
{svc_groups(here, heading="h4", head_tag="h3")}
<p class="mt-3 center" data-reveal="up"><a class="btn btn--ghost" href="{href(here, PATH["services"])}">Browse all services {ui("arrow")}</a></p>
</div>
</section>
{est_section}
{signs_html(p)}
{PH.gallery(PHOTOS, lambda x: asset(here, x[len("/assets/"):]), f"Recent work from {BIZ}", f"Real jobs from around {CFG['region_label']}.", classes=PHOTO_CLASSES)}
<section class="section section--tight" aria-labelledby="proc-title">
<div class="wrap">
<div class="sec-head"><div><p class="eyebrow">How it works</p><h2 class="display h-lg" id="proc-title" data-reveal="rise">From first call<br>to final inspection.</h2></div></div>
<ol class="procs" data-stagger>{procs}</ol>
</div>
</section>
<section class="section" aria-labelledby="why-title">
<div class="wrap">
<div class="sec-head"><div><p class="eyebrow">How we work</p><h2 class="display h-xl" id="why-title" data-reveal="rise">No shortcuts.<br><span class="outline">No surprises.</span></h2></div><p class="lead" data-reveal="up">{p["why_lead"]}</p></div>
<div class="features" data-stagger>{feats}</div>
</div>
</section>
<section class="section section--tight" aria-labelledby="areas-title" style="border-top:1px solid var(--line)">
<div class="wrap">
<div class="sec-head"><div><p class="eyebrow">Where we work</p><h2 class="display h-xl" id="areas-title" data-reveal="rise">Local to<br><span class="outline">{html.escape(CFG["region_label"])}.</span></h2></div><p class="lead" data-reveal="up">Every area page covers local housing, wiring and permits, along with every service we offer there.</p></div>
<div class="areas" data-stagger>{area_cards}</div>
</div>
</section>
<section class="section" aria-labelledby="faq-title">
<div class="wrap article" style="grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr)">
<div><p class="eyebrow">Questions</p><h2 class="display h-lg" id="faq-title" data-reveal="rise">Straight<br>answers.</h2><p class="lead mt-1" data-reveal="up">What homeowners ask us most, before they commit to anything.</p><p class="mt-2"><a class="link-arrow" href="{href(here, PATH["faq"])}">All FAQs {ui("arrow")}</a></p></div>
<div data-reveal="up">{faq_html(p["faqs"] if EST_ON else p["faqs"][1:])}</div>
</div>
</section>
{cta_band(here)}'''
    website = {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": BIZ, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-CA"}
    scripts = f'<script src="{vasset(here, "js/house.js")}" defer></script>' if HOUSE_ON else ""
    page(here, title=f"{BIZ} | Electrician, {CFG['region_label']}", desc=p["desc"], body=content, active="home", schema=[business_entity(), website], body_class="home", scripts_extra=scripts)

def money(v):
    return "${:,.0f}".format(v)

def build_estimate():
    if not EST_ON:
        return
    here = PATH["estimate"]
    crumbs = [("Home", PATH["home"]), ("Instant Electrical Estimate", None)]
    e = EST
    jobs = "".join(f'''<label class="opt opt--sys"><input type="radio" name="job" value="{j["id"]}"{" checked" if j["id"] == e.get("default_job") else ""}>
<span class="opt__box">{sicon(j.get("icon", "bolt"), "opt__icon")}<b>{html.escape(j["label"])}</b><small>{html.escape(j.get("hint", ""))}</small></span></label>''' for j in e["jobs"])

    def field(j, inp):
        k = f'{j["id"]}-{inp["id"]}'
        t = inp["type"]
        hint = f'<small class="muted inp__hint" id="h-{k}">{html.escape(inp["hint"])}</small>' if inp.get("hint") else ""
        dby = f' aria-describedby="h-{k}"' if inp.get("hint") else ""
        if t == "range":
            return (f'<div class="len" data-inp="{inp["id"]}"><label class="field-label" for="i-{k}">{html.escape(inp["label"])}</label>'
                    f'<div class="len__row"><label class="visually-hidden" for="r-{k}">{html.escape(inp["label"])}, slider</label><input class="len__range" id="r-{k}" type="range" min="{inp["min"]}" max="{inp["max"]}" step="{inp.get("step", 1)}" value="{inp["default"]}" data-range="{inp["id"]}">'
                    f'<div class="len__num"><input id="i-{k}" name="{k}" type="number" min="{inp["min"]}" max="{inp["max"]}" step="1" value="{inp["default"]}" inputmode="numeric" data-num="{inp["id"]}"{dby}><span>{html.escape(inp.get("unit", ""))}</span></div></div>{hint}</div>')
        if t == "choice":
            opts = "".join(f'<label class="opt"><input type="radio" name="{k}" value="{o["id"]}"{" checked" if n == 0 else ""}><span class="opt__box"><b>{html.escape(o["label"])}</b>{f"<small>{html.escape(o["hint"])}</small>" if o.get("hint") else ""}</span></label>' for n, o in enumerate(inp["options"]))
            return f'<fieldset class="opts" data-inp="{inp["id"]}"><legend>{html.escape(inp["label"])}</legend>{opts}</fieldset>'
        if t == "count":
            mx = inp.get("max", 20)
            return (f'<div class="gate-row" data-inp="{inp["id"]}"><div><span class="field-label" aria-hidden="true">{html.escape(inp["label"])}</span>{hint}</div>'
                    f'<div class="stepper"><button class="stepper__b" type="button" data-step="-1" aria-label="One fewer: {html.escape(inp["label"])}">−</button><label class="visually-hidden" for="i-{k}">{html.escape(inp["label"])}</label>'
                    f'<input id="i-{k}" name="{k}" type="number" min="0" max="{mx}" value="{inp.get("default", 0)}" inputmode="numeric"{dby}><button class="stepper__b" type="button" data-step="1" aria-label="One more: {html.escape(inp["label"])}">+</button></div></div>')
        return (f'<label class="chk chk--wide" data-inp="{inp["id"]}"><input type="checkbox" name="{k}" value="1"><span class="chk__box"><i aria-hidden="true">{ui("check")}</i><b>{html.escape(inp["label"])}</b><small class="chk__price">+{money(inp.get("add", 0))}</small></span></label>')

    groups = ""
    for j in e["jobs"]:
        inner = "".join(field(j, inp) for inp in j["inputs"])
        groups += f'<div class="job" data-job="{j["id"]}"{"" if j["id"] == e.get("default_job") else " hidden"}><h3 class="visually-hidden">{html.escape(j["label"])} details</h3>{inner}</div>'
    hidden = "".join(f'<input type="hidden" name="{n}" id="lead-{n.replace(" ", "-").lower()}" value="">' for n in ["Job", "Details", "Estimate shown"])
    sample = '<p class="est-sample" role="note">Demo pricing: the prices on this demo site are samples, set by each electrical contractor.</p>' if CFG.get("demo_mode") else ""
    cfg_js = {k: e[k] for k in ("jobs", "range_pct", "round_to", "minimum_job", "currency", "permit_included") if k in e}
    previews = "".join(f'<div class="est-art" data-art="{j["id"]}"{"" if j["id"] == e.get("default_job") else " hidden"}>{EA.job_art(j["id"])}</div>' for j in e["jobs"])
    permit = f'<p class="est-permit">{ui("shield")}<span>Includes the {html.escape(ESA)} permit and inspection.</span></p>' if e.get("permit_included") else ""
    tool = f'''<section class="est" id="estimator" aria-labelledby="est-tool-title">
<div class="wrap">
<h2 class="visually-hidden" id="est-tool-title">Electrical estimate tool</h2>
<noscript><div class="est-noscript"><p><strong>The instant estimate needs JavaScript.</strong> You can still <a href="{href(here, PATH["contact"])}">request a quote</a> or call <a href="tel:{TEL}">{PHONE}</a>.</p></div></noscript>
<div class="est__grid" data-estimator>
<form class="est__panel" id="est-form" novalidate>
<div class="est-card"><p class="est__step"><b>01</b> The job</p>
<fieldset class="opts opts--sys"><legend class="visually-hidden">Type of job</legend>{jobs}</fieldset></div>
<div class="est-card"><p class="est__step"><b>02</b> The details</p>{groups}</div>
</form>
<div class="est__side">
<div class="est-result" id="est-result">
<div class="est-preview" aria-hidden="true">{previews}<span class="est-preview__h" id="est-prev-h"></span></div>
<p class="est-result__label">Estimated price</p>
<p class="est-result__price" aria-live="polite"><span id="est-low">$0</span><i>–</i><span id="est-high">$0</span></p>
<p class="est-result__sum" id="est-sum">—</p>
<div class="est-notes" id="est-notes" aria-live="polite"></div>
<p class="fine" id="est-incl"></p>
{permit}
{sample}
<button class="btn btn--primary est-result__go" type="button" id="est-lead-open">Book my visit {ui("arrow")}</button>
</div>
<form class="form est-lead" id="est-lead" action="{html.escape(CFG["form_endpoint"])}" method="POST" data-validate novalidate hidden>
<p class="est__step"><b>03</b> Send it to us</p>
<p class="form__status" role="alert"></p>
<input type="hidden" name="_subject" value="New instant electrical estimate — {html.escape(BIZ)} website">
<input type="hidden" name="_next" value="{url_of(PATH["thanks"])}">
<input type="hidden" name="_template" value="table">
{hidden}
<div class="hp" aria-hidden="true"><label for="hp-est">Leave this field empty</label><input class="hp-input" id="hp-est" type="text" name="_honey" tabindex="-1" autocomplete="off"></div>
{_fld("lead-name", "Full name", '<input id="lead-name" name="name" type="text" autocomplete="name" required data-label="full name" aria-describedby="lead-name-error">')}
{_fld("lead-phone", "Phone", '<input id="lead-phone" name="phone" type="tel" autocomplete="tel" required data-label="phone number" aria-describedby="lead-phone-error">')}
{_fld("lead-email", "Email", '<input id="lead-email" name="email" type="email" autocomplete="email" required data-label="email address" aria-describedby="lead-email-error">', full=True)}
{_fld("lead-address", "Property address", '<input id="lead-address" name="address" type="text" autocomplete="street-address" aria-describedby="lead-address-error">', req=False, full=True)}
{_fld("lead-notes", "Anything we should know?", '<textarea id="lead-notes" name="message" rows="3" aria-describedby="lead-notes-error" placeholder="Panel size and age, the charger or fixtures you have, finished ceilings, timing…"></textarea>', req=False, full=True)}
<p class="form__privacy">We use your details only to follow up on this estimate and book a visit. See our <a href="{href(here, PATH["privacy"])}">Privacy Policy</a>.</p>
<div class="full"><button class="btn btn--primary" type="submit">Send my estimate {ui("arrow")}</button></div>
</form>
</div>
</div>
</div>
<div class="est-live" id="est-live" aria-hidden="true"><div><span class="est-live__k">Your estimate</span><span class="est-live__v" id="est-live-v">—</span></div><a class="btn btn--primary" href="#est-result" tabindex="-1">Details</a></div>
<script type="application/json" id="est-config">{json.dumps(cfg_js).replace("</", "<\\/")}</script>
</section>'''
    job_list = "".join(f"<li><strong>{html.escape(j['label'])}</strong> — includes {html.escape(j.get('includes', 'the parts and labour for the job'))}.</li>" for j in e["jobs"])
    explain = f'''<section class="section section--tight"><div class="wrap article">
<div class="prose" data-reveal="up">
<h2>How the instant estimate works</h2>
<p>Each job starts from {html.escape(BIZ)}'s typical price for that work. The tool adds the options you choose, such as the distance from your panel, the number of fixtures, your panel size and extras, then shows the result as a range. {"The " + html.escape(ESA) + " permit and inspection are included in the price." if e.get("permit_included") else ""}</p>
<p>Measure distances along the route a wire would actually take, along walls and through the basement, not in a straight line. If you're not sure of your panel size, look at the number on the main breaker at the top of the panel, or choose "Not sure".</p>
<h2>What each job includes</h2>
<ul>{job_list}</ul>
<h2>Why the final price can differ</h2>
<p>Some costs can't be known without seeing the house: the condition and capacity of the panel, how the wire can be routed, plaster or finished ceilings, what's found inside the walls, code updates that become required when work is done, and any utility charges. That's why the estimate is a range and your actual price is confirmed in a written quote after a site visit. For rewiring, renovations and commercial work, <a href="{href(here, PATH["contact"])}">contact us</a> for a quote.</p>
<h2>Instant estimate questions</h2>
{faq_html([
("Is the instant estimate a quote?", "No. It's a ballpark based on the options you choose. Your actual price comes in a written quote after a site visit."),
("Do you see my choices when I use the tool?", "No. The estimate is calculated in your browser, and nothing is sent to us unless you submit the form."),
("Does the estimate include utility charges?", "No. Where a job needs the utility, such as a service upgrade, any utility charges are confirmed separately."),
])}
</div>
{aside_html(here)}
</div></section>'''
    content = f'''{page_hero(here, eyebrow="Instant electrical estimate", h1="Instant Electrical Estimate", lead="Pick the job, answer a few quick questions, and see a ballpark price in about a minute. Nothing is sent to us until you choose to.", crumbs=crumbs, ctas=False, mark_icon="calc", compact=True)}
{tool}
{explain}
{cta_band(here, title="Ready for the real number?", text="Book a visit and we'll confirm the price in a written, itemized quote.")}'''
    scripts = f'<script src="{vasset(here, "js/estimate.js")}" defer></script>'
    schema = [{"@type": "WebApplication", "name": f"{BIZ} Instant Electrical Estimate", "url": url_of(here), "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": e.get("currency", "CAD")}, "provider": business_ref()}]
    names = [j["label"] for j in e["jobs"]]
    desc = f"Get a ballpark price for {and_join([n.lower().replace('ev ', 'EV ') for n in names[:4]])} in about a minute, with your options and the permit."
    if len(desc) > 158:
        desc = "Get a ballpark price for an EV charger, panel upgrade, pot lights or generator hookup in about a minute."
    page(here, title="Instant Electrical Estimate: EV Chargers, Panels & More", desc=desc,
         body=content, active="estimate", crumbs=crumbs, schema=schema, scripts_extra=scripts, body_class="page-estimate")

def _fld(id_, label, inp, req=True, full=False, hint=""):
    r = ' <span class="req" aria-hidden="true">*</span>' if req else ' <span class="muted">(optional)</span>'
    h = f'<span class="field__hint" id="{id_}-hint">{hint}</span>' if hint else ""
    return f'<div class="field{" full" if full else ""}"><label for="{id_}">{label}{r}</label>{inp}{h}<span class="field__error" id="{id_}-error" aria-live="polite"></span></div>'

def build_simple(key, *, title, desc, eyebrow, h1, lead, inner, mark="home", active=None, noindex=False, aside=True, schema=None, cta=True, hero_ctas=True):
    here = PATH[key]
    crumbs = [("Home", PATH["home"]), (h1, None)]
    side = aside_html(here) if aside else ""
    grid = "article" if aside else ""
    content = f'''{page_hero(here, eyebrow=eyebrow, h1=h1, lead=lead, crumbs=crumbs, mark_icon=mark, ctas=hero_ctas)}
<section class="section section--tight"><div class="wrap {grid}"><div class="prose" data-reveal="up">{expand(inner(here), here)}</div>{side}</div></section>
{cta_band(here) if cta else ""}'''
    page(here, title=title, desc=desc, body=content, active=active, crumbs=crumbs, noindex=noindex, schema=schema)

def build_contact():
    here = PATH["contact"]
    crumbs = [("Home", PATH["home"]), ("Contact", None)]
    svc_opts = "".join(f'<option>{s["name"]}</option>' for s in SERVICES) + "<option>Not sure / something else</option>"
    city_opts = "".join(f'<option>{c["name"]}</option>' for c in CITIES) + "<option>Another area</option>"
    panel_opts = "".join(f"<option>{x}</option>" for x in ["Not sure", "60 A or fuses", "100 A", "125 A", "200 A", "400 A"])
    form = f'''<form class="form" action="{html.escape(CFG["form_endpoint"])}" method="POST" data-validate novalidate>
<p class="form__status" role="alert"></p>
<input type="hidden" name="_subject" value="New electrical quote request — {html.escape(BIZ)} website">
<input type="hidden" name="_next" value="{url_of(PATH["thanks"])}">
<input type="hidden" name="_template" value="table">
<div class="hp" aria-hidden="true"><label for="hp-field">Leave this field empty</label><input class="hp-input" id="hp-field" type="text" name="_honey" tabindex="-1" autocomplete="off"></div>
{_fld("name", "Full name", '<input id="name" name="name" type="text" autocomplete="name" required data-label="full name" aria-describedby="name-error">')}
{_fld("phone", "Phone", '<input id="phone" name="phone" type="tel" autocomplete="tel" required data-label="phone number" aria-describedby="phone-error">')}
{_fld("email", "Email", '<input id="email" name="email" type="email" autocomplete="email" required data-label="email address" aria-describedby="email-error">')}
{_fld("city", "Property location", f'<select id="city" name="city" required data-label="property location" aria-describedby="city-error"><option value="">Select an area</option>{city_opts}</select>')}
{_fld("service", "What do you need?", f'<select id="service" name="service" required data-label="type of work" aria-describedby="service-error"><option value="">Select a service</option>{svc_opts}</select>')}
{_fld("panel", "Main panel size", f'<select id="panel" name="panel size" aria-describedby="panel-error">{panel_opts}</select>', req=False)}
{_fld("message", "Tell us about the job", '<textarea id="message" name="message" required data-label="job details" aria-describedby="message-hint message-error"></textarea>', full=True, hint="What you'd like done, the age of the house, any problems you've noticed, and when you'd like it done.")}
<p class="form__privacy">We use the information you submit only to respond to your request and prepare a quote. See our <a href="{href(here, PATH["privacy"])}">Privacy Policy</a>.</p>
<div class="full"><button class="btn btn--primary" type="submit">Send request {ui("arrow")}</button></div>
</form>'''
    hours = "<br>".join(hours_text())
    est_tip = (f'<div class="aside-card aside-card--est mt-2"><p class="mono accent">Want a number first?</p><h2>Instant estimate</h2><p>See a ballpark price for an EV charger, panel upgrade, pot lights and more before you send anything.</p><a class="btn btn--ghost" href="{href(here, PATH["estimate"])}">{ui("calc")} Start my estimate</a></div>' if EST_ON else "")
    urgent = (f'<p class="gas-note">{ui("bolt")}<span><strong>Sparks, a burning smell or lost power?</strong> Don\'t use the form. Call us now at <a href="tel:{TEL}">{PHONE}</a>. If there\'s smoke or fire, call 911.</span></p>' if EMERG
              else f'<p class="gas-note">{ui("bolt")}<span><strong>Smoke or fire?</strong> Call 911 first.</span></p>')
    content = f'''{page_hero(here, eyebrow="Contact", h1="Get an Electrical Quote", lead="Tell us about the job. We'll follow up to book a visit and give you a written, itemized quote.", crumbs=crumbs, ctas=False, mark_icon="outlet")}
<section class="section section--tight"><div class="wrap contact-grid">
<div class="contact-panel" data-reveal="up"><h2 class="display h-md" style="margin-bottom:24px">Your project</h2>{form}</div>
<div data-reveal="up"><ul class="info-list">
<li><span>Call</span><a href="tel:{TEL}">{PHONE}</a></li>
<li><span>Email</span><a class="info-list__email" href="mailto:{CFG["email"]}">{CFG["email"]}</a></li>
<li><span>Hours</span><p style="margin:0">{hours}<br><span class="muted">{CFG.get("hours_note","")}</span></p></li>
<li><span>Service area</span><p style="margin:0">{" · ".join(f'<a class="info-list__link" href="{href(here, city_path(c["slug"]))}">{c["name"]}</a>' for c in CITIES)}</p></li>
</ul>
{urgent}
<div class="prose mt-2"><h2 class="h-sm">What happens next</h2><ol><li><strong>We review your request</strong> and follow up by phone or email.</li><li><strong>Site visit.</strong> We look at the panel, the route and the work, and answer your questions.</li><li><strong>Written quote.</strong> You receive an itemized quote, permit included, to review on your own time.</li></ol>
<p class="muted">Tip: a photo of your panel with the door open, and the label on the main breaker, helps us quote faster.</p></div>
{est_tip}
</div>
</div></section>'''
    schema = [{"@type": "ContactPage", "url": url_of(here), "name": f"Contact {BIZ}", "about": {"@id": DOMAIN + "/#business"}}]
    page(here, title="Contact & Electrical Quote", desc=f"Request an electrical quote from {BIZ}. Call {PHONE} or send details about the panel, charger, wiring, lighting or repair you need.", body=content, active="contact", crumbs=crumbs, schema=schema)

def build_404():
    here = "404.html"
    global href, asset
    rel_href, rel_asset = href, asset
    def abs_href(_from, to):
        if to == "index.html": return BASE
        if to.endswith("index.html"): return BASE + to[:-len("index.html")]
        return BASE + to
    href = abs_href
    asset = lambda _f, a: BASE + "assets/" + a  # vasset() builds on asset(), so the 404 gets root-based versioned URLs
    links = "".join(f'<li><a href="{abs_href(None, svc_path(s["slug"]))}">{s["name"]}</a></li>' for s in SERVICES[:10])
    content = f'''<section class="notfound"><div class="wrap">
<p class="notfound__code" aria-hidden="true">404</p>
<h1 class="display h-lg mt-1">This page tripped the breaker.</h1>
<p class="lead mt-1">The page you're looking for may have moved or no longer exists. Try one of these instead:</p>
<div class="btn-row mt-2"><a class="btn btn--primary" href="{BASE}">Back to home {ui("arrow")}</a><a class="btn btn--ghost" href="{abs_href(None, PATH["services"])}">All services</a><a class="btn btn--ghost" href="{abs_href(None, PATH["contact"])}">Contact us</a></div>
<div class="prose mt-3"><h2 class="h-sm">Popular services</h2><ul style="columns:2;max-width:640px">{links}</ul></div>
</div></section>'''
    page(here, title="Page Not Found", desc="The page you're looking for couldn't be found.", body=content, noindex=True)
    href, asset = rel_href, rel_asset

def write_sitemap_robots():
    urls = [p for p in PAGES if p["url"] and not p["noindex"]]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"  <url><loc>{html.escape(p['url'])}</loc></url>" for p in urls]
    xml.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    return len(urls)

def write_cname():
    host = re.sub(r"^https?://", "", DOMAIN).strip("/")
    cname = os.path.join(ROOT, "CNAME")
    if "example.com" in host or host.endswith(".pages.dev"):
        if os.path.exists(cname): os.remove(cname)
        return None
    open(cname, "w").write(host + "\n")
    return host

def main():
    import shutil
    for d in ("services", "service-areas", "electrical-estimate"):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    prep_logo()
    PH.process(PHOTOS, ROOT)
    PH.ensure_css(os.path.join(ROOT, "assets", "css", "main.css"))
    try:
        import runpy
        runpy.run_path(os.path.join(HERE, "make_images.py"), run_name="__main__")
    except ImportError as e:
        print(f"WARNING: brand images not regenerated ({e}). pip install pillow fonttools brotli")
    build_home()
    build_estimate()
    build_services_hub()
    for s in SERVICES:
        build_service(s)
        for c in CITIES:
            build_service_city(s, c)
    build_areas_hub()
    for c in CITIES:
        build_city_hub(c)
    for key, spec in P.simple_pages(CFG, CITIES, SERVICES, city_list_text(), ALL_OFFERED).items():
        build_simple(key, **spec)
    build_contact()
    build_404()
    n = write_sitemap_robots()
    host = write_cname()
    json.dump([{"path": p["path"], "url": p["url"], "title": p["title"], "indexable": bool(p["url"]) and not p["noindex"]} for p in PAGES],
              open(os.path.join(HERE, "page-inventory.json"), "w"), indent=1)
    print(f"Built {len(PAGES)} pages, {n} URLs in sitemap.xml. CNAME: {host or 'not written (demo or example domain)'}")
    if CFG.get("demo_mode"):
        print("WARNING: demo_mode is ON. Every page has noindex and the demo banner. Set demo_mode to false at launch.")
    review = os.path.join(HERE, "removed-service-mentions.txt")
    if REMOVED_MENTIONS:
        with open(review, "w", encoding="utf-8") as f:
            f.write("Sentences that mention services this client does NOT offer. The links were turned into plain text,\n"
                    "but the wording may still imply the service is offered. Reword or remove each one in _build/content_*.py\n"
                    "or _build/pages.py, then rebuild until this file is gone.\n\n")
            for sent, names in sorted(REMOVED_MENTIONS.items()):
                f.write(f"- [{', '.join(sorted(names))}] {sent}\n")
        print(f"CLIENT REVIEW: {len(REMOVED_MENTIONS)} sentence(s) mention services this client does not offer. See _build/removed-service-mentions.txt")
    elif os.path.exists(review):
        os.remove(review)
    if not LOGO_FILE:
        print("CLIENT INPUT NEEDED: no client logo file (config 'logo'); the built-in mark and business name are used.")
    if not LICENCE:
        print("CLIENT INPUT NEEDED: no ESA licence number (config 'licence_number'); the footer and about page leave it out.")
    if not PHOTOS:
        print("CLIENT INPUT NEEDED: no work photos (config 'photos'); photo sections are hidden.")
    for k in ["domain", "phone_display", "email", "form_endpoint"]:
        if "example" in str(CFG[k]) or "555-01" in str(CFG[k]):
            print(f"WARNING: {k} still has a sample value: {CFG[k]}")
    if EST_ON:
        print("Instant estimate jobs: " + ", ".join(j["label"] for j in EST["jobs"]) + f" (±{EST['range_pct']}%)."
              + (" CLIENT INPUT NEEDED: set the client's real prices." if CFG.get("demo_mode") else ""))

if __name__ == "__main__":
    main()
