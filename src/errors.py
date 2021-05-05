class TweetNotFoundError(Exception):
    """ツイートが取得できないので後続処理実行不可を知らせる例外クラス"""

    pass


class ParameterError(Exception):
    """パラメータ指定の不正を知らせる例外クラス"""

    pass


class RateLimitError(Exception):
    """リクエスト上限到達を知らせる例外クラス"""

    pass


class TwitterApiError(Exception):
    """TwitterAPIからの応答エラーを知らせる例外クラス"""

    pass
