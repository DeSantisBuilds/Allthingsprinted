# Production-launch readiness — 2026-11-25

**Assessment: the code is ready to launch; the business setup is not.** The development build passes every automated check. Launch is blocked by four owner actions: approve the merge, connect the domain, activate the form, and review the French text.

| Gate | Status | Notes |
| --- | --- | --- |
| Build passes Cloudflare’s deploy check | Ready | `wrangler deploy --dry-run` accepted |
| All internal links load without redirect | Ready | 32 URLs, all 200 |
| Responsive at 375–1920 px | Ready | 126 page × width checks |
| Accessibility (automated, WCAG 2.2 AA) | Ready | 0 violations / 42 scans; manual screen-reader test pending |
| Performance | Ready | Lighthouse 99–100, layout shift 0 |
| Security headers | Ready | Verified on Cloudflare’s local server; re-check on the live domain after launch |
| SEO metadata and structured data | Ready | 20 indexable pages, sitemap |
| Content accuracy | Needs owner | Only confirmed facts used; French review and privacy-policy review pending |
| Merge into `main` | Needs owner approval | See `docs/deployment-and-drift.md` |
| Domain on Cloudflare, email preserved | Needs owner | `docs/domain-migration-checklist.md` |
| Lead delivery (FormSubmit activation, Bell text) | Needs owner approval | Not testable without sending a real lead |
| Real photos | Recommended before marketing push | Site works without them (Instagram panel) |
| Google Business Profile / Search Console | After launch | Checklist ready |

**Go / no-go:** Go for deployment once items 1–3 of the outstanding list are done (merge, domain, form activation). Photos, reviews and Business Profile can follow in the weeks after launch.
