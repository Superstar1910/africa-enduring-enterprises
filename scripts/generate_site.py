#!/usr/bin/env python3
"""Generate a static, accessible research directory from canonical CSV data."""
import csv
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(name):
    with (ROOT / "data" / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

def build():
    companies = sorted(read("companies.csv"), key=lambda r: (int(r["origin_year"]), r["name"]))
    countries = sorted({r["country"] for r in companies})
    options = "\n".join('<option value="%s">%s</option>' % (html.escape(c, quote=True), html.escape(c)) for c in countries)
    rows = []
    for r in companies:
        cells = [r["name"], r["country"], r["origin_year"], r["origin_type"].replace("_", " "), r["evidence_status"].replace("_", " ")]
        tds = "".join("<td>%s</td>" % html.escape(x) for x in cells)
        search = html.escape((r["name"]+" "+r["country"]).lower(), quote=True)
        country = html.escape(r["country"], quote=True)
        rows.append('<tr data-search="%s" data-country="%s">%s</tr>' % (search, country, tds))
    doc = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Africa's Enduring Enterprises | Legesi.xyz</title>
<meta name="description" content="Open research into the longevity, succession and governance of African enterprises.">
<link rel="canonical" href="https://legesi.xyz/projects/africa-enduring-enterprises/">
<style>:root{color-scheme:light}body{font:16px/1.55 system-ui,sans-serif;max-width:1080px;margin:auto;padding:32px 20px;background:#f8f6f1;color:#202a2c}h1{font-size:clamp(2rem,5vw,4rem);line-height:1.1}header{border-bottom:2px solid #173c36;padding-bottom:22px}input,select{padding:12px;border:1px solid #b7c1ba;border-radius:6px;max-width:100%}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:11px;border-bottom:1px solid #d7ddd8}th{white-space:nowrap}small{color:#596b65}.scroll{overflow-x:auto}a{color:#145d4d}tr[hidden]{display:none}.note{padding:14px;border-left:3px solid #145d4d;background:#edf1ed}label{display:inline-block;margin:8px 12px 8px 0}</style></head>
<body><header><p><a href="/projects/">← Projects</a></p><small>LEGESI.XYZ / OPEN RESEARCH</small>
<h1>Africa's Enduring Enterprises</h1><p>The companies that survived. The institutions they built. The lessons for Africa's next century.</p>
<p class="note">Provisional research register: <strong>__COUNT__ candidate institutions</strong>. Origin dates may represent predecessor lineages or group histories; no record is classified as independently verified yet.</p></header>
<main><section id="origin" aria-labelledby="origin-heading" style="margin:28px 0;padding:24px;border:1px solid #cbd5d0;border-radius:12px;background:#fff"><small>THE CONVERSATION THAT STARTED THE RESEARCH</small><h2 id="origin-heading">From a question about Uganda's oldest businesses to a research programme</h2><blockquote style="border-left:4px solid #145d4d;padding:10px 18px;margin:16px 0;background:#edf1ed;font-size:1.15rem">“Entrepreneurs start the businesses but never build the governance and institutions to ensure their longevity beyond the founder's vision.”</blockquote><p>— Kenneth Legesi, responding to <a href="https://x.com/ekiggundu/status/2077024689482797548" rel="noopener noreferrer" target="_blank">the original X post by @ekiggundu</a>.</p><p>The response was accompanied by a handwritten <strong>Uganda Business Longevity &amp; Institution-Building Map</strong>, bringing together enterprise-age data, examples of longstanding Ugandan businesses, the succession challenge, and the institutional reforms needed to build enduring enterprises.</p><p><a href="https://x.com/ekiggundu/status/2077024689482797548" rel="noopener noreferrer" target="_blank">Read the original conversation on X ↗</a></p><p><small>Editorial note: the map's establishment counts, founding dates and implied survival rates are research leads, not independently validated longitudinal survival estimates. The original handwritten image is awaiting upload to the public website asset library.</small></p></section><h2>Explore the register</h2><label for="q">Search <input id="q" type="search" placeholder="Company or country"></label>
<label for="country">Country <select id="country"><option value="">All countries</option>__OPTIONS__</select></label>
<p id="count" aria-live="polite"></p><div class="scroll"><table><thead><tr><th>Enterprise</th><th>Country</th><th>Origin year</th><th>Origin basis</th><th>Evidence</th></tr></thead>
<tbody id="rows">__ROWS__</tbody></table></div><h2>What we investigate</h2>
<p>Company origins, legal and operating continuity, ownership transitions, leadership succession, governance and long-term capital formation. This is not a ranking of the oldest legally continuous African companies.</p>
<p>Explore <a href="https://github.com/Superstar1910/africa-enduring-enterprises/tree/main/methodology">methodology</a>,
<a href="https://github.com/Superstar1910/africa-enduring-enterprises/tree/main/data">research data</a> and
<a href="https://legesi.substack.com/">editorial features</a>.</p></main>
<script>const q=document.getElementById('q'),c=document.getElementById('country'),r=[...document.querySelectorAll('#rows tr')],n=document.getElementById('count');function draw(){let k=0;for(const x of r){const show=x.dataset.search.includes(q.value.trim().toLowerCase())&&(!c.value||x.dataset.country===c.value);x.hidden=!show;if(show)k++}n.textContent=k+' of '+r.length+' candidates'}q.addEventListener('input',draw);c.addEventListener('change',draw);draw();</script></body></html>
"""
    return doc.replace("__COUNT__", str(len(companies))).replace("__OPTIONS__", options).replace("__ROWS__", "\n".join(rows))

if __name__ == "__main__":
    path = ROOT / "site" / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build(), encoding="utf-8")
    print("Generated", path)
