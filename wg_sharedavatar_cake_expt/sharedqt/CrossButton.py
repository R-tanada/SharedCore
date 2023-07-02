import cv2
import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets

from .SetStyle import ColorStyle, FontStyle


class CrossBtnWidget(QtWidgets.QLabel):
    def __init__(self, main_win: QtWidgets.QApplication, parent=None):
        super().__init__(parent)

        self.pos_widget_private = CrossBtnWidgetPrivate(main_win, parent=self)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.pos_widget_private.draw(painter)

    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("double clicked")
        self.pos_widget_private.get_mouse_pos.emit(event)
        return super().mousePressEvent(event)


class CrossBtnWidgetPrivate(QtWidgets.QLabel, ColorStyle):
    get_mouse_pos = QtCore.Signal(object)

    def __init__(self, main_win: QtWidgets.QApplication, parent=None):
        super().__init__(parent=parent)
        ColorStyle.__init__(self)

        self.first_widget_size = None

        self.btn_size = 0.3
        self.front_penta = PentaPoints(
            name="front",
            text="前",
            scale=self.btn_size,
            translate=(0.5, 0.05),
            rotate=0,
            parent=parent,
            main_win=main_win,
        )
        self.right_penta = PentaPoints(
            name="right",
            text="右",
            scale=self.btn_size,
            translate=(0.95, 0.5),
            rotate=90,
            parent=parent,
            main_win=main_win,
        )
        self.back_penta = PentaPoints(
            name="back",
            text="後",
            scale=self.btn_size,
            translate=(0.5, 0.95),
            rotate=180,
            parent=parent,
            main_win=main_win,
        )
        self.left_penta = PentaPoints(
            name="left",
            text="左",
            scale=self.btn_size,
            translate=(0.05, 0.5),
            rotate=270,
            parent=parent,
            main_win=main_win,
        )

        self.get_mouse_pos.connect(self.press_event)

    def draw(self, painter: QtGui.QPainter):
        if not self.first_widget_size:
            self.first_widget_size = self.parentWidget().size()

        widget_size = self.parentWidget().size()

        self.front_penta.draw_penta(widget_size, painter)
        self.right_penta.draw_penta(widget_size, painter)
        self.back_penta.draw_penta(widget_size, painter)
        self.left_penta.draw_penta(widget_size, painter)

    def press_event(self, event):
        self.front_penta.determine_inside(event)
        self.right_penta.determine_inside(event)
        self.back_penta.determine_inside(event)
        self.left_penta.determine_inside(event)


class PentaPoints(QtCore.QObject, ColorStyle, FontStyle):
    def __init__(
        self,
        name,
        text,
        scale,
        translate,
        rotate,
        parent,
        main_win: QtWidgets.QApplication,
    ):
        super().__init__(parent=parent)
        ColorStyle.__init__(self)
        FontStyle.__init__(self)

        self.name = name
        self.message = {"Button": self.name, "bool": True}
        self.main_win = main_win

        self.btn_name = name
        self.btn_text = text
        self.btn_scale = scale
        self.btn_translate = translate
        self.btn_rotate = rotate
        self.btn_parent = parent
        self.btn_base_font_size = self.pos_btn_font_size
        self.base_widget_size = None

        self._animValue = 0.0
        self.anim = QtCore.QPropertyAnimation(self)
        self.anim.setTargetObject(self)
        self.anim.setPropertyName(b"press")
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QtCore.QEasingCurve.Linear)
        self.anim.finished.connect(self.btn_parent.update())

    def draw_penta(self, widget_size: QtCore.QSize, painter: QtGui.QPainter):
        if not self.base_widget_size:
            self.base_widget_size = widget_size

        scale_w = widget_size.width() / self.base_widget_size.width()
        scale_h = widget_size.height() / self.base_widget_size.height()
        scale = min(scale_w, scale_h)

        painter.save()

        painter.setPen(self.button_border_pen)
        diff_color = self.pos_btn_color - self.pos_btn_on_color
        painter.setBrush(
            QtGui.QColor(
                self.pos_btn_color[0] - diff_color[0] * self._animValue,
                self.pos_btn_color[1] - diff_color[1] * self._animValue,
                self.pos_btn_color[2] - diff_color[2] * self._animValue,
            )
        )

        self.widget_size = widget_size
        if self.btn_rotate in (0, 180):
            penta_width = (
                widget_size.width()
                * self.btn_scale
                * 0.85
                * (1 + self._animValue * 0.05)
            )
            penta_height = (
                widget_size.height() * self.btn_scale * (1 + self._animValue * 0.05)
            )
        elif self.btn_rotate in (90, 270):
            penta_width = (
                widget_size.height()
                * self.btn_scale
                * 0.85
                * (1 + self._animValue * 0.05)
            )
            penta_height = (
                widget_size.width() * self.btn_scale * (1 + self._animValue * 0.05)
            )

        q_points = [
            QtCore.QPointF(0, 0),
            QtCore.QPointF(penta_width / 2, 0),
            QtCore.QPointF(penta_width / 2, penta_height),
            QtCore.QPointF(0, penta_height * 1.4),
            QtCore.QPointF(-penta_width / 2, penta_height),
            QtCore.QPointF(-penta_width / 2, 0),
        ]

        self.rotate_points = self.points_rotate(q_points, self.btn_rotate)
        self.translate_points = self.points_translate(
            self.rotate_points, self.btn_translate
        )
        self.poly = QtGui.QPolygonF(self.translate_points)
        painter.drawPolygon(self.poly)

        _font = self.button_font
        _font.setPointSizeF(self.btn_base_font_size * scale)
        _font.setBold(True)
        painter.setFont(self.button_font)

        button_font_color = np.array(self.button_font_color.getRgb()[:-1])
        font_diff_color = button_font_color - np.array([255, 255, 255])
        painter.setPen(
            QtGui.QColor(
                button_font_color[0] - font_diff_color[0] * self._animValue,
                button_font_color[1] - font_diff_color[1] * self._animValue,
                button_font_color[2] - font_diff_color[2] * self._animValue,
            )
        )

        if self.btn_text == "前":
            painter.drawText(
                self.widget_size.width() * 0.46,
                self.widget_size.height() * 0.2,
                self.btn_text,
            )

        elif self.btn_text == "右":
            painter.drawText(
                self.widget_size.width() * 0.8,
                self.widget_size.height() * 0.53,
                self.btn_text,
            )

        elif self.btn_text == "後":
            painter.drawText(
                self.widget_size.width() * 0.46,
                self.widget_size.height() * 0.85,
                self.btn_text,
            )

        elif self.btn_text == "左":
            painter.drawText(
                self.widget_size.width() * 0.13,
                self.widget_size.height() * 0.53,
                self.btn_text,
            )

        painter.restore()

    def points_translate(self, points, diff):
        translate_points = []
        for i in points:
            translate_x = i.x() + self.widget_size.width() * diff[0]
            translate_y = i.y() + self.widget_size.height() * diff[1]
            translate_points.append(QtCore.QPointF(translate_x, translate_y))
        return translate_points

    def points_rotate(self, points, angle):
        rotate_points = []
        for i in points:
            rotate_x = i.x() * np.cos(np.radians(angle)) - i.y() * np.sin(
                np.radians(angle)
            )
            rotate_y = i.x() * np.sin(np.radians(angle)) + i.y() * np.cos(
                np.radians(angle)
            )
            rotate_points.append(QtCore.QPointF(rotate_x, rotate_y))
        return rotate_points

    @QtCore.Property(float)
    def press(self):
        return self._animValue

    @press.setter
    def press(self, value):
        self._animValue = -4 * value * (value - 1)
        self.btn_parent.update()

    @QtCore.Slot(name="animate")
    def animate(self):
        self.anim.setDirection(QtCore.QPropertyAnimation.Forward)
        self.anim.start()

    def determine_inside(self, event: QtCore.QEvent):
        polygon = []
        for i in self.translate_points:
            polygon.append([int(i.x()), int(i.y())])
        polygon = np.array(polygon)

        mPos = (event.position().x(), event.position().y())

        if cv2.pointPolygonTest(polygon, mPos, False) > 0:
            self.main_win.on_signal.emit(self)
            self.animate()
