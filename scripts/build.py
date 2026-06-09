#!/usr/bin/env python3
"""Generate site/index.html from data/vans.json."""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VANS = json.load(open(os.path.join(ROOT, "data", "vans.json")))
PHONE = "07813 696011"
PHONE_INTL = "+447813696011"

e = html.escape


def miles(raw):
    digits = re.sub(r"\D", "", raw or "")
    return f"{int(digits):,} mi" if digits else raw


def card(van):
    s = van["specs"]
    payload = e(json.dumps({
        "title": van["title"],
        "summary": van["summary"],
        "photos": van["photos"],
        "specs": s,
    }), quote=True)
    cover = van["photos"][0] if van["photos"] else ""
    specs_bits = "".join(
        f"<span><b>{e(label)}</b>{e(val)}</span>"
        for label, val in [
            ("YR", s.get("Year", "—")),
            ("MI", miles(s.get("Mileage", ""))),
            ("BERTH", s.get("Berth", "—").replace(" Berth", "")),
            ("BOX", s.get("Transmission", "—")),
        ]
    )
    return f"""
      <button class="van-card reveal" data-van="{payload}" aria-haspopup="dialog">
        <div class="photo">
          <img src="{e(cover)}" alt="{e(van['title'])}" loading="lazy" width="798" height="466">
          <span class="stamp">Sold</span>
        </div>
        <div class="body">
          <h3>{e(van['title'])}</h3>
          <div class="spec-row">{specs_bits}</div>
        </div>
      </button>"""


def vehicle_ld(van):
    s = van["specs"]
    digits = re.sub(r"\D", "", s.get("Mileage", ""))
    item = {
        "@type": "Vehicle",
        "name": van["title"],
        "description": van["summary"],
        "vehicleTransmission": s.get("Transmission"),
        "fuelType": s.get("Fuel type"),
        "modelDate": s.get("Year"),
        "manufacturer": s.get("Make"),
        "model": s.get("Model"),
        "color": s.get("Exterior Color"),
    }
    if digits:
        item["mileageFromOdometer"] = {"@type": "QuantitativeValue", "value": int(digits), "unitCode": "SMI"}
    return {k: v for k, v in item.items() if v}


def hero_fig(slug, cls):
    van = next(v for v in VANS if v["slug"] == slug)
    s = van["specs"]
    cap = f"{s.get('Make', '')} {s.get('Model', '')} · {s.get('Year', '')}".strip(" ·")
    return f"""
        <figure class="{cls}">
          <img src="{e(van['photos'][0])}" alt="{e(van['title'])}" width="798" height="466">
          <figcaption>{e(cap)}</figcaption>
        </figure>"""


ld = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "AutoDealer",
            "@id": "https://trade-leisure.co.uk/#dealer",
            "name": "Trade Leisure",
            "description": "Quality pre-owned, professionally converted campervans for sale in Nottinghamshire. Every van HPI checked, serviced and sold with a 12-month Autoguard warranty.",
            "telephone": PHONE_INTL,
            "url": "https://trade-leisure.co.uk",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Calverton",
                "addressRegion": "Nottinghamshire",
                "addressCountry": "GB",
            },
            "areaServed": ["Nottingham", "Nottinghamshire", "East Midlands", "United Kingdom"],
            "priceRange": "££",
        },
        {
            "@type": "ItemList",
            "name": "Recently sold campervans",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "item": vehicle_ld(v)}
                for i, v in enumerate(VANS)
            ],
        },
    ],
}

ICON_VAN = """<svg viewBox="0 0 64 40" fill="none" aria-hidden="true"><path d="M4 28V16c0-2 1-4 3-5l9-5c1.2-.7 2.6-1 4-1h36a4 4 0 0 1 4 4v19" stroke="#1f3b2c" stroke-width="3" stroke-linejoin="round"/><path d="M4 28h56" stroke="#1f3b2c" stroke-width="3"/><circle cx="17" cy="31" r="6" fill="#f5efe2" stroke="#1f3b2c" stroke-width="3"/><circle cx="47" cy="31" r="6" fill="#f5efe2" stroke="#1f3b2c" stroke-width="3"/><path d="M10 14l8-4.4c.9-.5 1.9-.7 2.9-.7H27v9H8.5" fill="#d8772f" opacity=".85"/><rect x="31" y="9" width="10" height="9" rx="1" fill="#d8772f" opacity=".85"/><rect x="45" y="9" width="10" height="9" rx="1" fill="#d8772f" opacity=".85"/></svg>"""

ROUNDEL = """<svg class="roundel" viewBox="0 0 132 132" aria-hidden="true">
  <circle cx="66" cy="66" r="64" fill="#1f3b2c"/>
  <circle cx="66" cy="66" r="63" fill="none" stroke="#e9a23b" stroke-width="2"/>
  <circle cx="66" cy="66" r="40" fill="none" stroke="#e9a23b" stroke-width="1.5" stroke-dasharray="4 5"/>
  <defs><path id="rim" d="M66 18a48 48 0 1 1 0 96 48 48 0 1 1 0-96"/></defs>
  <text font-family="Karla, sans-serif" font-size="11.5" font-weight="800" letter-spacing="2.6" fill="#f5efe2">
    <textPath href="#rim">HPI CHECKED · 12-MONTH WARRANTY · SERVICED ·</textPath>
  </text>
  <text x="66" y="74" text-anchor="middle" font-family="Fraunces, serif" font-style="italic" font-size="22" fill="#e9a23b">TL</text>
</svg>"""

CHECK = """<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="10.5" stroke="currentColor" stroke-width="2" stroke-dasharray="3.5 3"/><path d="M7.5 12.5l3 3 6-7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

TRUST_ICONS = {
    "shield": """<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 2.5l8 3v6c0 5-3.4 8.6-8 10-4.6-1.4-8-5-8-10v-6l8-3z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8.5 12l2.5 2.5 4.5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "search": """<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" stroke-width="2"/><path d="M15.5 15.5L21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>""",
    "doc": """<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 2.5h8l4 4V21a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 12h6M9 16h6M9 8h2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>""",
    "key": """<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="8" cy="15" r="5" stroke="currentColor" stroke-width="2"/><path d="M11.5 11.5L20 3M16 7l3 3M13 10l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>""",
    "phone": """<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a12 12 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>""",
    "pin": """<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21.5s7-6.2 7-11.5a7 7 0 1 0-14 0c0 5.3 7 11.5 7 11.5z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.5" stroke="currentColor" stroke-width="2"/></svg>""",
    "clock": """<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="9.5" stroke="currentColor" stroke-width="2"/><path d="M12 6.5V12l3.5 2.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>""",
}

cards = "\n".join(card(v) for v in VANS)

page = f"""<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Trade Leisure — Quality Used Campervans for Sale in Nottingham &amp; Calverton</title>
  <meta name="description" content="Hand-picked, professionally converted campervans for sale in Calverton, Nottinghamshire. Every van HPI checked, serviced and sold with a 12-month Autoguard warranty. We buy quality campervans too — call {PHONE}.">
  <!-- PREVIEW BUILD: remove the noindex line before going live -->
  <meta name="robots" content="noindex, nofollow">
  <meta property="og:title" content="Trade Leisure — Quality Used Campervans, Nottinghamshire">
  <meta property="og:description" content="Hand-picked, professionally converted campervans. HPI checked, serviced, 12-month warranty.">
  <meta property="og:locale" content="en_GB">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=Karla:ital,wght@0,400..800;1,400..800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>

<header>
  <div class="nav">
    <a class="wordmark" href="#top">
      {ICON_VAN}
      <span2><b>Trade Leisure</b><span>Quality pre-owned campervans</span></span2>
    </a>
    <nav aria-label="Main">
      <a href="#vans">Recent vans</a>
      <a href="#sell">Sell your van</a>
      <a href="#about">About</a>
      <a href="#contact">Contact</a>
    </nav>
    <a class="btn btn-solid" href="tel:{PHONE_INTL}">{TRUST_ICONS['phone']}&nbsp;{PHONE}</a>
  </div>
</header>

<main id="top">

  <div class="hero">
    <div class="wrap">
      <div class="reveal in">
        <p class="kicker">Calverton · Nottinghamshire</p>
        <h1><em>Hand-picked</em> campervans for sale in Nottinghamshire</h1>
        <p class="lede">Trade Leisure buys and sells well-cared-for, professionally converted campervans. Every van is HPI checked, freshly serviced and backed by a 12-month Autoguard parts &amp; labour warranty — viewed one-to-one, no forecourt patter.</p>
        <div class="cta-row">
          <a class="btn btn-solid" href="tel:{PHONE_INTL}">Call Mick — {PHONE}</a>
          <a class="btn btn-ghost" href="#vans">See recent vans</a>
        </div>
      </div>
      <div class="stack reveal in">
{hero_fig("volkswagen-california-se-ocean-campervan", "ph-a")}
{hero_fig("volkswagen-camper-king-monte-carlo-campervan-2-0l-diesel-highline-euro-6", "ph-b")}
        <span class="badge-roundel">{ROUNDEL}</span>
      </div>
    </div>
  </div>

  <div class="trust">
    <div class="wrap">
      <div class="reveal">{TRUST_ICONS['shield']}<span><b>12-month warranty</b><small>Autoguard parts &amp; labour on every van</small></span></div>
      <div class="reveal">{TRUST_ICONS['search']}<span><b>HPI checked</b><small>History verified before it's offered</small></span></div>
      <div class="reveal">{TRUST_ICONS['doc']}<span><b>Serviced &amp; MOT'd</b><small>Service history with every sale</small></span></div>
      <div class="reveal">{TRUST_ICONS['key']}<span><b>By appointment</b><small>Unhurried one-to-one viewings</small></span></div>
    </div>
  </div>

  <section class="inventory on-green" id="vans">
    <div class="wrap">
      <div class="sec-head reveal">
        <p class="kicker">01 — Recent vans</p>
        <h2>Gone to <em>good homes</em></h2>
        <p>Every van below sold recently — good stock doesn't hang about. Tell us what you're after and you'll be first to hear when the right one lands. Tap a van to see its photos and full spec.</p>
      </div>
      <div class="van-grid">
{cards}
      </div>
      <div class="inv-foot reveal">
        <p><b>After something specific?</b> A T6.1 Highline, an auto, a 5-seater for the school run — say the word and we'll keep an eye out on our trade sources.</p>
        <a class="btn btn-ghost" href="tel:{PHONE_INTL}">Register your interest</a>
      </div>
    </div>
  </section>

  <section class="sell" id="sell">
    <div class="wrap">
      <div class="reveal">
        <p class="kicker">02 — Selling?</p>
        <h2>Got a campervan to <em>sell</em>?</h2>
        <p>We buy well-cared-for, professionally converted campervans and motorhomes — it's half of what we do.</p>
        <ul class="checks">
          <li>{CHECK}<span><b>A fair, honest valuation</b> — based on what vans like yours actually sell for.</span></li>
          <li>{CHECK}<span><b>No listing fees, no timewasters</b> — and no strangers turning up at your door.</span></li>
          <li>{CHECK}<span><b>Paperwork handled</b> — straightforward from first call to collection.</span></li>
        </ul>
      </div>
      <aside class="sell-card reveal">
        <h3>Start with a phone call</h3>
        <p>Tell us the year, conversion, mileage and condition — photos help too.</p>
        <a class="phone-big" href="tel:{PHONE_INTL}">{PHONE}</a>
        <p>Prefer to message first? Send photos on WhatsApp and we'll come back to you.</p>
        <a class="btn btn-solid" href="https://wa.me/447813696011">WhatsApp the van details</a>
      </aside>
    </div>
  </section>

  <section class="about" id="about">
    <div class="wrap">
      <blockquote class="reveal">Not a forecourt — a small dealership that only takes on vans worth putting a name to.</blockquote>
      <div class="col reveal">
        <p class="kicker" style="margin-bottom:18px">03 — About Trade Leisure</p>
        <p><b>Trade Leisure is a small, independent campervan dealer based in Calverton, Nottinghamshire.</b> We carefully source quality professional conversions — VW Transporters mostly, with the odd Ford Custom or California — and only those that have been genuinely well maintained and cared for.</p>
        <p>Every van is HPI checked, serviced and MOT'd where due, gas-safety certificated, and sold with a 12-month Autoguard parts &amp; labour warranty. Viewings are one-to-one and by appointment, so you can take your time, lift the cushions, and ask awkward questions.</p>
        <p>Buying or selling, you deal with the same person from first call to handover.</p>
      </div>
    </div>
  </section>

  <section class="contact on-green" id="contact">
    <div class="wrap">
      <div class="reveal">
        <p class="kicker">04 — Contact</p>
        <h2>Come and see the <em>vans</em></h2>
        <p class="lede">Viewings are by appointment — call or message and we'll sort a time that suits. Honest answers, no pressure, kettle's on.</p>
        <a class="btn btn-solid" href="tel:{PHONE_INTL}">Call {PHONE}</a>
      </div>
      <ul class="contact-list reveal">
        <li>{TRUST_ICONS['phone']}<span><b>Phone / WhatsApp</b><a href="tel:{PHONE_INTL}">{PHONE}</a></span></li>
        <li>{TRUST_ICONS['pin']}<span><b>Location</b><a href="https://maps.google.com/?q=Calverton,+Nottinghamshire">Calverton, Nottinghamshire</a></span></li>
        <li>{TRUST_ICONS['clock']}<span><b>Viewings</b>By appointment, seven days</span></li>
      </ul>
    </div>
  </section>

</main>

<footer>
  <div class="wrap">
    <span>© 2026 Trade Leisure · Quality pre-owned campervans · Calverton, Nottinghamshire</span>
    <span>Preview build — not yet live</span>
  </div>
</footer>

<dialog class="van-modal" id="van-modal">
  <button class="modal-close" aria-label="Close">✕</button>
  <div class="modal-gallery" tabindex="0"></div>
  <div class="modal-body">
    <h3></h3>
    <p class="gallery-hint">← Swipe / scroll the photos</p>
    <p class="summary"></p>
    <div class="modal-specs"></div>
  </div>
</dialog>

<script src="app.js"></script>
</body>
</html>
"""

# fix invalid span2 helper tag
page = page.replace("<span2>", "<span style=\"display:block\">").replace("</span2>", "</span>")

out = os.path.join(ROOT, "site", "index.html")
open(out, "w").write(page)
print(f"wrote {out} ({len(page):,} bytes, {len(VANS)} vans)")
