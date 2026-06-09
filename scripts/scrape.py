#!/usr/bin/env python3
"""Scrape inventory from trade-leisure.co.uk into data/vans.json + downloaded photos."""
import json
import os
import re
import urllib.request

BASE = "https://trade-leisure.co.uk"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (site rebuild for owner; contact via 07813 696011 listing)"}
MAX_PHOTOS = 8


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def listing_urls():
    urls = []
    for page in ["/inventory", "/inventory/page/2", "/inventory/page/3"]:
        html = get(BASE + page)
        urls += re.findall(r'href="(https://trade-leisure\.co\.uk/listings/[^"]+)"', html)
    seen, out = set(), []
    for u in urls:
        u = u.rstrip("/")
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def parse_listing(url, html):
    title = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    title = re.sub(r"<[^>]+>", "", title.group(1)).strip() if title else ""
    desc = re.search(r'property="og:description" content="([^"]*)"', html)
    desc = desc.group(1) if desc else ""
    # decode common entities
    for ent, ch in [("&#8217;", "’"), ("&amp;", "&"), ("&#039;", "'"), ("&hellip;", "…"), ("&#8230;", "…")]:
        desc = desc.replace(ent, ch)
        title = title.replace(ent, ch)
    specs = {}
    for label, value in re.findall(
        r'<td class="t-label">([^<]+)</td>.*?<td class="t-value[^"]*">([^<]+)</td>', html, re.S
    ):
        specs[label.strip()] = value.strip()
    imgs = re.findall(r'https://trade-leisure\.co\.uk/wp-content/uploads/[^"\'\s)]+?-798x466\.(?:jpe?g|png|webp)', html)
    uniq = []
    for i in imgs:
        if i not in uniq and "logo" not in i:
            uniq.append(i)
    return {
        "slug": url.rsplit("/", 1)[1],
        "url": url,
        "title": title,
        "summary": desc,
        "specs": specs,
        "image_urls": uniq[:MAX_PHOTOS],
    }


def main():
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    vans = []
    for url in listing_urls():
        try:
            html = get(url)
        except Exception as e:
            print(f"SKIP {url}: {e}")
            continue
        van = parse_listing(url, html)
        photo_dir = os.path.join(ROOT, "site", "photos", van["slug"])
        os.makedirs(photo_dir, exist_ok=True)
        local = []
        for n, img in enumerate(van["image_urls"]):
            ext = img.rsplit(".", 1)[1]
            path = os.path.join(photo_dir, f"{n:02d}.{ext}")
            if not os.path.exists(path):
                try:
                    req = urllib.request.Request(img, headers=UA)
                    with urllib.request.urlopen(req, timeout=60) as r:
                        open(path, "wb").write(r.read())
                except Exception as e:
                    print(f"  img fail {img}: {e}")
                    continue
            local.append(f"photos/{van['slug']}/{n:02d}.{ext}")
        van["photos"] = local
        vans.append(van)
        print(f"OK {van['slug']}: {len(local)} photos, specs={list(van['specs'].keys())}")
    json.dump(vans, open(os.path.join(ROOT, "data", "vans.json"), "w"), indent=2)
    print(f"\n{len(vans)} vans written to data/vans.json")


if __name__ == "__main__":
    main()
