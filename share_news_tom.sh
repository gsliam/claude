#!/bin/bash
# Daily 4pm news share to Tom Geurts (UUSM9N0MD) on Slack

cd /home/user/claude

/opt/node22/bin/claude -p "Search for the latest news today relevant to these topics and clients: social media, AI, TikTok Shop, social commerce, and any news about: HEMA, Amazon Prime Video, New York Pizza, Vodafone, Picnic, LEGO, Marktplaats, Unilever, Samsung, JBL, KLM, The Social Hub, Etos, Zeeman, HelloFresh, SharkNinja, OLA/Magnum. Then send a concise Slack DM to Tom Geurts (user_id: UUSM9N0MD) with the top news items from today. Format it clearly with sections for Client News and Industry News. Keep it brief and scannable." 2>&1
