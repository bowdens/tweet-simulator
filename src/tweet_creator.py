from src.markov import Markov
import html


def parse_tweet(tweet, name):
    # returns the reply_name, targets, and replyID
    reply_name = tweet.user.screen_name
    text = tweet.text
    targets = []
    for word in text.split():
        if word[0] == '@' and word != name:
            targets.append(word)
            break  # ONLY ALLOWS 1 TWEET AT A TIME
    return reply_name, targets, tweet.id


def create_tweet(api, reply_id, reply_name, target, log, send_tweet=True, verbose=False):
    if verbose:
        log.log("Creating a tweet in response to @{} about {}".format(reply_name, target))

    # get all the tweets
    all_tweets = get_all_tweets(api, target)
    if len(all_tweets) == 0:
        # can't create a tweet from nothing... send an error message in the tweet
        tweet_text = "@{}\nSorry! I couldn't find any of {}'s tweets! Try again with a different user".format(
            reply_name, target)
    else:
        # create a markov chain with all of the tweets, then use it to create the tweet
        markov = Markov()
        for tweet in all_tweets:
            # create list of words in tweet and remove disallowed ones
            words = tweet.split()
            # keep track of a list of all the items we need to remove
            # can't remove while iterating
            toRemove = []
            for word in words:
                # get rid of any t.co links (images)
                if "t.co" in word:
                    toRemove.append(word)
                # remove @ mentions
                if word[0] == '@':
                    toRemove.append(word)
            if verbose:
                log.log("removing {}".format(toRemove))
            for word in toRemove:
                words.remove(word)
            if verbose:
                log.log("adding words {} to markov".format(words))
            markov.add_words(words)

        reply_text = markov.create_sentence()
        tweet_prefix = "@{}\n{} says:\n".format(reply_name, target[1:])
        while (len(reply_text) > 240 - len(tweet_prefix)):
            reply_text = markov.create_sentence()
        tweet_text = tweet_prefix + reply_text
    if send_tweet:
        # send the tweet, print the error message if there is any
        try:
            api.update_status(tweet_text, in_reply_to_status_id=reply_id)
        except Exception as e:
            log.log("\terror sending the tweet: {}".format(e))

        log.log("\tTweeted \n\"{}\"\n to \"{}\" in response to tweet #{}\n".format(tweet_text, target, reply_id))
    else:
        if verbose:
            log.log(
                "\tDID NOT tweet \n\"{}\"\n to \"{}\" in response to tweet #{}\n".format(tweet_text, target, reply_id))


def get_all_tweets(api, target):
    try:
        tweets = api.user_timeline(screen_name=target, count=200, include_rts=False, tweet_mode="extended")
        decoded_tweets = [html.unescape(tweet.full_text) for tweet in tweets]
        return decoded_tweets
    except:
        return []
