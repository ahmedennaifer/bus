from src.errors.tcp import ClientAlreadyConnectedException
from src.messages.messages import Message

import socket
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

    def send(self, msg: Message) -> None:
        if not isinstance(msg, Message):
            raise Exception("Send only accepts `Message` format!")

        if not self._is_connected:
            logging.debug("Client isn't connected to server")
            self._connect_to_server()
            logging.info("Client Connected")

        encoded_msg = msg.to_json().encode("utf-8")
        try:
            self._socket.send(encoded_msg)
            logging.info(f"[CLIENT] Client sent msg: {msg}")
            response = self._socket.recv(1024).decode("utf-8")
            logging.info(f"[SERVER] {response}")
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            self.disconnect()
