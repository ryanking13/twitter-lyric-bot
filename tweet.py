import config
import twitter

api = twitter.Api(
    consumer_key=config.TWITTER_CONSUMER_KEY,
    consumer_secret=config.TWITTER_CONSUMER_SECRET,
    access_token_key=config.TWITTER_ACCESS_TOKEN_KEY,
    access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
)


def post(message):
    api.PostUpdate(status=message)

