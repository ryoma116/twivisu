import time

import tweepy

from .constants import API_TYPES


def get_rate_limit_reset_time(api: tweepy.API, api_path: str) -> int:
    """APIの制約解除秒数を取得する

    :param api: Tweepy.API
    :param api_path: APIのパス
    :return 検索APIの制約解除秒数
    """
    rate_limit = _get_api_rate_limit(api, api_path)
    return rate_limit["reset"] - int(time.time())


def is_rate_limit(api: tweepy.API, api_path: str) -> bool:
    """APIの上限に達したかチェック

    :param api: Tweepy.API
    :param api_path: APIのパス
    :return 上限に達した場合はTrue、達していない場合はFalse
    """
    rate_limit = _get_api_rate_limit(api, api_path)
    return rate_limit["remaining"] == 0


def _get_api_rate_limit(api: tweepy.API, api_path) -> int:
    """リミット情報を取得する

    :param api: Tweepy.API
    :param api_path: APIのパス
    :return 検索APIの制約解除秒数
    """
    api_type = API_TYPES[api_path]
    return api.rate_limit_status()["resources"][api_type][api_path]
