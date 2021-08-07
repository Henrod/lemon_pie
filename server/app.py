import argparse
import logging
from datetime import datetime

from lemon_pie import api, logger
from lemon_pie.constants import DEVELOPMENT, PRODUCTION
from lemon_pie.storage import storage
from lemon_pie.storage.postgres import PostgresStorage


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Lemon Pie')
    parser.add_argument('--cert', help="path to ssl certificate")
    parser.add_argument('--key', help="key file when specifying a certificate")
    parser.add_argument('--env', default=PRODUCTION,
                        choices=[PRODUCTION, DEVELOPMENT])
    parser.add_argument('--end_vote_time', default="15:00", type=str)
    parser.add_argument('--debug', default=False)
    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()

    logger.init(logging.DEBUG)
    storage.init(PostgresStorage())

    api.init(
        env=args.env,
        end_vote_time=datetime.strptime(args.end_vote_time, "%H:%M").time(),
    )

    ssl_context = (args.cert, args.key) if args.cert and args.key else None
    api.app.run(debug=args.debug, host='0.0.0.0', ssl_context=ssl_context)
