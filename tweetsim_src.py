from markov import Markov
from datetime import datetime
import threading, pickle, os, tweepy

def run_bot(api, repeat, debug=False, name="@MimicRobot"):
    threading.Timer(repeat, run_bot, [api,repeat]).start()
    seen_tweets = read_seen_tweets("seen_tweets.bin")
    mentions = collect_mentions(api, seen_tweets, name)
    print("\n{}: Collected {} tweets".format(datetime.now().strftime("%c"), len(mentions)))
    for tweet in mentions:
        res = parse_tweet(tweet, name)
        print("Tweet parsed from {}. Text reads \"{}\". Targets are {}".format(res["reply_name"], tweet.full_text, res["targets"]))
        targets = res["targets"]
        for target in targets:
            create_tweet(api,res["replyID"],res["reply_name"], target, send_tweet = not debug)
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

def collect_mentions(api,seen_tweets, name):
    return_mentions = []
    for mention in tweepy.Cursor(api.search, q=name, tweet_mode='extended').items(10):
        if mention.id not in seen_tweets and mention.user.id != "1010567287701553152" and mention.in_reply_to_status_id == None:
            # not a seen tweet and the user sending it isnt ME (@MimicRobot)
            return_mentions.append(mention)
            seen_tweets.append(mention.id)
    return return_mentions

def parse_tweet(tweet, name):
    reply_name = tweet.user.screen_name
    text = tweet.full_text
    targets = []
    for word in text.split():
        if word[0] == '@' and word != name:
            targets.append(word)
            break # ONLY ALLOWS 1 TWEET AT A TIME

    return {"reply_name" : reply_name, "targets" : targets, "replyID" : tweet.id}

def create_tweet(api,reply_id,reply_name, target, send_tweet=True):
    print("Creating a tweet in response to @{} about @{}".format(reply_name, target))
    all_tweets = get_all_tweets(api,target)
    if len(all_tweets) == 0:
        tweet_text = "@{}\nSorry! I couldn't find any of {}'s tweets! Try again with a different user".format(reply_name,target)
    else:
        markov = Markov()
        for tweet in all_tweets:
            markov.add_sentence(tweet.full_text)
        reply_text = markov.create_sentence()
        tweet_prefix = "@{}\n{} says:\n".format(reply_name,target[1:])
        while(len(reply_text) > 240 - len(tweet_prefix)):
            reply_text = markov.create_sentence()

        tweet_text = tweet_prefix + reply_text
    if send_tweet == True:
        try:
            api.update_status(tweet_text, in_reply_to_status_id=reply_id)
        except Exception as e:
            print("\terror with the following tweet: {}".format(e))
        print("\tTweeted \n\"{}\"\n to \"{}\" in response to tweet #{}\n".format(tweet_text, target, reply_id))
    else:
        print("\tDID NOT tweet \n\"{}\"\n to \"{}\" in response to tweet #{}\n".format(tweet_text, target, reply_id))


def get_all_tweets(api,target):
    try:
        tweets = api.user_timeline(screen_name=target, count=100, include_rts=False, tweet_mode="extended")
        return tweets
    except:
        return []
