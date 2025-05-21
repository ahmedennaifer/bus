from src.topic.topic import Topic
from src.registry.topic_registry import TopicRegistry
from src.messages.messages import Message
from src.errors.topic import TopicNotFoundException
from typing import List


from src.utils.logger import logger


class Publisher:
    def __init__(self, name: str, registry: TopicRegistry) -> None:
        self.name = name
        self._topics = []
        self._topic_store = registry._store

    def publish(self, message: Message, topics: List[Topic]):
        for topic in topics:
            if not self._topic_store.get(topic.name):
                logger.error(f"tried to publish to topic {topic} which does not exist")
                raise TopicNotFoundException
            else:
                self._topic_store[topic.name].append(message)
                logger.debug(
                    f"Publisher {self.name} published message: {message} to topic {topic}"
                )
