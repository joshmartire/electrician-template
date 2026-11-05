# Launch Checklist, Test Report & Technical Notes

Template build: November 4, 2026. Sample business "Voltline Electric Co." with placeholder contact details and **sample estimate pricing**. Not ready to index until the client items below are done and `demo_mode` is `false`.

## 1. Test report

### Passed (verified by running tests, not by reading code)

**Static QA** (`python3 _build/qa.py`, output in `_build/qa-latest.txt`): 33 passed, 0 warnings, 0 failed.
- 71 pages; 0 broken internal links or assets; 0 orphan pages.
- 69 indexable pages: unique titles and descriptions, titles ≤ 65 characters, descriptions ≤ 160, one H1 per page, no duplicate IDs, every form field labelled, every image has alt text.
- Canonical and `og:url` match the file path on every page. `sitemap.xml` is valid with 69 URLs, matching the indexable inventory. `robots.txt` points to it.
- JSON-LD parses everywhere: Electrician ×1, WebSite ×1, Service ×56, BreadcrumbList ×69, ItemList ×1, ContactPage ×1, WebApplication ×1.
- All 14 service pages have 500–600 words of main content. The 42 city pages have 342–414 words each; the highest overlap between any two is 41%.
- Contrast ≥ 4.5:1 on all key colour pairs. No template tokens or placeholder text. No "best / #1 / guarantee / years of experience / star rating" claims. No licence number shown until the client supplies one. Legal links in every footer. Demo banner on every page.
- Opening animation on exactly the 69 indexable pages, never the 404 or thank-you page. The estimate page carries the config's jobs; the home picker submits to it. The house scene has all six wired circuits with their rooms.

**Browser QA** (`python3 _build/qa_browser.py --axe axe.min.js`, headless Chromium at 1440×900 and 390×844, output in `_build/qa-browser-latest.txt`): 25 passed, 0 failed.
- **House scene:** pinned, starts dark, circuits trace and rooms light up in turn, everything is on at the end with the final message and the estimate card. With reduced motion, the hero isn't pinned and the house is shown fully powered.
- Opening animation plays when landing on a service page, flips 12 breakers, clears itself and doesn't replay on the next page. Skipped for a `#hash` and reduced motion; a click skips it.
- **Instant estimate:** all 6 jobs match prices recalculated from `site.config.json`, at defaults and with every option changed; option notes show; the hero picker opens the right job; the lead form opens with the job, options and estimate filled in; empty submit is blocked; the live price bar shows on phones.
- Contact form blocks empty submissions and flags invalid email. Mobile menu and call bar work.
- No horizontal scrolling at 390 px on 12 key pages. No JavaScript errors.
- axe-core (WCAG 2.1 A/AA): 0 violations on home, estimate, a service page, contact and a city hub.

### Not tested yet (needs the deployed site or client accounts)
- Form delivery: needs the client's email in `form_endpoint` and FormSubmit activation.
- Live domain, HTTPS, PageSpeed Insights / Core Web Vitals in the field, Rich Results Test, real iOS Safari and Android devices, Search Console.

### Requires client input
| Item | Where |
|---|---|
| Business name, legal name, phone, email, domain, hours | `site.config.json` |
| **ESA licence number** | `licence_number` |
| Public address or service-area business | `address` |
| **Real prices for each estimate job** (base prices, per-foot, per-light, options, extras, minimum job) and whether the permit is included | `estimator` |
| Jobs they actually do (emergency calls, commercial, three-phase, standby generators) | `services`, `emergency` |
| Form recipient + FormSubmit activation | `form_endpoint` |
| Google Business Profile and social URLs | `site.config.json` |
| Confirm hero badges and working standards are true (permit every job, written quotes, emergency calls answered) | `_build/pages.py` (`tags`, `features`, `statement_points`) |
| Real About story, master electrician, insurance and WSIB, warranties | `pages.py` → `about` |
| Real job photos | `photos` in config |
| **Check the house scene on a real iPhone and Android phone** | home page |
| Legal review of Privacy, Terms, Cookie drafts | `pages.py` |

## 2. Manual launch tasks
1. Fill in config, set real estimate pricing, set `"demo_mode": false`, run `build.py`, `qa.py`, `qa_browser.py`. All must pass.
2. **Hosting (Cloudflare Pages, like the other demos):** connect the repo, no build command, output `/`. Add the custom domain in Pages. `_headers` noindexes only `*.pages.dev`.
3. Submit a test quote and a test estimate, confirm the FormSubmit activation email, and submit again.
4. Search Console: verify the domain and submit `https://CLIENTDOMAIN/sitemap.xml`.
5. Rich Results Test and PageSpeed Insights (mobile) on home, a service page and the estimate page.
6. Make sure the Google Business Profile name, phone and service areas match the site.
7. If analytics, ad pixels, chat, financing or booking widgets are added: update the Privacy and Cookie policies and add consent blocking where required.

## 3. Instant estimate: how prices are calculated
For the chosen job: `base + choice adds + check adds + (range and count work) × choice multipliers`, where range work is `per_unit × (value − free_units)` and count work is `per_unit × count`. Shown as ± `range_pct`, rounded to `round_to`, never below `minimum_job`. Jobs and extras tied to a service disappear with it.

## 4. Permits and local facts (Ontario)
Copy states that electrical work for pay in Ontario must be done by an ESA Licensed Electrical Contractor who files the permit (notification) with the Electrical Safety Authority, which inspects and issues a Certificate of Acceptance; that generators need an interlock or transfer switch; and that EV energy management systems can avoid some panel upgrades. City pages name ENWIN Utilities for Windsor, the 2016/2017 flooding, Windsor's older neighbourhoods, LaSalle's newer subdivisions and Tecumseh's 1960s–70s housing and Oldcastle industrial area. The utility for LaSalle and Tecumseh is deliberately not named. **Re-check before launch**, and rewrite for any other province or state (`content_cities.py`, `content_services.py`, `pages.py`, `inspection_*` in config).

## 5. SEO and technical summary
- `lang="en-CA"`, unique title and description, canonical, Open Graph and Twitter card on every page; favicon set and 1200×630 share image generated in the brand colours.
- Schema: one `Electrician` business (`/#business`) on home; `Service` on service and city pages; `BreadcrumbList` matching visible breadcrumbs; `WebSite`, `ItemList`, `ContactPage`, `WebApplication` (estimate). No reviews, ratings, prices or FAQ markup.
- Internal linking: mega menu and footer link every service; each service links its 3 city pages and related services; city pages cross-link and link the hub; the estimate is linked from the nav, footer, hero, asides and CTAs.
- Performance: no images or video (every drawing is inline SVG), self-hosted fonts, one ~78 KB stylesheet, 14 KB of site JS, plus 9 KB for the house scene on the home page and 9 KB on the estimate page.
- Privacy: no cookies, no analytics, no third-party requests; one sessionStorage flag for the intro.

## 6. URL structure and redirects
Directory-style URLs with trailing slashes; legal pages use `.html`. If a page is renamed after launch, add a Cloudflare redirect rule.

## 7. Page inventory
Full list with canonical URLs: `_build/page-inventory.json`. Home 1, estimate 1, services hub 1, services 14, service × city 42, areas hub 1, city hubs 3, about/FAQ/contact 3, legal 3, thank-you 1 (noindex), 404 1.
