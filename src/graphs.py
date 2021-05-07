import pandas
import plotly.express

from .processors import (
    make_count_tweeted_weekday_df,
    make_title,
    make_tweet_user_weekday_max_hour_df,
)


def make_daily_tweets_graph(df: pandas.DataFrame, search_word: str, timezone):
    """日付別のツイート数を折れ線グラフで出力する

    :param df: 集計対象のDataFrame
    :param search_word: タイトルに表示する検索ワード
    :param timezone: timezoneオブジェクト
    """
    _df = make_count_tweeted_weekday_df(df, timezone=timezone)
    _total_count = _df.sum()["count"]
    fig = plot_line(
        _df,
        x_col="tweeted_weekday",
        x_label="ツイート日付",
        y_col="count",
        y_label="ツイート人数",
        title=make_title(
            df, main_title="日別ツイート数", count=_total_count, search_word=search_word
        ),
    )
    return fig


def make_daily_tweet_users_graph(df: pandas.DataFrame, search_word: str, timezone):
    """日付別のツイート人数を折れ線グラフで出力する

    :param df: 集計対象のDataFrame
    :param search_word: タイトルに表示する検索ワード
    :param timezone: timezoneオブジェクト
    """
    _df = make_tweet_user_weekday_max_hour_df(df)
    _df = make_count_tweeted_weekday_df(_df, timezone=timezone)
    _total_count = _df.sum()["count"]
    fig = plot_line(
        _df,
        x_col="tweeted_weekday",
        x_label="ツイート日付",
        y_col="count",
        y_label="ツイート人数",
        title=make_title(
            df, main_title="日別ツイート人数", count=_total_count, search_word=search_word
        ),
    )
    return fig


def plot_line(
    df: pandas.DataFrame, x_col: str, y_col: str, x_label: str, y_label: str, title: str
):
    """折れ線グラフを描画する

    :param df: 描画に使用するDataFrame
    :param x_col: x軸に使用するDataFrameカラム名
    :param x_label: グラフのx軸に表示するラベル
    :param y_col: y軸に使用するDataFrameカラム名
    :param y_label: グラフのy軸に表示するラベル
    :param title: グラフに表示するタイトル
    :return グラフオブジェクト
    """
    return plotly.express.line(
        df,
        x=x_col,
        y=y_col,
        text=y_col,
        title=title,
        labels={
            y_col: y_label,
            x_col: x_label,
        },
    )
