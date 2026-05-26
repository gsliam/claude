"""
Fetches latest social/AI/client news and sends a daily digest to Tom Geurts via Slack DM.
Runs daily at 16:00 Amsterdam time via GitHub Actions.

Required secrets: ANTHROPIC_API_KEY, SLACK_BOT_TOKEN, BRAVE_API_KEY
"""

import os
import sys
import requests
from datetime import datetime
import anthropic

TOM_SLACK_ID = "UUSM9N0MD"

CLIENT_WATCHLIST = [
    "HEMA", "Amazon Prime Video", "New York Pizza", "Vodafone", "Picnic",
    "LEGO", "Marktplaats", "Unilever", "Axe", "Signal", "Samsung", "JBL",
    "KLM", "The Social Hub", "Etos", "Zeeman", "Andrelon", "Vaseline",
    "HelloFresh", "SharkNinja", "OLA", "Magnum",
]

SEARCH_QUERIES = [
    "TikTok social commerce AI marketing news today",
    "social media AI news today",
    f"{' OR '.join(CLIENT_WATCHLIST[:8])} news today Netherlands",
    f"{' OR '.join(CLIENT_WATCHLIST[8:])} news today",
]


def search_news(query: str, brave_api_key: str) -> list[dict]:
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": brave_api_key,
    }
    params = {"q": query, "count": 5, "freshness": "pd"}
    try:
        resp = requests.get(
            "https://api.search.brave.com/res/v1/news/search",
            headers=headers,
            params=params,
            timeout=10,
        )
        if resp.status_code == 200:
            return [
                {
                    "title": r["title"],
                    "description": r.get("description", ""),
                    "url": r["url"],
                }
                for r in resp.json().get("results", [])
            ]
    except requests.RequestException:
        pass
    return []


def send_slack_dm(token: str, user_id: str, message: str) -> bool:
    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"channel": user_id, "text": message, "mrkdwn": True},
        timeout=10,
    )
    result = resp.json()
    if not result.get("ok"):
        print(f"Slack error: {result.get('error')}", file=sys.stderr)
    return result.get("ok", False)


def format_digest_with_claude(client: anthropic.Anthropic, articles: list[dict], today: str) -> str:
    news_text = "\n".join(
        f"- {a['title']}: {a['description']}" for a in articles[:20]
    )
    clients = ", ".join(CLIENT_WATCHLIST)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Format the following news into a clean Slack daily digest for Tom Geurts,
Technical Director at a social media marketing agency.

Date: {today}

Raw articles:
{news_text}

Rules:
- Header: "📰 *Daily News Digest — {today}*"
- Sections (include only if relevant articles exist):
  🤖 Social Media & AI
  🛍️ TikTok Shop & Social Commerce
  🎯 Client News (only for: {clients})
- Max 4 bullets per section, each starting with •
- Bold key names/numbers with *asterisks*
- Footer: "_Sent daily at 4pm by your AI assistant_"
- Use Slack markdown only (*bold*, _italic_, bullet •)
- Do not include URLs""",
            }
        ],
    )
    return response.content[0].text


def main():
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    slack_token = os.environ.get("SLACK_BOT_TOKEN", "")
    brave_key = os.environ.get("BRAVE_API_KEY", "")

    if not anthropic_key or not slack_token:
        print("Missing required env vars: ANTHROPIC_API_KEY, SLACK_BOT_TOKEN", file=sys.stderr)
        sys.exit(1)

    today = datetime.now().strftime("%d %B %Y")

    print("Fetching news...")
    articles = []
    for query in SEARCH_QUERIES:
        articles.extend(search_news(query, brave_key))

    if not articles:
        print("No articles fetched — check BRAVE_API_KEY", file=sys.stderr)
        sys.exit(1)

    print(f"Fetched {len(articles)} articles. Formatting with Claude...")
    client = anthropic.Anthropic(api_key=anthropic_key)
    message = format_digest_with_claude(client, articles, today)

    print("Sending to Tom Geurts on Slack...")
    ok = send_slack_dm(slack_token, TOM_SLACK_ID, message)

    if ok:
        print(f"✅ News digest sent to Tom Geurts ({today})")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
