# Tweet export schema

## Raw JSONL schema

File: `data/tweets_raw.jsonl`

Fields:

- `tweet_id` — tweet ID string
- `account_id` — account ID string
- `created_at` — ISO 8601 timestamp
- `full_text` — tweet text
- `retweet_count` — integer
- `favorite_count` — integer
- `reply_to_tweet_id` — nullable string
- `reply_to_user_id` — nullable string
- `reply_to_username` — nullable string
- `archive_upload_id` — integer
- `fts` — full-text search token data
- `updated_at` — ISO 8601 timestamp
- `source_dataset` — `raw_archive` or `api_incremental`
- `archive_fetched_at` — ISO 8601 timestamp

## Labeling CSV schema

File: `data/tweets_for_labeling.csv`

Fields:

- `row_id` — integer row identifier
- `tweet_id` — tweet ID string
- `created_at` — ISO 8601 timestamp
- `text` — tweet text
- `like_count` — integer
- `retweet_count` — integer
- `reply_count` — integer
- `primary_function` — label string
- `secondary_function` — label string
- `topic` — label string
- `attractor` — label string
- `originality` — label string
- `voice` — label string
- `notes` — free text notes

## LLM labeling JSONL schema

File: `data/tweets_for_llm_labeling.jsonl`

Fields:

- `row_id` — integer row identifier
- `tweet_id` — tweet ID string
- `created_at` — ISO 8601 timestamp
- `text` — tweet text
- `labels_to_fill` — object with target label fields

## Label taxonomy

Primary/secondary function labels:

- Original Theory
- Observation
- Synthesis
- Meta Analysis
- Research
- Teaching
- Personal Story
- Prediction
- Coordination
- News
- Coaching

Topic and attractor labels are free-form per event.

## Notes

- Unlabeled exports are public.
- Private analysis receipts should use `.private.jsonl` and remain local or in a separate private artifact store.
- Source: Community Archive raw JSON for @DefenderOfBasic, fetched 2026-06-22.
- Coverage: 2023-07-18 through 2024-11-19.
