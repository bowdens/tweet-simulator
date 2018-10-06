import tweepy
from src.tweet_creator import create_tweet, parse_tweet

class StreamListener(tweepy.StreamListener):
    def __init__(self, bot_name, api, send_tweets=True, verbose=False):
        super().__init__()
        self.send_tweet=send_tweets
        self.verbose=verbose
        self.bot_name = bot_name
        self.api = api

    def on_status(self, status):
        if self.verbose:
            print("Got tweet: {}".format(status.text))

        # parse the tweet
        reply_name, targets, tweetID = parse_tweet(status, self.bot_name)

        if len(targets) == 0:
            # don't send tweet
            if self.verbose:
                print("No targets found in tweet!")
        else:
            # send the tweet
            create_tweet(
                    self.api,
                    tweetID,
                    reply_name,
                    targets[0],
                    send_tweet=self.send_tweet,
                    verbose=self.verbose
                    )

    def on_error(self, status_code):
        if status_code == 420:
            # disconnect
            print("disconnected from stream!")
            return False
