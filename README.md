# All Things Printed — website

A static, single-page website for All Things Printed. It is plain HTML, CSS and JavaScript with no build step, so GitHub Pages can publish it as-is.

## Files

| File | What it is |
|------|------------|
| `index.html` | All page content (edit text and placeholders here) |
| `css/styles.css` | Styling. The "Press Proof" theme's brand colours and type are at the top under `:root` |
| `js/main.js` | Mobile menu, the quote form, and the one-time hero colour animation |
| `assets/images/` | Put your logo and photos here (`assets/images/gallery/` for gallery photos) |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is |

## Look and feel

The design is styled like a printer's proof sheet: process cyan, magenta and yellow with black ink on a cool white page, crop marks around the hero and quote form, a colour bar, and a headline printed in slightly offset inks. Everything uses one typeface, Archivo, with headings set in its expanded width. To change colours or type, edit the tokens under `:root` at the top of `css/styles.css`.

## Placeholders to fill in

Search `index.html` for **`PLACEHOLDER`** and **`EDIT`**. Placeholders show on the page with a yellow dashed highlight until you replace them.

1. **Email.** Replace `you@example.com` and the text `[PLACEHOLDER — your email]` in the Contact section.
2. **Quote form email.** Set `data-quote-email="you@example.com"` on the `<form id="quote-form">` tag to your real address. Until you change it, the form won't open an email. It tells visitors that online quotes aren't set up yet.
3. **Phone.** Replace `tel:+10000000000` and the visible text.
4. **Service area.** This appears in both the About section and the Contact section.
5. **Hours.** Fill in your hours or delete that line.
6. **Social links.** Replace `href="#"` with your profile URLs, change the link text (for example, "Facebook"), and remove `class="placeholder"` and `data-placeholder-link`. Delete any links you don't use.
7. **About text.** Replace the dashed placeholder paragraph with your story.
8. **Service details** (optional). HTML comments under each service show where to add details like minimums or specific products.
9. **Logo/favicon** (optional). Instructions are in comments in the `<head>` and header.
10. **Gallery photos.** Replace each `gallery-placeholder` block with an `<img>` tag. The exact markup is in the comment above the gallery.

Once you replace a placeholder, also remove its `class="placeholder"` so the yellow highlight goes away.

## How the quote form works

GitHub Pages can't run a server, so the form does not send anything by itself. When a visitor clicks **Prepare Email**, the form opens their email app with a pre-filled message addressed to you. The visitor then sends it, and can attach artwork first. The page says this clearly next to the form.

If you'd rather receive submissions without relying on the visitor's email app, you can connect a form service such as Formspree or Basin later. That would need changes to `js/main.js`.

## Publishing with GitHub Pages

1. Merge this work into your repository's default branch (for example `main`).
2. On GitHub, open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, select your default branch and `/ (root)`, then save.
4. Because the repository is named `desantisbuilds.github.io`, the site will be at `https://desantisbuilds.github.io/`.

To preview locally, open `index.html` in a browser, or run `python3 -m http.server` in this folder and visit `http://localhost:8000`.
