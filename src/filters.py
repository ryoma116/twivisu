import pandas


def filter_user(
    df: pandas.DataFrame,
    min_followers_count: int = None,
    max_followers_count: int = None,
) -> pandas.DataFrame:
    """ユーザ軸の項目でフィルタリング

    :param df: 計算対象のDataFrame
    :param min_followers_count: フォロワー数の下限値、指定した値よりフォロワー数が多いユーザを対象とする
    :param max_followers_count: フォロワー数の上限値、指定した値よりフォロワー数が少ないユーザを対象とする
    :return 計算後のDataFrame
    """
    _df = df
    if min_followers_count:
        _df = _df[_df["followers_count"] >= min_followers_count]

    if max_followers_count:
        _df = _df[_df["followers_count"] <= max_followers_count]

    return _df
