from enum import Enum

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
JA_WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]

MAX_SEARCH_COUNT = 100
FULL_TEXT_TWEET_MODE = "extended"

# 当日のツイートを除外したい場合はTrueとする（時間帯分析時は24時間分取得できない当日は除外した方がよさそう）
TODAY_EXCLUDED = False


class FfRatioOrderModes(Enum):
    HIGH = "high"
    LOW = "low"
    CLOSE_TO_ONE = "close_to_one"
