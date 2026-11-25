# Elevation sprint — implemented changes and outstanding items

Branch: `claude/elevation-sprint` (from the live version `575cd00`). Not merged, not deployed.

## Implemented and verified

### Architecture
- Small generator (`tools/build.py`, Python standard library only) builds all pages from one content file (`tools/content.py`). The generated HTML is committed, so Cloudflare needs no build step and no framework was added.
- 21 pages: French home (main) and English home, 8 service pages in each language, privacy policy in each language, a bilingual 404 page.
- Clean addresses (`/services/broderie/`, `/en/services/embroidery/`, `/confidentialite`) served directly with no redirects; old `.html` links still redirect correctly.
- Every CSS, JS and image link carries a version code, so browsers can cache them for a year and always get updates.

### Services (from the owner’s overview only; no prices, minimums, equipment or reviews)
- Custom apparel, DTF printing, embroidery, vinyl lettering, signage, promotional products, event printing, graphic design — each with a service hero, description, options, uses, who it’s for, FAQ, related services and a pre-selected quote form.

### Visual
- Hero: wider text column, kicker, trust chips (mockup included, 10–15 business days, Greater Montreal, hours), same ink circles and overprint effect.
- Overprinted headline drawn by CSS: identical look, but the words are in the page once (fixes SEO duplication and screen-reader repetition).
- Cap and tuque icon (the old one read as a hard hat); “( VOTRE LOGO ICI )” label enlarged (11–14 px tall, was 9 px).
- Service cards: fully clickable, ink-coded, “Voir le service →”.
- Portfolio component: real photos appear automatically when added; until then the public site shows an Instagram panel, and the private preview shows clearly labelled temporary slots naming the photo to take.
- Stylesheet rewritten: same tokens and look, removed rules for deleted sections; every remaining rule belongs to a real component or state.

### Commercial
- Phone action bar: Call, Text (`sms:`), Quote — always visible on phones.
- Quote form: request type (new / reorder), service pre-selected by page, artwork status, page address sent with the lead; garments add “Product: …” to the details.
- Artwork workflow box with an email button (subject pre-filled).
- Industries served section (six customer groups).
- Seasonal banner ready, off in production (`SEASONAL["enabled"]`).

### SEO
- Unique titles and descriptions per page; one keyword H1 per page; canonical to `https://allthingsprinted.ca/...`; reciprocal hreflang (fr-CA, en-CA, x-default); LocalBusiness + WebSite + Service + BreadcrumbList data; sitemap with 20 pages and alternates; social-sharing tags on every page.

### Security, privacy, accessibility, performance
- `_headers`: Content-Security-Policy (self only + FormSubmit), HSTS, nosniff, Referrer-Policy, Permissions-Policy, X-Frame-Options, COOP; long caching for versioned files.
- `wrangler.toml`: 404 page and clean-URL handling; `.assetsignore` keeps tools, docs and config private.
- Cookie notice links to the correct privacy page from every page; cookie-settings button is a proper tap target.
- Fixed a phone layout shift (0.3 → 0) caused by the no-JavaScript menu fallback; added metric-matched fallback fonts.
- Form uses the site’s own bilingual validation and focuses the first missing field.
- Logo files renamed (an “@” in the name caused a redirect).

## Bugs found and fixed during verification
- Overprint layers misaligned on multi-line headlines → layers now block-level.
- Cookie notice privacy link broken on service pages → reads the footer link.
- High-resolution header logo redirected (307) → renamed.
- `upgrade-insecure-requests` CSP directive removed (redundant on an all-HTTPS site; broke local testing).
- Empty-form submit showed the browser popup instead of the site message → `novalidate`.
- Phone layout shift race → `<noscript>` stylesheet.

## Outstanding — needs the owner

| # | Item | Why | Where |
| --- | --- | --- | --- |
| 1 | Approve a pull request from `claude/elevation-sprint` into `main` | Nothing is live until merged and deployed | GitHub |
| 2 | Connect allthingsprinted.ca to Cloudflare, keeping email | The domain shows Shopify’s error page | `docs/domain-migration-checklist.md` |
| 3 | Approve one real test lead; click FormSubmit’s activation email; confirm the Bell text | Leads are not delivered until activation | same, Phase 5 |
| 4 | Take and send real work photos | Biggest remaining design and trust gap | `docs/photography-shot-list.md` |
| 5 | Google Business Profile and reviews; Search Console | Local visibility | `docs/google-business-and-search-console-checklist.md` |
| 6 | Fluent Quebec-French review of all French text | Written by Claude | all French pages |
| 7 | Professional review of the privacy policy | Law 25 | `confidentialite.html` |
| 8 | Optional facts: minimum quantities, starting prices, embroidery wording, confirmed promotional products, city for Google | Not published until confirmed | `tools/content.py` |
| 9 | Decide on the Worker + Turnstile form later | Spam and exposed text address | `docs/lead-capture-options.md` |
| 10 | Test on a real iPhone and Android phone, and with a screen reader | Automated tests can’t replace it | — |

## Future recommendations (not started)
- Real photo gallery and before/after examples once photos exist.
- Cloudflare Web Analytics (with consent) to measure which pages bring quotes.
- Service-area pages only for areas actually served (for example Laval, Longueuil), and only with real local content.
