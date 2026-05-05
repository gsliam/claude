#!/bin/bash
# Daily news sender to Tom Geurts at 4pm Amsterdam time

CLAUDE_BIN="/opt/node22/bin/claude"
WORK_DIR="/home/user/claude"

cd "$WORK_DIR"

PROMPT='Search the web for the top 3-5 most important news stories from today in these categories: social media, AI, TikTok Shop, social commerce. Then send a Slack DM to user UUSM9N0MD (Tom Geurts) with the news in a clean, readable format. Start the message with "📰 *Latest News – $(date +"%d/%m/%Y, %H:%M")*" followed by the stories with a brief summary for each. Keep it concise and use bullet points.'

"$CLAUDE_BIN" --print --dangerously-skip-permissions -p "$PROMPT"
