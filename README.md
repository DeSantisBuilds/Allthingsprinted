# All Things Printed — website

A static, single-page website for All Things Printed. It is plain HTML, CSS and JavaScript with no build step, so GitHub Pages can publish it as-is.

## Files

| File | What it is |
|------|------------|
| `index.html` | **French page (main page)** at `/` |
| `en/index.html` | English page at `/en/` |
| `css/styles.css` | Styling. Brand colours are at the top under `:root` |
| `js/main.js` | Mobile menu, hero animation and the quote form (messages in French or English, based on the page language) |
| `assets/images/` | Logo files (PNG and WebP), favicon, social sharing image (`og-image.jpg`) |
| `confidentialite.html`, `en/privacy.html` | Privacy policy (French, English) |
| `worker/index.js`, `wrangler.toml` | Cloudflare Worker: serves the site and handles the online quote form |
| `tests/` | Tests for the Worker (`npm test`) |
| `assets/fonts/` | Self-hosted Archivo font (open licence in `OFL.txt`) |
| `robots.txt`, `sitemap.xml` | Help search engines find both language versions |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is |

**Any text change must be made in both `index.html` (French) and `en/index.html` (English).**

## Business details on the site

- Phone: (514) 815-1829 · Email: info@allthingsprinted.ca (also where the quote form sends) · Website: www.allthingsprinted.ca
- Instagram: @allthingsprintedinc · Hours: Monday to Saturday, 9 a.m. to 5 p.m. · Service area: Greater Montreal
- Turnaround 10–15 business days · Vector files print-ready, other files adjusted for a fee · Visual mockups included, sent once the quote is approved · 50% deposit, 50% on completion · Delivery fees may apply

These also appear in the structured data (`<script type="application/ld+json">`) in the `<head>` of both pages, which Google reads. Update them there too if they change.

## Still to add when you have them

1. **Gallery photos.** The Gallery section is hidden (`hidden` attribute) until real photos exist. Instructions are in the comment above it in both pages.
2. **Minimum quantities** and any other FAQ answers.
3. **Specific promotional products** you can confirm.

## How the quote form works

The form has two modes. The switch is `turnstileSiteKey` in the `CONFIG` block at the top of `js/main.js`.

- **Email-app mode (current, `turnstileSiteKey` empty).** Pressing *Préparer le courriel* opens the visitor's email app with the request filled in, addressed to `data-quote-email` on the form. The visitor attaches artwork and sends it. No server is needed.
- **Online mode (`turnstileSiteKey` set).** The form shows a file upload and a Cloudflare Turnstile security check, and sends the request to the Cloudflare Worker (`worker/index.js`). The Worker verifies the Turnstile token with Cloudflare, checks the fields and files (up to 5 files, 15 MB total; PNG, JPG, PDF, SVG, AI, EPS, PSD, TIFF, WEBP), and emails everything, files attached, to `QUOTE_TO` through [Resend](https://resend.com). It also has a hidden "honeypot" field that silently drops bots.

## Online quote form (Cloudflare Turnstile) setup

Do these once, in this order. Nothing secret goes in the code.

1. **Turnstile keys.** Cloudflare dashboard → *Turnstile* → *Add widget*. Add every hostname the site runs on (`allthingsprinted.ca`, `www.allthingsprinted.ca`, and your `*.workers.dev` or `desantisbuilds.github.io` address if used). Choose *Managed*. Copy the **site key** and the **secret key**.
2. **Email sending (Resend).** Create a Resend account, add the domain `allthingsprinted.ca` and add the DNS records it shows. Before saving, check that none of them replace your existing email (MX) records, so info@allthingsprinted.ca keeps working. Create an API key with sending access.
3. **Worker secrets.** Cloudflare dashboard → *Workers & Pages* → *allthingsprinted* → *Settings* → *Variables and Secrets*: add `TURNSTILE_SECRET` (the Turnstile secret key) and `RESEND_API_KEY` as **Secrets**. Or, from this folder: `npx wrangler secret put TURNSTILE_SECRET` and `npx wrangler secret put RESEND_API_KEY`.
4. **Check `wrangler.toml`:** `QUOTE_TO` (where requests arrive), `QUOTE_FROM` (must use the domain verified in Resend).
5. **Deploy the Worker.** Either connect this GitHub repository to the Worker (*Settings* → *Builds*), or run `npx wrangler deploy`. The Worker serves the whole website and the form at `/api/quote`.
6. **Switch the form on.** Paste the Turnstile **site key** into `turnstileSiteKey` in `js/main.js`. If the website stays on GitHub Pages instead of the Worker, also set `quoteEndpoint` to the Worker's full address ending in `/api/quote`.
7. **Test** by sending yourself a request with a small file.

Run the Worker tests with `npm test` (Node 18 or newer).

## Cookies and privacy

- The site sets **no advertising or tracking cookies** and loads nothing from Google (the font is self-hosted in `assets/fonts/`).
- A small notice appears on the first visit. Visitors can reopen it with *Paramètres des témoins / Cookie settings* in the footer. Their choice is stored in their own browser.
- **If you add analytics**, put the Cloudflare Web Analytics token or Google Analytics ID in `CONFIG` in `js/main.js`. The notice then automatically becomes a real choice (*Tout accepter / Refuser / Personnaliser*), and the analytics script only loads after the visitor accepts.
- Privacy policy pages: `confidentialite.html` (French) and `en/privacy.html` (English). Have them reviewed, and update them if you add analytics or other services.

## Publishing with GitHub Pages

1. Merge this work into your repository's default branch (for example `main`).
2. On GitHub, open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, select your default branch and `/ (root)`, then save.
4. Because the repository is named `desantisbuilds.github.io`, the site will be at `https://desantisbuilds.github.io/`.

To preview locally, open `index.html` in a browser, or run `python3 -m http.server` in this folder and visit `http://localhost:8000`.
