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

This website has no server, so the form does not send anything by itself. When a visitor clicks **Prepare Email**, the form opens their email app with a pre-filled message addressed to you. The visitor then sends it, and can attach artwork first. The page says this clearly next to the form.

If you'd rather receive submissions without relying on the visitor's email app, you can connect a form service such as Formspree or Basin later. That would need changes to `js/main.js`.

## Publishing with GitHub Pages

1. Merge this work into your repository's default branch (for example `main`).
2. On GitHub, open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, select your default branch and `/ (root)`, then save.
4. Because the repository is named `desantisbuilds.github.io`, the site will be at `https://desantisbuilds.github.io/`.

To preview locally, open `index.html` in a browser, or run `python3 -m http.server` in this folder and visit `http://localhost:8000`.
