#!/bin/bash
# Daily 4pm news share for Tom Geurts (UUSM9N0MD)

PROMPT="Search the web for the latest news from today and yesterday covering: \
(1) social media, AI, TikTok Shop, and social commerce trends, \
(2) news about these clients: HEMA, Amazon Prime Video, New York Pizza, Vodafone, Picnic, LEGO, Marktplaats, Unilever, Samsung, JBL, KLM, The Social Hub, Etos, Zeeman, HelloFresh, SharkNinja, OLA/Magnum. \
Focus on notable launches, mergers, takeovers, and campaigns. \
Then send a clean, concise Slack DM to Tom Geurts (user_id: UUSM9N0MD) with a brief news summary — \
max 3 items per client, only yesterday/today news. \
Format it with clear sections: *Client News* and *Industry & Social/AI News*."

/opt/node22/bin/claude --dangerously-skip-permissions -p "$PROMPT"
