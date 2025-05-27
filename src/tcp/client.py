from src.errors.tcp import ClientAlreadyConnectedException
from src.messages.messages import Message
from typing import Dict


import socket
import json
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Client:
    def __init__(self, host="localhost", port=8080, buffer_size=1024):
        self._host = host
        self._port = port
        self._BUFFER_SIZE = buffer_size
        # AF_INET = ipv4, SOCK_STREAM = tcp
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._is_connected = False

    def _connect_to_server(self):
        """connect to server, then update is_connected"""
        if self._is_connected:
            raise ClientAlreadyConnectedException(
                f"Already connected to host: {self._host} on port: {self._port}"
            )
        try:
            logging.info("Connecting client...")
            self._socket.connect((self._host, self._port))
            self._is_connected = True
            logging.info(f"Connection established with server {self._host}")
        except ConnectionRefusedError as cre:
            logging.error(f"Error: Server refused the connection : {cre}")
            self.disconnect()
        except Exception as e:
            logging.error(f"Error: {e}")
            self.disconnect()

        pass

    def disconnect(self):
        logging.debug("Trying to disconnect client... ")
        self._socket.close()
        self._is_connected = False
        logging.info("Client disconnected")

    def send_action(
        self, action: Dict[str, str]
    ) -> None:  # TODO: add proper action integration
        if not self._is_connected:
            logging.debug("Client isn't connected to server")
            self._connect_to_server()
            logging.info("Client Connected")

        encoded_action = json.dumps(action).encode("utf-8")
        try:
            self._socket.send(encoded_action)
            logging.info(f"[CLIENT] Client sent action: {action}")
            response = self._socket.recv(4096).decode("utf-8")
            print(f"[RESPONSE] {response}")
            logging.debug(f"[SERVER] {response}")
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            self.disconnect()

    def check_topic_exists(self, topic_name: str) -> bool:
        if not self._is_connected:
            logging.debug("Client isn't connected to server")
            self._connect_to_server()
            logging.info("Client Connected")

        try:
            check_request = json.dumps({"action": "check", "name": topic_name})
            self._socket.send(check_request.encode("utf-8"))
            results = self._socket.recv(1024).decode("utf-8")
            return results.strip() == "True"

        except Exception as e:
            logging.error(f"Cannot check if topic {topic_name} exists: {e}")
            self.disconnect()
            return False

    def send(self, msg: Message) -> None:
        if not isinstance(msg, Message):
            raise Exception("Send only accepts `Message` or `Action` format!")

        if not self._is_connected:
            logging.debug("Client isn't connected to server")
            self._connect_to_server()
            logging.info("Client Connected")

        encoded_msg = msg.to_json().encode("utf-8")
        try:
            self._socket.send(encoded_msg)
            logging.info(f"[CLIENT] Client sent msg: {msg}")
            response = self._socket.recv(4096).decode("utf-8")
            logging.info(f"[SERVER] {response}")
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            self.disconnect()
