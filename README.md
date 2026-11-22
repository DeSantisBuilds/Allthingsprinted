# All Things Printed — website

A static, single-page website for All Things Printed. It is plain HTML, CSS and JavaScript with no build step, so GitHub Pages can publish it as-is.

## Files

| File | What it is |
|------|------------|
| `index.html` | All page content (edit text and placeholders here) |
| `css/styles.css` | Styling. Brand colours and type are at the top under `:root` |
| `js/main.js` | Mobile menu, the quote form, and the one-time hero colour animation |
| `assets/images/` | Put your logo and photos here (`assets/images/gallery/` for gallery photos) |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is |

## Look and feel

The design uses the original All Things Printed colours (deep ink navy, warm off-white, process cyan, magenta and yellow) with printer's proof details: crop marks around the hero and quote form, a colour bar, and a headline printed in slightly offset inks. Everything uses one typeface, Archivo, with headings set in its expanded width. To change colours or type, edit the tokens under `:root` at the top of `css/styles.css`.

## Placeholders to fill in

Search `index.html` for **`PLACEHOLDER`** and **`EDIT`**. Placeholders show on the page with a yellow dashed highlight until you replace them.

Already filled in, in the Contact section and the footer:

- Email: info@allthingsprinted.ca (also where the quote form sends)
- Phone: (515) 815-1829
- Website: www.allthingsprinted.ca
- Instagram: @allthingprinted
- Hours: Monday to Saturday, 9 a.m. to 5 p.m.
- Service area: Greater Montreal (also in the About section)

If any of these change, update every place they appear. For the email, that includes the form's `data-quote-email`.

Still to add when you have them:

1. **Gallery photos.** Replace each `gallery-placeholder` block with an `<img>` tag. The exact markup is in the comment above the gallery.
2. **About text** (optional). Add paragraphs to the About section if you want to tell your story.
3. **Service details** (optional). HTML comments under each service show where to add details like minimums or specific products.
4. **Logo/favicon** (optional). Instructions are in comments in the `<head>` and header.

## How the quote form works

GitHub Pages can't run a server, so the form does not send anything by itself. When a visitor clicks **Prepare Email**, the form opens their email app with a pre-filled message addressed to you. The visitor then sends it, and can attach artwork first. The page says this clearly next to the form.

If you'd rather receive submissions without relying on the visitor's email app, you can connect a form service such as Formspree or Basin later. That would need changes to `js/main.js`.

## Publishing with GitHub Pages

1. Merge this work into your repository's default branch (for example `main`).
2. On GitHub, open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, select your default branch and `/ (root)`, then save.
4. Because the repository is named `desantisbuilds.github.io`, the site will be at `https://desantisbuilds.github.io/`.

To preview locally, open `index.html` in a browser, or run `python3 -m http.server` in this folder and visit `http://localhost:8000`.
