import argparse
import logging

from lemon_pie import api
from lemon_pie.constants import PRODUCTION, DEVELOPMENT
from lemon_pie.storage import storage
from lemon_pie.storage.postgres import PostgresStorage


def init_logger(level: int):
    logger = logging.getLogger("lemon_pie")
    logger.setLevel(logging.getLevelName(level))
    handler = logging.StreamHandler()
    logger.addHandler(handler)


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Lemon Pie')
    parser.add_argument('--cert', default='.cert/localhost.crt',
                        help="path to ssl certificate")
    parser.add_argument('--key', default='.cert/localhost.key',
                        help="key file when specifying a certificate")
    parser.add_argument('--env', default=PRODUCTION,
                        choices=[PRODUCTION, DEVELOPMENT])
    parser.add_argument('--debug', default=False)
    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()

    init_logger(logging.DEBUG)
    storage.init_storage(PostgresStorage())
    api.init(args.env)

    ssl_context = (args.cert, args.key)
    api.app.run(debug=args.debug, host='0.0.0.0', ssl_context=ssl_context)
