import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets


class ColorStyle:
    def __init__(self):
        self.main_window_background_color = QtGui.QColor(252, 250, 248)

        self.button_border_color = QtGui.QColor(249, 115, 21)
        self.button_border_width = 2
        self.button_border_pen = QtGui.QPen(
            self.button_border_color, self.button_border_width, QtCore.Qt.SolidLine
        )

        self.button_font_size = 14
        self.button_font = QtGui.QFont(
            "Arial", self.button_font_size, weight=QtGui.QFont.Normal
        )
        self.button_font_color = QtGui.QColor(139, 116, 100)

        self.button_hover_color = QtGui.QColor.fromRgbF(255, 217, 127, 0.2)

        self.pos_btn_color = np.array([252, 250, 248])
        self.pos_btn_on_color = np.array([249, 115, 21])

        self.button_style = f"""
        QLabel#parent{{
            background-color: rgb%s;
            border-style: solid;
            border-width: %s;
            border-color: rgb%s;
        }}
        """ % (
            self.main_window_background_color.getRgb()[:-1],
            self.button_border_width,
            self.button_border_color.getRgb()[:-1],
        )

    def setBtnPress(self, widget: QtWidgets.QLabel, event):
        def __on_time():
            widget.setGraphicsEffect(None)

        self.color_effect = QtWidgets.QGraphicsColorizeEffect()
        self.color_effect.setColor(
            QtGui.QColor(
                self.pos_btn_on_color[0],
                self.pos_btn_on_color[1],
                self.pos_btn_on_color[2],
            )
        )
        widget.setGraphicsEffect(self.color_effect)
        QtCore.QTimer.singleShot(150, __on_time)


class FontStyle:
    def __init__(self):
        self.pos_btn_font_size = 32

        self.height_widget_font_size = 20
        self.slider_value_font_size = 26
        self.height_push_btn_font_size = 38

        self.rotate_private1_font_size = 22
        self.rotate_private2_font_size = 32

        self.roll_private1_font_size = 20

        self.toggle_widget_font_size = 15

        self.fruit_font_size = 12

        self.cream_private1_font_size = 18
        self.cream_private2_font_size = 32

        self.squeeze_private1_font_size = 22
        self.squeeze_private2_font_size = 24
