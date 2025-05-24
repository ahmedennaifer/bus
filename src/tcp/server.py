import socket
import logging
import time
import json

from src.registry.topic_registry import TopicRegistry
from src.messages.messages import Message

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

    def run(self):
        while True:
            try:
                logging.info("Starting server...")
                client_socket, client_address = self._socket.accept()
                logging.info(f"Connection established with client {client_address}")
                while True:
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
                    elif decoded_client_data.startswith('{"action"'):
                        action_dict = json.loads(decoded_client_data)
                        logging.info("Got action!")

                        result = self._topic_registry.handle_action(action_dict)

                        if action_dict["action"] == "check":
                            response = str(result)
                            client_socket.send(response.encode("utf-8"))
                        else:
                            client_socket.send("action completed".encode("utf-8"))

                    else:
                        client_socket.send("message received".encode("utf-8"))
            except Exception as e:
                logging.error(f"Error sending msg to client: {e}")

            except KeyboardInterrupt:
                logging.info("Server shutting down...")
                time.sleep(0.5)
                break
