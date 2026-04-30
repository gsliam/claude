#!/bin/bash
# Daily 4pm news update for Tom Geurts

cd /home/user/claude

/opt/node22/bin/claude --dangerously-skip-permissions -p "Search for the latest news from today relevant to the following topics and send a concise summary to Tom Geurts via Slack DM (user_id: UUSM9N0MD).

Topics to cover:
1. Client news (mergers, acquisitions, new launches, notable news): HEMA, Amazon Prime Video, New York Pizza, Vodafone, Picnic, LEGO, Marktplaats, Unilever - Axe, Signal (Unilever), Samsung, JBL (Harman), KLM, The Social Hub, Etos, Zeeman, Andrelon (Unilever), Vaseline (Unilever), Hello Fresh, SharkNinja, OLA / Magnum
2. Social media news
3. AI news
4. TikTok Shop / social commerce news

Format the Slack message with clear sections and bullet points. Keep it concise — max 3 items per section. Only include news from today."
