"""Persistence operations for conversation messages."""

from app.database import connection_scope
from app.repositories.conversations import utc_now


class MessageRepository:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path

    def create(self, conversation_id: int, role: str, content: str) -> dict:
        timestamp = utc_now()
        with connection_scope(self.database_path) as connection:
            cursor = connection.execute(
                "INSERT INTO messages (conversation_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                (conversation_id, role, content, timestamp),
            )
            connection.execute(
                "UPDATE conversations SET updated_at = ? WHERE id = ?",
                (timestamp, conversation_id),
            )
            row = connection.execute(
                "SELECT * FROM messages WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
        return dict(row)

    def list_for_conversation(self, conversation_id: int) -> list[dict]:
        with connection_scope(self.database_path) as connection:
            rows = connection.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY id ASC",
                (conversation_id,),
            ).fetchall()
        return [dict(row) for row in rows]
