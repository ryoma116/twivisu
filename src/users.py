import time
from typing import List

import tweepy

from .constants import API_COUNTS, FOLLOWER_IDS_API_PATH
from .errors import RateLimitError
from .limits import get_rate_limit_reset_time, is_rate_limit
from .twitters import execute_get_method


def get_follower_ids(
    api: tweepy.API,
    user_id: int,
) -> List[int]:
    """フォロワーのIDを取得する

    :param api: tweepy.API
    :param user_id: 対象ユーザID
    """

    print(f"===== get_followers_ids Start =====")

    ids = []
    next_cursor = -1
    while True:
        _tweets = []

        if is_rate_limit(api, api_path=FOLLOWER_IDS_API_PATH):
            reset_time = get_rate_limit_reset_time(api, api_path=FOLLOWER_IDS_API_PATH)
            print(f"アクセス上限のため処理休止中({reset_time}秒)..")
            time.sleep(reset_time)

        try:
            params = {
                "count": API_COUNTS[FOLLOWER_IDS_API_PATH],
                "user_id": user_id,
                "cursor": next_cursor,
            }
            _results = execute_get_method(
                url="https://api.twitter.com/1.1/followers/ids.json",
                params=params,
                oauth=api.auth.oauth,
            )

        except RateLimitError:
            print("アクセス上限のため処理休止中(15分)..")
            time.sleep(15 * 60)

        _ids = _results["ids"]
        ids.extend(_ids)
        if len(_ids) < 5000:
            break

        print(f"{'{:,}'.format(len(ids))} 件取得")
        next_cursor = _results["next_cursor"]
        time.sleep(1)

    print(f"===== get_followers_ids End（合計{'{:,}'.format(len(ids))}） =====")
    return ids
