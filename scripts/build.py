#!/usr/bin/env python3
"""Generate site/index.html from data/vans.json — overland field-guide design."""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VANS = json.load(open(os.path.join(ROOT, "data", "vans.json")))
PHONE = "07813 696011"
PHONE_INTL = "+447813696011"
COORD = "53.03°N 1.08°W"  # Calverton, Nottinghamshire

e = html.escape


def miles(raw):
    digits = re.sub(r"\D", "", raw or "")
    return f"{int(digits):,}" if digits else (raw or "—")


def stock_code(i):
    return f"TL·{i + 1:02d}"


def card(van, i):
    s = van["specs"]
    payload = e(json.dumps({
        "code": stock_code(i),
        "title": van["title"],
        "bullets": van.get("bullets", []),
        "notes": van.get("notes", ""),
        "photos": van["photos"],
        "specs": s,
    }), quote=True)
    cover = van["photos"][0] if van["photos"] else ""
    cells = "".join(
        f'<div class="cell"><b>{e(b)}</b><span>{e(v)}</span></div>'
        for b, v in [
            ("YEAR", s.get("Year", "—")),
            ("MILES", miles(s.get("Mileage", ""))),
            ("BERTH", s.get("Berth", "—").replace(" Berth", "")),
            ("GEARBOX", s.get("Transmission", "—")),
        ]
    )
    return f"""
      <button class="van-card reveal" data-van="{payload}" aria-haspopup="dialog">
        <div class="photo">
          <img src="{e(cover)}" alt="{e(van['title'])}" loading="lazy" width="798" height="466">
          <span class="gridref">{e(stock_code(i))}</span>
          <span class="status-tag status-sold">Sold</span>
        </div>
        <div class="body">
          <h3>{e(van['title'])}</h3>
          <div class="data-strip">{cells}</div>
          <span class="view-link">{ICON_ARROW}&nbsp;View log &amp; photos</span>
        </div>
      </button>"""


def vehicle_ld(van):
    s = van["specs"]
    digits = re.sub(r"\D", "", s.get("Mileage", ""))
    item = {
        "@type": "Vehicle",
        "name": van["title"],
        "description": " ".join(van.get("bullets", [])) or van.get("summary", ""),
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


ICON_ARROW = '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

WORDMARK = """<svg viewBox="0 0 48 48" fill="none" aria-hidden="true"><circle cx="24" cy="24" r="22" fill="#1c3a30"/><circle cx="24" cy="24" r="22" stroke="#df5c28" stroke-width="1.5"/><path d="M24 7l4.2 14.8L43 24l-14.8 2.2L24 41l-4.2-14.8L5 24l14.8-2.2z" fill="#e1e6da"/><circle cx="24" cy="24" r="3" fill="#df5c28"/></svg>"""

COMPASS = """<svg class="compass spin" viewBox="0 0 96 96" fill="none" aria-hidden="true">
  <circle cx="48" cy="48" r="46" fill="#122a22"/>
  <circle cx="48" cy="48" r="45" stroke="#df5c28" stroke-width="1.5"/>
  <circle cx="48" cy="48" r="34" stroke="#79a7c2" stroke-width="1" stroke-dasharray="3 4"/>
  <path d="M48 12l7 31-7 8-7-8z" fill="#df5c28"/>
  <path d="M48 84l-7-31 7-8 7 8z" fill="#e1e6da"/>
  <text x="48" y="11" text-anchor="middle" font-family="'Spline Sans Mono',monospace" font-size="9" fill="#e1e6da">N</text>
  <circle cx="48" cy="48" r="2.6" fill="#e1e6da"/>
</svg>"""

ICONS = {
    "shield": '<svg viewBox="0 0 24 24" fill="none"><path d="M12 2.5l8 3v6c0 5-3.4 8.6-8 10-4.6-1.4-8-5-8-10v-6l8-3z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8.5 12l2.5 2.5 4.5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none"><circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" stroke-width="2"/><path d="M15.5 15.5L21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none"><path d="M6 2.5h8l4 4V21a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 12h6M9 16h6M9 8h2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "key": '<svg viewBox="0 0 24 24" fill="none"><circle cx="8" cy="15" r="5" stroke="currentColor" stroke-width="2"/><path d="M11.5 11.5L20 3M16 7l3 3M13 10l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none"><path d="M5 3h4l2 5-2.5 1.5a12 12 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none"><path d="M12 21.5s7-6.2 7-11.5a7 7 0 1 0-14 0c0 5.3 7 11.5 7 11.5z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.5" stroke="currentColor" stroke-width="2"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9.5" stroke="currentColor" stroke-width="2"/><path d="M12 6.5V12l3.5 2.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10.5" stroke="currentColor" stroke-width="2" stroke-dasharray="3.5 3"/><path d="M7.5 12.5l3 3 6-7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}

ld = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "AutoDealer",
            "@id": "https://trade-leisure.co.uk/#dealer",
            "name": "Trade Leisure",
            "description": "Quality pre-owned, professionally converted campervans for sale in Calverton, Nottinghamshire. Every van HPI checked, serviced and sold with a 12-month Autoguard warranty.",
            "telephone": PHONE_INTL,
            "url": "https://trade-leisure.co.uk",
            "address": {"@type": "PostalAddress", "addressLocality": "Calverton", "addressRegion": "Nottinghamshire", "addressCountry": "GB"},
            "geo": {"@type": "GeoCoordinates", "latitude": 53.03, "longitude": -1.08},
            "areaServed": ["Nottingham", "Nottinghamshire", "East Midlands", "United Kingdom"],
            "priceRange": "££",
        },
        {
            "@type": "ItemList",
            "name": "Recently sold campervans",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": vehicle_ld(v)} for i, v in enumerate(VANS)],
        },
    ],
}


def hero_view():
    van = next((v for v in VANS if v["slug"] == "volkswagen-california-se-ocean-campervan"), VANS[0])
    s = van["specs"]
    return f"""
      <div class="viewfinder reveal in">
        <div class="frame">
          <img src="{e(van['photos'][0])}" alt="{e(van['title'])}">
          <span class="corner c-tl"></span><span class="corner c-tr"></span>
          <span class="corner c-bl"></span><span class="corner c-br"></span>
          <span class="tag"><b>▸</b> {e(s.get('Make',''))} {e(s.get('Model',''))} · {e(s.get('Year',''))}</span>
        </div>
        {COMPASS}
      </div>"""


cards = "\n".join(card(v, i) for i, v in enumerate(VANS))

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
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Hanken+Grotesk:wght@400;500;600;700&family=Spline+Sans+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>

<header>
  <div class="nav">
    <a class="wordmark" href="#top">
      {WORDMARK}
      <span><b>Trade Leisure</b><span class="coord mono">CALVERTON · {COORD}</span></span>
    </a>
    <nav aria-label="Main">
      <a href="#vans">Recent vans</a>
      <a href="#sell">Sell your van</a>
      <a href="#about">About</a>
      <a href="#contact">Contact</a>
    </nav>
    <a class="btn btn-solid" href="tel:{PHONE_INTL}">{ICONS['phone']}&nbsp;{PHONE}</a>
  </div>
</header>

<main id="top">

  <div class="hero topo">
    <div class="wrap">
      <div class="hero-copy reveal in">
        <p class="marker">Calverton · Nottinghamshire</p>
        <h1><span class="line1">Campervans</span><br><span class="line2">for the</span><br><span class="line3">long way round</span></h1>
        <p class="lede">Trade Leisure buys and sells well-cared-for, professionally converted campervans. Every one is HPI checked, freshly serviced and backed by a 12-month Autoguard parts &amp; labour warranty — viewed one-to-one, no forecourt patter.</p>
        <div class="cta-row">
          <a class="btn btn-solid" href="tel:{PHONE_INTL}">Call Mick — {PHONE}</a>
          <a class="btn btn-ghost" href="#vans">See recent vans</a>
        </div>
        <div class="route"><span></span></div>
      </div>
      {hero_view()}
    </div>
  </div>

  <div class="fieldnotes">
    <div class="wrap">
      <div class="note reveal"><span class="num mono">01</span><div class="ico">{ICONS['shield']}<b>12-month warranty</b></div><small>Autoguard parts &amp; labour on every van</small></div>
      <div class="note reveal"><span class="num mono">02</span><div class="ico">{ICONS['search']}<b>HPI checked</b></div><small>History verified before it's offered</small></div>
      <div class="note reveal"><span class="num mono">03</span><div class="ico">{ICONS['doc']}<b>Serviced &amp; MOT'd</b></div><small>Service history with every sale</small></div>
      <div class="note reveal"><span class="num mono">04</span><div class="ico">{ICONS['key']}<b>By appointment</b></div><small>Unhurried one-to-one viewings</small></div>
    </div>
  </div>

  <section class="inventory on-pine topo" id="vans">
    <div class="wrap">
      <div class="sec-head reveal">
        <p class="marker">01 / Recent vans</p>
        <h2>Gone to <span class="hl">good homes</span></h2>
        <p>Every van below sold recently — good stock doesn't hang about. Tell us what you're after and you'll be first to hear when the right one lands. Tap a van for its full log and photos.</p>
      </div>
      <div class="van-grid">
{cards}
      </div>
      <div class="inv-foot reveal">
        <p><b>After something specific?</b> A T6.1 Highline, an auto box, a 5-seater for the school run — say the word and we'll keep watch on our trade sources.</p>
        <a class="btn btn-ghost" href="tel:{PHONE_INTL}">Register your interest</a>
      </div>
    </div>
  </section>

  <section class="sell topo" id="sell">
    <div class="wrap">
      <div class="reveal">
        <p class="marker">02 / Selling</p>
        <h2>Got a campervan <span class="hl">to sell?</span></h2>
        <p>We buy well-cared-for, professionally converted campervans and motorhomes — it's half of what we do.</p>
        <ul class="checks">
          <li>{ICONS['check']}<span><b>A fair, honest valuation</b> — based on what vans like yours actually sell for.</span></li>
          <li>{ICONS['check']}<span><b>No listing fees, no timewasters</b> — and no strangers turning up at your door.</span></li>
          <li>{ICONS['check']}<span><b>Paperwork handled</b> — straightforward from first call to collection.</span></li>
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
        <p class="marker" style="margin-bottom:18px">03 / About Trade Leisure</p>
        <p><b>Trade Leisure is a small, independent campervan dealer based in Calverton, Nottinghamshire.</b> We carefully source quality professional conversions — VW Transporters mostly, with the odd Ford Custom or California — and only those that have been genuinely well maintained and cared for.</p>
        <p>Every van is HPI checked, serviced and MOT'd where due, gas-safety certificated, and sold with a 12-month Autoguard parts &amp; labour warranty. Viewings are one-to-one and by appointment, so you can take your time, lift the cushions, and ask the awkward questions.</p>
        <p>Buying or selling, you deal with the same person from first call to handover.</p>
      </div>
    </div>
  </section>

  <section class="contact on-pine topo" id="contact">
    <div class="wrap">
      <div class="reveal">
        <p class="marker">04 / Contact</p>
        <h2>Come and see <span class="hl">the vans</span></h2>
        <p class="lede">Viewings are by appointment — call or message and we'll sort a time that suits. Honest answers, no pressure, kettle's on.</p>
        <a class="btn btn-solid" href="tel:{PHONE_INTL}">Call {PHONE}</a>
      </div>
      <ul class="contact-list reveal">
        <li>{ICONS['phone']}<span><b>Phone / WhatsApp</b><a href="tel:{PHONE_INTL}">{PHONE}</a></span></li>
        <li>{ICONS['pin']}<span><b>Location · {COORD}</b><a href="https://maps.google.com/?q=Calverton,+Nottinghamshire">Calverton, Nottinghamshire</a></span></li>
        <li>{ICONS['clock']}<span><b>Viewings</b>By appointment, seven days</span></li>
      </ul>
    </div>
  </section>

</main>

<footer>
  <div class="wrap">
    <span>© 2026 Trade Leisure · Quality pre-owned campervans · Calverton, Nottinghamshire</span>
    <span class="mono">PREVIEW BUILD · {COORD}</span>
  </div>
</footer>

<dialog class="van-modal" id="van-modal">
  <button class="modal-close" aria-label="Close">✕</button>
  <div class="modal-gallery" tabindex="0"></div>
  <div class="modal-body">
    <div class="modal-head"><h3></h3><span class="modal-ref mono"></span></div>
    <p class="gallery-hint">← Swipe / scroll the photos</p>
    <ul class="modal-bullets"></ul>
    <p class="modal-notes"></p>
    <div class="modal-specs"></div>
  </div>
</dialog>

<script src="app.js"></script>
</body>
</html>
"""

out = os.path.join(ROOT, "site", "index.html")
open(out, "w").write(page)
print(f"wrote {out} ({len(page):,} bytes, {len(VANS)} vans)")
