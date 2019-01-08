#!/usr/bin/env python3

import tweepy, sys
import time
from secret import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
import src.listener
from log import FileLog

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
bot_name = "@sim_tweet"
creator_name = "@bo_wd_en"
debug = False
log = FileLog()

def send_error_dm(msg):
    # api.send_direct_message(creator_name, msg)
    # api.send_direct_message is broken... just pass for now
    pass

if "--debug" in sys.argv:
    print("Entering debugging mode (will not send tweets)")
    debug = True

listener = src.listener.StreamListener(bot_name, api, log, send_tweets=(not debug), verbose=debug)
stream = tweepy.Stream(auth=api.auth, listener=listener)

streaming = True

while streaming:
    try:
        log.log("Starting to stream")
        stream.filter(track=[bot_name], async=False)
    except Exception as e:
        msg="{} broke with the following exception: {}".format(bot_name, e)
        log.log(msg)
        sent = False
        while sent is False:
            try:
                log.log("attempting to reconnect")
                send_error_dm(msg)
                sent = True
            except Exception as e:
                # wait 30 seconds
                log.log("error: {}".format(e))
                log.log("waiting 30 seconds before trying again...")
                time.sleep(30)
            else:
                sent = True
        log.log("starting to stream again...")


