import pickle
import socket
import threading
import time
from queue import Queue

from loggle import logger


class UDP_Server(threading.Thread):
    def __init__(self, port=8080):
        threading.Thread.__init__(self, daemon=True)

        self.message = None
        self.queue = Queue()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", port))

    def run(self):
        while True:
            try:
                self.message = None
                message, cli_addr = self.sock.recvfrom(4096)
                if message:
                    self.message = pickle.loads(message)
                    self.queue.put(self.message)
                time.sleep(0.001)
            except:
                pass
