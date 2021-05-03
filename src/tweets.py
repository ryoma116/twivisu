import time
from datetime import date, datetime, timedelta
from typing import Dict, List, Union

import tweepy

from .constants import FULL_TEXT_TWEET_MODE, JST, MAX_SEARCH_COUNT, TODAY_EXCLUDED
from .limits import get_search_limit_reset_time, is_search_limit
from .processors import make_weekday


def search_tweets(api: tweepy.API, search_query: str) -> List[Dict]:
    """ツイートを検索する

    :param api: tweepy.API
    :param search_query: 検索クエリ
    """

    print(f"===== Start =====")
    _now = datetime.now(JST)
    _today = _now.date()

    # TwitterAPIの無料プランで取得可能な一番古い日付は24時間分取得できていないため、日付軸分析、時間軸分析でノイズになり得る。
    # make_search_from_queryで分析対象から除外しておく。
    _query = search_query
    _query += " " + _make_search_from_query()
    if TODAY_EXCLUDED:
        # 当日除外が指定されていた場合はTo日付を指定
        _query += " " + _make_excluded_today_search_to_query()

    tweets = []
    next_max_tweet_id = None
    while True:
        _tweets = []
        try:
            _tweets = api.search(
                q=search_query,
                tweet_mode=FULL_TEXT_TWEET_MODE,
                count=MAX_SEARCH_COUNT,
                max_id=next_max_tweet_id,
            )
        except tweepy.RateLimitError:
            print("アクセス上限のため処理休止中(15分)..")
            time.sleep(15 * 60)

        # 取得するツイートがなくなった場合に処理終了
        if len(_tweets) == 0:
            break

        if is_search_limit(api):
            reset_time = get_search_limit_reset_time(api)
            print(f"アクセス上限のため処理休止中({reset_time}秒)..")
            time.sleep(reset_time)

        for t in _tweets:
            dt = _convert_utc_to_jst(t.created_at)
            tweets.append(
                {
                    "tweeted_dt": dt,
                    "tweeted_date": dt.date(),
                    "tweeted_weekday": make_weekday(dt),
                    "tweeted_hour": dt.strftime("%H"),
                    "tweet_id": t.id,
                    "favorite_count": t.favorite_count,
                    "retweet_count": t.retweet_count,
                    "source": t.source,
                    "user_id": t.user.id,
                    "user_screen_name": t.user.screen_name,
                    "user_name": t.user.name,
                    "user_profile_image_url": t.user.profile_image_url_https,
                    "followers_count": t.user.followers_count,
                    "friends_count": t.user.friends_count,
                    "following": t.user.following,
                }
            )

        next_max_tweet_id = _tweets[-1].id - 1
        print(f"{'{:,}'.format(len(tweets))} 件取得")
        time.sleep(1)

    print(f"===== End（合計{'{:,}'.format(len(tweets))}） =====")
    return tweets


def _make_search_from_query() -> str:
    """検索日付のFromに指定するクエリを生成する

    TwitterAPIの無料プランでは8日前のツイートも取得できるが、
    24時間分は取得できていないため、分析対象から除外する。

    :return 検索日付From形式の文字列
    """
    _dt = datetime.now(JST) - timedelta(days=7)
    return _convert_search_period_query_format(_dt.date())


def _make_excluded_today_search_to_query() -> str:
    """当日除外用に検索日付のToに指定するクエリを生成する

    当日のツイートは24時間分は取得できていないため、
    ユーザから指定された場合のみ、分析対象から除外する。

    :return 検索日付To形式の文字列
    """
    _today = datetime.now(JST).date()
    return _convert_search_period_query_format(_today)


def _convert_search_period_query_format(dt: Union[datetime, date]) -> str:
    """検索日付のFrom/Toに指定する形式の文字列を生成する

    :param dt: datetime or date
    :return 検索日付From形式の文字列
    """
    return dt.strftime("since:%Y-%m-%d_%H:%M:%S_JST")


def _convert_utc_to_jst(dt: datetime) -> datetime:
    """UTC時間をJST時間に変更

    Twitter APIから取得した時間はtimestamp

    :param dt: datetime(UTC)
    :return datetime(JST)
    """
    return dt + timedelta(hours=9)
