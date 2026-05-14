#!/bin/bash
# Daily 4pm news share to Tom Geurts (UUSM9N0MD)
cd /home/user/claude
/opt/node22/bin/claude --dangerously-skip-permissions -p "Search for today's top news across these topics: social media, AI, TikTok Shop, social commerce. Also check for any news about these clients: HEMA, Amazon Prime Video, New York Pizza, Vodafone, Picnic, LEGO, Marktplaats, Unilever, Samsung, JBL, KLM, The Social Hub, Etos, Zeeman, HelloFresh, SharkNinja, OLA/Magnum. Only include news from today or yesterday. Then send a Slack DM to Tom Geurts (user ID: UUSM9N0MD) with a concise summary of the top news — max 3 items per category. Format it clearly with sections: Client News and Industry News (social/AI/TikTok Shop/social commerce)." 2>&1
