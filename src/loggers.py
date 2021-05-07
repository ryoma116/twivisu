import logging
from datetime import datetime

from pytz import timezone

logging.basicConfig(level=logging.WARNING)
_timezone = timezone("UTC")


def set_logger_timezone(tz: str):
    global _timezone
    _timezone = timezone(tz)


def _convert_datetime(*args):
    return datetime.now(_timezone).timetuple()


def get_logger(name, loglevel):
    logger = logging.getLogger(name)

    # ログが複数回表示されるのを防止
    logger.propagate = False

    logger.setLevel(loglevel)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    formatter.converter = _convert_datetime
    handler.setFormatter(formatter)
    handler.setLevel(loglevel)
    logger.addHandler(handler)

    return logger
