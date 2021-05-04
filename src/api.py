import pandas
import pytz
import tweepy

from .constants import FfRatioOrderModes
from .errors import ParameterError
from .graphs import make_daily_tweet_users_graph, make_daily_tweets_graph
from .rankings import (
    make_close_to_one_ff_ratio_user_ranking,
    make_followers_user_ranking,
    make_friends_user_ranking,
    make_high_ff_ratio_user_ranking,
    make_low_ff_ratio_user_ranking,
    make_tweets_user_ranking,
)
from .tweets import search_tweets
from .validates import validate_tweet_exists


class TwiVisuAPI:
    def __init__(
        self, api_key, api_secret, access_token, access_token_secret, timezone="UTC"
    ):
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self._api = tweepy.API(auth)
        self._df = None
        self._search_word = None
        self._search_query = None
        self._timezone = pytz.timezone(timezone)

    def search_tweets(self, search_word: str, advanced_query: str, limit: int = None):
        search_query = search_word + " " + advanced_query
        tweets = search_tweets(
            api=self._api,
            search_query=search_query,
            limit=limit,
            timezone=self._timezone,
        )
        self._search_word = search_word
        self._search_query = search_query
        self._df = pandas.DataFrame(tweets)

    def make_daily_tweets_graph(self):
        validate_tweet_exists(self._df)
        make_daily_tweets_graph(
            self._df, search_word=self._search_word, timezone=self._timezone
        )

    def make_daily_tweet_users_graph(self):
        validate_tweet_exists(self._df)
        make_daily_tweet_users_graph(
            self._df, search_word=self._search_word, timezone=self._timezone
        )

    def make_tweets_user_ranking(self, top: int = 10):
        validate_tweet_exists(self._df)
        make_tweets_user_ranking(
            self._df,
            search_word=self._search_word,
            search_query=self._search_query,
            top=top,
        )

    def make_followers_user_ranking(self, top: int = 10):
        validate_tweet_exists(self._df)
        make_followers_user_ranking(
            self._df,
            search_word=self._search_word,
            search_query=self._search_query,
            top=top,
        )

    def make_friends_user_ranking(self, top: int = 10):
        validate_tweet_exists(self._df)
        make_friends_user_ranking(
            self._df,
            search_word=self._search_word,
            search_query=self._search_query,
            top=top,
        )

    def make_ff_ratio_user_ranking(
        self,
        order_mode: str = FfRatioOrderModes.HIGH,
        top: int = 10,
        min_followers_count: int = 0,
    ):
        validate_tweet_exists(self._df)
        if order_mode == FfRatioOrderModes.HIGH:
            make_high_ff_ratio_user_ranking(
                self._df,
                search_word=self._search_word,
                search_query=self._search_query,
                top=top,
                min_followers_count=min_followers_count,
            )

        elif order_mode == FfRatioOrderModes.LOW:
            make_low_ff_ratio_user_ranking(
                self._df,
                search_word=self._search_word,
                search_query=self._search_query,
                top=top,
                min_followers_count=min_followers_count,
            )

        elif order_mode == FfRatioOrderModes.CLOSE_TO_ONE:
            make_close_to_one_ff_ratio_user_ranking(
                self._df,
                search_word=self._search_word,
                search_query=self._search_query,
                top=top,
                min_followers_count=min_followers_count,
            )

        else:
            ParameterError(
                "Please select a valid choice for order_mode. (high, low, close_to_one)"
            )
