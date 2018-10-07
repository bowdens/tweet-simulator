# Contributing to tweet-simulator

If you want to contribute, you can fork the repo, commit your changes, then create a pull request. I'll go through it and if I think it's good, I'll merge it, otherwise I'll leave a comment explaining what you can fix up, or why your changes won't be added.

I've opened this repo up in time for [Hacktoberfest](https://hacktoberfest.digitalocean.com/) so hopefully it's good for beginners to contribute to.

You can check the issues to see if any are open. I'll add some with functionality to be added, and if you think of any functionality to be added you can create an issue too (or just implement it yourself and create a PR).

If you want to use what you've created on a live twitter account, you'll need to create a secret.py in the root folder which specifies CONSUMER\_KEY, CONSUMER\_SECRET, ACCESS\_KEY, and ACCESS\_SECRET which are part of the twitter API. It should look something like this:

```python
CONSUMER_KEY = "your consumer key"
CONSUMER_SECRET = "your consumer secret"
ACCESS_KEY = "your access key"
ACCESS_SECRET = "your access secret"
```

You'll also need to change the `bot_name` in `tweetsim.py` to whatever your bot's username on twitter is.

Run the bot with `python3 tweetsim.py` in the root folder. Use the `--debug` flag to turn off actually sending out the tweets.
