#!/usr/bin/env python3

import tweepy, sys
from secret import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
import src.listener

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
bot_name = "@sim_tweet"
creator_name = "@bo_wd_en"
debug = False

if "--debug" in sys.argv:
    print("Entering debugging mode (will not send tweets)")
    debug = True

listener = src.listener.StreamListener(bot_name, api, send_tweets=(not debug), verbose=debug)
stream = tweepy.Stream(auth=api.auth, listener=listener)

try:
    stream.filter(track=[bot_name], async=False)
except Exception as e:
    api.send_direct_message(creator_name, "{} broke with the following exception: {}".format(bot_name, e))

