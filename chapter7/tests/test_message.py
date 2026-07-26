"""Message 组件的最小行为测试。"""

from datetime import datetime

import pytest

from hello_agents.core.message import Message


def test_message_fills_teaching_defaults() -> None:
    message = Message(content="你好", role="user")

    assert message.content == "你好"
    assert message.role == "user"
    assert isinstance(message.timestamp, datetime)
    assert message.metadata == {}


def test_message_accepts_explicit_timestamp_and_metadata() -> None:
    timestamp = datetime(2026, 7, 26, 12, 0, 0)
    metadata = {"source": "test", "turn": 1}

    message = Message(
        content="继续学习",
        role="user",
        timestamp=timestamp,
        metadata=metadata,
    )

    assert message.timestamp == timestamp
    assert message.metadata == metadata


def test_message_to_dict_exposes_api_fields_only() -> None:
    message = Message(
        content="你好",
        role="assistant",
        metadata={"internal_id": "hidden"},
    )

    assert message.to_dict() == {
        "role": "assistant",
        "content": "你好",
    }


def test_message_rejects_unknown_role() -> None:
    with pytest.raises(ValueError):
        Message(content="错误角色", role="unknown")  # type: ignore[arg-type]


def test_message_string_representation() -> None:
    message = Message(content="你好", role="user")

    assert str(message) == "[user] 你好"
