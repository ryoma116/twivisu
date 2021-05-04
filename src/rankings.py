import urllib.parse

import pandas as pd

from .filters import filter_user
from .processors import make_user_df


def make_user_ranking(
    df: pd.DataFrame,
    col: str,
    top: int = 10,
    ascending: bool = True,
    search_word: str = "",
    search_query: str = "",
    value_fmt="{:,}",
    **kwargs,
):
    """ユーザを画面に出力する

    :param df: 出力対象のDataFrame
    :param col: 順位の評価対象カラム
    :param top: 上位から出力する件数を指定
    :param ascending: 並び順を指定、昇順はTrue、降順はFalse
    :param search_word: タイトルに表示する検索ワード
    :param search_query: 検索に使用したクエリ、リンク生成時に使用する
    :param value_fmt: 値のフォーマット、実数値の場合は{:.2f}を推奨する
    """
    _df = make_user_df(df)
    _df = filter_user(_df, **kwargs)
    _df = _df.sort_values(col, ascending=ascending)
    num = 1
    for idx, row in _df.iterrows():
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
