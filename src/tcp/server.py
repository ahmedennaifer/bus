import socket
import logging
import time

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Server:
    def __init__(self, host="localhost", port=8080, buffer_size=1024):
        self._host = host
        self._port = port
        self._BUFFER_SIZE = buffer_size
        # AF_INET = ipv4, SOCK_STREAM = tcp
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._init()
        self._raw_messages = []

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
                        f"[SERVER] Receieved {client_data.decode('utf-8')}. Sending response..."
                    )
                    self._raw_messages.append(client_data)
                    try:
                        client_socket.send("message received".encode("utf-8"))
                    except Exception as e:
                        logging.error(f"Error sending msg to client: {e}")

            except KeyboardInterrupt:
                logging.info("Server shutting down...")
                time.sleep(0.5)
                break

            except Exception as e:
                logging.error(f"Error on run: {e}")
