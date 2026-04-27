#!/bin/bash
# Daily 4pm news share to Tom Geurts (UUSM9N0MD)

cd /home/user/claude

/opt/node22/bin/claude --dangerously-skip-permissions -p "
Search the web for today's top news across these categories:
1. Social media news
2. AI / social AI news
3. TikTok Shop / social commerce news

Also check for any news today about these clients: HEMA, Amazon Prime Video, New York Pizza, Vodafone, Picnic, LEGO, Marktplaats, Unilever, Samsung, JBL, KLM, The Social Hub, Etos, Zeeman, HelloFresh, SharkNinja, OLA / Magnum.

Then send a Slack DM to Tom Geurts (user_id: UUSM9N0MD) with a concise summary. Format it as:
*Daily News - $(date +%d/%m/%Y) 🗞️*

*Top Social/AI/Commerce News:*
• [bullet points]

*Client News (if any):*
• [bullet points, or 'Nothing notable today' if none]

Keep it brief and scannable. Send it now via Slack DM.
" 2>&1 | tee -a /home/user/claude/logs/daily-news-tom.log
