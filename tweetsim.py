#!/usr/bin/env python3

import tweepy, sys
from secret import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
import src.listener

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
bot_name = "@sim_tweet"
debug = False

if "--debug" in sys.argv:
    print("Entering debugging mode (will not send tweets)")
    debug = True

listener = src.listener.StreamListener(bot_name, api, send_tweets=(not debug), verbose=debug)
stream = tweepy.Stream(auth=api.auth, listener=listener)
stream.filter(track=[bot_name], async=False)
