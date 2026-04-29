# Salsa Roja

Phone-first personal salsa vault for class videos and notes.

## Architecture

Google Form → Google Sheet → Apps Script → `data/salsa_vault.csv` → GitHub Action → Markdown files in `src/content/moves/` → Astro static site → GitHub Pages.

## Repo layout

- `data/salsa_vault.csv`: sheet export committed by Apps Script
- `scripts/generate_moves_from_csv.py`: seed markdown files from CSV (non-destructive)
- `src/content/moves/`: one markdown file per YouTube video
- `src/content/config.ts`: Astro content collection schema
- `src/pages/index.astro`: home page with cards/search
- `src/pages/moves/[id].astro`: move detail page
- `.github/workflows/deploy.yml`: generation + build + deploy pipeline

## Google Form + Sheet flow

1. Create a Google Form with fields: `title`, `youtube_url`, `category`, `tags`, `notes`.
2. Link form responses to a Google Sheet.
3. Keep CSV column order:
   `timestamp,title,youtube_url,category,tags,notes`

## Apps Script idea (Sheet → Repo CSV)

Use a time-driven trigger (for example every hour) in Apps Script to:

1. Read all rows from the response sheet.
2. Convert rows to CSV text.
3. Commit to this repo as `data/salsa_vault.csv` using GitHub API and a fine-grained token.

This repo treats CSV as the source for **new files only**.

## Markdown generation

Run locally:

```bash
python scripts/generate_moves_from_csv.py
```

Behavior:
- extracts YouTube IDs from `watch?v=`, `youtu.be/`, and `shorts/` URLs
- creates `src/content/moves/yt_<youtube_id>.md` only when missing
- never overwrites existing notes
- prints `created`, `skipped`, and `errors`

## Editing notes later

After a file exists, edit markdown directly in `src/content/moves/`.
CSV updates will not overwrite existing files.

## Deployment

On every push to `main`:

1. Generate missing markdown from CSV
2. Commit/push generated files if any (with `[skip ci]` to avoid loop)
3. Build Astro site
4. Deploy to GitHub Pages

## Why this setup

- No backend, no DB
- Fully static and low-maintenance
- Mobile-friendly, simple UI
