import sqlite3

import pytest

from app.database import connect, initialize_database
from app.repositories.conversations import ConversationRepository
from app.repositories.messages import MessageRepository


def repositories(tmp_path):
    database_path = str(tmp_path / "chatbot.sqlite3")
    initialize_database(database_path)
    return database_path, ConversationRepository(database_path), MessageRepository(database_path)


def test_conversation_and_message_crud(tmp_path) -> None:
    database_path, conversations, messages = repositories(tmp_path)
    conversation = conversations.create("First chat")
    assert conversations.get(conversation["id"])["title"] == "First chat"
    message = messages.create(conversation["id"], "user", "Hello")
    assert message["conversation_id"] == conversation["id"]
    assert conversations.get(conversation["id"])["updated_at"] == message["timestamp"]
    assert messages.list_for_conversation(conversation["id"])[0]["content"] == "Hello"
    assert conversations.rename(conversation["id"], "Renamed chat")["title"] == "Renamed chat"
    assert conversations.delete(conversation["id"]) is True
    assert conversations.get(conversation["id"]) is None
    with connect(database_path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM messages").fetchone()[0] == 0


def test_messages_cannot_belong_to_missing_conversation(tmp_path) -> None:
    database_path, _, messages = repositories(tmp_path)
    with pytest.raises(sqlite3.IntegrityError):
        messages.create(999, "user", "Orphan")


def test_conversation_histories_are_isolated(tmp_path) -> None:
    _, conversations, messages = repositories(tmp_path)
    first = conversations.create("First")
    second = conversations.create("Second")
    messages.create(first["id"], "user", "Only first")
    messages.create(second["id"], "user", "Only second")
    assert [m["content"] for m in messages.list_for_conversation(first["id"])] == ["Only first"]
    assert [m["content"] for m in messages.list_for_conversation(second["id"])] == ["Only second"]
