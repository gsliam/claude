#!/bin/bash
# Sends daily 4pm news digest to Tom Geurts via Slack DM.
# Runs via cron at 14:00 UTC (= 16:00 Amsterdam CEST).

set -euo pipefail

LOG_FILE="/home/user/claude/scripts/news_to_tom.log"
CLAUDE_BIN="/opt/node22/bin/claude"
PROJECT_DIR="/home/user/claude"

echo "=== $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" >> "$LOG_FILE"

cd "$PROJECT_DIR"

PROMPT="Today's date is $(date '+%Y-%m-%d'). Your task: search the web for the latest news from today and yesterday, then send a Slack DM to Tom Geurts (Slack user_id: UUSM9N0MD).

Search for news in two categories:
1. CLIENT NEWS — Any notable news (launches, campaigns, mergers, layoffs, controversies, takeovers) about these brands: HEMA, Amazon Prime Video, New York Pizza, Vodafone, Picnic, LEGO, Marktplaats, Unilever (including Axe / Signal / Andrelon / Vaseline), Samsung, JBL (Harman), KLM, The Social Hub, Etos, Zeeman, HelloFresh, SharkNinja, OLA / Magnum.
2. INDUSTRY NEWS — Top 3 stories from: social media, social AI, AI, TikTok Shop, social commerce.

Then send Tom the digest via Slack DM. Format the message with clear sections and bullet points. Keep it concise and scannable. Sign off as 'Your daily 4pm news update'."

"$CLAUDE_BIN" -p "$PROMPT" \
  --allowedTools "mcp__Slack__slack_send_message,mcp__Slack__slack_search_users,WebSearch,WebFetch" \
  2>> "$LOG_FILE"

echo "Done." >> "$LOG_FILE"
