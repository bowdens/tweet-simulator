#!/usr/bin/env python3

import tweepy, sys
from tweetsim_src import run_bot
from secret import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

if "--debug" in sys.argv:
    print("Entering debugging mode (will not send tweets)")
    run_bot(api, 60.0, debug=True, name="@MimicRobot")
else:
    run_bot(api, 60.0, name="@MimicRobot")

