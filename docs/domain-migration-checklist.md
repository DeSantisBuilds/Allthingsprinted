# Domain migration checklist — allthingsprinted.ca → Cloudflare

**Goal:** allthingsprinted.ca shows the new website (served by the Cloudflare Worker `allthingsprinted`), while **info@allthingsprinted.ca keeps receiving email without interruption.**

**Today (verified 2026-11-25):** `https://allthingsprinted.ca/` returns HTTP 402 “Store unavailable” from a Shopify store, and `www` redirects to it. The new site is live only at `allthingsprinted.salvatore-desantisg.workers.dev`.

Nothing in this checklist has been done. It needs the owner’s accounts (registrar, Shopify, Cloudflare, email provider). Plan about 1–2 hours of work, then up to 24–48 hours for DNS changes to spread. Do it on a quiet day, not before a big order.

---

## Phase 0 — Before touching anything (no risk)

- [ ] **Find the registrar** (where the domain was bought and is renewed): GoDaddy, Namecheap, Shopify, Squarespace (ex-Google Domains), etc. Check the renewal email or a WHOIS lookup.
- [ ] **Find the email provider** for info@allthingsprinted.ca: Google Workspace, Microsoft 365, Zoho, the registrar’s mailbox, or Shopify email forwarding.
- [ ] **Screenshot the current DNS records** at whoever manages DNS today (registrar or Shopify). Keep these screenshots: they are the rollback plan. Especially note:
  - **MX** records (email delivery)
  - **TXT** records: SPF (`v=spf1 …`), DKIM, DMARC (`_dmarc`), and any verification records
  - **CNAME** records for email (for example `autodiscover`, `mail`)
- [ ] **Shopify:** decide whether the store is closed for good. If the domain was *bought through Shopify*, the domain settings and possibly the email forwarding live in Shopify; plan to transfer the domain out, or change its nameservers from Shopify’s domain settings.
- [ ] **Merge pull request #4 / the sprint pull request into `main` first** (see `docs/deployment-and-drift.md`), so the version that goes live is the reviewed one.

## Phase 1 — Add the domain to Cloudflare (no effect yet)

- [ ] Cloudflare dashboard → **Add a domain** → `allthingsprinted.ca` → Free plan.
- [ ] Cloudflare scans the existing DNS. **Compare its list with your screenshots line by line.** Add anything missing, especially every **MX** and **TXT** (SPF, DKIM, DMARC) record and email CNAMEs.
- [ ] Email records must be **DNS only (grey cloud)**, never proxied.
- [ ] Remove or leave aside the old Shopify web records (`A` to Shopify, `CNAME www → shops.myshopify.com`); the Worker replaces them in Phase 3.
- [ ] Cloudflare shows **two nameservers**. Don’t change anything at the registrar yet.

## Phase 2 — Switch nameservers (DNS moves to Cloudflare)

- [ ] At the registrar (or in Shopify if bought there), replace the current nameservers with the two Cloudflare nameservers.
- [ ] Wait for Cloudflare to show the domain as **Active** (minutes to 24 h).
- [ ] **Email test right away:** send an email to info@allthingsprinted.ca from a personal address, and reply from info@. Both must work. If not, compare MX/TXT with the screenshots and fix before going further.

## Phase 3 — Point the domain at the website

- [ ] Cloudflare → **Workers & Pages** → `allthingsprinted` → **Settings** → **Domains & Routes** → **Add** → **Custom domain** → `allthingsprinted.ca`.
- [ ] Repeat for `www.allthingsprinted.ca`.
- [ ] Make `www` redirect to the main address (the site’s canonical address is `https://allthingsprinted.ca/`): **Rules → Redirect Rules** → “www to root” → `https://www.allthingsprinted.ca/*` → `https://allthingsprinted.ca/${1}`, status 301, keep query string.
- [ ] SSL/TLS mode **Full (strict)**; turn on **Always Use HTTPS**.
- [ ] Optional, only after everything works for a week: HSTS preload is **not** needed; the site already sends a one-year HSTS header.

## Phase 4 — Check the live site

- [ ] `https://allthingsprinted.ca/` shows the French home page; `/en/` the English one.
- [ ] `https://www.allthingsprinted.ca/services/broderie/` redirects to `https://allthingsprinted.ca/services/broderie/`.
- [ ] An unknown address (for example `/test-404`) shows the bilingual 404 page.
- [ ] Phone: the bottom bar Call / Text / Quote buttons work.
- [ ] Security headers present (check with securityheaders.com): Content-Security-Policy, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, X-Frame-Options, HSTS.

## Phase 5 — Activate and test the quote form (needs your approval to send)

- [ ] Send one real test request from the live site (your own name, “TEST” in details).
- [ ] FormSubmit emails an **activation link** to info@allthingsprinted.ca → click it.
- [ ] Send a second test. Expect: the email with all fields, and a text on 514 815-1829 (Bell email-to-text). If the text doesn’t arrive, Bell may have disabled email-to-text on the line; see `docs/lead-capture-options.md`.
- [ ] After activation, FormSubmit offers a random alias address. Replace the email in `form_action` in `tools/content.py`, run `python3 tools/build.py`, commit. This hides info@ from spam bots.

## Phase 6 — Tell Google

- [ ] Follow `docs/google-business-and-search-console-checklist.md` (Search Console verification, sitemap submission, Business Profile website link).

## Rollback

If email or the site breaks and can’t be fixed quickly: at the registrar, put back the **original nameservers** (from the Phase 0 screenshots). DNS returns to the previous state within hours. The Cloudflare zone can stay configured for a second attempt.
