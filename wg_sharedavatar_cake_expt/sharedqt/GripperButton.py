from PySide6 import QtCore, QtGui, QtWidgets

from . import ImagePath as IP
from .LabelButton import LabelBtnWidget, LabelBtnWidgetPrivate
from .SetStyle import ColorStyle, FontStyle


class GripperBtnWidget(QtWidgets.QWidget):
    def __init__(self, main_win, parent=None):
        super().__init__(parent=parent)

        self.widget_layout = QtWidgets.QGridLayout(self)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)

        self.mode_toggle = ToggleBtnWidget(main_win=main_win, parent=self)
        self.grip_widget = GripperBtnStacked(main_win=main_win, parent=self)

        self.widget_layout.addWidget(self.mode_toggle, 0, 0, 1, 2)
        self.widget_layout.addWidget(self.grip_widget, 1, 0, 2, 2)

        self.mode_toggle.mode_signal.connect(self.__get_mode)

    def __get_mode(self, mode):
        self.grip_widget.check_mode.emit(mode)


class ToggleBtnWidget(QtWidgets.QLabel):
    mode_signal = QtCore.Signal(str)

    def __init__(self, main_win, parent=None):
        super().__init__(parent=parent)

        self.main_win = main_win
        self.toggle_widget_private = ToggleBtnWidgetPrivate(main_win, parent=self)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        self.toggle_widget_private.draw(painter)

    def mousePressEvent(self, event):
        self.toggle_widget_private.get_mouse_pos.emit(event)
        return super().mousePressEvent(event)


class ToggleBtnWidgetPrivate(QtWidgets.QWidget, ColorStyle):
    get_mouse_pos = QtCore.Signal(object)

    def __init__(self, main_win, parent=None):
        super().__init__(parent=parent)
        ColorStyle.__init__(self)

        self.first_widget_size = None
        self.parent_widget = parent

        self.toggle_anim = ToggleAnim(main_win, parent=parent)

        self.get_mouse_pos.connect(self.press_event)

    def draw(self, painter: QtGui.QPainter):
        if not self.first_widget_size:
            self.first_widget_size = self.parentWidget().size()

        widget_size = self.parentWidget().size()

        self.toggle_anim.draw_toggle(widget_size, painter)

    def press_event(self, event):
        _mode = self.toggle_anim.determine_inside(event)
        self.parent_widget.mode_signal.emit(_mode)


class ToggleAnim(QtCore.QObject, ColorStyle, FontStyle):
    def __init__(self, main_win, parent=None):
        super().__init__(parent=parent)
        ColorStyle.__init__(self)
        FontStyle.__init__(self)

        self.main_win = main_win
        self.btn_parent = parent

        self.strawberry_brown_pixmap = QtGui.QPixmap(IP.STRAWBERRY_BROWN_FIG_PATH)
        self.base_strawberry_brown_pixmap = self.strawberry_brown_pixmap.scaled(
            self.strawberry_brown_pixmap.size() * 0.3,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )

        self.strawberry_white_pixmap = QtGui.QPixmap(IP.STRAWBERRY_WHITE_FIG_PATH)
        self.base_strawberry_white_pixmap = self.strawberry_white_pixmap.scaled(
            self.strawberry_white_pixmap.size() * 0.3,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )

        self.cupcake_brown_pixmap = QtGui.QPixmap(IP.CUPCAKE_BROWN_FIG_PATH)
        self.base_cupcake_brown_pixmap = self.cupcake_brown_pixmap.scaled(
            self.cupcake_brown_pixmap.size() * 0.3,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )

        self.cupcake_white_pixmap = QtGui.QPixmap(IP.CUPCAKE_WHITE_FIG_PATH)
        self.base_cupcake_white_pixmap = self.cupcake_white_pixmap.scaled(
            self.cupcake_white_pixmap.size() * 0.3,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )

        self._animValue = 0.0
        self.anim = QtCore.QPropertyAnimation(self)
        self.anim.setTargetObject(self)
        self.anim.setPropertyName(b"press")
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.anim.finished.connect(self.btn_parent.update())

        self.anim_off_background = QtGui.QColor(235, 232, 230)
        self.base_font_size = self.toggle_widget_font_size
        self.base_widget_size = None

        self._animColor = self.button_border_color
        self.color_anim = QtCore.QPropertyAnimation(self)
        self.color_anim.setTargetObject(self)
        self.color_anim.setPropertyName(b"color")
        self.color_anim.setStartValue(self.button_border_color)
        self.color_anim.setEndValue(self.anim_off_background)
        self.color_anim.setDuration(200)
        self.color_anim.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.color_anim.finished.connect(self.btn_parent.update())

        self._animColor_back = self.anim_off_background
        self.color_anim_back = QtCore.QPropertyAnimation(self)
        self.color_anim_back.setTargetObject(self)
        self.color_anim_back.setPropertyName(b"color_back")
        self.color_anim_back.setStartValue(self.anim_off_background)
        self.color_anim_back.setEndValue(self.button_border_color)
        self.color_anim_back.setDuration(200)
        self.color_anim_back.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.color_anim_back.finished.connect(self.btn_parent.update())

    def draw_toggle(self, widget_size: QtCore.QSize, painter: QtGui.QPainter):
        if not self.base_widget_size:
            self.base_widget_size = widget_size
            self.main_win.send_button_state.connect(self.__check_button_state)

        painter.save()

        self.widget_size = widget_size

        widget_ratio = (
            self.widget_size.width() / self.base_widget_size.width(),
            self.widget_size.height() / self.base_widget_size.height(),
        )
        widget_ratio = min(widget_ratio)

        _font = self.button_font
        _font.setPointSize(int(self.base_font_size * widget_ratio))
        _font.setBold(True)
        painter.setFont(_font)

        painter.setPen(self._animColor)
        painter.setBrush(self._animColor)
        painter.drawRect(
            0,
            widget_size.height() * 0.1 * (1 - self._animValue),
            widget_size.width() / 2,
            widget_size.height() * (1 - 0.1 * (1 - self._animValue)),
        )

        painter.setPen(self._animColor_back)
        painter.setBrush(self._animColor_back)
        painter.drawRect(
            widget_size.width() / 2,
            widget_size.height() * 0.1 * self._animValue,
            widget_size.width() / 2,
            widget_size.height() * (1 - 0.1 * self._animValue),
        )

        if self._animValue > 0.5:
            painter.drawPixmap(
                self.widget_size.width() * 0.18,
                self.widget_size.height() * 0.18,
                self.base_strawberry_brown_pixmap.scaled(
                    self.base_strawberry_brown_pixmap.size() * widget_ratio,
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation,
                ),
            )
        else:
            painter.drawPixmap(
                self.widget_size.width() * 0.18,
                self.widget_size.height() * 0.18,
                self.base_strawberry_white_pixmap.scaled(
                    self.base_strawberry_white_pixmap.size() * widget_ratio,
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation,
                ),
            )

        painter.setPen(self._animColor_back)
        painter.drawText(
            self.widget_size.width() * 0.01, widget_size.height() * 0.9, "フルーツモード"
        )

        if self._animValue < 0.5:
            painter.drawPixmap(
                self.widget_size.width() * 0.68,
                self.widget_size.height() * 0.18,
                self.base_cupcake_brown_pixmap.scaled(
                    self.base_cupcake_brown_pixmap.size() * widget_ratio,
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation,
                ),
            )
        else:
            painter.drawPixmap(
                self.widget_size.width() * 0.68,
                self.widget_size.height() * 0.18,
                self.base_cupcake_white_pixmap.scaled(
                    self.base_cupcake_white_pixmap.size() * widget_ratio,
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation,
                ),
            )

        painter.setPen(self._animColor)
        painter.drawText(
            self.widget_size.width() * 0.51, widget_size.height() * 0.9, "ホイップモード"
        )

        painter.restore()

    @QtCore.Property(float)
    def press(self):
        return self._animValue

    @press.setter
    def press(self, value):
        self._animValue = value
        self.btn_parent.update()

    @QtCore.Property(QtGui.QColor)
    def color(self):
        return self._animColor

    @color.setter
    def color(self, value):
        self._animColor = value

    @QtCore.Property(QtGui.QColor)
    def color_back(self):
        return self._animColor_back

    @color_back.setter
    def color_back(self, value):
        self._animColor_back = value

    @QtCore.Slot(bool, name="animate")
    def animate(self, check):
        self.color_anim.setDirection(
            QtCore.QPropertyAnimation.Forward
            if check
            else QtCore.QPropertyAnimation.Backward
        )
        self.color_anim.start()
        self.color_anim_back.setDirection(
            QtCore.QPropertyAnimation.Forward
            if check
            else QtCore.QPropertyAnimation.Backward
        )
        self.color_anim_back.start()
        self.anim.setDirection(
            QtCore.QPropertyAnimation.Forward
            if check
            else QtCore.QPropertyAnimation.Backward
        )
        self.anim.start()

    def determine_inside(self, event: QtCore.QEvent):
        if self.main_win.button_state == "fruit":
            if event.position().x() > self.widget_size.width() / 2:
                self.animate(True)

                self.main_win.button_state = "cream"
                self.message = {"state": "cream"}
                self.main_win.core.core_write_data(
                    "client-data-%s" % self.main_win.core.client_id,
                    "button-state",
                    self.message,
                )

                return self.main_win.button_state

        elif self.main_win.button_state == "cream":
            if event.position().x() < self.widget_size.width() / 2:
                self.animate(False)

                self.main_win.button_state = "fruit"
                self.message = {"state": "fruit"}
                self.main_win.core.core_write_data(
                    "client-data-%s" % self.main_win.core.client_id,
                    "button-state",
                    self.message,
                )

                return self.main_win.button_state

    def __check_button_state(self, state):
        if state == "fruit":
            self.animate(False)
        elif state == "cream":
            self.animate(True)

        self.btn_parent.mode_signal.emit(state)


class GripperBtnStacked(QtWidgets.QWidget):
    check_mode = QtCore.Signal(str)

    def __init__(self, main_win, parent=None):
        super().__init__(parent=parent)

        self.setStacked = False

        self.mode_layout = QtWidgets.QStackedLayout(self)

        self.fruit_widget = FruitWidget(main_win, parent=self)
        self.cream_widget = CreamWidget(main_win, parent=self)

        self.mode_layout.addWidget(self.cream_widget)
        self.mode_layout.addWidget(self.fruit_widget)

        self.check_mode.connect(self.__check_grip_mode)

    def resizeEvent(self, event):
        if not self.setStacked:
            self.mode_layout.setCurrentWidget(self.fruit_widget)
            self.setStacked = True

    def __check_grip_mode(self, mode):
        self.__set_mode_widget(mode)

    def __set_mode_widget(self, mode):
        if mode == "fruit":
            self.mode_layout.setCurrentWidget(self.fruit_widget)
        elif mode == "cream":
            self.mode_layout.setCurrentWidget(self.cream_widget)


class FruitWidget(QtWidgets.QLabel):
    def __init__(self, main_win, parent=None):
        super().__init__(parent=parent)

        self.fruit_layout = QtWidgets.QHBoxLayout(self)
        self.fruit_layout.setContentsMargins(0, 0, 0, 0)

        self.open_widget = FruitBtnWidget(
            "g_open", "開く", IP.OPEN_FIG_PATH, main_win, parent=self
        )
        self.close_widget = FruitBtnWidget(
            "grip", "閉じる", IP.CLOSE_FIG_PATH, main_win, parent=self
        )

        self.fruit_layout.addWidget(self.open_widget)
        self.fruit_layout.addWidget(self.close_widget)


class FruitBtnWidget(LabelBtnWidget, FontStyle):
    def __init__(self, name, text, file_path, main_win, parent=None):
        super().__init__(name=name, main_win=main_win, parent=parent)
        FontStyle.__init__(self)

        self.private_1 = LabelBtnWidgetPrivate()
        self.private_1.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.private_1.base_fig_scale = 0.03
        self.private_1.fig_pixmap = QtGui.QPixmap(file_path)
        self.private_1.setFigSize()

        self.private_2 = LabelBtnWidgetPrivate()
        self.private_2.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.private_2.base_font_size = self.fruit_font_size
        self.private_2.setFontSize()
        self.private_2.setText(text)

        self.btn_layout.setSpacing(15)
        self.btn_layout.addWidget(self.private_1, 0, 0, 5, 1)
        self.btn_layout.addWidget(self.private_2, 5, 0, 4, 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.private_1.get_scale.emit(self.btn_scale)
        self.private_2.get_scale.emit(self.btn_scale)


class CreamWidget(QtWidgets.QLabel):
    def __init__(self, main_win, parent=None):
        super().__init__(parent=parent)

        self.cream_layout = QtWidgets.QGridLayout(self)
        self.cream_layout.setContentsMargins(0, 0, 0, 0)

        self.cream_1 = CreamBtnWidget("cream_1", ["ホイップ", "1"], main_win, parent=self)
        self.cream_2 = CreamBtnWidget("cream_2", ["ホイップ", "2"], main_win, parent=self)
        self.squeeze = SqueezeBtnWidget("squeeze", main_win, parent=self)

        self.cream_layout.addWidget(self.cream_1, 0, 0, 1, 1)
        self.cream_layout.addWidget(self.cream_2, 1, 0, 1, 1)
        self.cream_layout.addWidget(self.squeeze, 0, 1, 2, 1)


class CreamBtnWidget(LabelBtnWidget, FontStyle):
    def __init__(self, name, text, main_win, parent=None):
        super().__init__(name=name, main_win=main_win, parent=parent)
        FontStyle.__init__(self)

        self.private_1 = LabelBtnWidgetPrivate()
        self.private_1.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.private_1.base_font_size = self.cream_private1_font_size
        self.private_1.setFontSize()
        self.private_1.setText(text[0])

        self.private_2 = LabelBtnWidgetPrivate()
        self.private_2.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.private_2.base_font_size = self.cream_private2_font_size
        self.private_2.setFontSize()
        self.private_2.setFontBold()
        self.private_2.setText(text[1])

        self.btn_layout.setSpacing(3)
        self.btn_layout.addWidget(self.private_1, 0, 0, 1, 1)
        self.btn_layout.addWidget(self.private_2, 1, 0, 1, 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.private_1.get_scale.emit(self.btn_scale)
        self.private_2.get_scale.emit(self.btn_scale)


class SqueezeBtnWidget(LabelBtnWidget, FontStyle):
    def __init__(self, name, main_win, parent=None):
        super().__init__(name, main_win, parent)
        FontStyle.__init__(self)

        self.squeeze_state = False

        self.private_1 = LabelBtnWidgetPrivate()
        self.private_1.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.private_1.base_font_size = self.squeeze_private1_font_size
        self.private_1.setFontSize()
        self.private_1.setText("しぼる")

        self.private_2 = LabelBtnWidgetPrivate()
        self.private_2.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.private_2.base_font_size = self.squeeze_private2_font_size
        self.private_2.setFontSize()
        self.private_2.setFontBold()
        self.private_2.setText("スタート")

        self.btn_layout.setSpacing(10)
        self.btn_layout.addWidget(self.private_1, 0, 0, 1, 1)
        self.btn_layout.addWidget(self.private_2, 1, 0, 1, 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.private_1.get_scale.emit(self.btn_scale)
        self.private_2.get_scale.emit(self.btn_scale)

    def mousePressEvent(self, event):
        if self.squeeze_state:
            self.private_2.setText("スタート")
            self.squeeze_state = False
        else:
            self.private_2.setText("ストップ")
            self.squeeze_state = True
        super().mousePressEvent(event)
