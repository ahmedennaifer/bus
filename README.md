### Simple message bus implem for learning purposes

Supports:
- creating topics
- listing topics
- publishing messages
- routing messages with the registry (broker) to topics
- communication via tcp (no protocol yet)

Usage:
```bash usage: main.py [-h] [--listen LISTEN] [--create_topic CREATE_TOPIC] [--server]
               [--list_topics]

options:
  -h, --help            show this help message and exit
  --listen LISTEN       shows messages from a topic
  --create_topic CREATE_TOPIC
                        creates a new topic
  --server              runs a tcp server for the broker
  --list_topics         list created topics```
