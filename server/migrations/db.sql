-- TODO: use a real migration process

CREATE TABLE IF NOT EXISTS users (
    id TEXT,
    key TEXT NOT NULL,
    email TEXT,
    name TEXT NOT NULL,
    create_time DATETIME NOT NULL,
    update_time DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS votes (
    src_user_key TEXT NOT NULL,
    dst_user_key TEXT NOT NULL,
    key TEXT NOT NULL,
    date DATE NOT NULL,
    create_time DATETIME NOT NULL,
    update_time DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS emojis (
    key TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL UNIQUE,
    create_time DATETIME NOT NULL,
    update_time DATETIME NOT NULL
);
