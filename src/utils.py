import pandas


def count_users(df: pandas.DataFrame) -> int:
    """ユーザ数をカウントする

    :param df: 対象のDataFrame
    :return ユーザ数
    """
    _cols = ["user_id"]
    _duplicated = df[_cols].duplicated()
    _df = df[~_duplicated]
    return _df.count().iloc[0]
