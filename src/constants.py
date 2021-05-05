from enum import Enum

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
JA_WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]

FULL_TEXT_TWEET_MODE = "extended"

# 当日のツイートを除外したい場合はTrueとする（時間帯分析時は24時間分取得できない当日は除外した方がよさそう）
TODAY_EXCLUDED = False


class FfRatioOrderModes(Enum):
    HIGH = "high"
    LOW = "low"
    CLOSE_TO_ONE = "close_to_one"


SEARCH_API_PATH = "/search/tweets"
FOLLOWER_IDS_API_PATH = "/followers/ids"
API_TYPES = {
    SEARCH_API_PATH: "search",
    FOLLOWER_IDS_API_PATH: "followers",
}
API_COUNTS = {
    SEARCH_API_PATH: 100,
    FOLLOWER_IDS_API_PATH: 5000,
}
