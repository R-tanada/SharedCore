import pickle
import socket
import threading
import time

import pyqtgraph as pg
import pyqtgraph.opengl as gl


class UDP_Server(threading.Thread):
    def __init__(self, port=8080):
        threading.Thread.__init__(self, daemon=True)

        self.message = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", port))

    def run(self):
        while True:
            try:
                self.message = None
                message, cli_addr = self.sock.recvfrom(1024)
                if message:
                    self.message = pickle.loads(message)
                time.sleep(0.001)
            except:
                pass


def update():
    if data_server.message:
        pos_list.append(data_server.message)
        plot_item.setData(pos=pos_list)


pos_list = []

data_server = UDP_Server(port=8585)
data_server.start()


app = pg.mkQApp("Qt_App")
w = gl.GLViewWidget()
w.show()
w.setWindowTitle("Visualize_Pos_App")
w.setCameraPosition(distance=800)
w.setCameraParams(fov=90, elevation=50)

gx = gl.GLGridItem()
gx.rotate(90, 0, 1, 0)
gx.translate(0, 0, 0)
w.addItem(gx)
gy = gl.GLGridItem()
gy.rotate(90, 1, 0, 0)
gy.translate(0, 0, 0)
w.addItem(gy)
gz = gl.GLGridItem()
gz.translate(0, 0, 0)
w.addItem(gz)

plot_item = gl.GLScatterPlotItem(size=6)
w.addItem(plot_item)

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0.001)

if __name__ == "__main__":
    pg.exec()
