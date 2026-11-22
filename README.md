# All Things Printed — website

A simple static website for All Things Printed: plain HTML, CSS and a little JavaScript, no build step. French is the main page; English is at `/en/`.

## Files

| File | What it is |
|------|------------|
| `index.html` | **French page (main page)** at `/` |
| `en/index.html` | English page at `/en/` |
| `confidentialite.html`, `en/privacy.html` | Privacy policy (French, English) |
| `css/styles.css` | Styling. Brand colours are at the top under `:root` |
| `js/main.js` | Mobile menu, hero animation, cookie notice and the lead form |
| `assets/images/` | Logo files (PNG and WebP), favicon, social sharing image (`og-image.jpg`) |
| `assets/fonts/` | Self-hosted Archivo font (open licence in `OFL.txt`) |
| `robots.txt`, `sitemap.xml` | Help search engines find both language versions |
| `wrangler.toml`, `.assetsignore` | Publishing on Cloudflare (see below) |

**Any text change must be made in both `index.html` (French) and `en/index.html` (English).**

## Page sections

Hero (T-shirt with a "( VOTRE LOGO ICI )" print area) → Services → Garments → About → FAQ → Contact and quote form.

## Business details on the site

- Phone: (514) 815-1829 · Email: info@allthingsprinted.ca · Website: www.allthingsprinted.ca
- Instagram: @allthingsprintedinc · Hours: Monday to Saturday, 9 a.m. to 5 p.m. · Service area: Greater Montreal
- FAQ: turnaround 10–15 business days · vector files print-ready, other files adjusted for a fee · visual mockup included, sent once the quote is approved · 50% deposit, 50% on completion · delivery fees may apply

These also appear in the structured data (`<script type="application/ld+json">`) in the `<head>` of both pages. Update them there too if they change.

## Lead form

The form sends each lead straight to **info@allthingsprinted.ca** through [FormSubmit](https://formsubmit.co) (free, no account). The visitor stays on the page and sees a confirmation.

- **Fields:** name, phone, email, service and project details. Clicking a garment adds it to the details.
- **Email:** a table with all the details. Replying to it replies to the customer.
- **Text-message alert:** a copy goes to the Bell email-to-text address `5148151829@txt.bell.ca` (`_cc` in the form), so it arrives as a text on 514 815-1829. The email subject holds the name, phone and service, so the text shows the key facts. If the phone changes carrier, update `_cc` on both pages.
- **Spam:** a hidden "honeypot" field (`_honey`) blocks most bots.

**One-time activation:** the very first time the form is used on the live site, FormSubmit emails info@allthingsprinted.ca an activation link. Click it, and every lead after that is delivered. FormSubmit then also offers a random alias to use in the form's `action` instead of the email address. Swap it in on both pages to keep the address hidden from spam bots.

To change where leads go, edit the form's `action` (email) and `_cc` (text alert) in **both** `index.html` and `en/index.html`.

## Cookies and privacy

- The site sets **no advertising or tracking cookies** and loads nothing from Google (the font is self-hosted).
- A small notice appears on the first visit. Visitors can reopen it with *Paramètres des témoins / Cookie settings* in the footer.
- **If you add analytics**, put the Cloudflare Web Analytics token or Google Analytics ID in `CONFIG` at the top of `js/main.js`. The notice then becomes a real choice (*Tout accepter / Refuser / Personnaliser*), and analytics only load after the visitor accepts. Update the privacy policy too.
- Have the privacy policy pages reviewed before launch.

## Still to add when you have them

- **Photos** of completed work (a gallery section can be added).
- **Minimum quantities** and any other FAQ answers.

## Publishing on Cloudflare (allthingsprinted.ca)

The site is published by the Cloudflare Worker `allthingsprinted`, which serves these files.

1. **Connect the repository.** Cloudflare dashboard → *Workers & Pages* → *allthingsprinted* → *Settings* → *Builds* → connect this GitHub repository, production branch `main`. Every change merged into `main` then deploys automatically. (Alternative: run `npx wrangler deploy` from this folder.)
2. **Connect the domain.** The domain's DNS must be managed by Cloudflare (*Add a domain*, then change the nameservers at your registrar to the two Cloudflare gives you). Then *allthingsprinted* → *Settings* → *Domains & Routes* → *Add* → *Custom domain*: add `allthingsprinted.ca` and `www.allthingsprinted.ca`. HTTPS certificates are created automatically.
3. **Before changing nameservers**, check that Cloudflare imported your existing email records (MX and TXT), so info@allthingsprinted.ca keeps working.
4. Send one test lead from the live site and click FormSubmit's activation email (see "Lead form").

To preview locally, run `python3 -m http.server` in this folder and visit `http://localhost:8000`.
