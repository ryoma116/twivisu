import pandas


def print_last_tweeted_datetime(df: pandas.DataFrame):
    """ツイートを取得した時間を出力する

    :param df: 描画に使用するDataFrame
    """
    print(f"※last tweet time: {df.tweeted_dt.max().strftime('%Y/%-m/%-d %-H:%M:%S')}")
