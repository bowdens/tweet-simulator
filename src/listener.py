import tweepy
from src.tweet_creator import create_tweet, parse_tweet

class StreamListener(tweepy.StreamListener):
    def __init__(self, bot_name, api, log, send_tweets=True, verbose=False):
        super().__init__()
        self.send_tweet=send_tweets
        self.verbose=verbose
        self.bot_name = bot_name
        self.api = api
        self.log = log

    def on_status(self, status):
        self.log.log("Got tweet: {}".format(status.text))

        # parse the tweet
        reply_name, targets, tweetID = parse_tweet(status, self.bot_name)

        if len(targets) == 0:
            # don't send tweet
            if self.verbose:
                self.log.log("No targets found in tweet; not sending")
        else:
            # send the tweet
            create_tweet(
                    self.api,
                    tweetID,
                    reply_name,
                    targets[0],
                    self.log,
                    send_tweet=self.send_tweet,
                    verbose=self.verbose
                    )

    def on_error(self, status_code):
        if status_code == 420:
            # disconnect
            self.log.log("disconnected from stream! (status code 420)")
            return False
        else:
            self.log.log("Unhandled error in lisener: error {}".format(status_code))
