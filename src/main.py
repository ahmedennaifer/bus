import time
import argparse

from threading import Thread

from src.messages.messages import Message
from src.publisher.publisher import Publisher
from src.registry.topic_registry import TopicRegistry
from src.topic.topic import Topic
from src.tcp.server import Server
from src.tcp.client import Client
from src.utils.logger import logger


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--listen", help="shows messages from a topic")  # TODO
    parser.add_argument("--create_topic", help="creates a new topic")
    parser.add_argument("--topic", help="publish to a topic")
    parser.add_argument(
        "--server", action="store_true", help="runs a tcp server for the broker"
    )
    parser.add_argument(
        "--list_topics", action="store_true", help="list created topics"
    )
    args = parser.parse_args()
    tr = TopicRegistry()
    s = Server(topic_registry=tr)
    thread = Thread(target=s.run)
    thread.start()

    if args.list_topics:
        action = {"action": "list", "name": "empty"}
        client = Client()
        client.send_action(action)
        logger.info(f"Sent action {action}..")

    if args.create_topic:
        action = {"action": "create", "name": args.create_topic.strip()}
        client = Client()
        client.send_action(action)
        logger.info(f"Sent action {action}..")

    if args.topic:
        tpc = Topic(name=args.topic.strip())
        pb = Publisher("test_publisher")
        n = 0
        while True:
            msg = Message(topic=tpc.name, data=f"test data {n}")
            pb.publish(msg, [tpc])
            time.sleep(1)
            n += 1

    if args.listen:
        topic = args.listen.strip()
        action = {"action": "listen", "name": topic}
        msgs = tr.listen_to_topic(topic)
        print("Msgs:", msgs)
        for msg in msgs:
            print(msg)
            time.sleep(0.3)
