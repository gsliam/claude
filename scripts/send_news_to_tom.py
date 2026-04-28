#!/usr/bin/env python3
"""Daily news script - sends top social/AI/tech news to Tom Geurts via Slack DM."""

import subprocess
import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

TOM_GEURTS_SLACK_ID = "UUSM9N0MD"
PROJECT_DIR = Path(__file__).parent.parent


def load_env():
    env_file = PROJECT_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def search_news() -> str:
    prompt = (
        "Search for today's top 5 news stories across these categories: "
        "social media, social AI, general AI/tech breakthroughs, TikTok Shop, and social commerce. "
        "Format the response as a clean Slack message with: "
        "a short header line with today's date, "
        "then 5 bullet points each with an emoji, bold story title, and a one-sentence summary. "
        "Use 📱 for social media, 🤖 for AI, 🛍️ for commerce/TikTok. "
        "Output ONLY the formatted message text, nothing else."
    )

    result = subprocess.run(
        [
            "claude", "-p", prompt,
            "--output-format", "text",
            "--allowed-tools", "WebSearch",
        ],
        capture_output=True,
        text=True,
        timeout=180,
        env=os.environ.copy(),
    )

    if result.returncode != 0:
        raise RuntimeError(f"claude exited {result.returncode}: {result.stderr[:500]}")

    return result.stdout.strip()


def send_slack_dm(user_id: str, message: str) -> None:
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        raise RuntimeError("SLACK_BOT_TOKEN is not set")

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"channel": user_id, "text": message, "unfurl_links": False},
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data.get('error')}")


def main():
    load_env()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    if not os.environ.get("SLACK_BOT_TOKEN"):
        print("ERROR: SLACK_BOT_TOKEN is not set — add it to .env or the environment", file=sys.stderr)
        sys.exit(1)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[{ts}] Searching for latest news...")

    try:
        news = search_news()
    except Exception as e:
        print(f"[{ts}] ERROR fetching news: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[{ts}] Sending to Tom Geurts ({TOM_GEURTS_SLACK_ID})...")

    try:
        send_slack_dm(TOM_GEURTS_SLACK_ID, news)
    except Exception as e:
        print(f"[{ts}] ERROR sending Slack message: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[{ts}] Done.")


if __name__ == "__main__":
    main()
