"""
Fetch latest industry news and send a curated digest to Tom Geurts via Slack DM.
Requires env vars: ANTHROPIC_API_KEY, SLACK_BOT_TOKEN
"""

import os
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
import anthropic

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
TOM_SLACK_USER_ID = "UUSM9N0MD"

RSS_FEEDS = [
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("VentureBeat AI", "https://venturebeat.com/ai/feed/"),
    ("Social Media Today", "https://www.socialmediatoday.com/rss.xml"),
    ("Marketing Week", "https://www.marketingweek.com/feed/"),
    ("Adweek", "https://www.adweek.com/feed/"),
    ("Digiday", "https://digiday.com/feed/"),
]

CLIENT_KEYWORDS = [
    "HEMA", "Amazon Prime Video", "New York Pizza", "Vodafone", "Picnic",
    "LEGO", "Marktplaats", "Unilever", "Axe", "Signal", "Samsung", "JBL",
    "Harman", "KLM", "Social Hub", "Etos", "Zeeman", "Andrelon", "Vaseline",
    "HelloFresh", "SharkNinja", "OLA", "Magnum",
]

TOPIC_KEYWORDS = [
    "AI", "artificial intelligence", "TikTok", "social commerce", "social media",
    "influencer", "creator economy", "ChatGPT", "generative AI", "Instagram",
    "Meta", "marketing", "advertising", "social AI",
]


def fetch_rss(name: str, url: str, max_age_hours: int = 24) -> list[dict]:
    items = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read())
    except Exception as e:
        print(f"  [warn] {name}: {e}")
        return items

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall(".//item") or root.findall(".//atom:entry", ns)
    for entry in entries[:20]:
        title_el = entry.find("title")
        link_el = entry.find("link")
        desc_el = entry.find("description") or entry.find("summary")
        pub_el = entry.find("pubDate") or entry.find("published") or entry.find("atom:published", ns)

        title = title_el.text.strip() if title_el is not None and title_el.text else ""
        link = link_el.text.strip() if link_el is not None and link_el.text else ""
        if not link and link_el is not None:
            link = link_el.get("href", "")
        desc = desc_el.text or "" if desc_el is not None else ""
        # Strip HTML tags from description
        import re
        desc = re.sub(r"<[^>]+>", "", desc).strip()[:300]

        if not title:
            continue

        # Parse publish date if available
        if pub_el is not None and pub_el.text:
            try:
                from email.utils import parsedate_to_datetime
                pub_dt = parsedate_to_datetime(pub_el.text.strip())
                if pub_dt.tzinfo is None:
                    pub_dt = pub_dt.replace(tzinfo=timezone.utc)
                if pub_dt < cutoff:
                    continue
            except Exception:
                pass  # Keep item if we can't parse the date

        items.append({"source": name, "title": title, "link": link, "desc": desc})

    return items


def is_relevant(item: dict) -> bool:
    text = (item["title"] + " " + item["desc"]).lower()
    for kw in CLIENT_KEYWORDS + TOPIC_KEYWORDS:
        if kw.lower() in text:
            return True
    return False


def curate_with_claude(items: list[dict]) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    articles_text = "\n".join(
        f"[{i+1}] ({item['source']}) {item['title']}\n    {item['desc']}\n    {item['link']}"
        for i, item in enumerate(items[:60])
    )

    today = datetime.now(timezone(timedelta(hours=2))).strftime("%A %d %B %Y")

    prompt = f"""You are preparing a daily news digest for Tom Geurts, Technical Director at Gospooky — a social media & creative agency in Amsterdam.

Today is {today}.

Select the 5–7 most relevant and interesting stories from the list below. Focus on:
- AI, generative AI, and social AI developments
- Social media platform news (TikTok, Instagram, Meta, YouTube)
- Social commerce and TikTok Shop
- News about any of these clients: HEMA, Amazon Prime Video, New York Pizza, Vodafone, Picnic, LEGO, Marktplaats, Unilever, Samsung, JBL, KLM, Etos, Zeeman, HelloFresh, SharkNinja, OLA/Magnum
- Marketing, advertising, and creator economy

Format as a clean Slack message using these guidelines:
- Start with: *Latest News for {today}* 📰
- For each story: bold the title, include the source in brackets, one sentence summary, and the link
- Group by theme if there are clear clusters
- End with a short sign-off line (friendly, brief)

Articles:
{articles_text}

Return only the formatted Slack message text, no extra commentary."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def get_or_open_dm(user_id: str) -> str:
    data = json.dumps({"users": user_id}).encode()
    req = urllib.request.Request(
        "https://slack.com/api/conversations.open",
        data=data,
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if not result.get("ok"):
        raise RuntimeError(f"conversations.open failed: {result.get('error')}")
    return result["channel"]["id"]


def send_slack_message(channel_id: str, text: str) -> None:
    data = json.dumps({"channel": channel_id, "text": text}).encode()
    req = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=data,
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if not result.get("ok"):
        raise RuntimeError(f"chat.postMessage failed: {result.get('error')}")
    print(f"Message sent to channel {channel_id}")


def main():
    print("Fetching news from RSS feeds...")
    all_items = []
    for name, url in RSS_FEEDS:
        items = fetch_rss(name, url)
        print(f"  {name}: {len(items)} items")
        all_items.extend(items)

    relevant = [item for item in all_items if is_relevant(item)]
    print(f"\nRelevant articles: {len(relevant)} / {len(all_items)}")

    if not relevant:
        # Fall back to all items if nothing matched keywords
        relevant = all_items

    print("Curating with Claude...")
    message_text = curate_with_claude(relevant)
    print("\n--- Message preview ---")
    print(message_text)
    print("---\n")

    print(f"Opening DM with Tom Geurts ({TOM_SLACK_USER_ID})...")
    channel_id = get_or_open_dm(TOM_SLACK_USER_ID)
    send_slack_message(channel_id, message_text)
    print("Done.")


if __name__ == "__main__":
    main()
