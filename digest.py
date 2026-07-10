"""Fetch top AI / data science headlines from RSS feeds and email a digest."""

import os
import smtplib
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import feedparser

FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.artificialintelligence-news.com/feed/",
    "https://www.marktechpost.com/feed/",
    "http://export.arxiv.org/rss/cs.AI",
    "http://export.arxiv.org/rss/cs.LG",
]

KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "data science",
    "llm", "large language model", "neural network", "deep learning",
    "generative ai", "genai", "nlp", "chatgpt", "claude", "gemini",
    "openai", "anthropic", "model", "dataset", "algorithm",
]

TOP_N = 10


def is_relevant(title, summary):
    text = f"{title} {summary}".lower()
    return any(keyword in text for keyword in KEYWORDS)


def fetch_headlines():
    entries = []
    for feed_url in FEEDS:
        parsed = feedparser.parse(feed_url)
        source = parsed.feed.get("title", feed_url)
        for entry in parsed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "")
            summary = entry.get("summary", "")
            published = entry.get("published_parsed") or entry.get("updated_parsed")
            if not title or not link:
                continue
            if not is_relevant(title, summary):
                continue
            entries.append(
                {
                    "title": title,
                    "link": link,
                    "source": source,
                    "published": published,
                }
            )

    entries.sort(key=lambda e: e["published"] or 0, reverse=True)

    seen_titles = set()
    unique_entries = []
    for entry in entries:
        key = entry["title"].lower()
        if key in seen_titles:
            continue
        seen_titles.add(key)
        unique_entries.append(entry)

    return unique_entries[:TOP_N]


def build_email_body(headlines):
    today = datetime.now(timezone.utc).strftime("%B %d, %Y")
    lines = [f"Top {len(headlines)} AI / Data Science headlines for {today}\n"]
    for i, item in enumerate(headlines, start=1):
        lines.append(f"{i}. {item['title']} ({item['source']})\n   {item['link']}\n")
    return "\n".join(lines)


def send_email(subject, body):
    gmail_user = os.environ["GMAIL_USER"]
    gmail_app_password = os.environ["GMAIL_APP_PASSWORD"]
    to_email = os.environ.get("TO_EMAIL", gmail_user)

    message = MIMEMultipart()
    message["From"] = gmail_user
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_app_password)
        server.sendmail(gmail_user, to_email, message.as_string())


def main():
    headlines = fetch_headlines()
    if not headlines:
        print("No headlines found; skipping email.")
        return

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    subject = f"AI / Data Science Digest - {today}"
    body = build_email_body(headlines)

    send_email(subject, body)
    print(f"Sent digest with {len(headlines)} headlines to {os.environ.get('TO_EMAIL', 'GMAIL_USER')}.")


if __name__ == "__main__":
    main()
