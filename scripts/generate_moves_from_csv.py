#!/usr/bin/env python3
"""Generate move markdown files from data/salsa_vault.csv without overwriting existing files."""
from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path

CSV_PATH = Path("data/salsa_vault.csv")
MOVES_DIR = Path("src/content/moves")

YOUTUBE_PATTERNS = [
    re.compile(r"(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})"),
    re.compile(r"(?:youtu\.be/)([A-Za-z0-9_-]{11})"),
    re.compile(r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})"),
]


def extract_youtube_id(url: str) -> str | None:
    for pattern in YOUTUBE_PATTERNS:
        match = pattern.search(url or "")
        if match:
            return match.group(1)
    return None


def parse_tags(raw_tags: str) -> list[str]:
    if not raw_tags:
        return []
    return [tag.strip() for tag in raw_tags.split(",") if tag.strip()]


def to_markdown(row: dict[str, str], yt_id: str) -> str:
    tags = parse_tags(row.get("tags", ""))
    tags_block = "\n".join(f"  - {tag}" for tag in tags)
    notes = (row.get("notes") or "").strip()
    today = date.today().isoformat()

    return f"""---
id: yt_{yt_id}
youtube_id: {yt_id}
youtube_url: {row.get('youtube_url', '').strip()}
title: {row.get('title', '').strip()}
category: {row.get('category', '').strip()}
tags:
{tags_block if tags_block else '  -'}
status: new
date_added: {today}
---

## Notes

{notes}

## Practice Log
"""


def main() -> int:
    created = 0
    skipped = 0
    errors = 0

    MOVES_DIR.mkdir(parents=True, exist_ok=True)

    if not CSV_PATH.exists():
        print(f"errors: missing CSV at {CSV_PATH}")
        return 1

    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):
            url = (row.get("youtube_url") or "").strip()
            yt_id = extract_youtube_id(url)
            if not yt_id:
                print(f"error line {idx}: invalid YouTube URL: {url}")
                errors += 1
                continue

            md_path = MOVES_DIR / f"yt_{yt_id}.md"
            if md_path.exists():
                skipped += 1
                continue

            md_path.write_text(to_markdown(row, yt_id), encoding="utf-8")
            created += 1

    print(f"created: {created}")
    print(f"skipped: {skipped}")
    print(f"errors: {errors}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
