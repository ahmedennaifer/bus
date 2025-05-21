from typing import Any
from src.topic.topic import Topic
import time

from uuid import uuid1, UUID


class Message:
    def __init__(self, topic: Topic, data: str) -> None:
        self._topic: Topic = topic
        self._data: str = data
        self._timestamp: Any = time.time()
        self._id: UUID = uuid1()
        self._publisher = None

    def __repr__(self) -> str:
        return f"Message(id:{self._id}, topic:{self._topic}, data: {self._data}, time: {self._timestamp})"


class EmptyMessage(Message):
    def __init__(self):
        self._data = ""

    def __repr__(self):
        return "Message: None"
