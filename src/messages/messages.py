from __future__ import annotations

from typing import Any
import time
import json
from uuid import uuid1, UUID


class Message:
    def __init__(self, topic: str, data: str) -> None:
        self._topic: str = topic
        self._data: str = data
        self._timestamp: Any = time.time()
        self._id: UUID = uuid1()
        self._publisher: str = ""

    def to_json(self):
        msg = {
            "topic": self._topic,
            "data": self._data,
            "timestamp": self._timestamp,
            "id": str(self._id),
            "publisher": self._publisher,
        }
        return json.dumps(msg)

    @classmethod
    def from_json(cls, message: Any) -> Message:
        json_msg = json.loads(message)
        msg = cls(topic=json_msg["topic"], data=json_msg["data"])
        msg._timestamp = json_msg["timestamp"]
        msg._id = UUID(json_msg["id"])
        msg._publisher = json_msg["publisher"]
        return msg

    def __repr__(self) -> str:
        return f"Message(id:{self._id}, topic:{self._topic}, data: {self._data}, time: {self._timestamp})"


class EmptyMessage(Message):
    def __init__(self):
        super().__init__("Empty", "Empty")

    def __repr__(self):
        return "Message: None"
