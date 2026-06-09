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
AUTOTRADER = "https://www.autotrader.co.uk/dealers/nottinghamshire/nottingham/trade-leisure-10043108"
INSTAGRAM = "https://www.instagram.com/trade_leisure_campers/"
YOUTUBE = "https://www.youtube.com/channel/UCn_UhCRsrEzHKDpKOy0UkbA"
FACEBOOK = "https://www.facebook.com/profile.php?id=61580647537263"
ADDRESS_STREET = "129 Flatts Lane"
ADDRESS_POSTCODE = "NG14 6LA"

# Verbatim 5-star reviews from the AutoTrader dealer page (5.0 average across 15 reviews).
RATING_AVG = "5.0"
RATING_COUNT = 15
REVIEWS = [
    {"name": "James", "date": "2026-03-10", "when": "March 2026",
     "text": "Mike was honest, professional, friendly and knowledgeable on all aspects of the vehicle."},
    {"name": "Sarah Offord", "date": "2024-11-16", "when": "November 2024",
     "text": "Great campervan. Very professional, friendly and knowledgeable service. Fast and easy purchase. Highly recommend."},
    {"name": "Adrian Faulkner", "date": "2025-02-02", "when": "February 2025",
     "text": "Mike is a joy to deal with — nothing is too much trouble and everything he says he will do happens."},
    {"name": "Gail Adair", "date": "2024-07-10", "when": "July 2024",
     "text": "The van was exactly as described and I would not hesitate to recommend Mike as a very trustworthy dealer."},
    {"name": "Rob", "date": "2025-06-28", "when": "June 2025",
     "text": "Mike was excellent to deal with. Very straightforward, all questions answered, smooth process. Very trustworthy."},
    {"name": "Paul Horn", "date": "2025-10-15", "when": "October 2025",
     "text": "Excellent communication, vehicle exactly as described — my buying experience was made very easy."},
]

FAQ = [
    ("What campervans does Trade Leisure buy?",
     "We buy well-cared-for, professionally converted VW and Ford campervans up to 10 years old. We don't buy DIY conversions."),
    ("How does selling to you work?",
     "Fill in the 'sell your campervan' form with a few photos and you'll get a no-obligation offer, usually within 24 hours. If you're happy, we'll arrange to view the van, then pay by instant bank transfer and collect it — free of charge."),
    ("Why should I sell to Trade Leisure?",
     "We're a registered company with excellent feedback. You get a competitive offer, instant payment and free collection, any outstanding finance settled on the day, and none of the hassle or time-wasters that come with selling privately."),
    ("How will I get paid?",
     "By instant bank transfer, straight into your account, on the day we collect the van."),
    ("Are there any hidden costs?",
     "None. You're under no obligation to accept our offer, and we never charge anything to value your campervan."),
    ("Do your vans come with a warranty?",
     "Yes — every van we sell is HPI checked, serviced where due and comes with a 12-month Autoguard parts & labour warranty, plus a gas safety certificate on conversions."),
]

e = html.escape


def miles(raw):
    digits = re.sub(r"\D", "", raw or "")
    return f"{int(digits):,}" if digits else (raw or "—")


def card(van, code):
    s = van["specs"]
    available = van.get("available", False)
    price = van.get("price", "")
    payload = e(json.dumps({
        "code": code,
        "title": van["title"],
        "bullets": van.get("bullets", []),
        "notes": van.get("notes", ""),
        "photos": van["photos"],
        "specs": s,
        "available": available,
        "price": price,
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
    if available:
        status = '<span class="status-tag status-available">For sale</span>'
        foot = f'<div class="card-foot"><span class="price">{e(price)}</span><span class="view-link">{ICON_ARROW}&nbsp;Details &amp; viewing</span></div>'
    else:
        status = '<span class="status-tag status-sold">Sold</span>'
        foot = f'<span class="view-link">{ICON_ARROW}&nbsp;View log &amp; photos</span>'
    return f"""
      <button class="van-card{' is-available' if available else ''} reveal" data-van="{payload}" aria-haspopup="dialog">
        <div class="photo">
          <img src="{e(cover)}" alt="{e(van['title'])}" loading="lazy" width="798" height="466">
          <span class="gridref">{e(code)}</span>
          {status}
        </div>
        <div class="body">
          <h3>{e(van['title'])}</h3>
          <div class="data-strip">{cells}</div>
          {foot}
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
    "external": '<svg viewBox="0 0 24 24" fill="none"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "star": '<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 1.5l2.47 5.18 5.68.74-4.2 3.86 1.08 5.62L10 14.9l-5.03 2.0 1.08-5.62-4.2-3.86 5.68-.74z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.3" fill="currentColor"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" fill="none"><rect x="2" y="5" width="20" height="14" rx="4" stroke="currentColor" stroke-width="2"/><path d="M10 9l5 3-5 3z" fill="currentColor"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24" fill="none"><path d="M14 8.5V7c0-.8.5-1 1-1h1.5V3H14c-2.2 0-3.5 1.3-3.5 3.6V8.5H8V12h2.5v9H14v-9h2.3l.7-3.5z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "chevron": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "arrow_left": '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" aria-hidden="true"><path d="M14 8H3M7 4L3 8l4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
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
            "address": {"@type": "PostalAddress", "streetAddress": ADDRESS_STREET, "addressLocality": "Calverton", "addressRegion": "Nottinghamshire", "postalCode": ADDRESS_POSTCODE, "addressCountry": "GB"},
            "geo": {"@type": "GeoCoordinates", "latitude": 53.03, "longitude": -1.08},
            "areaServed": ["Nottingham", "Nottinghamshire", "East Midlands", "United Kingdom"],
            "sameAs": [AUTOTRADER, INSTAGRAM, YOUTUBE, FACEBOOK],
            "priceRange": "££",
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": RATING_AVG, "reviewCount": RATING_COUNT, "bestRating": "5"},
            "review": [
                {
                    "@type": "Review",
                    "author": {"@type": "Person", "name": r["name"]},
                    "datePublished": r["date"],
                    "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
                    "reviewBody": r["text"],
                }
                for r in REVIEWS
            ],
        },
        {
            "@type": "ItemList",
            "name": "Recently sold campervans",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": vehicle_ld(v)} for i, v in enumerate(VANS)],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in FAQ
            ],
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
        <img class="logo-badge" src="brand/trade-leisure-logo-2.png" alt="Trade Leisure" width="112" height="112">
      </div>"""


# --- PLACEHOLDER available stock (demo only — remove/replace once real stock is listed) ---
# Two existing vans re-flagged "for sale" with example prices so the owner can see the
# live-listing state. Delete this block to return the site to a fully-sold archive.
PLACEHOLDERS = {
    "volkswagen-camper-king-monte-carlo-campervan-2-0l-diesel-highline-euro-6": "£34,950",
    "volkswagen-transporter-t30-highline-day-van-camper-van": "£28,995",
}
for v in VANS:
    if v["slug"] in PLACEHOLDERS:
        v["available"] = True
        v["price"] = PLACEHOLDERS[v["slug"]]

available_vans = [v for v in VANS if v.get("available")]
sold_vans = [v for v in VANS if not v.get("available")]

faq_items = "\n".join(
    f"""
      <details class="faq-item reveal">
        <summary><span>{e(q)}</span><span class="faq-chevron">{ICONS['chevron']}</span></summary>
        <div class="faq-answer"><p>{e(a)}</p></div>
      </details>"""
    for q, a in FAQ
)

STARS5 = ICONS["star"] * 5

reviews_cards = "\n".join(
    f"""
      <figure class="review-card reveal">
        <div class="stars">{STARS5}</div>
        <blockquote>{e(r['text'])}</blockquote>
        <figcaption><b>{e(r['name'])}</b><span>{e(r['when'])} · AutoTrader</span></figcaption>
      </figure>"""
    for r in REVIEWS
)

available_cards = "\n".join(card(v, f"TL·A{i + 1}") for i, v in enumerate(available_vans))

SOLD_VISIBLE = 6  # show this many sold vans; the rest hide behind a toggle
sold_codes = [f"TL·{i + 1:02d}" for i in range(len(sold_vans))]
sold_cards = "\n".join(card(v, sold_codes[i]) for i, v in enumerate(sold_vans[:SOLD_VISIBLE]))
sold_extra_cards = "\n".join(card(v, sold_codes[SOLD_VISIBLE + i]) for i, v in enumerate(sold_vans[SOLD_VISIBLE:]))
sold_extra_count = len(sold_vans) - SOLD_VISIBLE

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
      <img class="logo-mark" src="brand/trade-leisure-logo-2.png" alt="Trade Leisure campervans logo" width="48" height="48">
      <span><b>Trade Leisure</b><span class="coord mono">CALVERTON · {COORD}</span></span>
    </a>
    <nav class="nav-menu" id="nav-menu" aria-label="Main">
      <a href="#vans">Stock</a>
      <a href="#sell">Sell your van</a>
      <a href="#reviews">Reviews</a>
      <a href="#faq">FAQ</a>
      <a href="#about">About</a>
      <a href="#contact">Contact</a>
      <a class="nav-call" href="tel:{PHONE_INTL}">{ICONS['phone']}&nbsp;{PHONE}</a>
    </nav>
    <a class="btn btn-solid nav-call-btn" href="tel:{PHONE_INTL}">{ICONS['phone']}&nbsp;{PHONE}</a>
    <button class="nav-toggle" id="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="nav-menu">
      <span></span><span></span><span></span>
    </button>
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
          <a class="btn btn-solid" href="tel:{PHONE_INTL}">Call Mike — {PHONE}</a>
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
        <p class="marker">01 / Available now</p>
        <h2>In stock <span class="hl">today</span></h2>
        <p>Each van is HPI checked, freshly serviced and ready to drive away with a 12-month warranty. Tap one for the full log, photos and price — then call to book an unhurried viewing.</p>
        <a class="btn btn-ghost autotrader-cta" href="{AUTOTRADER}" target="_blank" rel="noopener">{ICONS['external']}&nbsp;See all live stock on AutoTrader</a>
      </div>
      <div class="van-grid">
{available_cards}
      </div>

      <div class="group-divider reveal">
        <p class="marker">Recently sold</p>
        <span class="route"><span></span></span>
      </div>
      <div class="sec-head reveal" style="margin-bottom:36px">
        <h2 style="font-size:clamp(28px,3.4vw,42px)">Gone to <span class="hl">good homes</span></h2>
        <p>A flavour of what's passed through recently — good stock doesn't hang about. Tell us what you're after and you'll be first to hear when the right one lands.</p>
      </div>
      <div class="van-grid">
{sold_cards}
      </div>
      <div class="van-grid sold-extra" id="sold-extra" hidden>
{sold_extra_cards}
      </div>
      <div class="sold-toggle-wrap reveal">
        <button class="btn btn-ghost sold-toggle" id="sold-toggle" aria-expanded="false" aria-controls="sold-extra">Show all {sold_extra_count} more sold vans</button>
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
        <p>We pay top trade prices for well-cared-for, professionally converted <b>VW and Ford</b> campervans up to 10 years old — it's half of what we do. Fill in the details and Mike will come back with a no-obligation offer, usually within 24 hours.</p>
        <ul class="checks">
          <li>{ICONS['check']}<span><b>A fair, honest valuation</b> — no obligation, and free to value your camper.</span></li>
          <li>{ICONS['check']}<span><b>Instant bank transfer &amp; free collection</b> — outstanding finance settled on the day.</span></li>
          <li>{ICONS['check']}<span><b>No listing fees, no timewasters</b> — and no strangers turning up at your door.</span></li>
        </ul>
        <p class="sell-talk">Prefer to talk? Call <a href="tel:{PHONE_INTL}">{PHONE}</a> or <a href="https://wa.me/447813696011">send photos on WhatsApp</a>.</p>
      </div>

      <form class="tl-form reveal" id="sell-form" novalidate>
        <h3>Sell your campervan</h3>
        <p class="form-intro">A few details to get you a quick, no-obligation offer.</p>
        <div class="field-row">
          <label class="field"><span>Make</span><input type="text" name="make" placeholder="e.g. Volkswagen" required></label>
          <label class="field"><span>Model</span><input type="text" name="model" placeholder="e.g. T6 Transporter" required></label>
        </div>
        <div class="field-row">
          <label class="field"><span>Year</span><input type="text" name="year" inputmode="numeric" placeholder="e.g. 2018"></label>
          <label class="field"><span>Mileage</span><input type="text" name="mileage" inputmode="numeric" placeholder="e.g. 45,000"></label>
        </div>
        <div class="field-row">
          <label class="field"><span>Gearbox</span>
            <select name="transmission"><option>Manual</option><option>Automatic</option></select>
          </label>
          <label class="field"><span>Who converted it?</span><input type="text" name="converter" placeholder="Converter / DIY"></label>
        </div>
        <div class="field-row">
          <label class="field"><span>Condition</span>
            <select name="condition"><option>Excellent</option><option>Good</option><option>Average</option><option>Below average</option></select>
          </label>
          <label class="field"><span>Photos <em>(up to 6)</em></span><input type="file" name="photos" accept="image/*" multiple></label>
        </div>
        <div class="field-row">
          <label class="field"><span>Your name</span><input type="text" name="name" autocomplete="name" required></label>
          <label class="field"><span>Email</span><input type="email" name="email" autocomplete="email" required></label>
        </div>
        <label class="field"><span>Anything else?</span><textarea name="message" rows="3" placeholder="Service history, extras, reg number, asking price…"></textarea></label>
        <div class="form-foot">
          <button type="submit" class="btn btn-solid">Get my offer</button>
          <p class="form-note mono">Preview form — wired to Mike's inbox when the site goes live.</p>
        </div>
        <p class="form-status" role="status" hidden></p>
      </form>
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

  <section class="reviews" id="reviews">
    <div class="wrap">
      <div class="reviews-head reveal">
        <div>
          <p class="marker">04 / Reviews</p>
          <h2>Rated <span class="hl">{RATING_AVG}</span> by buyers</h2>
        </div>
        <a class="ratings-badge" href="{AUTOTRADER}" target="_blank" rel="noopener">
          <span class="stars">{STARS5}</span>
          <b>{RATING_AVG} out of 5</b>
          <span class="count">{RATING_COUNT} reviews on AutoTrader {ICONS['external']}</span>
        </a>
      </div>
      <div class="reviews-grid">
{reviews_cards}
      </div>
    </div>
  </section>

  <section class="faq" id="faq">
    <div class="wrap">
      <div class="sec-head reveal">
        <p class="marker">05 / FAQ</p>
        <h2>Common <span class="hl">questions</span></h2>
        <p>Buying or selling, here are the things people ask most. Anything else — just call or drop Mike a message.</p>
      </div>
      <div class="faq-list">
{faq_items}
      </div>
    </div>
  </section>

  <section class="contact on-pine topo" id="contact">
    <div class="wrap">
      <div class="contact-intro reveal">
        <p class="marker">06 / Contact</p>
        <h2>Come and see <span class="hl">the vans</span></h2>
        <p class="lede">Viewings are by appointment — call, message or drop us a line below and we'll sort a time that suits. Honest answers, no pressure, kettle's on.</p>
        <ul class="contact-list">
          <li>{ICONS['phone']}<span><b>Phone / WhatsApp</b><a href="tel:{PHONE_INTL}">{PHONE}</a></span></li>
          <li>{ICONS['pin']}<span><b>Location · {COORD}</b><a href="https://maps.google.com/?q={ADDRESS_STREET.replace(' ', '+')},+Calverton,+{ADDRESS_POSTCODE.replace(' ', '+')}">{ADDRESS_STREET}, Calverton, {ADDRESS_POSTCODE}</a></span></li>
          <li>{ICONS['external']}<span><b>Live stock</b><a href="{AUTOTRADER}" target="_blank" rel="noopener">View on AutoTrader</a></span></li>
          <li>{ICONS['clock']}<span><b>Viewings</b>By appointment, seven days</span></li>
        </ul>
      </div>

      <form class="tl-form reveal" id="contact-form" novalidate>
        <h3>Send Mike a message</h3>
        <div class="field-row">
          <label class="field"><span>Your name</span><input type="text" name="name" autocomplete="name" required></label>
          <label class="field"><span>Email</span><input type="email" name="email" autocomplete="email" required></label>
        </div>
        <div class="field-row">
          <label class="field"><span>Phone <em>(optional)</em></span><input type="tel" name="phone" autocomplete="tel"></label>
          <label class="field"><span>I'm enquiring about</span>
            <select name="topic">
              <option>Buying a campervan</option>
              <option>Selling my campervan</option>
              <option>A specific van in stock</option>
              <option>Something else</option>
            </select>
          </label>
        </div>
        <label class="field"><span>Message</span><textarea name="message" rows="4" placeholder="Which van, your budget, part-exchange details — whatever helps." required></textarea></label>
        <div class="form-foot">
          <button type="submit" class="btn btn-solid">Send message</button>
          <p class="form-note mono">Preview form — wired to Mike's inbox when the site goes live.</p>
        </div>
        <p class="form-status" role="status" hidden></p>
      </form>
    </div>
  </section>

</main>

<footer>
  <div class="wrap">
    <span>© 2026 Trade Leisure · {ADDRESS_STREET}, Calverton, Nottingham {ADDRESS_POSTCODE} · <a href="{AUTOTRADER}" target="_blank" rel="noopener" style="color:inherit">AutoTrader</a></span>
    <div class="socials">
      <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Trade Leisure on Instagram">{ICONS['instagram']}</a>
      <a href="{YOUTUBE}" target="_blank" rel="noopener" aria-label="Trade Leisure on YouTube">{ICONS['youtube']}</a>
      <a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Trade Leisure on Facebook">{ICONS['facebook']}</a>
    </div>
    <span class="mono"><a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a> · PREVIEW BUILD</span>
  </div>
</footer>

<dialog class="van-modal" id="van-modal">
  <button class="modal-close" aria-label="Close">✕</button>
  <div class="modal-gallery" tabindex="0"></div>
  <div class="modal-body">
    <div class="modal-head"><h3></h3><span class="modal-ref mono"></span></div>
    <div class="modal-status"></div>
    <p class="gallery-hint">← Swipe / scroll the photos</p>
    <ul class="modal-bullets"></ul>
    <p class="modal-notes"></p>
    <div class="modal-specs"></div>
  </div>
</dialog>

<button class="to-top" id="to-top" aria-label="Back to top" hidden>{ICONS['chevron']}</button>

<script src="app.js"></script>
</body>
</html>
"""

out = os.path.join(ROOT, "site", "index.html")
open(out, "w").write(page)
print(f"wrote {out} ({len(page):,} bytes, {len(VANS)} vans)")


# ---------------------------------------------------------------------------
# Legal pages (privacy + terms). Placeholder copy — have a solicitor review
# before going live; flagged on-page so it isn't mistaken for final wording.
# ---------------------------------------------------------------------------
def legal_page(slug, title, body):
    html_doc = f"""<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)} — Trade Leisure</title>
  <meta name="robots" content="noindex, nofollow">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Hanken+Grotesk:wght@400;500;600;700&family=Spline+Sans+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
<header>
  <div class="nav">
    <a class="wordmark" href="index.html">
      <img class="logo-mark" src="brand/trade-leisure-logo-2.png" alt="Trade Leisure campervans logo" width="48" height="48">
      <span><b>Trade Leisure</b><span class="coord mono">CALVERTON · {COORD}</span></span>
    </a>
    <a class="btn btn-solid" href="index.html">{ICONS['arrow_left']}&nbsp;Back to site</a>
  </div>
</header>
<main class="legal">
  <div class="wrap">
    <p class="marker">Trade Leisure</p>
    <h1>{e(title)}</h1>
    <p class="legal-note mono">Placeholder wording for the preview — to be reviewed before the site goes live.</p>
    {body}
  </div>
</main>
<footer>
  <div class="wrap">
    <span>© 2026 Trade Leisure · {ADDRESS_STREET}, Calverton, Nottingham {ADDRESS_POSTCODE}</span>
    <span class="mono"><a href="privacy.html" style="color:inherit">Privacy</a> · <a href="terms.html" style="color:inherit">Terms</a></span>
  </div>
</footer>
</body>
</html>
"""
    p = os.path.join(ROOT, "site", slug)
    open(p, "w").write(html_doc)
    print(f"wrote {p}")


PRIVACY_BODY = f"""
  <p>This notice explains how Trade Leisure ("we", "us") handles the personal information you share with us. We are a campervan dealer based at {ADDRESS_STREET}, Calverton, Nottingham {ADDRESS_POSTCODE}.</p>
  <h2>What we collect</h2>
  <p>When you use our contact or "sell your campervan" forms, or call us, we collect the details you provide — typically your name, email address, phone number, and information about a vehicle you want to buy or sell (including any photos you send).</p>
  <h2>How we use it</h2>
  <p>We use your details only to respond to your enquiry, provide a valuation or quote, arrange a viewing or sale, and keep the records we're legally required to keep as a motor trader. We do not sell your data, and we don't send marketing unless you ask us to.</p>
  <h2>How long we keep it</h2>
  <p>We keep enquiry details only as long as needed to deal with your enquiry and meet our legal obligations, then delete them.</p>
  <h2>Your rights</h2>
  <p>You can ask to see the information we hold about you, ask us to correct or delete it, or object to how we use it. To do so, call {PHONE} or email us using the address on the contact page.</p>
  <h2>Contact</h2>
  <p>Questions about this notice? Call {PHONE} or get in touch via the <a href="index.html#contact">contact form</a>.</p>
"""

TERMS_BODY = f"""
  <p>These terms cover the use of this website and the buying and selling of vehicles with Trade Leisure. They don't affect your statutory rights as a consumer.</p>
  <h2>Vehicles &amp; descriptions</h2>
  <p>We describe every vehicle as accurately as we can, and all of our stock is HPI checked and prepared before sale. Specifications and prices may change, and a vehicle is only reserved once agreed with us directly.</p>
  <h2>Warranty</h2>
  <p>Vehicles are sold with a 12-month Autoguard parts &amp; labour warranty unless stated otherwise. Full warranty terms are provided at the point of sale.</p>
  <h2>Selling or part-exchanging to us</h2>
  <p>Any valuation we give is an offer, not a binding contract, and is subject to us inspecting the vehicle. We buy professionally converted VW and Ford campervans; we don't buy DIY conversions. Payment is made by bank transfer on collection.</p>
  <h2>This website</h2>
  <p>Content on this site is provided in good faith for information only. Live stock and pricing should be confirmed with us directly or via our AutoTrader listings.</p>
  <h2>Contact</h2>
  <p>Call {PHONE} or use the <a href="index.html#contact">contact form</a>.</p>
"""

legal_page("privacy.html", "Privacy Policy", PRIVACY_BODY)
legal_page("terms.html", "Terms & Conditions", TERMS_BODY)
