import os

TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY") or ""
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET") or ""
TWITTER_ACCESS_TOKEN_KEY = os.environ.get("TWITTER_ACCESS_TOKEN_KEY") or ""
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET") or ""

GITHUB_ACCESS_KEY = os.environ.get("GITHUB_ACCESS_KEY") or ""
GITHUB_REPO_URL = "ryanking13/twitter-lyric-bot"
GITHUB_ISSUE_ID = 7
TWEET_LENGTH_LIMIT = 140

DEBUG = bool(os.environ.get("LYRIC_BOT_DEBUG") or "")
