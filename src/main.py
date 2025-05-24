import time
import argparse


from src.messages.messages import Message
from src.publisher.publisher import Publisher
from src.registry.topic_registry import TopicRegistry
from src.topic.topic import Topic
from src.tcp.server import Server
from src.tcp.client import Client
from src.utils.logger import logger


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--listen")
    parser.add_argument("--create_topic")
    parser.add_argument("--topic")  # for testing tcp client
    parser.add_argument("--server")  # for testing tcp server
    parser.add_argument("--client")  # for testing tcp client
    args = parser.parse_args()
    tr = TopicRegistry()
    s = Server(topic_registry=tr)
    if args.server:
        s.run()

    else:
        if args.create_topic:
            action = {"action": "create", "name": args.create_topic.strip()}
            client = Client()
            client.send_action(action)
            logger.info(f"Sent action {action}..")

        if args.topic:
            tpc = Topic(name=args.topic.strip())

            print("stores:", tr.store)

            pb = Publisher("test_publisher")
            n = 0
            while True:
                msg = Message(topic=tpc.name, data=f"test data {n}")
                pb.publish(msg, [tpc])
                time.sleep(1)
                n += 1
                print(f"Messages stored in tr: {tr.store}")
