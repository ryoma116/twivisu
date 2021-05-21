from dataclasses import dataclass

import tweepy


@dataclass
class TwitterAuthKeys:
    api_key: str
    api_secret: str
    access_token: str
    access_token_secret: str


def auth_twitter_api(auth_keys: TwitterAuthKeys):
    _auth = tweepy.OAuthHandler(auth_keys.api_key, auth_keys.api_secret)
    _auth.set_access_token(auth_keys.access_token, auth_keys.access_token_secret)
    return tweepy.API(
        _auth,
        retry_count=10,
        retry_delay=60,
        wait_on_rate_limit=True,
        timeout=120,
        wait_on_rate_limit_notify=True,
    )
