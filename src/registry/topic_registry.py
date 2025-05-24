from typing import List, Dict, Any
from src.messages.messages import Message, EmptyMessage
from src.topic.topic import Topic
from errors.topic import TopicAlreadyExistsException, TopicNotFoundException


from src.utils.logger import logger


class TopicRegistry:
    def __init__(self):
        self._store: Dict[
            str, List[Message]
        ] = {}  # in memory store of topics : {'topic_name': [messages]}

    def handle_action(
        self, action_msg: str
    ) -> None | bool:  # TODO: change action to enum
        """
        handles actions like create, delete, etc.. for topics
        schema: {'action': 'create', 'name': 'topic_name'}
        actions : create, destroy, check (if topic exists) ...
        returns none or bool for exists
        """
        logger.info(f"Got action {action_msg}. Processing...")
        action = action_msg["action"]  # pyright: ignore
        name = action_msg["name"]  # pyright: ignore
        if action == "create":
            self.add_to_store(topic=Topic(name=str(name)))
            logger.info(f"Finished processing action {action}")

        if action == "check":
            logger.debug(f"Checking if topic {name} exists...")
            print("-----store got:", self._store.get(name))
            if self._store.get(name) is None:
                return False
            return True

    def handle_message(self, message: Message) -> None:
        """routes a message to its topic"""
        logger.info(f"Routing message {message}...")
        if not isinstance(message, Message):
            raise TypeError("Message shoud be of type `Message`")

        if self._store.get(message._topic) is None:
            raise TopicNotFoundException(
                f"Topic {message._topic} does not exist in the registry"
            )
        print("gotten passed the not exist exception")
        print("printing topics..")
        print("topic:", self._store.get(message._topic))
        self._store[message._topic].append(message)
        print("added to store")

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
    def store(self):
        return self._store
