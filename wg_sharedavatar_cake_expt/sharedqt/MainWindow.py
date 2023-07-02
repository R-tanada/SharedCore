import os
from queue import Queue

from corepy import CoreClient
from PySide6 import QtCore, QtGui, QtWidgets
from sharedqt.PartnerCursor import CursorLabel

from .SetStyle import ColorStyle


class CoreClient(CoreClient):
    def __init__(self, server_ip: str, client_ip: str, services: list, base_alias: str):
        super().__init__(server_ip, client_ip, services, base_alias)

        self.cursor_pos = [0, 0]
        self.cursor_pressed = False

        self.grip_state = False
        self.cream_state = False
        self.open_state = False
        self.table_state = 0
        self.button_anim = False
        self.button_state = "fruit"
        self.robot_height = 50
        self.pickup_cream_state = False

        self.micro_video_queue = Queue(maxsize=256)
        self.fruit_video_queue = Queue(maxsize=256)
        self.cake_video_queue = Queue(maxsize=256)

        self.core_resource.subscribe_video("micro-camera-RGB")
        self.core_resource.subscribe_video("fruit-camera-RGB")
        self.core_resource.subscribe_video("cake-camera-RGB")
        self.core_resource.subscribe_data("server-data", "robot-height")
        self.core_resource.subscribe_data("server-data", "cursor")
        self.core_resource.subscribe_data("server-data", "cursor-pressed")
        self.core_resource.subscribe_data("server-data", "robot-position")
        self.core_resource.subscribe_data("server-data", "grip-state")
        self.core_resource.subscribe_data("server-data", "table-state")
        self.core_resource.subscribe_data("server-data", "button-state")
        self.core_resource.subscribe_data("server-data", "robot-height")
        self.core_resource.subscribe_data("server-data", "pickup_cream")

    def on_resource_frame_arrived(self, type, resource, channel, frame):
        super().on_resource_frame_arrived(type, resource, channel, frame)
        if type == "video":
            self.__on_video_frame_arrived(resource, frame)
        elif type == "data":
            self.__on_data_frame_arrived(resource, channel, self.receive_data)

    def __on_data_frame_arrived(self, resource, channel, frame):
        data = frame
        if channel == "cursor":
            if not data["user"] == self.client_id:
                CursorLabel.cursor_pos = [data["x"], data["y"]]

        elif channel == "cursor-pressed":
            if not data["user"] == self.client_id:
                CursorLabel.cursor_pressed = data["pressed"]

        elif channel == "grip-state":
            if data["Button"] == "grip":
                self.grip_state = data["state"]

            elif data["Button"] == "cream":
                self.cream_state = data["state"]

            elif data["Button"] == "open":
                self.open_state = data["state"]

        elif channel == "table-state":
            self.table_state = data["state"]

        elif channel == "button-state":
            if not data["user"] == str(self.client_id):
                self.button_state = data["state"]

        elif channel == "robot-height":
            self.robot_height = data["per-z"]

        elif channel == "pickup_cream":
            self.pickup_cream_state = data

    def __on_video_frame_arrived(self, resource, frame):
        image = QtGui.QImage(
            frame.pixel_data.tobytes(),
            frame.width,
            frame.height,
            QtGui.QImage.Format_RGB888,
        )
        pixmap = QtGui.QPixmap.fromImage(image)
        if "micro" in resource:
            self.micro_video_queue.put(pixmap)
        elif "fruit" in resource:
            self.fruit_video_queue.put(pixmap)
        elif "cake" in resource:
            self.cake_video_queue.put(pixmap)


class MainWin(QtWidgets.QMainWindow, ColorStyle):
    on_signal = QtCore.Signal(object)
    send_height = QtCore.Signal(int)
    send_state = QtCore.Signal(dict)
    send_table_state = QtCore.Signal(int)
    send_button_state = QtCore.Signal(str)

    def __init__(self, settings):
        super().__init__()
        ColorStyle.__init__(self)

        self.core = CoreClient(
            server_ip=settings["CoreSDK"]["SERVER_IP"],
            client_ip=settings["CoreSDK"]["CLIENT_IP"],
            services=["config/core_client_services.json"],
            base_alias="Client",
        )

        self.setWindowTitle(os.path.basename(__file__))
        self.setMouseTracking(True)
        self.setStyleSheet(
            "background-color: rgb(%s,%s,%s)"
            % self.main_window_background_color.getRgb()[:-1]
        )

        self.first_win_width = 1280
        self.first_win_ratio = 0.63
        self.resize(self.first_win_width, self.first_win_width * self.first_win_ratio)

        screen = QtWidgets.QApplication.primaryScreen()
        self.move(screen.size().width() / 2 - self.first_win_width / 2, 0)

        minimum_win_scale = 0.4
        self.setMinimumSize(
            self.first_win_width * minimum_win_scale,
            self.first_win_width * self.first_win_ratio * minimum_win_scale,
        )

        self.old_height = 50
        self.button_state = "fruit"
        self.old_cursor_pos_per = (0, 0)

        self.on_signal.connect(self.get_signal)

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.__update)
        self.update_timer.start(1)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        scale_width = self.width() / self.first_win_width
        scale_height = self.height() / (self.first_win_width * self.first_win_ratio)
        self.window_scale = min(scale_width, scale_height)
        CursorLabel.scale = self.window_scale
        CursorLabel.win_size = (self.width(), self.height())
        return super().resizeEvent(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent, message=None):
        self.core.core_write_data(
            "client-data-%s" % self.core.client_id,
            "cursor-pressed",
            {"pressed": True},
        )
        return super().mousePressEvent(event)

    @QtCore.Slot(object)
    def get_signal(self, widget):
        self.core.core_write_data(
            "client-data-%s" % self.core.client_id, "command", widget.message
        )

    def __update(self):
        if self.core.robot_height != self.old_height:
            self.send_height.emit(self.core.robot_height)
            self.old_height = self.core.robot_height

        self.send_state.emit(
            {
                "grip": self.core.grip_state,
                "cream": self.core.cream_state,
                "open": self.core.open_state,
                "pickup_cream": self.core.pickup_cream_state,
            }
        )

        if self.core.button_state:
            self.send_button_state.emit(self.core.button_state)
            self.core.button_state = None

        if not self.core.table_state == None:
            self.send_table_state.emit(self.core.table_state)
            self.core.table_state = None

        self.__get_cursor_pos()

    def __get_cursor_pos(self):
        self.cursor_pos = self.mapFromGlobal(QtGui.QCursor.pos())
        self.window_size = self.geometry()

        if self.cursor_pos.x() > 0 and self.cursor_pos.y() > 0:
            if (
                self.cursor_pos.x() < self.window_size.width()
                and self.cursor_pos.y() < self.window_size.height()
            ):
                self.cursor_pos_per_x = self.cursor_pos.x() / self.window_size.width()
                self.cursor_pos_per_y = self.cursor_pos.y() / self.window_size.height()

                if not (
                    self.cursor_pos_per_x == self.old_cursor_pos_per[0]
                    and self.cursor_pos_per_y == self.old_cursor_pos_per[1]
                ):
                    message = {"x": self.cursor_pos_per_x, "y": self.cursor_pos_per_y}
                    self.core.core_write_data(
                        "client-data-%s" % self.core.client_id, "cursor", message
                    )

                self.old_cursor_pos_per = (self.cursor_pos_per_x, self.cursor_pos_per_y)

    def closeEvent(self, event):
        self.core.core_stop()
        event.accept()
