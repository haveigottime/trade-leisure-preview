# Trade Leisure — current site audit (2026-06-09)

Audit of https://trade-leisure.co.uk ahead of the rebuild.

## Google presence

- **"trade leisure"** — site ranks, but drowned out by near-identical names:
  Trading Leisure Ltd (Berkshire, same trade), Leisure Travel Vans (US), Uber Leisure.
  Brand term is contested.
- **"campervans calverton" / "campervans nottingham for sale"** — absent entirely.
  Local results owned by Lowdhams, LeisureDrive, Autocraft Motor Caravans, Fuller Leisure.
- No evidence of a Google Business Profile feeding the local map pack.
  The site never mentions Calverton; only "Nottingham" once on the contact page.

## Technical weak points

| Area | Finding |
|------|---------|
| Performance | Homepage HTML alone: 4.4s. Listing page: 6.0s. |
| Stack bloat | WordPress + Elementor + WPBakery (two page builders) + Slider Revolution. 52 JS files, 38 CSS files on the homepage. |
| Title tag | "Quality Campervans And Motorhomes For Sale" — no brand, no location. |
| H1 | None on the homepage. |
| Alt text | 3 of 19 homepage images. |
| Content type | Homepage marked up as an article "written by Mickpembo, less than a minute read". |
| Structured data | One bare Organization JSON-LD (name only). No LocalBusiness/AutoDealer (address, phone, geo, hours). No Vehicle/Product/Offer schema on listings → no rich results. |
| Seller intent | No "we buy your campervan" landing content despite buying being half the business. |
| Inventory | All vehicles marked SOLD, no prices shown. |

Contact details on site: 07813 696011, Nottingham, viewings by appointment.

## Rebuild opportunities

1. **Speed** — static site, one stylesheet, near-zero JS; sub-second loads, 95+ Lighthouse.
2. **Local SEO** — titles/H1s targeting "campervans for sale Nottingham / Calverton";
   AutoDealer LocalBusiness schema with phone/geo/hours; location-rich copy.
3. **Rich results** — Vehicle + Offer JSON-LD per listing; full alt text.
4. **Seller capture** — dedicated "Sell your campervan" section targeting seller-intent searches.
5. **Trust** — 12-month Autoguard warranty, HPI check, service history surfaced prominently.
6. **Off-site (recommend to owner)** — create/claim a Google Business Profile (biggest
   single win for local queries, free), gather Google reviews, consistent NAP citations.
