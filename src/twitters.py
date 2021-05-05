import json
from typing import Dict

from .errors import RateLimitError, TwitterApiError


def execute_get_method(
    url: str,
    params: Dict,
    oauth: str,
):
    res = oauth.get(url, params=params)

    # リクエスト上限エラー
    if res.status_code == 429:
        raise RateLimitError()

    # 異常終了
    elif res.status_code >= 300:  # NGの場合
        raise TwitterApiError(f"HTTP status: {res.status_code}")

    return json.loads(res.text)
