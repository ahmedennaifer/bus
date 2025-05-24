from typing import List, Dict, Any
from src.messages.messages import Message, EmptyMessage
from src.topic.topic import Topic
from errors.topic import TopicAlreadyExistsException, TopicNotFoundException


from src.utils.logger import logger
from src.tcp.server import Server


class TopicRegistry(Server):
    def __init__(self):
        super().__init__()
        self._store: Dict[
            str, List[Message]
        ] = {}  # in memory store of topics : {'topic_name': [messages]}

    def add_to_store(self, topic: Topic) -> None:
        if not isinstance(topic, Topic):
            logger.error(f"Topic of type {topic} is not a valid topic!")

        if not self._store.get(topic.name):
            logger.info(f"Topic {topic} not found in registry. adding ...")
            self._store[topic.name] = [EmptyMessage()]
            logger.info(
                f"Added topic {topic} to registry with {len(topic._messages)} messages"
            )
        else:
            logger.error(f"Topic {topic} already exists")
            raise TopicAlreadyExistsException

    def listen_to_topic(self, topic_name: str) -> List[Message] | Any:
        if self._store.get(topic_name) is None:
            raise TopicNotFoundException(f"Topic {topic_name} does not exist")
        else:
            yield self._store.get(topic_name)

    @property
    def topics(self) -> Dict[str, List[Message]]:
        return self._store

    @property
    def messages(self):
        return self._raw_messages
