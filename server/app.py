from lemon_pie import api
from lemon_pie.storage.postgres import PostgresStorage
from lemon_pie.storage import storage
import logging


def init_logger(level: str):
    logger = logging.getLogger("lemon_pie")
    logger.setLevel(logging.getLevelName(level))
    handler = logging.StreamHandler()
    logger.addHandler(handler)


if __name__ == '__main__':
    init_logger("DEBUG")
    storage.init_storage(PostgresStorage())
    api.init()
    ssl_context = ('../.cert/localhost.crt', '../.cert/localhost.key')
    api.app.run(debug=True, host='0.0.0.0', ssl_context=ssl_context)
