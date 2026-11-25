# Deployment state and drift (checked 2026-11-25)

| Where | Version | Notes |
| --- | --- | --- |
| allthingsprinted.ca | Shopify “Store unavailable” (HTTP 402) | Not connected to this repository. `www` redirects to it. |
| allthingsprinted.salvatore-desantisg.workers.dev | Commit `575cd00` (branch `claude/focused-meitner-3484fr`) | Byte-for-byte identical to that branch (home pages, CSS, JS, sitemap compared). |
| Pull request #4 (`claude/focused-meitner-3484fr` → `main`) | `575cd00` | Open, not merged. |
| `main` | `2277329` | **15 commits behind** the live site; still the older single-page design. |
| `claude/elevation-sprint` (this sprint) | branched from `575cd00` | Not deployed. Private preview only. |

## The drift risk

The live Worker was deployed from the pull-request branch, not from `main`. If Cloudflare Builds is (or later gets) connected to `main`, the next build would publish the **older** design and undo the live site.

## Safe order to go live (each step needs your approval)

1. Review the sprint in the private preview.
2. Approve a pull request from `claude/elevation-sprint` into `main` (it contains everything in PR #4 plus the sprint; PR #4 can then be closed).
3. Connect Cloudflare Builds to `main` (or run `npx wrangler deploy` from `main`).
4. Follow `docs/domain-migration-checklist.md`.

Nothing in this sprint was merged, deployed, or changed in DNS, Shopify or email.
