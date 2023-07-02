from PySide6 import QtCore, QtGui, QtWidgets

from .SetStyle import ColorStyle


class LabelBtnWidget(QtWidgets.QLabel, ColorStyle):
    def __init__(self, name, main_win: QtWidgets.QApplication, parent=None):
        super().__init__(parent=parent)
        ColorStyle.__init__(self)

        self.setObjectName("parent")
        self.setStyleSheet(self.button_style)

        self.name = name
        self.main_win = main_win
        self.message = {"Button": self.name, "bool": True}
        self.base_btn_size = None

        self.btn_layout = QtWidgets.QGridLayout(self)
        self.btn_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_layout.setSpacing(0)

    def resizeEvent(self, event):
        if not self.base_btn_size:
            self.base_btn_size = self.size()

        btn_width_scale = self.width() / self.base_btn_size.width()
        btn_height_scale = self.height() / self.base_btn_size.height()
        self.btn_scale = min(btn_width_scale, btn_height_scale)

    def mousePressEvent(self, event):
        self.setBtnPress(self, event)
        self.main_win.on_signal.emit(self)
        super().mousePressEvent(event)


class LabelBtnWidgetPrivate(QtWidgets.QLabel, ColorStyle):
    get_scale = QtCore.Signal(float)

    def __init__(self):
        super().__init__()
        ColorStyle.__init__(self)

        self.base_font_size = None
        self.font_size = self.base_font_size

        self.base_fig_scale = None
        self.fig_scale = None
        self.fig_pixmap = None

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet(
            "color: rgb(%s,%s,%s)" % self.button_font_color.getRgb()[:-1]
        )
        self.setFont(self.button_font)

        self.get_scale.connect(self.getParentScale)

    def setFontSize(self):
        if not self.font_size:
            self.font_size = self.base_font_size
        _font = self.button_font
        _font.setPointSizeF(self.font_size)
        self.setFont(_font)

    def setFontBold(self):
        _font = self.button_font
        _font.setBold(True)
        self.setFont(_font)

    def setFigSize(self):
        if not self.fig_scale:
            self.fig_scale = self.base_fig_scale
            self.base_fig_pixmap = self.fig_pixmap

        _fig_pixmap = self.base_fig_pixmap.scaled(
            self.base_fig_pixmap.size() * self.fig_scale,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )

        self.setPixmap(_fig_pixmap)

    def getParentScale(self, scale):
        if bool(self.text()):
            self.font_size = self.base_font_size * scale
            self.setFontSize()

        elif bool(self.pixmap()):
            self.fig_scale = self.base_fig_scale * scale
            self.setFigSize()
