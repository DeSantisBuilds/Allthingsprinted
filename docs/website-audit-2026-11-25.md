# All Things Printed — Website Re-Audit after the Elevation Sprint

**Date:** 2026-11-25 · **Branch audited:** `claude/elevation-sprint` (private development preview, **not deployed**) · **Baseline:** audit of 2026-11-25 (live site at workers.dev, commit `575cd00`)

## Verdict

The development version scores **83.75 / 100**, up from **71.25**, using the same eight categories and the same 0–10 scale as the first audit. The remaining distance to the 90–95 target is blocked by things only the owner can provide: the domain connection, real photos of finished work, Google reviews and a live form test. Nothing on the live website has changed yet; it still scores 71.25 until this branch is approved and deployed.

## Scorecard (same methodology: eight categories, 0–10 each, average × 10)

| Category | Before | After (dev) | Evidence for the change | What still holds it back |
| --- | --- | --- | --- | --- |
| Technical performance | 10 | 10 | Lighthouse 99–100 performance on 12 runs (6 pages × phone/desktop); layout shift 0 on 20 repeated runs; pages 119–128 KB (was 173–178 KB); one-year caching of versioned files | Nothing significant |
| Accessibility | 9 | 9.5 | axe: 0 violations in 42 scans (all 21 pages, desktop + phone, cookie notice and phone menu open); keyboard order and focus outline on 60 stops; worst-case hero text contrast 7.4:1 measured on rendered pixels; cookie-settings tap target fixed | No manual screen-reader test yet (VoiceOver/NVDA) |
| Responsive design | 9 | 10 | 21 pages × 6 widths (375–1920 px) = 126 checks: no horizontal scroll, overlap, clipped content, text under 12 px or tap target under 24 px; shirt label now 11–14 px tall (was 9 px) | — |
| Visual design and branding | 7 | 8 | Same identity, refined: wider hero text column, trust chips, clickable ink-coded service cards, cap and tuque icon (was a hard hat), larger shirt label, Instagram panel, consistent system across 21 pages | **No real photography** — the main premium gap |
| User experience | 7 | 8.5 | 8 service pages with breadcrumbs; phone action bar (Call / Text / Quote); every service and garment pre-fills the form; artwork and reorder workflow; industries section; the site’s own bilingual form validation | No proof of work yet (photos, reviews) |
| SEO and discoverability | 5 | 7 | 16 bilingual service pages with unique titles (35–60 characters), descriptions (113–155), one keyword H1 each (headline text now once in code); clean URLs with no internal redirects; hreflang reciprocal; LocalBusiness, WebSite, Service and BreadcrumbList data; sitemap of 20 pages | **Domain still serves Shopify’s error page**, so Google cannot index the site; no Google Business Profile |
| Security and privacy | 6 | 8 | Content-Security-Policy, HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, X-Frame-Options, COOP via `_headers`, verified on Cloudflare’s own local server with no console violations; no third-party requests on page load | Form-routing email and Bell text address readable in page source; honeypot is the only spam filter; FormSubmit is a third party with no guarantee |
| Commercial effectiveness | 4 | 6 | Quote reachable from every screen on phones; text option; service-specific quote buttons; reorder path; seasonal banner ready (off); Instagram promoted | Domain broken; form not activated or tested live; no photos, reviews or price cues |
| **Total** | **71.25** | **83.75** | | |

**Projection, not a measured score:** if the owner completes the domain migration, Google Business Profile, 15–30 real photos, first reviews and the form activation (and later the Worker + Turnstile form), the same method would place the site at roughly **93–95** (SEO 9, commercial 9, visual 9.5, UX 9.5, security 9–9.5).

## What was verified, and how

| Check | Result | Evidence file |
| --- | --- | --- |
| Internal links and files on every page | 32 unique internal URLs, all HTTP 200 with no redirect (only the deliberate 404 test returns 404) | `evidence/suite-summary.txt`, `suite-report.json` |
| Responsive, 21 pages × 6 widths | 126 checks, no layout issue (6 lines are the 404 page’s own “not found” status) | `evidence/suite-summary.txt` |
| Accessibility (axe-core 4.10, WCAG 2.0–2.2 A/AA + best practices) | 0 violations in 42 scans | `evidence/suite-report.json` |
| Contrast on gradients (manual measurement) | Lowest 7.4:1 (requirement 4.5:1) | `evidence/hero-contrast.txt` |
| Keyboard, focus, skip link, phone menu, reduced motion, animation end | All pass | `evidence/interaction-tests.txt` |
| Quote form (FormSubmit replaced by a stand-in; nothing sent) | Correct endpoint, fields, subject, Bell copy, page address; validation, success and failure messages in FR and EN | `evidence/interaction-tests.txt` |
| SEO metadata on all pages | Titles 35–60 characters, descriptions 113–155, one H1, canonical = own clean URL, 3 hreflang links, valid structured data | `evidence/seo-checks.txt` |
| Security headers and caching | Applied by Cloudflare’s local server (`wrangler dev`); private files (README, tools, config) return 404 | this report, `evidence/deploy-dry-run.txt` |
| Lighthouse 12.2 | 99–100 / 100 / 100 / 100 on 12 runs | `evidence/lighthouse/` (HTML reports) |
| Production build | `wrangler deploy --dry-run` accepted (static assets, no server code) | `evidence/deploy-dry-run.txt` |

Lighthouse ran against the local Cloudflare server, which does not compress files the way the live Cloudflare network does (Brotli was verified on the live address), so real-world transfer sizes will be slightly smaller.

## Not verified (requires approval or the owner’s accounts)

- A real form submission, the FormSubmit activation email and the Bell text alert (would send email and a text to the owner).
- The site on allthingsprinted.ca, its HTTPS certificate and `www` redirect (domain not connected).
- DNS and email records (not reachable from the test environment).
- Manual screen-reader testing, and testing on physical iPhone and Android devices.
- French copy review by a fluent Quebec-French reader; legal review of the privacy policy.

## Deployment drift

The live workers.dev site was deployed from the pull-request branch (`575cd00`), while `main` is 15 commits behind (`2277329`). Merging the sprint into `main` before connecting Cloudflare Builds avoids publishing the old design. Details: `docs/deployment-and-drift.md`.

## Related documents

- `docs/sprint-changes-and-outstanding.md` — every implemented change and every open item that needs the owner
- `docs/launch-readiness.md` — go / no-go list for production
- `docs/domain-migration-checklist.md` — allthingsprinted.ca to Cloudflare, protecting email
- `docs/google-business-and-search-console-checklist.md`
- `docs/photography-shot-list.md` — 30 photos, matched to the site’s photo slots
- `docs/lead-capture-options.md` — FormSubmit vs. Worker + Turnstile
