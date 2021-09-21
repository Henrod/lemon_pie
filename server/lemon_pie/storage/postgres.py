from __future__ import annotations

import logging
import os
from datetime import date
from typing import Any, Callable, List, Tuple

import psycopg2
from lemon_pie.models import Emoji, User, Vote
from lemon_pie.models.configs import Configs
from lemon_pie.storage.storage import Storage
from psycopg2.extensions import cursor as pgcursor
from psycopg2.extras import LoggingConnection

_DATABASE_URL = os.environ.get(
    "LEMON_PIE_DATABASE_URL",
    "postgresql://admin:admin@localhost:5432/lemon_pie")


def cursor(func: Callable) -> Callable:
    def with_cursor(
        self: PostgresStorage,
        *args: Any,
        **kwargs: Any,
    ) -> Callable:
        with self.conn, self.conn.cursor() as cur:
            return func(self, cur, *args, **kwargs)
    return with_cursor


class PostgresStorage(Storage):
    def __init__(self) -> None:
        logger = logging.getLogger(__name__)
        self.conn = psycopg2.connect(
            _DATABASE_URL,
            connection_factory=LoggingConnection)
        self.conn.initialize(logger)

    @cursor
    def select_votes_date(self, cur: pgcursor, date: date) -> List[Vote]:
        cur.execute(
            """
            SELECT src_user_key, dst_user_key, key, date
            FROM votes WHERE date = %s
            """, (date,)
        )
        return [
            Vote(
                src=User(key=src),
                dst=User(key=dst),
                key=value,
                date=date,
            ) for (src, dst, value, date) in cur.fetchall()
        ]

    @cursor
    def select_votes(self, cur: pgcursor) -> List[Vote]:
        cur.execute(
            """
            SELECT src_user_key, dst_user_key, key, date
            FROM votes
            """,
        )
        return [
            Vote(
                src=User(key=src),
                dst=User(key=dst),
                key=value,
                date=date,
            ) for (src, dst, value, date) in cur.fetchall()
        ]

    @cursor
    def insert_vote(self, cur: pgcursor, vote: Vote) -> None:
        cur.execute(
            """
            INSERT INTO votes(
                src_user_key, dst_user_key, key, date,
                create_time, update_time
            ) VALUES(
                %s, %s, %s, %s,
                NOW(), NOW()
            )
            """, (vote.src.key, vote.dst.key, vote.key, vote.date),
        )

    @cursor
    def delete_vote(
        self, cur: pgcursor,
        vote_pk: Tuple[date, str, str]
    ) -> None:
        vote_date, vote_src, vote_dst = vote_pk
        cur.execute(
            """
            DELETE FROM votes
            WHERE date = %s AND src_user_key = %s AND dst_user_key = %s
            """,
            (vote_date, vote_src, vote_dst),
        )

    @cursor
    def select_users(self, cur: pgcursor) -> List[User]:
        cur.execute("""
            SELECT key, name, email, create_time
            FROM users
            WHERE is_playing
        """)
        return [
            User(key=key, name=name, email=email, create_time=create_time)
            for (key, name, email, create_time) in cur.fetchall()
        ]

    @cursor
    def select_user(
        self,
        cur: pgcursor,
        user_id: str = None,
        user_email: str = None,
        user_key: str = None,
    ) -> User:
        cur.execute(
            """
            SELECT id, key, name, email, is_admin
            FROM users
            WHERE id = %s or email = %s or key = %s
            """,
            (user_id, user_email, user_key)
        )
        user = cur.fetchone()
        if user is None:
            return User(key="")
        else:
            (id, key, name, email, is_admin) = user
            return User(
                id=id,
                key=key,
                name=name,
                email=email,
                is_admin=is_admin
            )

    @cursor
    def update_user(self, cur: pgcursor, user: User) -> None:
        cur.execute(
            """
            UPDATE users
            SET id = %s, update_time = NOW()
            WHERE email = %s
            """,
            (user.id, user.email),
        )

    @cursor
    def insert_emoji(self, cur: pgcursor, emoji: Emoji) -> None:
        cur.execute(
            """
            INSERT INTO emojis (key, value, create_time, update_time)
            VALUES (%s, %s, NOW(), NOW())
            """,
            (emoji.key, emoji.value)
        )

    @cursor
    def delete_emoji(self, cur: pgcursor, emoji_key: str) -> None:
        cur.execute(
            """
            DELETE FROM emojis WHERE key = %s
            """,
            (emoji_key,)
        )

    @cursor
    def select_emojis(self, cur: pgcursor) -> List[Emoji]:
        cur.execute(
            """
            SELECT key, value, create_time, update_time FROM emojis
            """
        )
        return [
            Emoji(
                key=key,
                value=value,
                create_time=create_time,
                update_time=update_time
            ) for (key, value, create_time, update_time) in cur.fetchall()
        ]

    @cursor
    def select_configs(self, cur: pgcursor) -> Configs:
        cur.execute(
            """
            SELECT is_total_enabled FROM configs
            """
        )
        (is_total_enabled,) = cur.fetchone()

        return Configs(
            is_total_enabled=is_total_enabled,
        )
