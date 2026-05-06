#!/bin/bash
set -euo pipefail

cd /home/user/claude

claude --print "Search the web for the latest top 3 news items from today about social media, AI, TikTok Shop, and social commerce. Then send a Slack DM to Tom Geurts (Slack user ID: UUSM9N0MD) with a concise, well-formatted message containing those 3 news items as bullet points with a short summary for each. Start the message with 'Hey Tom, here are today's top news items:'"
