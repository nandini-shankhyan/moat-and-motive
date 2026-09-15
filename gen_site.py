#!/usr/bin/env python3
"""
Builds the Moat & Motive static site from articles.json.
Run: python3 gen_site.py
Regenerates index.html and articles/*.html from the shared templates below.
No build tooling needed afterwards — the output is plain, dependency-free HTML/CSS.
"""
import json, re, os, math

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, 'articles.json'), encoding='utf-8'))
OUT_ARTICLES = os.path.join(ROOT, 'articles')
os.makedirs(OUT_ARTICLES, exist_ok=True)

PALETTE = ['verdigris', 'brass']
HEX = {'verdigris': '#6f9c8d', 'brass': '#c79a4b'}

def slugify(name):
    s = name.lower()
    s = s.replace('&', 'and')
    s = re.sub(r"[’']", '', s)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s

for i, a in enumerate(DATA):
    a['slug'] = slugify(a['company'])
    a['accent'] = PALETTE[i % 2]

def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

def rings_svg(seed, accent_hex, size=200, big=False):
    """Concentric, slightly irregular ring motif — the site's one recurring mark."""
    rnd = lambda k: (math.sin(seed * 12.9898 + k * 78.233) * 43758.5453) % 1
    cx, cy = size/2, size/2
    parts = []
    n = 4 if big else 3
    base_r = size * 0.44
    for k in range(n):
        r = base_r * (1 - k * (0.22 + rnd(k)*0.05))
        dash_gap = 6 + rnd(k+10) * 10
        opacity = 1 - k * 0.14
        parts.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" '
            f'stroke="{accent_hex}" stroke-width="{1.1 if not big else 1.4}" '
            f'stroke-dasharray="{900}" opacity="{opacity:.2f}"/>'
        )
    # small centre mark — the keep
    parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{2.6 if not big else 3.4}" fill="{accent_hex}"/>')
    cls = 'ring-draw' if big else ''
    return f'<svg class="{cls}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{"".join(parts)}</svg>'

SITE_NAME = 'Moat & Motive'
AUTHOR = 'Nandini Shankhyan'
TAGLINE = 'A field guide to why some companies keep winning, and what could end it.'

ICON_DATA = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="%2312140f"/><circle cx="16" cy="16" r="12" fill="none" stroke="%23c79a4b" stroke-width="1.6"/><circle cx="16" cy="16" r="7" fill="none" stroke="%236f9c8d" stroke-width="1.6"/><circle cx="16" cy="16" r="2" fill="%23c79a4b"/></svg>'

def masthead(css_path):
    """css_path: 'assets/styles.css' for the homepage, or 'articles/x.html' for an essay page."""
    root = '' if css_path == 'assets/styles.css' else '../'
    return f'''<header class="masthead">
  <div class="wrap">
    <a class="mark" href="{root}index.html">Moat <em>&amp;</em> Motive</a>
    <nav>
      <a href="{root}index.html#index">Essays</a>
      <a href="{root}index.html#about">About</a>
    </nav>
  </div>
</header>'''

def footer(css_path):
    return f'''<footer>
  <div class="wrap">
    <span>&copy; 2026 {AUTHOR}. {SITE_NAME}.</span>
    <span>Twelve essays on corporate advantage, 2026.</span>
  </div>
</footer>'''

# ---------------- INDEX PAGE ----------------

index_items = []
for a in DATA:
    accent_hex = HEX[a['accent']]
    thumb = rings_svg(a['num'], accent_hex)
    index_items.append(f'''    <li class="index-item">
      <a href="articles/{a['slug']}.html">
        <span class="index-num">{a['num']:02d}</span>
        <span class="index-thumb">{thumb}</span>
        <span class="index-body">
          <h3>{esc(a['company'])}</h3>
          <p class="question">{esc(a['question_title'])}</p>
        </span>
        <span class="index-arrow">&#8594;</span>
      </a>
    </li>''')

hero_art = rings_svg(0.5, HEX['brass'], size=240, big=True)

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
      <h1>Every business<br>digs a moat.<br><span class="accent">Not every moat holds.</span></h1>
      <p class="lede">{TAGLINE} Twelve essays by {AUTHOR} on the companies redrawing their defenses for the age of AI — and where the water is already draining out.</p>
    </div>
    <div class="hero-art">{hero_art}</div>
  </div>
</section>

<section class="wrap" id="index">
  <div class="section-head">
    <h2>The essays</h2>
    <span class="count">01 — 12</span>
  </div>
  <ul class="index-list">
{chr(10).join(index_items)}
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

{footer('assets/styles.css')}
</body>
</html>'''

open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(index_html)

# ---------------- ARTICLE PAGES ----------------

for i, a in enumerate(DATA):
    accent_hex = HEX[a['accent']]
    watermark = rings_svg(a['num'], accent_hex, size=420, big=True)
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

<section class="article-header">
  <div class="watermark">{watermark}</div>
  <div class="wrap">
    <div class="eyebrow-row"><span class="dot"></span> Essay {a['num']:02d} of 12</div>
    <h1>{esc(a['company'])} — {esc(a['question_title'])}</h1>
    <p class="deck">{esc(a['strategic_question'])}</p>
  </div>
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

{footer('articles/x.html')}
</body>
</html>'''

    open(os.path.join(OUT_ARTICLES, f"{a['slug']}.html"), 'w', encoding='utf-8').write(article_html)

print('Built index.html and', len(DATA), 'article pages.')
for a in DATA:
    print(' -', f"articles/{a['slug']}.html")
