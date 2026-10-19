# Africa's Enduring Enterprises

**The companies that survived. The institutions they built. The lessons for Africa's next century.**

An open research and editorial project by [legesi.xyz](https://legesi.xyz/projects/africa-enduring-enterprises/), with features intended for [legesi.substack.com](https://legesi.substack.com).

## Public research directory

The site is published in the [Legesi.xyz website repository](https://github.com/Superstar1910/Superstar1910.github.io/tree/main/projects/africa-enduring-enterprises). This repository is the **canonical research data source**. The public HTML is generated from `data/companies.csv` using `scripts/generate_site.py` and copied into the website repository. Cross-repository publication is currently a manual commit, not automated deployment.

## Repository structure

- `data/companies.csv`: 22 provisional institutions, stable company IDs, origin type, continuity notes and evidence status.
- `data/sources.csv`: documentary references tied to a company and claim.
- `data/ownership-events.csv`, `data/leadership-events.csv`: time-stamped changes.
- `data/financials.csv`, `data/anniversaries.csv`: reported metrics and milestones.
- `methodology/`: verification, research framework, experimental longevity scoring and editorial safeguards.
- `profiles/`: company research briefs.
- `research/`: case studies, comparative analysis and institutional lessons.
- `editorial/`: drafts, publication register and content calendar.
- `site/index.html`: generated static directory, **do not edit by hand**.
- `scripts/validate.py`: schema and foreign-key validation.
- `scripts/generate_site.py`: deterministic HTML generation.
- `.github/workflows/validate.yml`: validation and site consistency check.

## Reproduce

```sh
python3 scripts/validate.py
python3 scripts/generate_site.py
```

The workflow rejects changes where generated HTML is out of sync with canonical CSV data.

## Important qualifications

**No definitive ranking is claimed.** Origins may refer to a predecessor lineage, brand, family group or cooperative rather than the same continuously operating legal entity. All 22 records are provisional and none has yet passed the project's full independent verification protocol. Empty event tables mean **not yet researched**, not that no changes occurred. The original `data/candidates.csv` is a legacy snapshot; use `data/companies.csv` for all new work.

Research text: CC BY 4.0; code: MIT. Third-party images and trademarks excluded. License files are pending.
