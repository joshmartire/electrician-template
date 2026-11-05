# -*- coding: utf-8 -*-
"""Every drawing on the site, as inline SVG (no image files, no outside requests).

house_svg()       the cut-away house at the top of the home page, wired circuit by circuit as the visitor scrolls
                  (assets/js/house.js drives it: each [data-c] wire gets --w 0..1, each [data-room] gets .is-lit)
hero_lines_svg()  circuit traces behind the hero when the house scene is off (config "house_scene": false)
panel_svg()       the breaker panel on the home page's estimate teaser
job_art(id)       the preview in the instant estimate's result card, one per job type
defs_svg()        shared gradients, included once per page that uses any drawing

Colours come from CSS custom properties (--accent, --alt), so the drawings follow the client's brand colours.
"""
import html

GROUND = 700


def defs_svg():
    return '''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<radialGradient id="eg-warm" cx="50%" cy="0%" r="95%"><stop offset="0" stop-color="#ffe7a8" stop-opacity=".55"/><stop offset=".45" stop-color="#ffc35a" stop-opacity=".18"/><stop offset="1" stop-color="#ffb02e" stop-opacity="0"/></radialGradient>
<linearGradient id="eg-cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2c4" stop-opacity=".55"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></linearGradient>
<radialGradient id="eg-bulb"><stop offset="0" stop-color="#fffbe8"/><stop offset=".35" stop-color="#ffe08a" stop-opacity=".9"/><stop offset="1" stop-color="#ffc94a" stop-opacity="0"/></radialGradient>
<radialGradient id="eg-cool"><stop offset="0" stop-color="#bfeaff" stop-opacity=".9"/><stop offset=".5" stop-color="#5cc8ff" stop-opacity=".35"/><stop offset="1" stop-color="#5cc8ff" stop-opacity="0"/></radialGradient>
<linearGradient id="eg-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070c"/><stop offset=".7" stop-color="#0b1220"/><stop offset="1" stop-color="#121a2a"/></linearGradient>
<linearGradient id="eg-earth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14110d"/><stop offset="1" stop-color="#0a0908"/></linearGradient>
<pattern id="eg-hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0v10" stroke="#2a241c" stroke-width="2"/></pattern>
</defs></svg>'''


# ------------------------------------------------------------------ house scene
# Wire routes start at the top of the panel in the basement and run through the joists to each room.
WIRES = [
    ("kitchen",  "M458 750V714H985V548H1150M985 548H835"),
    ("living",   "M464 750V720H610V548H790M610 548H450"),
    ("bedrooms", "M470 750V726H800V398H1150M800 398H450"),
    ("basement", "M476 750V732H1150"),
    ("garage",   "M482 750V738H1160V628H1186"),
    ("exterior", "M450 806H322V652"),
]


def _cone(x, y, w, h, cls="cone"):
    return f'<path class="{cls}" d="M{x - 6} {y}L{x - w} {y + h}H{x + w}L{x + 6} {y}z" fill="url(#eg-cone)"/>'


def _pot(x, y):
    return f'<g class="fx"><rect class="fx-can" x="{x - 9}" y="{y - 3}" width="18" height="5" rx="1.5"/><circle class="fx-glow" cx="{x}" cy="{y + 3}" r="16" fill="url(#eg-bulb)"/></g>'


def _bulb(x, y, r=20):
    return f'<circle class="fx-glow" cx="{x}" cy="{y}" r="{r}" fill="url(#eg-bulb)"/><circle class="fx-dot" cx="{x}" cy="{y}" r="4"/>'


def _window(x, y, w, h):
    return (f'<g class="win"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2"/>'
            f'<path d="M{x + w / 2} {y}V{y + h}M{x} {y + h / 2}H{x + w}"/></g>')


def house_svg(label):
    stars = "".join(f'<circle cx="{(i * 397) % 2600 - 500}" cy="{(i * 211) % 330 + 20}" r="{1.2 if i % 3 else 1.8}"/>' for i in range(70))
    wires = "".join(
        f'<g class="wire" data-c="{c}"><path class="wire__base" d="{d}"/><path class="wire__live" pathLength="1" d="{d}"/>'
        f'<path class="wire__flow" d="{d}"/></g>' for c, d in WIRES)
    breakers = "".join(f'<rect class="brk" style="--k:{i}" x="{458 + (i % 2) * 22}" y="{772 + (i // 2) * 9}" width="16" height="6" rx="1"/>' for i in range(10))

    living = (_window(470, 568, 70, 56) + _window(690, 568, 70, 56)
              + "".join(_cone(x, 552, 34, 146) for x in (490, 570, 650, 730))
              + "".join(_pot(x, 550) for x in (490, 570, 650, 730))
              + '<path class="furn" d="M470 700v-38h150v38M478 662v-12h134v12M640 640h40v60M700 616h70v40h-70zM735 656v44"/>'
              + '<path class="furn tv" d="M700 616h70v40h-70z"/>')
    kitchen = (_window(1080, 566, 70, 50)
               + _cone(955, 600, 40, 98) + _cone(1035, 600, 40, 98)
               + '<path class="furn" d="M955 548v44M1035 548v44M940 592h30l-6 8h-18zM1020 592h30l-6 8h-18zM915 642h150v58M915 642v58M845 560h55v140h-55zM845 610h55M1080 640h80v60"/>'
               + _bulb(955, 604, 26) + _bulb(1035, 604, 26)
               + '<rect class="strip" x="1080" y="634" width="80" height="4" rx="2"/>')
    bed = (_window(560, 416, 90, 60) + _window(940, 416, 90, 60)
           + '<path class="furn" d="M450 540v-40h150v40M450 500v-30h20v30M470 512h130M840 540v-46h120v46M870 494v-14h60v14M1080 540v-60h60v60M1092 496h36"/>'
           + _cone(620, 404, 70, 132) + _cone(990, 404, 70, 132) + _bulb(620, 406, 30) + _bulb(990, 406, 30))
    base = ('<path class="furn" d="M560 860v-40h160v40M570 820v-14h140v14M820 790h90v52h-90zM865 842v18M1100 832h44v28h-44z"/>'
            + '<path class="furn sump" d="M1112 832v-14h20v14M1122 818v-30"/>'
            + "".join(_cone(x, 758, 46, 100) for x in (600, 760, 920, 1060))
            + '<path class="drop" d="M520 754H1166"/>'
            + "".join(_pot(x, 756) for x in (600, 760, 920, 1060)))
    garage = ('<path class="furn car" d="M1210 700v-22c0-8 6-14 14-16l30-6 26-22c6-5 14-8 22-8h66c10 0 18 4 24 11l18 21 18 4c8 2 14 8 14 16v22"/>'
              '<circle class="furn" cx="1252" cy="700" r="15"/><circle class="furn" cx="1392" cy="700" r="15"/>'
              '<path class="furn" d="M1296 652l20-17h46l16 17z"/>'
              + _cone(1320, 556, 60, 140) + _bulb(1320, 558, 26)
              + '<rect class="ev" x="1186" y="606" width="22" height="40" rx="4"/><circle class="ev-led" cx="1197" cy="618" r="4"/>'
              '<path class="ev-cable" d="M1197 646c0 30 6 36 20 30s14-12 4-6"/>'
              '<g class="evbar"><rect x="1270" y="590" width="100" height="16" rx="4"/><rect class="evbar__fill" x="1273" y="593" width="94" height="10" rx="2"/><path d="M1370 594v8"/></g>')
    ext = ('<g class="tub"><path class="furn" d="M190 700v-42h110v42"/><rect class="tub__water" x="196" y="660" width="98" height="10" rx="3"/>'
           '<path class="steam" d="M220 650c-8-10 8-16 0-28M245 648c-8-10 8-16 0-28M270 650c-8-10 8-16 0-28"/></g>'
           '<path class="furn" d="M322 700v-62M314 638h16v20h-16z"/>'
           + _bulb(440, 398, 22) + _bulb(1160, 398, 22) + _bulb(1462, 552, 18)
           + '<g class="land">' + "".join(_bulb(x, 694, 14) for x in (372, 1520, 1560)) + "</g>")

    return f'''<svg class="house" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{html.escape(label)}">
<rect class="sky" x="-1200" y="-800" width="4000" height="{GROUND + 800}" fill="url(#eg-sky)"/>
<g class="stars">{stars}</g>
<circle class="moon__halo" cx="1500" cy="110" r="70" fill="url(#eg-cool)"/><circle class="moon" cx="1500" cy="110" r="16"/>
<rect class="earth" x="-1200" y="{GROUND}" width="4000" height="900" fill="url(#eg-earth)"/>
<path class="grass" d="M-1200 {GROUND}H2800"/>
<g class="pole"><rect x="94" y="200" width="12" height="500" rx="2"/><path d="M60 236H140M68 236v-10M132 236v-10M100 236v-12"/><rect class="xfmr" x="108" y="262" width="26" height="46" rx="5"/></g>
<g class="svc" data-c="service"><path class="drop-wire" d="M132 230Q290 330 416 338"/><path class="drop-wire drop-wire--live" pathLength="1" d="M132 230Q290 330 416 338"/><path class="drop-flow" d="M132 230Q290 330 416 338"/>
<path class="mast" d="M416 330V608"/><rect class="meter" x="402" y="608" width="28" height="42" rx="12"/><circle class="meter__dial" cx="416" cy="624" r="7"/><path class="meter__tick" d="M416 624V618"/>
<path class="feed" d="M416 650V806H450"/><path class="feed feed--live" pathLength="1" d="M416 650V806H450"/></g>
<g class="shell">
<path class="roof" d="M398 392L800 186L1202 392"/><path class="roof" d="M1158 548L1320 466L1482 548"/>
<rect class="wall" x="430" y="392" width="740" height="468"/>
<rect class="wall" x="1170" y="548" width="300" height="152"/>
<rect class="slab" x="430" y="538" width="740" height="10"/><rect class="slab" x="430" y="700" width="1040" height="8"/>
<path class="part" d="M800 398V538M820 548V700"/>
<rect class="found" x="420" y="700" width="10" height="168" fill="url(#eg-hatch)"/><rect class="found" x="1170" y="700" width="10" height="168" fill="url(#eg-hatch)"/><rect class="found" x="420" y="860" width="760" height="10"/>
<path class="stair" d="M720 700l20-20h20l20-20h20l20-20h20M1150 860l-20-20h-20l-20-20h-20l-20-20h-20"/>
</g>
<g class="room" data-room="bedrooms"><rect class="glow" x="432" y="400" width="736" height="138" fill="url(#eg-warm)"/>{bed}</g>
<g class="room" data-room="living"><rect class="glow" x="432" y="550" width="386" height="150" fill="url(#eg-warm)"/>{living}</g>
<g class="room" data-room="kitchen"><rect class="glow" x="822" y="550" width="346" height="150" fill="url(#eg-warm)"/>{kitchen}</g>
<g class="room" data-room="basement"><rect class="glow" x="432" y="710" width="736" height="148" fill="url(#eg-warm)"/>{base}</g>
<g class="room" data-room="garage"><rect class="glow" x="1172" y="550" width="296" height="150" fill="url(#eg-warm)"/>{garage}</g>
<g class="room room--ext" data-room="exterior">{ext}</g>
<g class="wires">{wires}</g>
<g class="panel" data-room="panel"><rect class="panel__box" x="450" y="750" width="52" height="66" rx="3"/><rect class="panel__main" x="458" y="756" width="36" height="10" rx="2"/>{breakers}<circle class="panel__flash" cx="476" cy="760" r="40" fill="url(#eg-cool)"/></g>
</svg>'''


def hero_lines_svg():
    """Circuit traces running toward a glowing node, behind the hero when the house scene is off."""
    paths = []
    for i in range(14):
        y = 120 + i * 48
        mid = 860 + (i % 5) * 70
        paths.append(f'<path class="trace" style="--k:{i}" d="M-20 {y}H{mid - 120}l60 {(-1) ** i * 24}H{mid}L1180 {440 + (i - 7) * 6}"/>')
        paths.append(f'<circle class="node" style="--k:{i}" cx="{mid}" cy="{y + (-1) ** i * 24}" r="4"/>')
    return f'''<svg class="hero-lines" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
<g>{"".join(paths)}</g><circle class="hero-lines__core" cx="1180" cy="440" r="160" fill="url(#eg-cool)"/><circle class="hero-lines__dot" cx="1180" cy="440" r="10"/></svg>'''


def panel_svg(rows, label):
    """Breaker panel for the home page estimate teaser: one labelled breaker per (title, sub) row."""
    n = len(rows)
    h = 120 + n * 58
    items = ""
    for i, (t, s) in enumerate(rows):
        y = 104 + i * 58
        items += (f'<g class="pb" style="--k:{i}"><rect class="pb__slot" x="44" y="{y}" width="352" height="46" rx="6"/>'
                  f'<rect class="pb__lever" x="56" y="{y + 10}" width="40" height="26" rx="4"/><circle class="pb__led" cx="374" cy="{y + 23}" r="6"/>'
                  f'<text class="pb__t" x="112" y="{y + 21}">{html.escape(t)}</text><text class="pb__s" x="112" y="{y + 38}">{html.escape(s)}</text></g>')
    return f'''<svg class="pnl" viewBox="0 0 440 {h}" role="img" aria-label="{html.escape(label)}">
<rect class="pnl__box" x="10" y="10" width="420" height="{h - 20}" rx="14"/><rect class="pnl__door" x="24" y="24" width="392" height="{h - 48}" rx="8"/>
<text class="pnl__title" x="44" y="62">PANEL SCHEDULE</text><text class="pnl__amp" x="396" y="62" text-anchor="end">200 A</text>
<path class="pnl__rule" d="M44 80H396"/>{items}</svg>'''


def job_art(job_id):
    """Preview drawing for one estimate job (viewBox 400x200). The estimate script lights parts of it."""
    if job_id == "ev":
        inner = ('<path class="ja-line" d="M40 170H360"/><rect class="ja-dev" x="56" y="70" width="34" height="62" rx="6"/><circle class="ja-led" cx="73" cy="88" r="6"/>'
                 '<path class="ja-cable ja-live" d="M73 132c0 34 14 40 60 30s90-14 116-16"/>'
                 '<path class="ja-line" d="M170 170v-26c0-10 8-16 18-18l34-6 30-24c8-6 16-8 26-8h52c12 0 20 6 26 14l18 22 14 4"/>'
                 '<circle class="ja-line" cx="214" cy="170" r="16"/><circle class="ja-line" cx="340" cy="170" r="16"/>'
                 '<g class="ja-bar"><rect x="210" y="40" width="130" height="20" rx="5"/><rect class="ja-bar__fill" x="214" y="44" width="122" height="12" rx="3"/></g>')
    elif job_id == "panel":
        br = "".join(f'<rect class="ja-brk" style="--k:{i}" x="{150 + (i % 2) * 54}" y="{56 + (i // 2) * 22}" width="44" height="14" rx="3"/>' for i in range(10))
        inner = (f'<rect class="ja-dev" x="136" y="20" width="128" height="170" rx="8"/><rect class="ja-main" x="160" y="30" width="80" height="18" rx="4"/>{br}'
                 '<path class="ja-cable ja-live" d="M200 20V0M60 100H136M264 100H340"/><text class="ja-amp" x="200" y="186" text-anchor="middle">200 A</text>')
    elif job_id == "potlights":
        dots = "".join(f'<g class="ja-pot" data-i="{i}"><circle class="ja-pot__glow" cx="{40 + (i % 10) * 36}" cy="{40 + (i // 10) * 38}" r="16" fill="url(#eg-bulb)"/><circle class="ja-pot__can" cx="{40 + (i % 10) * 36}" cy="{40 + (i // 10) * 38}" r="5"/></g>' for i in range(40))
        inner = f'<rect class="ja-line" x="16" y="16" width="368" height="168" rx="8"/>{dots}'
    elif job_id == "generator":
        inner = ('<path class="ja-line" d="M30 170H370M60 170V90l80-50 80 50v80"/><rect class="ja-dev" x="92" y="116" width="26" height="36" rx="3"/><rect class="ja-dev" x="230" y="122" width="22" height="22" rx="4"/>'
                 '<path class="ja-cable ja-live" d="M118 134H230M252 133H286"/><rect class="ja-dev ja-gen" x="286" y="112" width="70" height="58" rx="8"/>'
                 '<path class="ja-line" d="M300 128h42M300 140h42M300 152h42"/><circle class="ja-led" cx="348" cy="122" r="4"/>')
    elif job_id == "hottub":
        inner = ('<path class="ja-line" d="M20 170H380"/><rect class="ja-dev" x="40" y="80" width="30" height="50" rx="4"/>'
                 '<path class="ja-cable ja-live" d="M55 130V170H230V130"/><rect class="ja-dev" x="218" y="96" width="24" height="34" rx="3"/><circle class="ja-led" cx="230" cy="108" r="4"/>'
                 '<path class="ja-line" d="M260 170v-60h110v60"/><rect class="ja-water" x="266" y="114" width="98" height="12" rx="4"/>'
                 '<path class="ja-steam" d="M286 100c-8-12 8-18 0-32M314 98c-8-12 8-18 0-32M342 100c-8-12 8-18 0-32"/>')
    else:  # outlets
        outs = "".join(f'<g class="ja-out" data-i="{i}"><rect x="{36 + i * 66}" y="78" width="48" height="66" rx="8"/><path d="M{52 + i * 66} 98v12M{68 + i * 66} 98v12M{56 + i * 66} 124a4 4 0 0 0 8 0"/></g>' for i in range(5))
        inner = f'<path class="ja-cable ja-live" d="M20 58H380M60 58v20M126 58v20M192 58v20M258 58v20M324 58v20"/>{outs}<path class="ja-line" d="M20 180H380"/>'
    return f'<svg class="ja ja--{job_id}" viewBox="0 0 400 200" aria-hidden="true" focusable="false">{inner}</svg>'
