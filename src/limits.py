import time

import tweepy


def get_search_limit_remaining(api: tweepy.API) -> int:
    """検索APIの上限に達したかチェック

    :param api: Tweepy.API
    :return 検索APIの15分間残り回数
    """
    return api.rate_limit_status()["resources"]["search"]["/search/tweets"]["remaining"]


def get_search_limit_reset_time(api: tweepy.API) -> int:
    """検索APIの制約解除秒数を取得する

    :param api: Tweepy.API
    :return 検索APIの制約解除秒数
    """
    unix_time = api.rate_limit_status()["resources"]["search"]["/search/tweets"][
        "reset"
    ]
    return unix_time - int(time.time())


def is_search_limit(api: tweepy.API) -> bool:
    """検索APIの上限に達したかチェック

    :param api: Tweepy.API
    :return 上限に達した場合はTrue、達していない場合はFalse
    """
    return get_search_limit_remaining(api) == 0
