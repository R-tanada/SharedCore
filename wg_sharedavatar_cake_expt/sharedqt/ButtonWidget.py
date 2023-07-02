from PySide6 import QtCore, QtGui, QtWidgets

from . import ImagePath as IP
from .CrossButton import CrossBtnWidget
from .GripperButton import GripperBtnWidget
from .HeightButton import HeightBtnWidget
from .RotateButton import RotateBtnWidget
from .SetStyle import ColorStyle
from .StatusButton import StatusWidget


class ButtonFrame(QtWidgets.QLabel):
    def __init__(self, main_win, parent):
        super().__init__(parent=parent)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(11, 0, 11, 11)

        self.cross_widget = CrossBtnWidget(main_win=main_win, parent=self)
        self.height_widget = HeightBtnWidget(main_win=main_win, parent=self)
        self.rotate_widget = RotateBtnWidget(main_win=main_win, parent=self)
        self.status_widget = StatusWidget(main_win=main_win, parent=self)
        self.gripper_widget = GripperBtnWidget(main_win=main_win, parent=self)

        layout.addWidget(self.cross_widget, 3)
        layout.addWidget(self.height_widget, 2)
        layout.addWidget(self.rotate_widget, 2)
        layout.addWidget(self.status_widget, 2)
        layout.addWidget(self.gripper_widget, 2)
