import pickle
import socket

from getkey import getkey

SERVER_ADDRESS = ("127.0.0.1", 8890)


class KeyGUI:
    def __init__(self):
        self.key_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def update(self):
        while True:
            try:
                key = getkey()
                print(key)
                if key == "w":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "front"}), SERVER_ADDRESS
                    )
                elif key == "s":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "back"}), SERVER_ADDRESS
                    )
                elif key == "a":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "left"}), SERVER_ADDRESS
                    )
                elif key == "d":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "right"}), SERVER_ADDRESS
                    )
                elif key == " ":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "up"}),
                        SERVER_ADDRESS,
                    )
                elif key == "g":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "grip"}), SERVER_ADDRESS
                    )
                elif key == "h":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "g_open"}), SERVER_ADDRESS
                    )
                elif key == "c":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "cake"}), SERVER_ADDRESS
                    )
                elif key == "f":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "fruit"}), SERVER_ADDRESS
                    )
                elif key == "3":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "height_slider", "bool": 30}),
                        SERVER_ADDRESS,
                    )
                elif key == "5":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "height_slider", "bool": 50}),
                        SERVER_ADDRESS,
                    )
                elif key == "8":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "height_slider", "bool": 80}),
                        SERVER_ADDRESS,
                    )
                elif key == "e":
                    self.key_sock.sendto(
                        pickle.dumps({"Button": "micro", "bool": (0.8, 0.8)}),
                        SERVER_ADDRESS,
                    )

            except KeyboardInterrupt:
                exit()


if __name__ == "__main__":
    key_gui = KeyGUI()
    key_gui.update()
