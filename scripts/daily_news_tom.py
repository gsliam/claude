#!/usr/bin/env python3
"""Fetch the latest social/AI/TikTok/social-commerce news and DM Tom Geurts on Slack."""

import os
import json
from datetime import date
import anthropic
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_USER_ID = "UUSM9N0MD"  # Tom Geurts

NEWS_PROMPT = f"""Today is {date.today().strftime('%d %B %Y')}.

Search the web for the LATEST news (today or yesterday only) across these topics:
1. Social media platform news (Instagram, TikTok, YouTube, LinkedIn, X/Twitter)
2. AI / generative AI news relevant to marketing and content
3. TikTok Shop / social commerce updates
4. Social media advertising and brand news

Return ONLY news from the last 48 hours. For each item provide:
- A short headline
- 1-sentence summary
- Source name

Format your response as a clean Slack message with sections. Use *bold* for headlines.
Keep it concise — max 5 items total, most impactful first.
Start with: *Latest News — {date.today().strftime('%d %b %Y')}* 🗞️
"""


def fetch_news(client: anthropic.Anthropic) -> str:
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": NEWS_PROMPT}],
    )

    # Extract the final text response
    for block in reversed(response.content):
        if block.type == "text":
            return block.text

    # If no text block in final response, do a follow-up to get summary
    messages = [
        {"role": "user", "content": NEWS_PROMPT},
        {"role": "assistant", "content": response.content},
        {"role": "user", "content": "Please provide the formatted news summary now."},
    ]
    follow_up = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        messages=messages,
    )
    return follow_up.content[0].text


def send_to_slack(message: str, slack_token: str) -> None:
    slack = WebClient(token=slack_token)
    try:
        result = slack.chat_postMessage(channel=SLACK_USER_ID, text=message, mrkdwn=True)
        print(f"Message sent, ts={result['ts']}")
    except SlackApiError as e:
        raise RuntimeError(f"Slack error: {e.response['error']}") from e


def main() -> None:
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    slack_token = os.environ.get("SLACK_BOT_TOKEN")

    if not anthropic_key:
        raise EnvironmentError("ANTHROPIC_API_KEY is not set")
    if not slack_token:
        raise EnvironmentError("SLACK_BOT_TOKEN is not set")

    print("Fetching latest news via Claude...")
    client = anthropic.Anthropic(api_key=anthropic_key)
    news_message = fetch_news(client)

    print("Sending to Tom Geurts on Slack...")
    send_to_slack(news_message, slack_token)
    print("Done.")


if __name__ == "__main__":
    main()
