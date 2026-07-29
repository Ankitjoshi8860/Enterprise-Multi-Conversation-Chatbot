"""SQLite connection and schema management."""

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Iterator

SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id
    ON messages (conversation_id, id);
"""


def connect(database_path: str) -> sqlite3.Connection:
    """Open SQLite with row access and foreign-key enforcement enabled."""

    path = Path(database_path)
    if database_path != ":memory:":
        path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(database_path: str) -> None:
    """Create the schema if it does not exist."""

    with connect(database_path) as connection:
        connection.executescript(SCHEMA)


@contextmanager
def connection_scope(database_path: str) -> Iterator[sqlite3.Connection]:
    """Yield an initialized connection and close it after use."""

    connection = connect(database_path)
    try:
        connection.executescript(SCHEMA)
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
