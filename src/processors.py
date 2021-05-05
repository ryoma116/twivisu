from datetime import datetime, timedelta
from typing import List

import pandas

from .constants import JA_WEEKDAYS, WEEKDAYS
from .utils import count_users


def make_tweet_user_weekday_max_hour_df(df: pandas.DataFrame) -> pandas.DataFrame:
    """1日複数回ツイートしたユーザを1カウントとするDataFrameを生成する

    ユーザが大量ツイートするとノイズになる。ノイズ除去のために使用。
    残すツイートは1日に多くツイートした時間としている。

    :param df: 対象のDataFrame
    :return 加工後のDataFrame
    """
    _cols = ["user_id", "tweeted_weekday", "tweeted_hour", "tweet_id"]
    _group_cols = ["user_id", "tweeted_weekday"]
    return df[_cols].groupby(_group_cols).max().reset_index()


def make_weekday(dt: datetime, timezone) -> str:
    """曜日付きの日付を生成する

    :param dt: datetime
    :param timezone: timezoneオブジェクト
    :return 形式：%-m/%-d(曜日)
    """
    dstr = dt.strftime("%-m/%-d")
    if timezone.zone == "Asia/Tokyo":
        return f"{dstr}({JA_WEEKDAYS[dt.weekday()]})"
    else:
        return f"{dstr}({WEEKDAYS[dt.weekday()]})"


def make_tweeted_weekday_range(timezone) -> List[str]:
    """グラフに描画する曜日付き日付ラベルの範囲を生成する

    :param timezone: timezoneオブジェクト
    :return 曜日付き日付ラベルのリスト
    """
    weekdays = []
    _now = datetime.now(timezone)
    for i in range(7):
        ts = _now - timedelta(days=i + 1)
        weekdays.append(make_weekday(ts, timezone=timezone))

    return weekdays[::-1]


def make_count_tweeted_weekday_df(df: pandas.DataFrame, timezone) -> pandas.DataFrame:
    """日付別にツイート数をカウントしたDataFrameを生成する

    :param df: 対象のDataFrame
    :param timezone: timezoneオブジェクト
    :return 日付別ツイート数DataFrame
    """
    _df = df.groupby("tweeted_weekday")["tweet_id"].agg(count="count")
    for wd in make_tweeted_weekday_range(timezone=timezone):
        if wd not in _df.index:
            _zero_df = pandas.DataFrame([0], index=[wd], columns=["count"])
            _zero_df.index.name = "tweeted_weekday"
            _df = _df.append(_zero_df)
    return _df.sort_index().reset_index()


def make_tweeted_hour_label_range() -> List[str]:
    """グラフに描画する時間ラベルの範囲を生成する

    :return 時間ラベルのリスト
    """
    return [str(i).zfill(2) for i in range(24)]


def make_count_tweeted_hour_df(df: pandas.DataFrame) -> pandas.DataFrame:
    """時間別にツイート数をカウントしたDataFrameを生成する

    :param df: 対象のDataFrame
    :return 時間別ツイート数DataFrame
    """
    _df = df.groupby("tweeted_hour")["tweet_id"].agg(count="count")
    for wd in make_tweeted_hour_label_range():
        if wd not in _df.index:
            _zero_df = pandas.DataFrame([0], index=[wd], columns=["count"])
            _zero_df.index.name = "tweeted_hour"
            _df = _df.append(_zero_df)
    return _df.sort_index().reset_index()


def make_user_df(
    df: pandas.DataFrame,
) -> pandas.DataFrame:
    """ユーザをユニークにしたDataFrameを生成する

    :param df: 計算対象のDataFrame
    :return 計算後のDataFrame
    """
    _df = (
        df.groupby(["user_screen_name", "user_name"])
        .agg(
            friends_count=("friends_count", "max"),
            followers_count=("followers_count", "max"),
            tweets_count=("tweet_id", "count"),
            following=("following", "max"),
        )
        .reset_index()
    )

    # フォロー数、フォロワー数どちらかが0は計算ができないので、1に変換して計算する
    _df["_friends_count"] = _df["friends_count"].apply(lambda x: x if x > 0 else 1)
    _df["_followers_count"] = _df["followers_count"].apply(lambda x: x if x > 0 else 1)
    _df["ff_ratio"] = _df["_followers_count"] / _df["_friends_count"]
    _df["ff_ratio_close_to_one"] = (1.0 - _df["ff_ratio"]).abs()
    cols = [
        "user_screen_name",
        "user_name",
        "tweets_count",
        "followers_count",
        "friends_count",
        "ff_ratio",
        "ff_ratio_close_to_one",
        "following",
    ]
    return _df[cols]


def make_title(df: pandas.DataFrame, main_title: str, count: int, search_word: str):
    """タイトルを生成する

    :param df: 計算対象のDataFrame
    :param main_title: メインとなるタイトル
    :param count: タイトルに表示する合計値
    :param search_word: タイトルに表示する検索ワード
    :return 生成したタイトル
    """
    _title = main_title
    _title += f" 【検索ワード:{search_word}】"
    _title += f" 【合計: {'{:,}'.format(count)}】 "
    _title += f" 【通算人数: {'{:,}'.format(count_users(df))}名】 "
    return _title
