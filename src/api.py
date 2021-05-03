import pandas
import tweepy

from .graphs import show_daily_tweet_count, show_daily_tweet_user_count
from .rankings import (
    print_top_ff_ratio_close_to_one_user,
    print_top_ff_ratio_high_user,
    print_top_ff_ratio_low_user,
    print_top_followers_count_user,
    print_top_friends_count_user,
)
from .tweets import search_tweets


class TwiPlotlyAPI:
    def __init__(self, api_key, api_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self._api = tweepy.API(auth)
        self._df = None
        self._search_word = None
        self._search_query = None

    def search_tweets(self, search_word: str, search_query: str):
        tweets = search_tweets(
            api=self._api, search_query=search_word + " " + search_query
        )
        self._search_word = search_word
        self._search_query = search_query
        self._df = pandas.DataFrame(tweets)

    def show_daily_tweet_count(self):
        show_daily_tweet_count(self._df, search_word=self._search_word)

    def show_daily_tweet_user_count(self):
        show_daily_tweet_user_count(self._df, search_word=self._search_word)

    def print_top_tweet_count_user(self):
        show_daily_tweet_user_count(self._df, search_word=self._search_word)

    def print_top_followers_count_user(self, top: int = 10):
        print_top_followers_count_user(
            self._df,
            search_word=self._search_word,
            search_query=self._search_query,
            top=top,
        )

    def print_top_friends_count_user(self, top: int = 10):
        print_top_friends_count_user(
            self._df,
            search_word=self._search_word,
            search_query=self._search_query,
            top=top,
        )

    def print_top_ff_ratio_high_user(self, top: int = 10, min_followers_count: int = 0):
        print_top_ff_ratio_high_user(
            self._df,
            search_word=self._search_word,
            search_query=self._search_query,
            top=top,
            min_followers_count=min_followers_count,
        )

    def print_top_ff_ratio_low_user(self, top: int = 10, min_followers_count: int = 0):
        print_top_ff_ratio_low_user(
            self._df,
            search_word=self._search_word,
            search_query=self._search_query,
            top=top,
            min_followers_count=min_followers_count,
        )

    def print_top_ff_ratio_close_to_one_user(
        self, top: int = 10, min_followers_count: int = 0
    ):
        print_top_ff_ratio_close_to_one_user(
            self._df,
            search_word=self._search_word,
            search_query=self._search_query,
            top=top,
            min_followers_count=min_followers_count,
        )
