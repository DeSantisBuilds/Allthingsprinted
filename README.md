# All Things Printed — website

Static bilingual website for All Things Printed (Greater Montreal). French is the main language (`/`), English is at `/en/`. Plain HTML, CSS and a small script; no framework. Hosted as static files by the Cloudflare Worker `allthingsprinted`.

## How the site is built

Pages are **generated** from one content file, so the header, footer, quote form and metadata stay identical everywhere.

| File | What it is |
|------|------------|
| `tools/content.py` | **All site text and facts** (services, FAQ, industries, contact details, photo list, seasonal banner). Edit this. |
| `tools/build.py` | The generator (Python 3, standard library only). Writes the HTML pages, `sitemap.xml` and `robots.txt`. |
| `tools/policy_fr.html`, `tools/policy_en.html` | Privacy policy text |
| `css/styles.css` | Styles. Brand colours and fonts are at the top under `:root`. `css/nojs.css` is used only without JavaScript. |
| `js/main.js` | Phone menu, hero animation, cookie notice, quote form. Optional analytics settings in `CONFIG` at the top. |
| `_headers` | Security headers and caching rules (Cloudflare) |
| `wrangler.toml`, `.assetsignore` | Cloudflare settings; files that are never published |
| `docs/` | Audit, checklists and shot list (never published) |

Generated (do not edit by hand): `index.html`, `en/index.html`, `services/*/index.html`, `en/services/*/index.html`, `confidentialite.html`, `en/privacy.html`, `404.html`, `sitemap.xml`, `robots.txt`.

### To change something

1. Edit `tools/content.py` (or the CSS/JS).
2. Run `python3 tools/build.py`.
3. Commit the changed files.

To see a private preview copy (links end in `index.html`, temporary photo slots visible, the form sends nothing): `python3 tools/build.py --preview /some/folder`.

To test locally exactly as Cloudflare serves it (clean URLs, headers, 404): `npx wrangler dev`.

## Pages

| French | English |
| --- | --- |
| `/` | `/en/` |
| `/services/vetements-personnalises/` | `/en/services/custom-apparel/` |
| `/services/impression-dtf/` | `/en/services/dtf-printing/` |
| `/services/broderie/` | `/en/services/embroidery/` |
| `/services/lettrage-vinyle/` | `/en/services/vinyl-lettering/` |
| `/services/enseignes/` | `/en/services/signage/` |
| `/services/produits-promotionnels/` | `/en/services/promotional-products/` |
| `/services/impression-evenements/` | `/en/services/event-printing/` |
| `/services/conception-graphique/` | `/en/services/graphic-design/` |
| `/confidentialite` | `/en/privacy` |

## Business facts on the site (owner-confirmed)

Phone (514) 815-1829 · info@allthingsprinted.ca · Instagram @allthingsprintedinc · Monday–Saturday 9–17 · Greater Montreal · turnaround 10–15 business days · vector files print-ready, other files adjusted for a fee · visual mockup included, sent once the quote is approved · 50% deposit, 50% on completion · delivery fees may apply.

Do not add prices, minimum quantities, equipment, client names or reviews unless the owner confirms them.

## Quote form

Delivered by FormSubmit to info@allthingsprinted.ca, with a copy to the Bell email-to-text address for 514 815-1829. It needs a one-time activation (first real submission). See `docs/lead-capture-options.md` for the comparison with a Cloudflare Worker + Turnstile form.

## Photos of completed work

Add real photos to `PORTFOLIO` in `tools/content.py` (format shown there) and rebuild. Until then, the public site shows an Instagram panel. What to shoot: `docs/photography-shot-list.md`.

## Launch

See `docs/launch-readiness.md`, `docs/deployment-and-drift.md` and `docs/domain-migration-checklist.md`.
