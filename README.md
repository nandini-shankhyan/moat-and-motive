# Moat & Motive

A twelve-essay strategy field guide by **Nandini Shankhyan** — plain, editorial, dependency-free HTML and CSS. No build step, no framework, nothing to install to view it.

## What's in here

```
index.html            the homepage (masthead, hero, essay index, about)
articles/*.html        the 12 essays, one file each
assets/styles.css      the entire design system (fonts, colors, layout)
articles.json           the essay text, structured — edit this, not the HTML
gen_site.py             regenerates index.html + articles/*.html from articles.json
```

The site is built from `articles.json` by `gen_site.py`. If you want to fix a typo or update an essay, it's easiest to edit `articles.json` and re-run the generator (see below) rather than hand-editing the HTML files, since they get overwritten on every rebuild.

## View it locally

No server or build tools needed — just open `index.html` in a browser. (Some browsers block fonts/relative links on `file://` — if anything looks off, run a tiny local server instead: `python3 -m http.server`, then visit `http://localhost:8000`.)

## Editing content

1. Open `articles.json`. Each essay is an object with `company`, `question_title`, `strategic_question`, `sections` (each with a `heading` and a list of `paragraphs`), and `sources`.
2. Edit the text.
3. Regenerate the HTML:
   ```
   python3 gen_site.py
   ```
   (Needs Python 3, no extra packages.)
4. Reload the page — that's it.

To add a 13th essay, add one more object to the JSON array with the next `num`, then rebuild.

## Deploy to GitHub Pages

1. **Create a repository** on GitHub (e.g. `moat-and-motive`) — public, so Pages can serve it for free.
2. **Push this folder to it:**
   ```bash
   cd site                      # this folder
   git init
   git add .
   git commit -m "Moat & Motive: initial site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/moat-and-motive.git
   git push -u origin main
   ```
3. **Turn on Pages:** on GitHub, go to the repo's **Settings → Pages**. Under "Build and deployment," set **Source** to "Deploy from a branch," pick branch **main** and folder **/ (root)**, then **Save**.
4. GitHub will publish the site at `https://<your-username>.github.io/moat-and-motive/` within a minute or two — the same Settings → Pages screen shows the live link once it's ready.
5. Whenever you edit `articles.json` and re-run `gen_site.py`, just commit and push again (`git add . && git commit -m "update essay" && git push`) — Pages redeploys automatically.

### Using a custom domain (optional)

If you own a domain, add it in Settings → Pages → "Custom domain," then create a `CNAME` record at your DNS provider pointing to `<your-username>.github.io`. GitHub adds a `CNAME` file to the repo automatically once you save that setting.

## Design notes

The whole visual identity runs on one recurring idea — a generated abstract cover for every essay, built from layered gradients, faceted line-art shapes, and a fine grain pass, all as inline SVG. Nothing is a stock photo or an external image, so the page loads instantly, nothing ever 404s, and there's no image licensing to worry about. Each essay has its own color palette keyed to its subject (amber for energy, green for compute, monochrome for Apple, and so on) — see PALETTES near the top of gen_site.py to change them. Two typefaces carry it: **Fraunces** for display headlines, **Source Serif 4** for reading text, set in ink-black on a warm paper background. Everything lives in `assets/styles.css` if you want to adjust colors, type sizes, or spacing.
