# Google Business Profile and Search Console checklist

Do these **after** allthingsprinted.ca serves the new site (see `docs/domain-migration-checklist.md`). No rankings or results are promised; these steps make the business eligible to appear and let you see how Google treats the site.

## Google Business Profile (Maps and “near me” searches)

- [ ] Go to business.google.com with the business Google account (not a personal one, if possible).
- [ ] **Business name:** exactly the real-world name, “All Things Printed” (no keywords added; Google penalizes keyword-stuffed names).
- [ ] **Business type:** a **service-area business** if customers don’t visit a shop. Then **hide the address**; enter the service area as cities/regions (for example Montréal, Laval, Longueuil, and the others you really serve). Don’t publish an address you don’t want public, and never a fake one.
- [ ] **Primary category:** choose the closest real one offered, for example “T-shirt printing service” / “Service d’impression de t-shirts”, or “Screen printer” only if accurate. **Secondary categories:** only services you really offer (embroidery, sign shop, promotional products supplier, etc., as listed by Google).
- [ ] **Phone:** 514 815-1829. **Website:** `https://allthingsprinted.ca/`. **Hours:** Monday–Saturday, 9:00–17:00.
- [ ] **Services:** add the eight services from the website, in French and English descriptions.
- [ ] **Verification:** Google decides the method (video, phone, mail). Follow it; it can take days.
- [ ] **Photos:** logo, cover photo, and real work photos (see `docs/photography-shot-list.md`). Add new ones regularly.
- [ ] **Reviews:** after each completed order, send the profile’s review link to happy customers. Never buy reviews, write them yourself or offer discounts for reviews (against Google’s rules and Quebec consumer law). Reply to every review, in the customer’s language.
- [ ] Keep name, phone and website **identical** on Instagram, Facebook (if added) and directories (for example Pages Jaunes / Yellow Pages).

## Google Search Console (indexing and search performance)

- [ ] search.google.com/search-console → **Add property** → **Domain** → `allthingsprinted.ca`.
- [ ] Verify with the **DNS TXT record** Google provides: Cloudflare → DNS → Add record → TXT at `@`. (Verification covers http/https and www.)
- [ ] **Sitemaps** → submit `https://allthingsprinted.ca/sitemap.xml` (20 pages: home, 8 services and privacy, in French and English).
- [ ] **URL Inspection** → test `https://allthingsprinted.ca/` and `https://allthingsprinted.ca/en/` → **Request indexing**.
- [ ] After 1–2 weeks, check **Pages** (indexed vs not), **Experience → Core Web Vitals** (expected good: layout shift 0 and fast loading in tests), and **Enhancements** (breadcrumbs).
- [ ] Bing: bing.com/webmasters → **Import from Google Search Console** (2 minutes, covers Bing and DuckDuckGo).

## Optional measurement (with consent)

- [ ] If you want visitor statistics, the simplest privacy-friendly option is **Cloudflare Web Analytics** (free). Put its token in `CONFIG.cloudflareAnalyticsToken` in `js/main.js`, add `https://static.cloudflareinsights.com` to `script-src` and `https://cloudflareinsights.com` to `connect-src` in `_headers`, rebuild, and update the privacy policy. The cookie notice then asks visitors for consent automatically.
