# All Things Printed — website

A static, single-page website for All Things Printed. It is plain HTML, CSS and JavaScript with no build step, so GitHub Pages can publish it as-is.

## Files

| File | What it is |
|------|------------|
| `index.html` | All page content (edit text and placeholders here) |
| `css/styles.css` | Styling. Brand colours are at the top under `:root` |
| `js/main.js` | Mobile menu and the quote form |
| `assets/images/` | Put your logo and photos here (`assets/images/gallery/` for gallery photos) |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is |

## Placeholders to fill in

Search `index.html` for **`PLACEHOLDER`** and **`EDIT`**. Placeholders show on the page with a yellow dashed highlight until you replace them.

Already filled in: email (info@allthingsprinted.ca, also used by the quote form), phone ((515) 815-1829) and website (www.allthingsprinted.ca). They appear in the Contact section and the footer. If any of them change, update both places and the form's `data-quote-email`.

Still to fill in:

1. **Service area.** This appears in both the About section and the Contact section.
2. **Hours.** Fill in your hours or delete that line.
3. **Social links.** Replace `href="#"` with your profile URLs, change the link text (for example, "Facebook"), and remove `class="placeholder"` and `data-placeholder-link`. Delete any links you don't use.
4. **About text.** Replace the dashed placeholder paragraph with your story.
5. **Service details** (optional). HTML comments under each service show where to add details like minimums or specific products.
6. **Logo/favicon** (optional). Instructions are in comments in the `<head>` and header.
7. **Gallery photos.** Replace each `gallery-placeholder` block with an `<img>` tag. The exact markup is in the comment above the gallery.

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
