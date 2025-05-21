import time
import argparse


from src.messages.messages import Message
from src.publisher.publisher import Publisher
from src.registry.topic_registry import TopicRegistry
from src.topic.topic import Topic


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--listen")
    parser.add_argument("--topic")

    args = parser.parse_args()

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
        if args.listen:
            msgs = tr.listen_to_topic(args.listen)
            for msg in msgs:
                print(msg)
