from .errors import TweetNotFoundError


def validate_tweet_exists(df):
    if df.empty:
        raise TweetNotFoundError()
