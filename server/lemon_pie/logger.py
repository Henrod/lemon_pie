import logging


def init(level: str):
    logger = logging.getLogger("api")
    logger.setLevel(logging.getLevelName(level))
    handler = logging.StreamHandler()
    logger.addHandler(handler)
