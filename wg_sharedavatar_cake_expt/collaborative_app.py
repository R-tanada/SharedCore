import json
import os
import sys
import threading

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from sharedqt import ButtonFrame, MainWin, VideoFrame
from sharedqt.PartnerCursor import CursorLabel

if __name__ == "__main__":
    settings = json.load(open("config/settings.json", "r"))

    app = QtWidgets.QApplication(sys.argv)

    main_win = MainWin(settings)

    panel = QtWidgets.QWidget()
    panel_layout = QtWidgets.QVBoxLayout(panel)
    panel_layout.setContentsMargins(0, 0, 0, 0)

    video_frame = VideoFrame(main_win, panel)
    button_widget = ButtonFrame(main_win, panel)

    panel_layout.addWidget(video_frame, 3)
    panel_layout.addWidget(button_widget, 2)

    partner_cursor = CursorLabel(parent=panel)

    main_win.setCentralWidget(panel)

    main_win.show()
    app.exec_()
