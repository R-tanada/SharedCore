from PySide6 import QtCore, QtGui, QtWidgets

from . import ImagePath as IP
from .LabelButton import LabelBtnWidget, LabelBtnWidgetPrivate
from .SetStyle import FontStyle


class RotateBtnWidget(QtWidgets.QWidget):
    def __init__(self, main_win, parent=None):
        super().__init__(parent=parent)

        self.main_win = main_win

        self.widget_layout = QtWidgets.QGridLayout(self)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)

        self.rotate_table = RotateTableWidget("table", main_win, parent=self)
        self.roll_minus = RollBtnWidget(
            "roll_minus", ["反時計回り", "↺"], IP.ROLL_MINUS_FIG_PATH, main_win, parent=self
        )
        self.roll_plus = RollBtnWidget(
            "roll_plus", ["時計周り", "↻"], IP.ROLL_PLUS_FIG_PATH, main_win, parent=self
        )

        self.widget_layout.addWidget(self.rotate_table, 0, 0, 1, 2)
        self.widget_layout.addWidget(self.roll_minus, 1, 0, 2, 1)
        self.widget_layout.addWidget(self.roll_plus, 1, 1, 2, 1)


class RotateTableWidget(LabelBtnWidget, FontStyle):
    def __init__(self, name, main_win, parent=None):
        super().__init__(name=name, main_win=main_win, parent=parent)
        FontStyle.__init__(self)

        self.parent_widget = parent
        self.setSignal = False

        self.private_1 = LabelBtnWidgetPrivate()
        self.private_1.base_font_size = self.rotate_private1_font_size
        self.private_1.setFontSize()
        self.private_1.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.private_1.setText("テーブル回転")

        self.private_2 = LabelBtnWidgetPrivate()
        self.private_2.base_font_size = self.rotate_private2_font_size
        self.private_2.setFontSize()
        self.private_2.setText("スタート")

        self.btn_layout.addWidget(self.private_1, 0, 0, 3, 1)
        self.btn_layout.addWidget(self.private_2, 3, 0, 4, 1)

    def resizeEvent(self, event):
        if not self.setSignal:
            self.parent_widget.main_win.send_table_state.connect(self.__get_table_state)
            self.setSignal = True

        super().resizeEvent(event)

        self.private_1.get_scale.emit(self.btn_scale)
        self.private_2.get_scale.emit(self.btn_scale)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def __get_table_state(self, state):
        if state == 0:
            self.private_2.setText("スタート")
        elif state == 1:
            self.private_2.setText("ストップ")


class RollBtnWidget(LabelBtnWidget, FontStyle):
    def __init__(self, name, text, file_path, main_win, parent=None):
        super().__init__(name=name, main_win=main_win, parent=parent)
        FontStyle.__init__(self)

        self.roll_state = False

        self.btn_layout.setSpacing(10)

        self.private_1 = LabelBtnWidgetPrivate()
        self.private_1.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.private_1.base_font_size = self.roll_private1_font_size
        self.private_1.setFontSize()
        self.private_1.setText(text[0])

        self.private_2 = LabelBtnWidgetPrivate()
        self.private_2.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.private_2.base_fig_scale = 0.5
        self.private_2.fig_pixmap = QtGui.QPixmap(file_path)
        self.private_2.setFigSize()

        self.btn_layout.addWidget(self.private_1, 0, 0, 3, 1)
        self.btn_layout.addWidget(self.private_2, 3, 0, 5, 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.private_1.get_scale.emit(self.btn_scale)
        self.private_2.get_scale.emit(self.btn_scale)
