#!/usr/bin/env python3
"""
Fetch the latest DefenderOfBasic archive from the community archive,
diff against the currently-normalized corpus in data/, and append
any new tweets / note-tweets / community-tweets that have appeared
since the last pull.

Usage:
    python scripts/pull_latest.py
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests not installed", file=sys.stderr)
    sys.exit(1)

ARCHIVE_URL = (
    "https://fabxmporizzqflnftavs.supabase.co"
    "/storage/v1/object/public/archives/defenderofbasic/archive.json"
)
REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = REPO_ROOT / "data" / "tweets_raw.jsonl"
COVERAGE_PATH = REPO_ROOT / "receipts" / "coverage.json"
CHECKPOINT_PATH = REPO_ROOT / "data" / ".archive_checkpoint.json"


def parse_date(val: str):
    fmt = "%a %b %d %H:%M:%S %z %Y"
    try:
        return datetime.strptime(val, fmt)
    except Exception:
        return None


def extract_existing_ids()-> set:
    ids = set()
    if not RAW_PATH.exists():
        return ids
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                tid = obj.get("id") or obj.get("tweet_id") or obj.get("noteTweetId")
                if tid:
                    ids.add(str(tid))
            except json.JSONDecodeError:
                continue
    return ids


def main():
    print("Fetching latest archive...")
    resp = requests.get(ARCHIVE_URL, timeout=120)
    resp.raise_for_status()
    blob = resp.content

    print(f"Downloaded {len(blob):,} bytes")
    data = resp.json()

    sections = {
        "tweets": lambda item: item.get("tweet", {}).get("created_at", ""),
        "note-tweet": lambda item: item.get("noteTweet", {}).get("createdAt", ""),
        "community-tweet": lambda item: item.get("tweet", {}).get("created_at", ""),
    }

    existing_ids = extract_existing_ids()
    print(f"Existing normalized IDs: {len(existing_ids)}")

    new_records = []
    max_seen = None

    for key, date_fn in sections.items():
        items = data.get(key, [])
        for item in items:
            if key == "tweets":
                tweet = item.get("tweet", {})
                vtype = "tweet"
                tid = str(tweet.get("id") or tweet.get("id_str", ""))
                created = tweet.get("created_at", "")
                text = tweet.get("full_text", "")
                user = tweet.get("user", {})
                username = user.get("screen_name", "defenderofbasic")
                urls = []
                for url_ent in tweet.get("entities", {}).get("urls", []):
                    urls.append(url_ent.get("expanded_url", url_ent.get("url", "")))
            elif key == "note-tweet":
                note = item.get("noteTweet", {})
                vtype = "note"
                tid = str(note.get("noteTweetId", ""))
                created = note.get("createdAt", "")
                text = note.get("core", {}).get("text", "")
                username = "defenderofbasic"
                urls = note.get("core", {}).get("urls", [])
            else:
                tweet = item.get("tweet", {})
                vtype = "community"
                tid = str(tweet.get("id") or tweet.get("id_str", ""))
                created = tweet.get("created_at", "")
                text = tweet.get("full_text", "")
                user = tweet.get("user", {})
                username = user.get("screen_name", "defenderofbasic")
                urls = []
                for url_ent in tweet.get("entities", {}).get("urls", []):
                    urls.append(url_ent.get("expanded_url", url_ent.get("url", "")))

            if tid and tid in existing_ids:
                continue
            if not tid:
                continue

            d = parse_date(created)
            if d:
                if max_seen is None or d > max_seen:
                    max_seen = d

            record = {
                "id": tid,
                "created_at": created,
                "type": vtype,
                "username": username,
                "text": text,
                "urls": urls,
            }
            new_records.append(record)

    if not new_records:
        print("No new records to add. Corpus is up to date.")
        if max_seen:
            print(f"Latest date in archive: {max_seen.isoformat()}")
        return 0

    # Append to raw JSONL
    with open(RAW_PATH, "a", encoding="utf-8") as f:
        for rec in new_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Appended {len(new_records)} new records to {RAW_PATH}")
    if max_seen:
        print(f"Latest date added: {max_seen.isoformat()}")

    # Update checkpoint
    checkpoint = {
        "pulled_at": datetime.now(timezone.utc).isoformat(),
        "archive_size": len(blob),
        "latest_date": max_seen.isoformat() if max_seen else None,
        "new_records": len(new_records),
    }
    CHECKPOINT_PATH.write_text(
        json.dumps(checkpoint, indent=2), encoding="utf-8"
    )
    print(f"Checkpoint written to {CHECKPOINT_PATH}")
    print("Next step: run the normalization script (if schema formatting needed), then commit + push.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)
