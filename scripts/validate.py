#!/usr/bin/env python3
"""Validate research data and its foreign-key relationships."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "companies.csv": ("company_id","name","country","origin_year","category","origin_type","evidence_status","continuity_note"),
    "sources.csv": ("source_id","company_id","claim_id","source_title","source_url","publisher","publication_date","accessed_date","source_type","verification_status","notes"),
    "ownership-events.csv": ("event_id","company_id","event_date","event_type","from_owner","to_owner","ownership_percentage","source_id","notes"),
    "leadership-events.csv": ("event_id","company_id","event_date","person","role","event_type","source_id","notes"),
    "financials.csv": ("record_id","company_id","fiscal_year","currency","metric","value","unit","audited","source_id","notes"),
    "financing-events.csv": ("financing_id","company_id","project","document_date","financier","instrument","currency","amount_millions","amount_basis","source_id","notes"),
    "anniversaries.csv": ("anniversary_id","company_id","anniversary_year","years_since_origin","origin_basis","source_id","verification_status","notes"),
}
tables = {}
for filename, columns in SCHEMAS.items():
    with (ROOT/"data"/filename).open(encoding="utf-8",newline="") as handle:
        reader = csv.DictReader(handle)
        assert tuple(reader.fieldnames or ()) == columns, "Unexpected schema: "+filename
        tables[filename] = list(reader)
companies=tables["companies.csv"]
ids={r["company_id"] for r in companies}
assert len(ids)==len(companies) and all(ids), "Duplicate or missing company IDs"
assert len({(r["name"],r["country"]) for r in companies})==len(companies)
for r in companies:
    assert 1800 <= int(r["origin_year"]) <= 2026
    assert r["evidence_status"] in {"verified","partially_verified","disputed","unverified"}
sources={r["source_id"] for r in tables["sources.csv"]}
assert len(sources)==len(tables["sources.csv"])
for filename, rows in tables.items():
    for r in rows:
        if filename!="companies.csv":
            assert r["company_id"] in ids, "Unknown company in "+filename
        if r.get("source_id"):
            assert r["source_id"] in sources, "Unknown source in "+filename
print("Validated",len(companies),"companies and",sum(len(v) for k,v in tables.items() if k!="companies.csv"),"linked records")
