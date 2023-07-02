from PySide6 import QtCore, QtGui, QtWidgets

from .LabelButton import LabelBtnWidget, LabelBtnWidgetPrivate
from .SetStyle import ColorStyle, FontStyle


class StatusWidget(QtWidgets.QWidget):
    def __init__(self, main_win, parent=None):
        super().__init__(parent=parent)

        self.first_widget_size = None

        self.status_list = [
            "何も持っていません",
            "フルーツを持っています",
            "ホイップを持っています",
            "ホイップ戻し中",
            "ホイップ絞り中",
        ]

        self.status_layout = QtWidgets.QVBoxLayout(self)
        self.status_layout.setContentsMargins(0, 10, 0, 5)
        self.status_layout.setSpacing(10)

        for i, status in enumerate(self.status_list):
            status_label = StatusWidgetPrivate(status, main_win, self)
            self.status_layout.addWidget(status_label)


class StatusWidgetPrivate(QtWidgets.QLabel, ColorStyle):
    def __init__(self, text, main_win, parent=None):
        super().__init__(parent=parent)
        ColorStyle.__init__(self)

        self.main_win = main_win
        self.base_font_size = 16
        self.base_widget_size = None

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText(text)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        if not self.base_widget_size:
            self.base_widget_size = self.size()
            self.main_win.send_state.connect(self.check_status_signal)

        scale = (
            self.width() / self.base_widget_size.width(),
            self.height() / self.base_widget_size.height(),
        )
        scale = min(scale)

        self.status_off_style = f"""
        QLabel{{
            color: rgba(139, 116, 100, 130);
            background-color: rgba(235, 232, 230, 100);
            border-style: solid;
            border-width: 3px;
            border-color: rgba(235, 232, 230, 150);
            border-radius: %spx
        }}
        """ % (
            self.height() * 0.4
        )

        self.status_on_style = f"""
        QLabel{{
            color: rgb(85, 65, 51);
            background-color: rgba(255, 237, 213, 150);
            border-style: solid;
            border-width: 3px;
            border-color: rgba(255, 237, 213, 250);
            border-radius: %spx
        }}
        """ % (
            self.height() * 0.4
        )

        self.setStyleSheet(self.status_off_style)

        if self.text() == "何も持っていません":
            self.setStyleSheet(self.status_on_style)

        _font = self.button_font
        _font.setPointSizeF(self.base_font_size * scale)
        self.setFont(_font)

    def check_status_signal(self, data):
        if data["pickup_cream"]:
            if data["pickup_cream"]["state"]:
                if self.text() == "何も持っていません":
                    self.setStyleSheet(self.status_off_style)
                if data["pickup_cream"]["state"] == "open":
                    if self.text() == "ホイップを持っています":
                        self.setStyleSheet(self.status_on_style)
                    elif self.text() == "ホイップ絞り中":
                        if data["cream"]:
                            self.setStyleSheet(self.status_on_style)
                        else:
                            self.setStyleSheet(self.status_off_style)
                    if self.text() == "フルーツを持っています":
                        self.setStyleSheet(self.status_off_style)
                elif data["pickup_cream"]["state"] == "grip":
                    if self.text() == "ホイップを持っています":
                        self.setStyleSheet(self.status_off_style)
                    elif self.text() == "ホイップ戻し中":
                        self.setStyleSheet(self.status_on_style)
                    if self.text() == "フルーツを持っています":
                        self.setStyleSheet(self.status_off_style)
                    self.check = True
            elif data["pickup_cream"]["state"] == None:
                if self.text() == "ホイップ戻し中":
                    self.setStyleSheet(self.status_off_style)
                if data["grip"] == 0:
                    if self.text() == "フルーツを持っています":
                        self.setStyleSheet(self.status_off_style)
                    elif self.text() == "何も持っていません":
                        self.setStyleSheet(self.status_on_style)
                    self.check = False
                elif data["grip"] == 1:
                    if self.check:
                        if self.text() == "フルーツを持っています":
                            self.setStyleSheet(self.status_off_style)
                        elif self.text() == "何も持っていません":
                            self.setStyleSheet(self.status_on_style)
                    if not self.check:
                        self.check = False
                        if self.text() == "フルーツを持っています":
                            self.setStyleSheet(self.status_on_style)
                        elif self.text() == "何も持っていません":
                            self.setStyleSheet(self.status_off_style)
        else:
            if data["grip"] == 0:
                if self.text() == "フルーツを持っています":
                    self.setStyleSheet(self.status_off_style)
                elif self.text() == "何も持っていません":
                    self.setStyleSheet(self.status_on_style)
            elif data["grip"] == 1:
                if self.text() == "フルーツを持っています":
                    self.setStyleSheet(self.status_on_style)
                elif self.text() == "何も持っていません":
                    self.setStyleSheet(self.status_off_style)
