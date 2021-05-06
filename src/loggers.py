import logging

logging.basicConfig(level=logging.WARNING)


def get_logger(name, loglevel):
    logger = logging.getLogger(name)

    # ログが複数回表示されるのを防止
    logger.propagate = False

    logger.setLevel(loglevel)

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    handler.setLevel(loglevel)
    logger.addHandler(handler)

    return logger
