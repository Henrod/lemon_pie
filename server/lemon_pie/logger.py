import logging


def init(level: int) -> None:
    logger = logging.getLogger("lemon_pie")
    logger.setLevel(logging.getLevelName(level))
    handler = logging.StreamHandler()
    logger.addHandler(handler)
