import logging
import time
from typing import List

import tweepy

from .constants import API_COUNTS, API_URLS, FOLLOWER_IDS_API_PATH, FRIEND_IDS_API_PATH
from .errors import RateLimitError
from .limits import get_rate_limit_reset_time, is_rate_limit
from .loggers import get_logger
from .twitters import execute_get_method

logger = get_logger(__name__, loglevel=logging.INFO)


def get_follower_ids(api: tweepy.API, user_screen_name: str) -> List[int]:
    """フォロワーのユーザIDを取得する

    :param api: tweepy.API
    :param user_screen_name: 対象ユーザ名
    :return フォロワーのユーザIDリスト
    """
    return _get_user_ids(api, user_screen_name, api_path=FOLLOWER_IDS_API_PATH)


def get_following_ids(api: tweepy.API, user_screen_name: str) -> List[int]:
    """フォロー中ユーザのIDを取得する

    :param api: tweepy.API
    :param user_screen_name: 対象ユーザ名
    :return フォロー中のユーザIDリスト
    """
    return _get_user_ids(api, user_screen_name, api_path=FRIEND_IDS_API_PATH)


def _get_user_ids(api: tweepy.API, user_screen_name: str, api_path: str) -> List[int]:
    """フォロワー or フォロー中ユーザのIDを取得する

    :param api: tweepy.API
    :param user_screen_name: 対象ユーザ名
    :param api_path: Twitter APIのパス
    :return Twitter APIから取得したユーザIDリスト
    """
    ids = []
    next_cursor = -1
    while True:
        _tweets = []

        if is_rate_limit(api, api_path=api_path):
            reset_time = get_rate_limit_reset_time(api, api_path=api_path)
            logger.info(f"アクセス上限のため処理休止中({reset_time}秒)..")
            time.sleep(reset_time)

        try:
            params = {
                "count": API_COUNTS[api_path],
                "screen_name": user_screen_name,
                "cursor": next_cursor,
            }
            _results = execute_get_method(
                url=API_URLS[api_path],
                params=params,
                oauth=api.auth.oauth,
            )

        except RateLimitError:
            logger.info("アクセス上限のため処理休止中(15分)..")
            time.sleep(15 * 60)
            continue

        _ids = _results["ids"]
        ids.extend(_ids)
        if len(_ids) < API_COUNTS[api_path]:
            break

        logger.info(f"{'{:,}'.format(len(ids))} 件取得")
        next_cursor = _results["next_cursor"]
        time.sleep(1)

    return ids
