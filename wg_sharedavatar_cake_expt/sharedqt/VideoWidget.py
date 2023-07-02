from PySide6 import QtCore, QtGui, QtWidgets

from . import ImagePath as IP
from .SetStyle import ColorStyle


class VideoFrame(QtWidgets.QLabel):
    def __init__(self, main_win: QtWidgets.QApplication, parent: QtWidgets.QWidget):
        super().__init__(parent=parent)

        self.main_win = main_win

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(11, 11, 11, 0)

        left_layout = QtWidgets.QVBoxLayout()
        right_layout = QtWidgets.QVBoxLayout()

        layout.addLayout(left_layout, 2)
        layout.addLayout(right_layout, 1)

        self.per_y = 0.55
        self.micro_video = VideoWidget("micro", self.main_win, self.per_y, parent=self)
        self.fruit_video = VideoWidget("fruit", self.main_win, parent=self)
        self.cake_video = VideoWidget("cake", self.main_win, parent=self)

        left_layout.addWidget(self.micro_video)
        right_layout.addWidget(self.cake_video)
        right_layout.addWidget(self.fruit_video)


class VideoWidget(QtWidgets.QLabel):
    def __init__(self, name, main_win: QtWidgets.QApplication, per_y=None, parent=None):
        super().__init__(parent=parent)

        self.name = name
        self.per_y = per_y
        self.setWidgetFlag = False

        self.private_widget = VideoWidgetPrivate(
            self.name, main_win, self.per_y, parent=self
        )

    def resizeEvent(self, event):
        if not self.setWidgetFlag:
            self.private_widget.init_pixmap()
            self.private_widget.resize_signal.connect(self.__get_resize_signal)
            self.setWidgetFlag = True

        self.private_widget.move(
            self.width() / 2 - self.private_widget.width() / 2,
            self.height() / 2 - self.private_widget.height() / 2,
        )
        self.private_widget.resize(
            self.private_widget.loading_image.scaled(
                event.size(), QtCore.Qt.KeepAspectRatio
            ).size()
        )

    @QtCore.Slot(object)
    def __get_resize_signal(self, event):
        self.resizeEvent(event)


class VideoWidgetPrivate(QtWidgets.QLabel, ColorStyle):
    resize_signal = QtCore.Signal(object)

    def __init__(self, name, main_win: QtWidgets.QApplication, per_y, parent=None):
        super().__init__(parent=parent)
        ColorStyle.__init__(self)

        self.name = name
        self.main_win = main_win
        self.per_y = per_y
        self.message = {}
        self.setScaledContents(True)
        self.setAlignment(QtCore.Qt.AlignCenter)

        if self.name == "micro":
            self.crosshair_widget = CrosshairWidget(self.per_y, parent=self)

        self.video_update_timer = QtCore.QTimer(self)
        self.video_update_timer.timeout.connect(self.update_video)
        self.video_update_timer.start()

    def init_pixmap(self):
        self.loading_image = QtGui.QPixmap(IP.LOADING_FIG_PATH)
        self.loading_image = self.loading_image.scaled(
            self.parentWidget().size(),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )

        self.resize(self.loading_image.size())
        self.setPixmap(self.loading_image)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        self.resize_signal.emit(event)

        if self.name == "micro":
            self.crosshair_widget.get_parent_size.emit(self.size())

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        def __on_time():
            self.setGraphicsEffect(None)

        self.color_effect = QtWidgets.QGraphicsColorizeEffect()
        self.color_effect.setColor(
            QtGui.QColor(
                self.pos_btn_on_color[0],
                self.pos_btn_on_color[1],
                self.pos_btn_on_color[2],
                50,
            )
        )
        self.setGraphicsEffect(self.color_effect)
        QtCore.QTimer.singleShot(150, __on_time)

        if self.name in ["fruit", "cake"]:
            self.message = {"Button": self.name, "bool": True}
        elif self.name == "micro":
            pos_micro_per_x = (event.position().x() - self.width() / 2) / (
                self.width() / 2
            )
            if event.position().y() < self.height() * self.per_y:
                pos_micro_per_y = (
                    self.height() * self.per_y - event.position().y()
                ) / (self.height() * self.per_y)
            elif event.position().y() >= self.height() * self.per_y:
                pos_micro_per_y = -(
                    1
                    - (
                        self.height() * (1 - self.per_y)
                        - (event.position().y() - self.height() * self.per_y)
                    )
                    / (self.height() * (1 - self.per_y))
                )
            self.message = {
                "Button": self.name,
                "bool": (pos_micro_per_x, pos_micro_per_y),
            }

        self.main_win.on_signal.emit(self)

        return super().mousePressEvent(event)

    def update_video(self):
        if "micro" == self.name:
            try:
                frame = self.main_win.core.micro_video_queue.get(block=False)
                self.setPixmap(frame)
            except:
                pass
        elif "fruit" == self.name:
            try:
                frame = self.main_win.core.fruit_video_queue.get(block=False)
                self.setPixmap(frame)
            except:
                pass
        elif "cake" == self.name:
            try:
                frame = self.main_win.core.cake_video_queue.get(block=False)
                self.setPixmap(frame)
            except:
                pass


class CrosshairWidget(QtWidgets.QLabel, ColorStyle):
    get_parent_size = QtCore.Signal(object)

    def __init__(self, per_y, parent):
        super().__init__(parent=parent)
        ColorStyle.__init__(self)

        self.per_y = per_y
        self.crosshair_size_per = 0.02

        self.get_parent_size.connect(self.resizeBaseSize)

    @QtCore.Slot(object)
    def resizeBaseSize(self, size: QtCore.QSize):
        self.crosshair_base_style = f"""
        QLabel{{
            background-color: transparent;
            min-width: %spx;
            min-height: %spx;
            max-width: %spx;
            max-height: %spx;
        }}
        """ % (
            size.width(),
            size.height(),
            size.width(),
            size.height(),
        )

        self.setStyleSheet(self.crosshair_base_style)

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.setPen(self.button_border_pen)

        self.crosshair_size = self.parentWidget().width() * self.crosshair_size_per
        painter.drawLine(
            self.parentWidget().width() / 2 - self.crosshair_size / 2,
            self.parentWidget().height() * self.per_y,
            self.parentWidget().width() / 2 + self.crosshair_size / 2,
            self.parentWidget().height() * self.per_y,
        )
        painter.drawLine(
            self.parentWidget().width() / 2,
            self.parentWidget().height() * self.per_y - self.crosshair_size / 2,
            self.parentWidget().width() / 2,
            self.parentWidget().height() * self.per_y + self.crosshair_size / 2,
        )
