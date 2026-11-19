# Plain Text Humans

**Site:** [plaintexthumans.com](https://plaintexthumans.com)  
**In praise of:** plain text — and [MarkBreak](https://markbreak.com) ([app](https://markbreak.app) · [specification](https://markbreak.com/specification.md) · [source](https://github.com/13-Books/markbreak))

We are the humans who still write in plain text — files any machine can open, any person can read, and no app can hold hostage.

> A manuscript should say what it is, and where it breaks, without asking an app to remember for it.

## Files

| Path | Contents |
|------|----------|
| `index.html` | Praise page (B&W, fluo on hover). Plain HTML/CSS/JS; no build step. |
| `shop.html` | Tote and tee shop (Stripe Payment Links). |
| `thanks.html` | Post-checkout thank-you page. |
| `assets/mark.png` | Stacked brand mark, left-aligned (Plain / Text / Humans), IBM Plex Mono. |
| `assets/fonts/IBMPlexMono-SemiBold.ttf` | Font used by `render_mark.py` (matches site header). |
| `assets/tote.png` · `assets/tee.png` | White tote / tee product shots with mark. |
| `assets/render_mark.py` | Regenerates `mark.png`. |
| `assets/composite_products.py` | Composites mark onto blank product photos. |
| `CNAME` | `plaintexthumans.com` (GitHub Pages custom domain) |
| `.github/workflows/pages.yml` | Deploys the site to GitHub Pages on push to `master` |

## Merch

| Product | Notes |
|---------|--------|
| **Tote** | Natural canvas. Stacked mark on the front. |
| **Tee** | Soft black or white cotton. The stacked mark. Optional back print: *Mark the role. Break the page.* |
| **Page Breaker tee** | Same base tee; back (or alt front) copy for the `//break` creed — *Mark the role. Break the page.* Wire as its own Stripe product when ready. |

Shop checkout uses Stripe Payment Links on `shop.html`. After payment, Confirmation page should redirect to `https://plaintexthumans.com/thanks.html`.

## Publish

1. Push this repo to GitHub and enable Pages (GitHub Actions).
2. Point `plaintexthumans.com` DNS at GitHub Pages; the `CNAME` in this repo claims the domain.
3. Push to `master` — the workflow deploys `.` as-is.

The normative MarkBreak rules live at [markbreak.com/specification.md](https://markbreak.com/specification.md).
