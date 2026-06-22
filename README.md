# Mind Lab — DefenderOfBasic

A public research repository for observing one mind over time: Defender's public record, structured for analysis, annotation, and long-term study.

## What this is

This repo peers into the mind of DefenderOfBasic through public tweets and Substack posts.

It contains:

- `data/tweets_raw.jsonl` — exported public tweets in JSONL format
- `data/tweets_for_labeling.csv` — tabular export prepared for human labeling
- `data/tweets_for_llm_labeling.jsonl` — export formatted for LLM-assisted labeling
- `data/substack/` — one directory per Substack post, markdown content + metadata
- `references/schema.md` — field definitions and labeling schema
- `receipts/coverage.json` — coverage and data lineage receipts

The data comes from public sources. Shared here to make the analytical record inspectable, reproducible, and improvable.

## Principles

- Public data, public repo
- No secret keys, no private credentials, no hidden snapshots
- Schema documented in code
- Changes tracked like any research artifact

## Data overview

- Source: Community Archive + Substack
- Format: JSONL + Markdown
- Scope: 2023-07-18 through 2024-11-19 (archive snapshot)
- Size: ~23k tweets, 435 note-tweets, ~10 Substack posts

## Schema

See `references/schema.md` for field definitions and labeling taxonomy.

## Safety

This repo is intentionally lean:

```text
.env
.env.*
*.private.*
.venv/
venv/
.ipynb_checkpoints/
node_modules/
*.parquet
*.csv.gz
*.tar.gz
*.zip
.DS_Store
Thumbs.db
.secrets/
secrets/
key*
id_rsa
*.pem
*.key
```

If a file could contain credentials, it stays out.

## How to use

```bash
git clone ...
cd mind-lab-defender
```

Work in branches. Open issues for schema changes. Do not add keys.

## Citation

DefenderOfBasic public corpus via Community Archive (github.com/TheExGenesis/community-archive) and Substack.
<!-- test -->
