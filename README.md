# tweet-simulator
A twitter bot that uses markov chains to simulate tweets from any user.

Checkout [@sim\_tweet](https://www.twitter.com/sim_tweet) for the bot on twitter

Anybody is free to make a pull request to add functionality. If you have an idea but don't want to implement it feel free to open an issue too. Check CONTRIBUTING.md for more details.

## Implementation

The bot uses [Tweepy](https://www.tweepy.org/) to access the Twitter API.

It looks for mentions on twitter. Valid tweets it will respond to are where the tweet includes @sim\_tweet and @username (where @username is the username of the user to be mimicked).

The bot gets the users last 200 tweets and builds a markov chain of each space separated word appearing in their previous tweets (words except @mentions and t.co links). The bot then uses that markov chain to create a new tweet that looks like something the user might write.

You can email me at [tom@bowdens.me](mailto://tom@bowdens.me) if you have any questions about the implemenation or contributing, but I'll probably respond sooner if you create an issue.
