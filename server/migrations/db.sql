-- TODO: use a real migration process

CREATE TABLE IF NOT EXISTS users (
    id TEXT,
    key TEXT NOT NULL,
    email TEXT,
    name TEXT NOT NULL,
    is_admin BOOL NOT NULL,
    is_playing BOOL NOT NULL,
    create_time TIMESTAMP NOT NULL,
    update_time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS votes (
    src_user_key TEXT NOT NULL,
    dst_user_key TEXT NOT NULL,
    key TEXT NOT NULL,
    date DATE NOT NULL,
    create_time TIMESTAMP NOT NULL,
    update_time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS emojis (
    key TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL UNIQUE,
    create_time TIMESTAMP NOT NULL,
    update_time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS configs (
    is_total_enabled BOOL,
    is_vote_opened BOOL
);
