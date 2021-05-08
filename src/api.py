import logging

import pandas
import pytz
import tweepy

from .filters import filter_user
from .graphs import make_daily_tweet_users_graph, make_daily_tweets_graph
from .loggers import get_logger, set_logger_timezone
from .rankings import make_user_ranking, print_user_rankings
from .tweets import search_tweets
from .users import get_follower_ids, get_following_ids
from .validates import validate_tweet_exists

logger = get_logger(__name__, loglevel=logging.INFO)


class TwiVisAPI:
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
        set_logger_timezone(timezone)

    def search_tweets(self, search_word: str, advanced_query: str, limit: int = None):
        logger.info("=== search_tweets Start")
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
        logger.info(f"=== search_tweets End（合計{'{:,}'.format(len(tweets))}）")

    def set_followers(self, user_screen_name):
        logger.info("=== set_followers Start")
        follower_ids = get_follower_ids(
            api=self._api, user_screen_name=user_screen_name
        )
        self._df["follower"] = self._df.apply(
            lambda x: x.user_id in follower_ids, axis=1
        )
        logger.info(f"=== set_followers End（合計{'{:,}'.format(len(follower_ids))}）")

    def set_following(self, user_screen_name):
        logger.info("=== set_following Start")
        following_ids = get_following_ids(
            api=self._api, user_screen_name=user_screen_name
        )
        self._df["following"] = self._df.apply(
            lambda x: x.user_id in following_ids, axis=1
        )
        logger.info(f"=== set_following End（合計{'{:,}'.format(len(following_ids))}）")

    def make_daily_tweets_graph(self, **kwargs):
        validate_tweet_exists(self._df)
        _df = filter_user(self._df, **kwargs)
        figure = make_daily_tweets_graph(
            _df, search_word=self._search_word, timezone=self._timezone
        )
        figure.show()

    def make_daily_tweet_users_graph(self, **kwargs):
        validate_tweet_exists(self._df)
        _df = filter_user(self._df, **kwargs)
        figure = make_daily_tweet_users_graph(
            _df, search_word=self._search_word, timezone=self._timezone
        )
        figure.show()

    def make_tweets_user_ranking(self, **kwargs):
        validate_tweet_exists(self._df)
        rankings = make_user_ranking(
            self._df,
            search_query=self._search_query,
            col="tweets_count",
            ascending=False,
            **kwargs,
        )
        print_user_rankings(rankings, ranking_name="tweets_user_ranking")

    def make_followers_user_ranking(self, **kwargs):
        validate_tweet_exists(self._df)
        rankings = make_user_ranking(
            self._df,
            search_query=self._search_query,
            col="followers_count",
            ascending=False,
            **kwargs,
        )
        print_user_rankings(rankings, ranking_name="followers_user_ranking")

    def make_friends_user_ranking(self, **kwargs):
        validate_tweet_exists(self._df)
        rankings = make_user_ranking(
            self._df,
            search_query=self._search_query,
            col="friends_count",
            ascending=False,
            **kwargs,
        )
        print_user_rankings(rankings, ranking_name="friends_user_ranking")

    def make_ff_ratio_user_ranking(self, **kwargs):
        validate_tweet_exists(self._df)
        rankings = make_user_ranking(
            self._df,
            search_query=self._search_query,
            col="ff_ratio",
            **kwargs,
        )
        print_user_rankings(
            rankings, value_fmt="{:.4f}", ranking_name="ff_ratio_user_ranking"
        )

    def make_ff_ratio_close_to_one_user_ranking(self, **kwargs):
        validate_tweet_exists(self._df)
        rankings = make_user_ranking(
            self._df,
            search_query=self._search_query,
            col="ff_ratio_close_to_one",
            ascending=True,
            **kwargs,
        )
        print_user_rankings(
            rankings,
            value_fmt="{:.4f}",
            ranking_name="ff_ratio_close_to_one_user_ranking",
        )

    def print_last_tweeted_time(self):
        print(
            f"last tweeted time: {self._df.tweeted_dt.max().strftime('%Y/%-m/%-d %-H:%M:%S')}"
        )
