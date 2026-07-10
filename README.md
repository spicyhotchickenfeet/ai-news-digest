# ai-news-digest

Sends a free daily email with the top 10 AI / data science headlines, pulled from RSS feeds (TechCrunch, MIT Tech Review, VentureBeat, arXiv cs.AI/cs.LG, and more). Runs automatically every morning via GitHub Actions — no server or paid API required.

## Setup

1. **Create a Gmail App Password** (the Gmail account you send *from*):
   - Enable 2-Step Verification on that Google account.
   - Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) and generate an app password for "Mail".

2. **Add repo secrets** (Settings → Secrets and variables → Actions → New repository secret):
   - `GMAIL_USER` — the Gmail address to send from.
   - `GMAIL_APP_PASSWORD` — the 16-character app password from step 1.
   - `TO_EMAIL` — the address to receive the digest (e.g. your student email). Optional — defaults to `GMAIL_USER`.

3. Done. The workflow in [.github/workflows/daily-digest.yml](.github/workflows/daily-digest.yml) runs daily at 06:00 UTC (~07:00–08:00 Netherlands time). Trigger it manually anytime from the Actions tab ("Run workflow") to test.

## Local run

```bash
pip install -r requirements.txt
GMAIL_USER=you@gmail.com GMAIL_APP_PASSWORD=xxxx TO_EMAIL=you@example.com python digest.py
```

## Customizing

- Edit `FEEDS` in [digest.py](digest.py) to add/remove RSS sources.
- Edit `KEYWORDS` to change relevance filtering.
- Edit the cron schedule in the workflow file to change delivery time.
