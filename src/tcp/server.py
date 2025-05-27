import socket
import logging
import time
import json

from threading import Thread
from src.registry.topic_registry import TopicRegistry
from src.messages.messages import Message
from src.messages.messages import EmptyMessage


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Server:
    def __init__(
        self,
        topic_registry: TopicRegistry,
        host="localhost",
        port=8080,
        buffer_size=1024,
    ):
        self._host = host
        self._port = port
        self._BUFFER_SIZE = buffer_size
        # AF_INET = ipv4, SOCK_STREAM = tcp
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._init()
        self._topic_registry = topic_registry

    def _init(self):
        logging.debug("Initializing server...")
        try:
            self._socket.bind((self._host, self._port))
            self._socket.listen()
            logging.info(f"Server listening on {self._host}:{self._port}")
        except Exception as e:
            logging.error(f"Error on init: {e}")

    def _process(self, client_socket):
        while True:
            try:
                client_data = client_socket.recv(self._BUFFER_SIZE)
                if not client_data:  # avoid permanent empty buffers
                    break
                logging.info(
                    f"[SERVER] Received {client_data.decode('utf-8')}. Sending response..."
                )
                decoded_client_data = client_data.decode(
                    "utf-8"
                )  # TODO: add protocol for actions and/or messages
                if decoded_client_data.startswith('{"topic"'):
                    msg = Message.from_json(decoded_client_data)
                    self._topic_registry.handle_message(msg)
                    client_socket.send("message received from here".encode("utf-8"))

                elif decoded_client_data.startswith('{"action"'):
                    action_dict = json.loads(decoded_client_data)
                    logging.info(f"Got action {action_dict}!")
                    result = self._topic_registry.handle_action(action_dict)
                    logging.info(f"bool result: {result}")

                    if action_dict["action"] in ["check", "list"]:
                        response = str(result)
                        logging.info(f"list req result : {response.encode('utf-8')}")
                        client_socket.send(response.encode("utf-8"))

                    elif action_dict["action"] == "listen":
                        logging.info("[SERVER] got listen")
                        topic_name = action_dict.get("name")
                        try:
                            while True:
                                msgs = self._topic_registry.listen_to_topic(topic_name)
                                if msgs:
                                    if isinstance(msgs[0], EmptyMessage):
                                        msgs.pop(0)
                                        continue

                                    msg = msgs.pop(0)
                                    logging.info(f"[SERVER] Sending message {msg}...")
                                    msg_json = msg.to_json()
                                    client_socket.send(msg_json.encode("utf-8"))
                                    logging.info(f"[SERVER] Sent message {msg}")

                                else:
                                    logging.info("Waiting for messages...")
                                    time.sleep(0.2)

                        except Exception as e:
                            logging.error(
                                f"Failed sending response to client {client_socket}: {e}"
                            )
                    else:
                        client_socket.send("action completed".encode("utf-8"))

                else:
                    client_socket.send("message received".encode("utf-8"))
            except Exception as e:
                logging.error(f"Error sending msg to client: {e}")
                client_socket.close()
                break

    def run(self):
        try:
            while True:
                logging.info("Starting server...")
                client_socket, client_address = self._socket.accept()
                logging.info(f"Connection established with client {client_address}")
                logging.debug(f"Starting thread at {time.time()}...")
                thread = Thread(target=self._process, args=[client_socket])
                thread.start()
        except Exception as e:
            logging.error(f"Error running the thread {e}")
