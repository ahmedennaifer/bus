from src.topic.topic import Topic
from src.messages.messages import Message
from src.errors.topic import TopicNotFoundException
from typing import List


from src.utils.logger import logger
from src.tcp.client import Client


class Publisher:
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self._topics = []
        self._client = Client()

    def publish(self, message: Message, topics: List[Topic]):
        """publish msg to topic(s) and set publisher field in msg"""
        for topic in topics:
            exists = self._client.check_topic_exists(topic.name)
            if not exists:
                raise TopicNotFoundException(f"Topic {topic} does not exist!")

            message._publisher = self.name
            self._client.send(message)
            logger.debug(
                f"Publisher {self.name} published message: {message} to topic {topic}"
            )
