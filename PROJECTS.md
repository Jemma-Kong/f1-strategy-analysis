# Project Index

This repository is organised as a Formula 1 strategy and performance analysis portfolio.

## Race Analyses

| Project | Status | Focus |
| --- | --- | --- |
| `analyses/race_analyses/2024_monaco_gp_baseline` | Archived baseline | Early FastF1/OpenF1 practice scripts and Monaco race visualisations |

## Directory Conventions

- `analysis.md`: public-facing write-up for a completed or in-progress analysis.
- `scripts/` or analysis `.py` files: reproducible data extraction and plotting code.
- `figures/`: generated visualisations used in the write-up.
- `outputs/`: generated CSV/Markdown evidence tables.
- `cache/`: local FastF1 cache, ignored by git.

New race projects should be created under:

```text
analyses/race_analyses/YYYY_event_name_topic/
```
