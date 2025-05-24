from src.topic.topic import Topic
from src.registry.topic_registry import TopicRegistry
from src.messages.messages import Message
from src.errors.topic import TopicNotFoundException
from typing import List


from src.utils.logger import logger
from src.tcp.client import Client


class Publisher(Client):
    def __init__(self, name: str, registry: TopicRegistry) -> None:
        super().__init__()
        self.name = name
        self._topics = []
        self._topic_store = registry._store

    def publish(self, message: Message, topics: List[Topic]):
        """publish msg to topic(s) and set publisher field in msg"""
        for topic in topics:
            if not self._topic_store.get(topic.name):
                logger.error(f"tried to publish to topic {topic} which does not exist")
                raise TopicNotFoundException
            else:
                message._publisher = self.name
                self.send(message)
                logger.debug(
                    f"Publisher {self.name} published message: {message} to topic {topic}"
                )
