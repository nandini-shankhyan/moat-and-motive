#!/usr/bin/env python3
"""
Builds the Moat & Motive static site from articles.json.
Run: python3 gen_site.py
Regenerates index.html and articles/*.html from the shared templates below.
No build tooling needed afterwards — the output is plain, dependency-free HTML/CSS.

Cover art: every essay gets an original, generated abstract "digital art" cover
(layered gradient blobs + fine line work + grain), built as inline SVG so the
site never depends on external images or stock photography.
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

# One thematic palette per essay: [base(dark), mid, bright, highlight]
PALETTES = {
    1:  ['#1a1006', '#c96a1f', '#f2b705', '#ffe9b3'],   # Reliance — energy
    2:  ['#0a1620', '#1f6f8b', '#4fd1c5', '#dff5f2'],   # TCS — services/tech
    3:  ['#07130c', '#1f6b45', '#7CFC98', '#e7fff0'],   # NVIDIA — compute
    4:  ['#0c0b16', '#463a86', '#8a7fd6', '#eae6fb'],   # Palantir — defense/data
    5:  ['#111111', '#4a4a4a', '#b9b9b9', '#ffffff'],   # Apple — monochrome
    6:  ['#0b1524', '#a8641f', '#f2b705', '#ffedcf'],   # Amazon — logistics
    7:  ['#1a0505', '#8a1023', '#e8434f', '#ffe3d9'],   # Coca-Cola — brand
    8:  ['#08161a', '#1c7c74', '#6fd7c4', '#e6fbf5'],   # Unilever — FMCG
    9:  ['#0c0c0c', '#8a1023', '#e0393e', '#f6d9d9'],   # Tesla — electric
    10: ['#0d0a1a', '#5c3a94', '#f2b705', '#f7ecc9'],   # AI energy — power/grid
    11: ['#0a140a', '#2f6b3a', '#9ed35c', '#eef8dd'],   # Dabur — herbal
    12: ['#08131f', '#1f5c8b', '#e0a83a', '#fff3d9'],   # GCCs — global
}

def slugify(name):
    s = name.lower().replace('&', 'and')
    s = re.sub(r"[’']", '', s)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s

for a in DATA:
    a['slug'] = slugify(a['company'])
    a['palette'] = PALETTES.get(a['num'], ['#111111', '#4a4a4a', '#b9b9b9', '#ffffff'])

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def _rnd(seed, k):
    v = math.sin(seed * 12.9898 + k * 78.233) * 43758.5453
    return v - math.floor(v)

GRAIN_DEFS = '''<filter id="grain{u}" x="-20%" y="-20%" width="140%" height="140%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="{seed}" result="noise"/>
  <feColorMatrix in="noise" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.05 0"/>
</filter>'''

def art_svg(a, w=640, h=512):
    """One generated cover per essay: a soft gradient field, a scatter of fine
    arcs (the site's recurring 'moat ring' mark), and a grain pass on top."""
    seed = a['num']
    dark, mid, bright, hi = a['palette']
    u = a['slug']
    variant = seed % 2  # alternate composition: orb vs shard

    defs = [f'''<radialGradient id="rg{u}" cx="{40+_rnd(seed,1)*20:.0f}%" cy="{35+_rnd(seed,2)*20:.0f}%" r="75%">
      <stop offset="0%" stop-color="{hi}"/>
      <stop offset="35%" stop-color="{bright}"/>
      <stop offset="75%" stop-color="{mid}"/>
      <stop offset="100%" stop-color="{dark}"/>
    </radialGradient>''']
    defs.append(GRAIN_DEFS.format(u=u, seed=seed*7+3))

    body = [f'<rect width="{w}" height="{h}" fill="{dark}"/>']

    if variant == 0:
        cx = w * (0.38 + _rnd(seed, 3) * 0.28)
        cy = h * (0.42 + _rnd(seed, 4) * 0.22)
        r = min(w, h) * (0.42 + _rnd(seed, 5) * 0.1)
        body.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="url(#rg{u})"/>')
        for k in range(6):
            x1 = -40 + _rnd(seed, k+10) * w * 0.5
            y1 = h * (0.15 + _rnd(seed, k+20) * 0.7)
            cxp = cx + (_rnd(seed, k+30) - 0.5) * w * 0.7
            cyp = cy + (_rnd(seed, k+40) - 0.5) * h * 0.7
            x2 = w + 40 - _rnd(seed, k+50) * w * 0.5
            y2 = h * (0.1 + _rnd(seed, k+60) * 0.8)
            op = 0.16 + _rnd(seed, k+70) * 0.18
            body.append(f'<path d="M{x1:.0f} {y1:.0f} Q {cxp:.0f} {cyp:.0f} {x2:.0f} {y2:.0f}" fill="none" stroke="{hi}" stroke-width="1" opacity="{op:.2f}"/>')
    else:
        cx = w * (0.5 + (_rnd(seed, 3)-0.5) * 0.3)
        cy = h * (0.5 + (_rnd(seed, 4)-0.5) * 0.3)
        for k in range(4):
            ang = _rnd(seed, k+5) * math.pi * 2
            len1 = min(w, h) * (0.5 + _rnd(seed, k+15) * 0.4)
            len2 = min(w, h) * (0.3 + _rnd(seed, k+25) * 0.3)
            a1 = ang
            a2 = ang + math.pi * (0.35 + _rnd(seed, k+35) * 0.25)
            x1, y1 = cx + math.cos(a1)*len1, cy + math.sin(a1)*len1
            x2, y2 = cx + math.cos(a2)*len2, cy + math.sin(a2)*len2
            x3, y3 = cx - math.cos(a1)*len2*0.6, cy - math.sin(a1)*len2*0.6
            fill = [dark, mid, bright, hi][k % 4]
            op = 0.55 + _rnd(seed, k+45) * 0.4
            body.append(f'<polygon points="{cx:.0f},{cy:.0f} {x1:.0f},{y1:.0f} {x2:.0f},{y2:.0f} {x3:.0f},{y3:.0f}" fill="{fill}" opacity="{op:.2f}"/>')
        body.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{min(w,h)*0.5:.0f}" fill="url(#rg{u})" opacity="0.5"/>')
        for k in range(3):
            r = min(w, h) * (0.16 + k * 0.09)
            body.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="none" stroke="{hi}" stroke-width="1" opacity="{0.5 - k*0.12:.2f}"/>')

    body.append(f'<rect width="{w}" height="{h}" filter="url(#grain{u})"/>')

    svg = (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
           f'aria-label="Cover art for {esc(a["company"])}"><defs>{"".join(defs)}</defs>{"".join(body)}</svg>')
    return svg

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
    <span>&copy; 2026 {AUTHOR}. {SITE_NAME}.</span>
    <span>Twelve essays on corporate advantage, 2026.</span>
  </div>
</footer>'''

# ---------------- INDEX PAGE ----------------

TOTAL_SOURCES = sum(len(a['sources']) for a in DATA)

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

index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{SITE_NAME} — {AUTHOR}</title>
<meta name="description" content="{TAGLINE} Twelve essays on the moats — and motives — behind today's biggest companies, by {AUTHOR}.">
<link rel="icon" href="data:image/svg+xml,{ICON_DATA}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
{masthead('assets/styles.css')}

<section class="hero">
  <div class="wrap">
    <div>
      <h1>Hi, I'm {AUTHOR_FIRST}!</h1>
      <p class="lede">{TAGLINE}</p>
      <a class="pill-btn" href="#essays">Read the essays</a>
    </div>
    <ul class="stat-list">
      <li><span class="num">12</span><span class="label">Strategic essays</span></li>
      <li><span class="num">{TOTAL_SOURCES}+</span><span class="label">Sources cited</span></li>
      <li><span class="num">2026</span><span class="label">Edition</span></li>
    </ul>
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

<section class="manifesto" id="about">
  <div class="wrap">
    <h2>About this&nbsp;field&nbsp;guide</h2>
    <div class="body">
      <p>{SITE_NAME} reads companies the way a strategist reads a map: where is the advantage, who can take it, and what would have to be true for it to disappear. Each essay opens with the strategic question actually at stake, follows the money and the incentives, and closes with a plain-spoken answer for the person who has to decide what to do next.</p>
      <p>The subjects here range from Reliance's bet on sovereign AI infrastructure to Coca-Cola's hundred-and-forty-year-old brand — different industries, the same underlying question: is this advantage durable, or is it just current?</p>
      <p class="signoff">— {AUTHOR}</p>
    </div>
  </div>
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
