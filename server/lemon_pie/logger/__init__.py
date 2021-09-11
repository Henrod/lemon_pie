import logging


def init(level: int) -> None:
    for m in ["lemon_pie", "waitress"]:
        logger = logging.getLogger(m)
        logger.setLevel(logging.getLevelName(level))
        handler = logging.StreamHandler()
        logger.addHandler(handler)
