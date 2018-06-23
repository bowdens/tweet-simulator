from markov import Markov
from datetime import datetime
import threading, pickle, os

def run_bot(api, repeat):
    threading.Timer(repeat, run_bot, [api,repeat]).start()
    seen_tweets = read_seen_tweets("seen_tweets.bin")
    mentions = collect_mentions(api, seen_tweets)
    print("{}: Collected {} tweets".format(datetime.now().strftime("%c"), len(mentions)))
    for tweet in mentions:
        res = parse_tweet(tweet)
        print("Tweet parsed from {}. Text reads \"{}\". Targets are {}".format(res["name"], tweet.text, res["targets"]))
        targets = res["targets"]
        for target in targets:
            create_tweet(api,res["replyID"],res["name"], target)
    save_seen_tweets("seen_tweets.bin", seen_tweets)

def read_seen_tweets(location):
    if not os.path.isfile(location):
        return []
    with open(location, "rb") as inp:
        tweets = []
        tweets = pickle.load(inp)
        return tweets

def save_seen_tweets(location, tweets):
    with open(location, "wb") as output:
        pickle.dump(tweets, output, pickle.HIGHEST_PROTOCOL)

def collect_mentions(api,seen_tweets):
    mentions = api.search(q="@TweetSim")
    return_mentions = []
    for mention in mentions:
        if mention.id not in seen_tweets and mention.user.id != "1010431060583202817" and mention.in_reply_to_status_id == None:
            # not a seen tweet and the user sending it isnt ME (tweetSim)
            return_mentions.append(mention)
            seen_tweets.append(mention.id)
    return return_mentions

def parse_tweet(tweet):
    name = tweet.user.screen_name
    text = tweet.text
    targets = []
    for word in text.split():
        if word[0] == '@' and word != '@TweetSim':
            targets.append(word)

    return {"name" : name, "targets" : targets, "replyID" : tweet.id}

def create_tweet(api,reply_id,reply_name, target):
    all_tweets = get_all_tweets(api,target)
    markov = Markov()
    for tweet in all_tweets:
        markov.add_sentence(tweet.text)
    reply_text = markov.create_sentence()
    tweet_prefix = "@{}\n{} says:\n".format(reply_name,target[1:])
    while(len(reply_text) > 240 - len(tweet_prefix)):
        reply_text = markov.create_sentence()

    tweet_text = tweet_prefix + reply_text
    api.update_status(tweet_text, in_reply_to_status_id=reply_id)
    print("Tweeted \"{}\" to \"{}\" in response to tweed #{}".format(tweet_text, target, reply_id))

def get_all_tweets(api,target):
    tweets = api.user_timeline(screen_name=target, count=100, include_rts=False)
    return tweets

