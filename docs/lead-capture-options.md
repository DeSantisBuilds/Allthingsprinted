# Lead capture: FormSubmit today vs. the Cloudflare Worker + Turnstile option

**Recommendation:** keep FormSubmit for launch (it is built, tested and needs no new account). Once allthingsprinted.ca runs on Cloudflare and the site has been live for a few weeks, switch to the Worker + Turnstile option **if** spam reaches your phone or a lead goes missing. Nothing has been changed; both need your approval.

## What the current form does (verified with a stand-in for FormSubmit, nothing sent)

- Posts to `https://formsubmit.co/ajax/info@allthingsprinted.ca` with: request type (new / reorder), name, phone, email, service, artwork status, details, page address and language.
- Email subject carries the key facts, for example `Nouveau lead: Marie Tremblay - 514 555-0100 - Broderie - Recommande`.
- `_cc` sends a copy to `5148151829@txt.bell.ca` (Bell email-to-text) for a text alert.
- Spam protection: a hidden “honeypot” field (`_honey`) only. FormSubmit’s own reCAPTCHA page is turned off (`_captcha=false`) because it loads Google.
- Requires a one-time activation (first real submission → activation email to info@).

## Exposed addresses

Anyone (and any bot) reading the page source sees:

- `info@allthingsprinted.ca` in the form address. Mitigation available now: after activation, replace it with the FormSubmit alias (random string). The address is also published on the site on purpose as a contact link, so this mainly reduces automated form spam.
- `5148151829@txt.bell.ca` in the hidden `_cc` field. Mitigation: only possible by moving the form to a server (option B), or removing the text alert.

## Comparison

| | A. FormSubmit (current) | B. Cloudflare Worker + Turnstile (built earlier, removed) |
| --- | --- | --- |
| Reliability | Free service with no service guarantee; if it is down or changes its rules, leads fail (visitors see an error with your phone and email). | Runs on your Cloudflare account; Cloudflare’s uptime. Email delivery depends on the email service chosen (for example Resend). |
| Spam protection | Honeypot only. Spam becomes emails **and texts on your phone**. | Turnstile check verified on the server + honeypot; bots are stopped before any email or text. |
| Privacy | Personal data passes through FormSubmit (US). Disclosed in the privacy policy. | Data passes through Cloudflare and the email service (both US-based). Disclosed the same way. |
| Exposed addresses | Email (alias possible) and text address visible in page source. | None in the page; addresses stay in Cloudflare settings. |
| Artwork upload | Not used (customers email their logo). | Possible (the earlier version accepted 5 files, 15 MB). |
| Setup effort | Done. One activation click. | About 1 hour after the domain is on Cloudflare: Turnstile keys, email-service account + DNS records, two secrets in the Worker, redeploy. Code exists in git history (commit `a11c998`). |
| Ongoing work | None. | Low; occasional key rotation. |
| Cost | Free. | Free tiers of Cloudflare Workers, Turnstile and email services cover a small business’s volume; check current limits before choosing. No paid service needed at your volume. |

## Text-message alert caveat

Carrier email-to-text gateways are unofficial and can be slow, truncated or switched off by the carrier. Test it after activation. If Bell doesn’t deliver, alternatives are: notifications from your email app (free), or a paid SMS service (would need your approval).
