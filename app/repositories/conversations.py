"""Persistence operations for conversations."""

from datetime import UTC, datetime

from app.database import connection_scope


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class ConversationRepository:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path

    def create(self, title: str) -> dict:
        timestamp = utc_now()
        with connection_scope(self.database_path) as connection:
            cursor = connection.execute(
                "INSERT INTO conversations (title, created_at, updated_at) VALUES (?, ?, ?)",
                (title, timestamp, timestamp),
            )
            row = connection.execute(
                "SELECT * FROM conversations WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
        return dict(row)

    def get(self, conversation_id: int) -> dict | None:
        with connection_scope(self.database_path) as connection:
            row = connection.execute(
                "SELECT * FROM conversations WHERE id = ?", (conversation_id,)
            ).fetchone()
        return dict(row) if row else None

    def list(self) -> list[dict]:
        with connection_scope(self.database_path) as connection:
            rows = connection.execute(
                "SELECT * FROM conversations ORDER BY updated_at DESC, id DESC"
            ).fetchall()
        return [dict(row) for row in rows]

    def rename(self, conversation_id: int, title: str) -> dict | None:
        with connection_scope(self.database_path) as connection:
            connection.execute(
                "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
                (title, utc_now(), conversation_id),
            )
            row = connection.execute(
                "SELECT * FROM conversations WHERE id = ?", (conversation_id,)
            ).fetchone()
        return dict(row) if row else None

    def delete(self, conversation_id: int) -> bool:
        with connection_scope(self.database_path) as connection:
            cursor = connection.execute(
                "DELETE FROM conversations WHERE id = ?", (conversation_id,)
            )
        return cursor.rowcount == 1
