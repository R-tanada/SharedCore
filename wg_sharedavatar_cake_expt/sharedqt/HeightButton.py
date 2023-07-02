from PySide6 import QtCore, QtGui, QtWidgets

from .LabelButton import LabelBtnWidget, LabelBtnWidgetPrivate
from .SetStyle import ColorStyle, FontStyle


class HeightBtnWidget(QtWidgets.QWidget, ColorStyle, FontStyle):
    def __init__(self, main_win: QtWidgets.QApplication, parent=None):
        super().__init__(parent=parent)
        ColorStyle.__init__(self)
        FontStyle.__init__(self)

        layout = QtWidgets.QGridLayout(self)
        layout.setContentsMargins(0, 0, 15, 0)
        layout.setSpacing(15)

        self.base_widget_size = None
        self.base_font_size = self.height_widget_font_size

        self.text_label = QtWidgets.QLabel("高さ")
        _font = self.button_font
        _font.setPointSize(self.base_font_size)
        self.text_label.setFont(_font)
        style = (
            f"""
        color: rgb(%s,%s,%s);
        border-bottom-style: solid;
        border-bottom-width: 2px;
        border-radius: 0px;
        border-color: rgba(139,116,100,50);
        """
            % self.button_font_color.getRgb()[:-1]
        )
        self.text_label.setStyleSheet(style)
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)

        self.height_slider = HeightSliderWidget(main_win, parent=self)
        self.height_push_btn = HeightPushBtnWidget(main_win, parent=self)

        layout.addWidget(self.text_label, 0, 0, 1, 2)
        layout.addWidget(self.height_slider, 1, 0, 30, 1)
        layout.addWidget(self.height_push_btn, 1, 1, 30, 1)

    def resizeEvent(self, event):
        if not self.base_widget_size:
            self.base_widget_size = self.size()

        btn_width_scale = self.width() / self.base_widget_size.width()
        btn_height_scale = self.height() / self.base_widget_size.height()
        self.btn_scale = min(btn_width_scale, btn_height_scale)

        _font_size = self.base_font_size * self.btn_scale
        _font = self.button_font
        _font.setPointSizeF(_font_size)
        self.text_label.setFont(_font)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        return super().mousePressEvent(event)


class HeightSliderWidget(QtWidgets.QLabel):
    def __init__(self, main_win: QtWidgets.QApplication, parent=None):
        super().__init__(parent=parent)

        self.widget_layout = QtWidgets.QHBoxLayout(self)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)

        self.first_value = 50
        self.value_widget = ValueWidget(main_win, parent=self)
        self.slider_widget = SliderWidget(main_win, parent=self)

        self.widget_layout.addWidget(self.value_widget)
        self.widget_layout.addWidget(self.slider_widget)


class SliderWidget(QtWidgets.QLabel, ColorStyle):
    slider_signal = QtCore.Signal(object)

    def __init__(self, main_win, parent):
        super().__init__(parent=parent)
        ColorStyle.__init__(self)

        self.press_pos = QtCore.QPoint(0, 135)
        self.handle_size = [50, 10]

        self.slider = SliderBase(main_win, parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.slider)

        self.handle_color = self.button_border_color
        self.handle_color.setAlphaF(0.5)


class SliderBase(QtWidgets.QSlider, ColorStyle):
    def __init__(self, main_win: QtWidgets.QApplication, parent=None):
        super().__init__(parent=parent)
        ColorStyle.__init__(self)

        slider_style = f"""
        QSlider::add-page:vertical{{
            background-color: #E1D5CB;
            width: 5px;
            border-radius: 3px;
        }}

        QSlider::sub-page:vertical{{
            background-color: #F97315;
            width: 5px;
            border-radius: 3px;
        }}

        QSlider::groove:vertical{{
            background-color: transparent;
            width: 6px;
        }}

        QSlider::handle:vertical{{
            height: 10px;
            width: 15px;
            margin: 0px -15px;
            border-radius: 10px;
            background-color: rgb(139,116,100);
        }}
        """
        self.setStyleSheet(slider_style)

        self.main_win = main_win
        self.parent_widet = parent
        self.pos_y = 0

        self.setOrientation(QtCore.Qt.Vertical)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(self.parent_widet.first_value)
        self.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBothSides)
        self.setTickInterval(10)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.press_pos = event.position()
        sliderValue = (1 - event.position().y() / self.height()) * 100
        self.message = {"Button": "height_slider", "bool": sliderValue}
        self.main_win.on_signal.emit(self)
        self.parent_widet.slider_widget.slider_signal.emit(event)
        self.main_win.core.core_write_data(
            "client-data-%s" % self.main_win.core.client_id,
            "cursor-pressed",
            {"pressed": True},
        )


class ValueWidget(QtWidgets.QLabel, ColorStyle, FontStyle):
    def __init__(self, main_win: QtWidgets.QApplication, parent=None):
        super().__init__(parent=parent)
        ColorStyle.__init__(self)
        FontStyle.__init__(self)

        self.main_win = main_win
        self.parent_widget = parent
        self.slider_value = self.parent_widget.first_value
        self.base_font_size = self.slider_value_font_size
        self.base_widget_size = None
        self.scale = 1

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        if not self.base_widget_size:
            self.base_widget_size = self.size()
            self.main_win.send_height.connect(self.__get_value)

        scale_width = self.width() / self.base_widget_size.width()
        scale_height = self.height() / self.base_widget_size.height()
        self.scale = min(scale_width, scale_height)

        painter.setPen(self.button_font_color)
        _font = self.button_font
        _font.setPointSizeF(self.base_font_size * self.scale)
        painter.setFont(self.button_font)

        painter.drawText(
            self.width() * 0.25,
            self.height() * 0.9 * (1 - 0.01 * self.slider_value) + self.height() * 0.09,
            str(self.slider_value),
        )

        self.update()

    def __get_value(self, value):
        self.slider_value = int(value)
        self.parent_widget.slider_widget.slider.setValue(self.slider_value)


class HeightPushBtnWidget(QtWidgets.QWidget):
    def __init__(self, main_win, parent=None):
        super().__init__(parent=parent)

        self.widget_layout = QtWidgets.QVBoxLayout(self)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_layout.setSpacing(10)

        self.height_plus = HeightPushBtn(main_win, name="up", text="＋", parent=self)

        self.height_minus = HeightPushBtn(main_win, name="down", text="ー", parent=self)

        self.widget_layout.addStretch(1)
        self.widget_layout.addWidget(self.height_plus, 20)
        self.widget_layout.addWidget(self.height_minus, 20)
        self.widget_layout.addStretch(1)


class HeightPushBtn(LabelBtnWidget, FontStyle):
    def __init__(self, main_win, name, text, parent=None):
        super().__init__(name=name, main_win=main_win, parent=parent)
        FontStyle.__init__(self)

        self.private_1 = LabelBtnWidgetPrivate()
        self.private_1.base_font_size = self.height_push_btn_font_size
        self.private_1.setFontSize()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.private_1.setText(text)

        self.btn_layout.addWidget(self.private_1, 0, 0, 1, 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.private_1.get_scale.emit(self.btn_scale)
