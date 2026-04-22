#!/bin/bash
# Daily 4pm news briefing for Tom Geurts (UUSM9N0MD)

PROMPT="Search the web for today's latest news (focus on: social media, AI, TikTok Shop, social commerce, and client news for HEMA, Amazon Prime Video, New York Pizza, Vodafone, Picnic, LEGO, Marktplaats, Unilever, Samsung, JBL, KLM, The Social Hub, Etos, Zeeman, HelloFresh, SharkNinja, OLA/Magnum). Prioritise: new launches, mergers/takeovers, notable campaigns. Then send a concise summary message to Tom Geurts in Slack (user_id: UUSM9N0MD) with the top news items. Format with clear sections: Client News and Industry / Social / AI News."

/opt/node22/bin/claude --dangerously-skip-permissions -p "$PROMPT"
