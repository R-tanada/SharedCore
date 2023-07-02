from PySide6 import QtCore, QtGui, QtWidgets


class CursorLabel(QtWidgets.QLabel):
    scale = 1.0
    cursor_pos = [0, 0]
    cursor_pressed = False
    win_size = None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.partner_cursor_size = 30
        self.cursor_size = self.partner_cursor_size
        self.cursor_style = f"""
        QLabel{{
            background-color: rgba(83,191,245,100);
            min-width: %spx;
            min-height: %spx;
            max-width: %spx;
            max-height: %spx;
            border-radius: %spx;
        }}
        """ % (
            self.partner_cursor_size,
            self.partner_cursor_size,
            self.partner_cursor_size,
            self.partner_cursor_size,
            self.partner_cursor_size / 2,
        )
        self.setStyleSheet(self.cursor_style)
        self.move(50, 50)

        self.cursor_update = QtCore.QTimer()
        self.cursor_update.timeout.connect(self.__update_cursor)
        self.cursor_update.start(5)

    def __update_cursor(self):
        self.__update_cursor_draw()

    def __update_cursor_draw(self):
        def __on_time():
            self.cursor_style = f"""
            QLabel{{
                background-color: rgba(83,191,245,100);
                min-width: %spx;
                min-height: %spx;
                max-width: %spx;
                max-height: %spx;
                border-radius: %spx;
            }}
            """ % (
                self.cursor_size,
                self.cursor_size,
                self.cursor_size,
                self.cursor_size,
                int(self.cursor_size / 2),
            )
            self.setStyleSheet(self.cursor_style)
            CursorLabel.cursor_pressed = False

        self.cursor_size = self.partner_cursor_size * CursorLabel.scale
        self.cursor_style = f"""
        QLabel{{
            background-color: rgba(83,191,245,100);
            min-width: %spx;
            min-height: %spx;
            max-width: %spx;
            max-height: %spx;
            border-radius: %spx;
        }}
        """ % (
            self.cursor_size,
            self.cursor_size,
            self.cursor_size,
            self.cursor_size,
            int(self.cursor_size / 2),
        )
        self.setStyleSheet(self.cursor_style)
        self.move(
            CursorLabel.win_size[0] * CursorLabel.cursor_pos[0] - self.width() / 2,
            CursorLabel.win_size[1] * CursorLabel.cursor_pos[1] - self.height() / 2,
        )

        if CursorLabel.cursor_pressed:
            self.cursor_style = f"""
            QLabel{{
                background-color: rgba(249,115,21,100);
                min-width: %spx;
                min-height: %spx;
                max-width: %spx;
                max-height: %spx;
                border-radius: %spx;
            }}
            """ % (
                self.cursor_size,
                self.cursor_size,
                self.cursor_size,
                self.cursor_size,
                int(self.cursor_size / 2),
            )
            self.setStyleSheet(self.cursor_style)
            QtCore.QTimer.singleShot(150, __on_time)
