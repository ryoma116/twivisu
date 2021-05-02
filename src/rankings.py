import urllib.parse

import pandas as pd

from .processors import make_ff_ratio_df


def print_top_user(
    df: pd.DataFrame,
    col: str,
    top: int = 10,
    search_word: str = "",
    search_query: str = "",
    value_fmt="{:,}",
):
    """ユーザを画面に出力する

    :param df: 出力対象のDataFrame
    :param col: 順位の評価対象カラム
    :param top: 上位から出力する件数を指定
    :param search_word: タイトルに表示する検索ワード
    :param search_query: 検索に使用したクエリ、リンク生成時に使用する
    :param value_fmt: 値のフォーマット、実数値の場合は{:.2f}を推奨する
    """
    num = 1
    for idx, row in df.iterrows():
        if num > top:
            break
        twitter_query = urllib.parse.quote(
            f"from:@{row.user_screen_name} {search_word} {search_query}"
        )
        twitter_url = (
            f"https://twitter.com/search?src=typed_query&f=live&q={twitter_query}"
        )
        value = value_fmt.format(row[col])
        print(f"{value}　\t　{row.user_name}\t\t{twitter_url}")
        num += 1


def print_top_ff_ratio_low_user(
    df: pd.DataFrame,
    top: int = 10,
    search_word: str = "",
    search_query: str = "",
    min_followers_count: int = 0,
):
    """FF比が低いユーザを画面に出力する

    :param df: 集計対象のDataFrame
    :param top: 上位から出力する件数を指定
    :param search_word: タイトルに表示する検索ワード
    :param search_query: 検索に使用したクエリ、リンク生成時に使用する
    :param min_followers_count: フォロワー数の下限値、指定した値よりフォロワー数が多いユーザを対象とする
    """
    _df = make_ff_ratio_df(df, min_followers_count=min_followers_count)
    _df = _df.sort_values("ff_ratio", ascending=True)
    print_top_user(
        _df,
        top=top,
        search_word=search_word,
        search_query=search_query,
        col="ff_ratio",
        value_fmt="{:.2f}",
    )


def print_top_ff_ratio_high_user(
    df: pd.DataFrame,
    top: int = 10,
    search_word: str = "",
    search_query: str = "",
    min_followers_count: int = 0,
):
    """FF比が高いユーザを画面に出力する

    :param df: 集計対象のDataFrame
    :param top: 上位から出力する件数を指定
    :param search_word: タイトルに表示する検索ワード
    :param search_query: 検索に使用したクエリ、リンク生成時に使用する
    :param min_followers_count: フォロワー数の下限値、指定した値よりフォロワー数が多いユーザを対象とする
    """
    _df = make_ff_ratio_df(df, min_followers_count=min_followers_count)
    _df = _df.sort_values("ff_ratio", ascending=False)
    print_top_user(
        _df,
        top=top,
        search_word=search_word,
        search_query=search_query,
        col="ff_ratio",
        value_fmt="{:.2f}",
    )


def print_top_ff_ratio_close_to_one_user(
    df: pd.DataFrame,
    top: int = 10,
    search_word: str = "",
    search_query: str = "",
    min_followers_count: int = 0,
):
    """FF比が1.0に近いユーザを画面に出力する

    :param df: 集計対象のDataFrame
    :param top: 上位から出力する件数を指定
    :param search_word: タイトルに表示する検索ワード
    :param search_query: 検索に使用したクエリ、リンク生成時に使用する
    :param min_followers_count: フォロワー数の下限値、指定した値よりフォロワー数が多いユーザを対象とする
    """
    _df = make_ff_ratio_df(df, min_followers_count=min_followers_count)
    _df["ff_ratio_close_to_one"] = (1.0 - _df["ff_ratio"]).abs()
    _df = _df.sort_values(
        ["ff_ratio_close_to_one", "followers_count"], ascending=[True, False]
    )
    print_top_user(
        _df,
        top=top,
        search_word=search_word,
        search_query=search_query,
        col="ff_ratio_close_to_one",
        value_fmt="{:.4f}",
    )


def print_top_followers_count_user(
    df: pd.DataFrame, top: int = 10, search_word: str = "", search_query: str = ""
):
    """ツイート数の多いユーザを画面に出力する

    :param df: 集計対象のDataFrame
    :param top: 上位から出力する件数を指定
    :param search_word: タイトルに表示する検索ワード
    :param search_query: 検索に使用したクエリ、リンク生成時に使用する
    """
    _df = (
        df.groupby(["user_screen_name", "user_name"])["followers_count"]
        .agg(followers_count="max")
        .reset_index()
    )
    _df = _df.sort_values("followers_count", ascending=False)
    print_top_user(
        _df,
        top=top,
        search_word=search_word,
        search_query=search_query,
        col="followers_count",
    )


def print_top_friends_count_user(
    df: pd.DataFrame, top: int = 10, search_word: str = "", search_query: str = ""
):
    """ツイート数の多いユーザを画面に出力する

    :param df: 集計対象のDataFrame
    :param top: 上位から出力する件数を指定
    :param search_word: タイトルに表示する検索ワード
    :param search_query: 検索に使用したクエリ、リンク生成時に使用する
    """
    _df = (
        df.groupby(["user_screen_name", "user_name"])["friends_count"]
        .agg(friends_count="max")
        .reset_index()
    )
    _df = _df.sort_values("friends_count", ascending=False)
    print_top_user(
        _df,
        top=top,
        search_word=search_word,
        search_query=search_query,
        col="friends_count",
    )


def print_top_tweet_count_user(
    df: pd.DataFrame, top: int = 10, search_word: str = "", search_query: str = ""
):
    """ツイート数の多いユーザを画面に出力する

    :param df: 集計対象のDataFrame
    :param top: 上位から出力する件数を指定
    :param search_word: タイトルに表示する検索ワード
    :param search_query: 検索に使用したクエリ、リンク生成時に使用する
    """
    _df = (
        df.groupby(["user_screen_name", "user_name"])["tweet_id"]
        .agg(tweet_count="count")
        .reset_index()
    )
    _df = _df.sort_values("tweet_count", ascending=False)
    print_top_user(
        _df,
        top=top,
        search_word=search_word,
        search_query=search_query,
        col="tweet_count",
    )
