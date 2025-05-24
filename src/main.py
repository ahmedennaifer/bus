import time
import argparse


from src.messages.messages import Message
from src.publisher.publisher import Publisher
from src.registry.topic_registry import TopicRegistry
from src.topic.topic import Topic
from src.tcp.client import Client
from src.tcp.server import Server

from threading import Thread


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--listen")
    parser.add_argument("--topic")
    parser.add_argument("--server")  # for testing tcp server
    parser.add_argument("--client")  # for testing tcp client
    args = parser.parse_args()
    s = Server()
    if args.server:
        s.run()

    tpc = Topic(str(args.topic))
    tr = TopicRegistry()
    tr.add_to_store(tpc)
    pb = Publisher("test_publisher", tr)
    n = 0
    while True:
        msg = Message(tpc, f"test data {n}")
        pb.publish(msg, [tpc])
        time.sleep(1)
        n += 1
        print(f"Messages stored in tr: {tr.messages}")

