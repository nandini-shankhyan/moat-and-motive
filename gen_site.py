#!/usr/bin/env python3
"""
Builds the Moat & Motive static site from articles.json.
Run: python3 gen_site.py
Regenerates index.html and articles/*.html from the shared templates below.
No build tooling needed afterwards — the output is plain, dependency-free HTML/CSS.

Cover art: every essay gets an original, flat-illustration cover (a muted
pastel ground, a fence-line "moat" perimeter, a subject icon, and a couple
of onlooking figures), built as inline SVG so the site never depends on
external images or stock photography.
"""
import json, re, os, math

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, 'articles.json'), encoding='utf-8'))
OUT_ARTICLES = os.path.join(ROOT, 'articles')
os.makedirs(OUT_ARTICLES, exist_ok=True)

SITE_NAME = 'Moat & Motive'
AUTHOR = 'Nandini Shankhyan'
AUTHOR_FIRST = 'Nandini'
TAGLINE = 'Welcome to Moat & Motive — a blog where I write about ingenious strategies employed by companies across the world.'

def slugify(name):
    s = name.lower().replace('&', 'and')
    s = re.sub(r"[’']", '', s)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s

for a in DATA:
    a['slug'] = slugify(a['company'])

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def _rnd(seed, k):
    v = math.sin(seed * 12.9898 + k * 78.233) * 43758.5453
    return v - math.floor(v)

# Muted, flat illustration backgrounds — one per essay, keyed to its subject.
PASTELS = {
    1:  '#e3a34e',  # Reliance — amber, energy
    2:  '#8fb3c9',  # TCS — dusty blue, services
    3:  '#9bbf8a',  # NVIDIA — sage, compute
    4:  '#b6a4c9',  # Palantir — mauve, data
    5:  '#cfc8bb',  # Apple — sand, minimal
    6:  '#e0b04a',  # Amazon — mustard, logistics
    7:  '#d98a86',  # Coca-Cola — rose, brand
    8:  '#9ccbb9',  # Unilever — seafoam, FMCG
    9:  '#d17a6a',  # Tesla — coral, electric
    10: '#eda98c',  # AI Energy Bottleneck — salmon, industrial
    11: '#a8b16a',  # Dabur — moss, herbal
    12: '#8fb8d9',  # India's GCCs — sky, global
}
CREAM = '#f4ecdb'   # the flat "object" color used across every icon
INK_SHADOW = '#00000030'

CLOTHES = [('#e9bdb6', '#b8492f'), ('#f6f1e6', '#5b6b78'), ('#f6f1e6', '#2c3e50')]
SKIN = '#caa07a'

def _person(x, y, s, shirt, pants, arm_up=False):
    head_r = s * 0.34
    parts = [f'<circle cx="{x:.0f}" cy="{y-s*1.55:.0f}" r="{head_r:.0f}" fill="{SKIN}"/>']
    parts.append(f'<rect x="{x-s*0.4:.0f}" y="{y-s*1.2:.0f}" width="{s*0.8:.0f}" height="{s*0.95:.0f}" rx="{s*0.18:.0f}" fill="{shirt}"/>')
    parts.append(f'<rect x="{x-s*0.36:.0f}" y="{y-s*0.3:.0f}" width="{s*0.32:.0f}" height="{s*0.95:.0f}" rx="{s*0.1:.0f}" fill="{pants}"/>')
    parts.append(f'<rect x="{x+s*0.04:.0f}" y="{y-s*0.3:.0f}" width="{s*0.32:.0f}" height="{s*0.95:.0f}" rx="{s*0.1:.0f}" fill="{pants}"/>')
    if arm_up:
        parts.append(f'<rect x="{x+s*0.32:.0f}" y="{y-s*1.5:.0f}" width="{s*0.62:.0f}" height="{s*0.17:.0f}" rx="{s*0.08:.0f}" fill="{shirt}" transform="rotate(-42 {x+s*0.32:.0f} {y-s*1.42:.0f})"/>')
    else:
        parts.append(f'<rect x="{x-s*0.72:.0f}" y="{y-s*1.1:.0f}" width="{s*0.34:.0f}" height="{s*0.82:.0f}" rx="{s*0.14:.0f}" fill="{shirt}" transform="rotate(14 {x-s*0.6:.0f} {y-s*0.9:.0f})"/>')
    return ''.join(parts)

def _fence(cx, cy, rx, ry, seed):
    n = 8
    pts = []
    for k in range(n):
        ang = (k / n) * math.pi * 2
        jr = 0.92 + _rnd(seed, k + 200) * 0.16
        pts.append((cx + math.cos(ang) * rx * jr, cy + math.sin(ang) * ry * jr * 0.55))
    d = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + ' Z'
    parts = [f'<path d="{d}" fill="none" stroke="{CREAM}" stroke-width="3" opacity="0.85"/>']
    for x, y in pts:
        parts.append(f'<rect x="{x-2.5:.0f}" y="{y-18:.0f}" width="5" height="26" fill="{CREAM}" opacity="0.9"/>')
    return ''.join(parts)

def _icon_factory(cx, cy, s, fg, sh):
    w1, w2, hgt = s*0.62, s*0.9, s*1.5
    body = f'<path d="M{cx-w1:.0f} {cy-hgt:.0f} L{cx+w1:.0f} {cy-hgt:.0f} L{cx+w2:.0f} {cy+s*0.2:.0f} L{cx-w2:.0f} {cy+s*0.2:.0f} Z" fill="{fg}"/>'
    shadow = f'<path d="M{cx:.0f} {cy-hgt:.0f} L{cx+w1:.0f} {cy-hgt:.0f} L{cx+w2:.0f} {cy+s*0.2:.0f} L{cx:.0f} {cy+s*0.2:.0f} Z" fill="{sh}"/>'
    smoke = ''.join(f'<circle cx="{cx+(_rnd(cx+k,k)-0.5)*s*0.5:.0f}" cy="{cy-hgt-s*(0.3+k*0.32):.0f}" r="{s*(0.22+k*0.05):.0f}" fill="{CREAM}" opacity="{0.5-k*0.1:.2f}"/>' for k in range(4))
    return body + shadow + smoke

def _icon_cooling_tower(cx, cy, s, fg, sh):
    top, mid, bot, hgt = s*0.75, s*0.42, s*0.95, s*1.7
    d = f'M{cx-bot:.0f} {cy+s*0.2:.0f} C{cx-mid:.0f} {cy-hgt*0.3:.0f} {cx-mid:.0f} {cy-hgt*0.6:.0f} {cx-top:.0f} {cy-hgt:.0f} L{cx+top:.0f} {cy-hgt:.0f} C{cx+mid:.0f} {cy-hgt*0.6:.0f} {cx+mid:.0f} {cy-hgt*0.3:.0f} {cx+bot:.0f} {cy+s*0.2:.0f} Z'
    body = f'<path d="{d}" fill="{fg}"/>'
    shadow_d = f'M{cx:.0f} {cy+s*0.2:.0f} L{cx+bot:.0f} {cy+s*0.2:.0f} C{cx+mid:.0f} {cy-hgt*0.3:.0f} {cx+mid:.0f} {cy-hgt*0.6:.0f} {cx+top:.0f} {cy-hgt:.0f} L{cx:.0f} {cy-hgt:.0f} Z'
    shadow = f'<path d="{shadow_d}" fill="{sh}"/>'
    smoke = ''.join(f'<circle cx="{cx+(_rnd(cx+k,k+9)-0.5)*s*0.6:.0f}" cy="{cy-hgt-s*(0.3+k*0.34):.0f}" r="{s*(0.26+k*0.05):.0f}" fill="{CREAM}" opacity="{0.5-k*0.1:.2f}"/>' for k in range(4))
    return body + shadow + smoke

def _icon_server(cx, cy, s, fg, sh):
    parts = []
    for i in range(3):
        y = cy - s*0.9 + i*s*0.62
        parts.append(f'<rect x="{cx-s*0.85:.0f}" y="{y:.0f}" width="{s*1.7:.0f}" height="{s*0.5:.0f}" rx="{s*0.08:.0f}" fill="{fg}" opacity="{1.0 if i%2==0 else 0.82}"/>')
        parts.append(f'<circle cx="{cx+s*0.6:.0f}" cy="{y+s*0.25:.0f}" r="{s*0.06:.0f}" fill="{CREAM}"/>')
    return ''.join(parts)

def _icon_chip(cx, cy, s, fg, sh):
    r = s*0.75
    body = f'<rect x="{cx-r:.0f}" y="{cy-r:.0f}" width="{r*2:.0f}" height="{r*2:.0f}" rx="{s*0.12:.0f}" fill="{fg}"/>'
    pins = ''
    for i in range(-1, 2):
        off = i * s*0.5
        pins += f'<rect x="{cx+off-4:.0f}" y="{cy-r-s*0.32:.0f}" width="8" height="{s*0.32:.0f}" fill="{fg}"/>'
        pins += f'<rect x="{cx+off-4:.0f}" y="{cy+r:.0f}" width="8" height="{s*0.32:.0f}" fill="{fg}"/>'
        pins += f'<rect x="{cx-r-s*0.32:.0f}" y="{cy+off-4:.0f}" width="{s*0.32:.0f}" height="8" fill="{fg}"/>'
        pins += f'<rect x="{cx+r:.0f}" y="{cy+off-4:.0f}" width="{s*0.32:.0f}" height="8" fill="{fg}"/>'
    grid = f'<rect x="{cx-r*0.5:.0f}" y="{cy-r*0.5:.0f}" width="{r:.0f}" height="{r:.0f}" fill="none" stroke="{sh}" stroke-width="3" opacity="0.5"/>'
    return pins + body + grid

def _icon_satellite(cx, cy, s, fg, sh):
    pole = f'<rect x="{cx-s*0.05:.0f}" y="{cy-s*0.2:.0f}" width="{s*0.1:.0f}" height="{s*1.1:.0f}" fill="{fg}"/>'
    dish = f'<path d="M{cx-s*0.95:.0f} {cy-s*0.2:.0f} A{s*0.95:.0f} {s*0.55:.0f} 0 0 1 {cx+s*0.95:.0f} {cy-s*0.2:.0f} L{cx:.0f} {cy+s*0.15:.0f} Z" fill="{fg}"/>'
    waves = ''.join(f'<path d="M{cx-s*(0.5+k*0.35):.0f} {cy-s*(1.1+k*0.35):.0f} A{s*(0.6+k*0.35):.0f} {s*(0.6+k*0.35):.0f} 0 0 1 {cx+s*(0.5+k*0.35):.0f} {cy-s*(1.1+k*0.35):.0f}" fill="none" stroke="{CREAM}" stroke-width="3" opacity="{0.55-k*0.15:.2f}"/>' for k in range(3))
    return pole + dish + waves

def _icon_device(cx, cy, s, fg, sh):
    body = f'<rect x="{cx-s*0.55:.0f}" y="{cy-s*1.1:.0f}" width="{s*1.1:.0f}" height="{s*2.0:.0f}" rx="{s*0.28:.0f}" fill="{fg}"/>'
    screen = f'<rect x="{cx-s*0.42:.0f}" y="{cy-s*0.92:.0f}" width="{s*0.84:.0f}" height="{s*1.5:.0f}" rx="{s*0.1:.0f}" fill="{sh}" opacity="0.35"/>'
    btn = f'<circle cx="{cx:.0f}" cy="{cy+s*0.72:.0f}" r="{s*0.1:.0f}" fill="{CREAM}"/>'
    return body + screen + btn

def _icon_box(cx, cy, s, fg, sh):
    top = f'<polygon points="{cx-s*0.85:.0f},{cy-s*0.15:.0f} {cx:.0f},{cy-s*0.6:.0f} {cx+s*0.85:.0f},{cy-s*0.15:.0f} {cx:.0f},{cy+s*0.3:.0f}" fill="{CREAM}"/>'
    left = f'<polygon points="{cx-s*0.85:.0f},{cy-s*0.15:.0f} {cx:.0f},{cy+s*0.3:.0f} {cx:.0f},{cy+s*1.2:.0f} {cx-s*0.85:.0f},{cy+s*0.75:.0f}" fill="{fg}"/>'
    right = f'<polygon points="{cx+s*0.85:.0f},{cy-s*0.15:.0f} {cx:.0f},{cy+s*0.3:.0f} {cx:.0f},{cy+s*1.2:.0f} {cx+s*0.85:.0f},{cy+s*0.75:.0f}" fill="{sh}"/>'
    tape = f'<line x1="{cx:.0f}" y1="{cy+s*0.3:.0f}" x2="{cx:.0f}" y2="{cy+s*1.2:.0f}" stroke="{CREAM}" stroke-width="4" opacity="0.6"/>'
    return top + left + right + tape

def _icon_bottle(cx, cy, s, fg, sh):
    neck = f'<rect x="{cx-s*0.16:.0f}" y="{cy-s*1.6:.0f}" width="{s*0.32:.0f}" height="{s*0.55:.0f}" fill="{fg}"/>'
    body = f'<path d="M{cx-s*0.16:.0f} {cy-s*1.1:.0f} C{cx-s*0.5:.0f} {cy-s*0.75:.0f} {cx-s*0.62:.0f} {cy-s*0.5:.0f} {cx-s*0.62:.0f} {cy-s*0.1:.0f} L{cx-s*0.62:.0f} {cy+s*1.0:.0f} C{cx-s*0.62:.0f} {cy+s*1.2:.0f} {cx+s*0.62:.0f} {cy+s*1.2:.0f} {cx+s*0.62:.0f} {cy+s*1.0:.0f} L{cx+s*0.62:.0f} {cy-s*0.1:.0f} C{cx+s*0.62:.0f} {cy-s*0.5:.0f} {cx+s*0.5:.0f} {cy-s*0.75:.0f} {cx+s*0.16:.0f} {cy-s*1.1:.0f} Z" fill="{fg}"/>'
    label = f'<rect x="{cx-s*0.62:.0f}" y="{cy+s*0.05:.0f}" width="{s*1.24:.0f}" height="{s*0.55:.0f}" fill="{CREAM}" opacity="0.85"/>'
    cap = f'<rect x="{cx-s*0.18:.0f}" y="{cy-s*1.7:.0f}" width="{s*0.36:.0f}" height="{s*0.16:.0f}" fill="{sh}"/>'
    return body + neck + cap + label

def _icon_leafdrop(cx, cy, s, fg, sh):
    leaf = f'<path d="M{cx-s*0.9:.0f} {cy+s*0.5:.0f} C{cx-s*0.9:.0f} {cy-s*0.6:.0f} {cx+s*0.2:.0f} {cy-s*1.1:.0f} {cx+s*0.9:.0f} {cy-s*0.9:.0f} C{cx+s*0.3:.0f} {cy-s*0.2:.0f} {cx-s*0.1:.0f} {cy+s*0.2:.0f} {cx-s*0.9:.0f} {cy+s*0.5:.0f} Z" fill="{fg}"/>'
    vein = f'<path d="M{cx-s*0.8:.0f} {cy+s*0.35:.0f} L{cx+s*0.75:.0f} {cy-s*0.85:.0f}" stroke="{sh}" stroke-width="3" opacity="0.5" fill="none"/>'
    drop = f'<path d="M{cx+s*0.15:.0f} {cy+s*0.6:.0f} C{cx+s*0.15:.0f} {cy+s*0.95:.0f} {cx+s*0.55:.0f} {cy+s*0.95:.0f} {cx+s*0.55:.0f} {cy+s*0.6:.0f} C{cx+s*0.55:.0f} {cy+s*0.35:.0f} {cx+s*0.35:.0f} {cy+s*0.15:.0f} {cx+s*0.35:.0f} {cy+s*0.15:.0f} C{cx+s*0.35:.0f} {cy+s*0.15:.0f} {cx+s*0.15:.0f} {cy+s*0.35:.0f} {cx+s*0.15:.0f} {cy+s*0.6:.0f} Z" fill="{CREAM}"/>'
    return leaf + vein + drop

def _icon_car(cx, cy, s, fg, sh):
    body = f'<rect x="{cx-s*1.1:.0f}" y="{cy-s*0.15:.0f}" width="{s*2.2:.0f}" height="{s*0.55:.0f}" rx="{s*0.2:.0f}" fill="{fg}"/>'
    roof = f'<path d="M{cx-s*0.55:.0f} {cy-s*0.15:.0f} L{cx-s*0.3:.0f} {cy-s*0.6:.0f} L{cx+s*0.4:.0f} {cy-s*0.6:.0f} L{cx+s*0.65:.0f} {cy-s*0.15:.0f} Z" fill="{sh}"/>'
    w1 = f'<circle cx="{cx-s*0.6:.0f}" cy="{cy+s*0.45:.0f}" r="{s*0.28:.0f}" fill="{CREAM}"/>'
    w2 = f'<circle cx="{cx+s*0.6:.0f}" cy="{cy+s*0.45:.0f}" r="{s*0.28:.0f}" fill="{CREAM}"/>'
    return body + roof + w1 + w2

def _icon_globe(cx, cy, s, fg, sh):
    circle = f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{s*0.95:.0f}" fill="{fg}"/>'
    lines = f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{s*0.4:.0f}" ry="{s*0.95:.0f}" fill="none" stroke="{sh}" stroke-width="3" opacity="0.5"/>'
    lat = ''.join(f'<line x1="{cx-s*0.95:.0f}" y1="{cy-s*0.6+k*s*0.6:.0f}" x2="{cx+s*0.95:.0f}" y2="{cy-s*0.6+k*s*0.6:.0f}" stroke="{sh}" stroke-width="3" opacity="0.4"/>' for k in range(3))
    return circle + lines + lat

def _icon_leaf(cx, cy, s, fg, sh):
    leaf = f'<path d="M{cx:.0f} {cy+s*1.1:.0f} C{cx-s*1.0:.0f} {cy+s*0.6:.0f} {cx-s*0.9:.0f} {cy-s*0.8:.0f} {cx:.0f} {cy-s*1.3:.0f} C{cx+s*0.9:.0f} {cy-s*0.8:.0f} {cx+s*1.0:.0f} {cy+s*0.6:.0f} {cx:.0f} {cy+s*1.1:.0f} Z" fill="{fg}"/>'
    vein = f'<line x1="{cx:.0f}" y1="{cy+s*1.0:.0f}" x2="{cx:.0f}" y2="{cy-s*1.2:.0f}" stroke="{sh}" stroke-width="3" opacity="0.55"/>'
    return leaf + vein

ICONS = {1:_icon_factory, 2:_icon_server, 3:_icon_chip, 4:_icon_satellite, 5:_icon_device,
         6:_icon_box, 7:_icon_bottle, 8:_icon_leafdrop, 9:_icon_car, 10:_icon_cooling_tower,
         11:_icon_leaf, 12:_icon_globe}

GRAIN_DEFS = '''<filter id="grain{u}" x="-20%" y="-20%" width="140%" height="140%">
  <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="{seed}" result="noise"/>
  <feColorMatrix in="noise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.06 0"/>
</filter>'''

def art_svg(a, w=640, h=512):
    """A flat, grainy editorial illustration for each essay: a muted pastel
    ground, a fence-line perimeter (the moat), a subject icon at its centre,
    and a couple of figures looking on — no stock photography involved."""
    seed = a['num']
    bg = PASTELS.get(seed, '#cccccc')
    u = a['slug']
    m = min(w, h)

    cx, cy = w*0.60, h*0.62
    scale = m * 0.20

    body = [f'<rect width="{w}" height="{h}" fill="{bg}"/>']
    body.append(_fence(cx, cy, m*0.37, m*0.34, seed))
    icon_fn = ICONS.get(seed, _icon_globe)
    body.append(icon_fn(cx, cy, scale, CREAM, INK_SHADOW))

    py = h * 0.90
    p_size = m * 0.115
    x0 = w * 0.09
    figures = [
        (x0, py, p_size*0.85, CLOTHES[0][0], CLOTHES[0][1], False),
        (x0 + p_size*2.0, py - p_size*0.1, p_size*0.95, CLOTHES[1][0], CLOTHES[1][1], False),
        (x0 + p_size*3.9, py - p_size*0.2, p_size*1.05, CLOTHES[2][0], CLOTHES[2][1], True),
    ]
    for x, y, s, shirt, pants, arm in figures:
        body.append(_person(x, y, s, shirt, pants, arm))

    defs = f'<defs>{GRAIN_DEFS.format(u=u, seed=seed*7+3)}</defs>'
    body.append(f'<rect width="{w}" height="{h}" filter="url(#grain{u})"/>')

    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="Illustration for {esc(a["company"])}">{defs}{"".join(body)}</svg>')

ICON_DATA = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="%23f2ece0"/><circle cx="16" cy="16" r="11" fill="none" stroke="%2318150f" stroke-width="1.6"/><circle cx="16" cy="16" r="5.5" fill="none" stroke="%2318150f" stroke-width="1.6"/></svg>'

def masthead(css_path):
    root = '' if css_path == 'assets/styles.css' else '../'
    return f'''<header class="masthead">
  <div class="wrap">
    <a class="mark" href="{root}index.html">Moat &amp; Motive</a>
    <nav>
      <a href="{root}index.html#essays">Essays</a>
      <a href="{root}index.html#about">About</a>
    </nav>
  </div>
</header>'''

def footer():
    return f'''<footer>
  <div class="wrap">
    <span>&copy; {AUTHOR}. {SITE_NAME}.</span>
    <span>Twelve essays on corporate advantage.</span>
  </div>
</footer>'''

# ---------------- INDEX PAGE ----------------

ABOUT_PARAGRAPHS = [
    f"Welcome to {SITE_NAME} — a blog where I read companies the way a strategist reads a map: where is the advantage, who can take it, and what would have to be true for it to disappear. Each essay opens with the strategic question actually at stake, follows the money and the incentives, and closes with a plain-spoken answer for the person who has to decide what to do next.",
    "The subjects here range from Reliance's bet on sovereign AI infrastructure to Coca-Cola's hundred-and-forty-year-old brand — different industries, the same underlying question: is this advantage durable, or is it just current?",
]

case_items = []
for a in DATA:
    art = art_svg(a)
    case_items.append(f'''    <li class="case-card">
      <a href="articles/{a['slug']}.html">
        <div class="case-art">{art}</div>
        <div class="case-caption">
          <span class="index-num">{a['num']:02d}</span>
          <span class="text">
            <h3>{esc(a['company'])}</h3>
            <p>{esc(a['question_title'])}</p>
          </span>
          <span class="arrow">&#8594;</span>
        </div>
      </a>
    </li>''')

about_html = '\n      '.join(f'<p>{esc(p)}</p>' for p in ABOUT_PARAGRAPHS)

index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{SITE_NAME} — {AUTHOR}</title>
<meta name="description" content="{TAGLINE}">
<link rel="icon" href="data:image/svg+xml,{ICON_DATA}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
{masthead('assets/styles.css')}

<section class="hero" id="about">
  <div class="wrap">
    <h1>Hi, I'm {AUTHOR_FIRST}!</h1>
    <div class="lede-about">
      {about_html}
      <p class="signoff">— {AUTHOR}</p>
    </div>
    <a class="pill-btn" href="#essays">Read the essays</a>
  </div>
</section>

<section class="wrap" id="essays">
  <div class="section-head">
    <h2>Selected essays</h2>
    <span class="count">01 — 12</span>
  </div>
  <ul class="case-grid">
{chr(10).join(case_items)}
  </ul>
</section>

{footer()}
</body>
</html>'''

open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(index_html)

# ---------------- ARTICLE PAGES ----------------

for i, a in enumerate(DATA):
    cover = art_svg(a, w=1200, h=520)
    prev_a = DATA[i-1] if i > 0 else DATA[-1]
    next_a = DATA[i+1] if i < len(DATA)-1 else DATA[0]

    sections_html = []
    for sec in a['sections']:
        paras = '\n'.join(f'      <p>{esc(p)}</p>' for p in sec['paragraphs'])
        sections_html.append(f'      <h2>{esc(sec["heading"])}</h2>\n{paras}')

    sources_html = ''
    if a['sources']:
        items = '\n'.join(f'        <li>{esc(s)}</li>' for s in a['sources'])
        sources_html = f'''    <div class="sources">
      <h3>Selected sources</h3>
      <ul>
{items}
      </ul>
    </div>'''

    article_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(a['company'])} — {esc(a['question_title'])} | {SITE_NAME}</title>
<meta name="description" content="{esc(a['strategic_question'])}">
<link rel="icon" href="data:image/svg+xml,{ICON_DATA}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="../assets/styles.css">
</head>
<body>
{masthead('articles/x.html')}

<section class="wrap article-header">
  <a class="back-link" href="../index.html#essays">&#8592; All essays</a>
  <div class="article-cover">{cover}</div>
  <div class="eyebrow-row"><span class="dot"></span> Essay {a['num']:02d} of 12</div>
  <h1>{esc(a['company'])} — {esc(a['question_title'])}</h1>
  <p class="deck">{esc(a['strategic_question'])}</p>
</section>

<section class="wrap article-body">
  <div class="col">
{chr(10).join(sections_html)}
{sources_html}
  </div>
</section>

<section class="wrap">
  <div class="pager">
    <a class="prev" href="{prev_a['slug']}.html">
      <span class="label">Previous</span>
      <span class="title">{esc(prev_a['company'])}</span>
    </a>
    <a class="next" href="{next_a['slug']}.html">
      <span class="label">Next</span>
      <span class="title">{esc(next_a['company'])}</span>
    </a>
  </div>
</section>

{footer()}
</body>
</html>'''

    open(os.path.join(OUT_ARTICLES, f"{a['slug']}.html"), 'w', encoding='utf-8').write(article_html)

print('Built index.html and', len(DATA), 'article pages.')
