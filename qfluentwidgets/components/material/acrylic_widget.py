# coding:utf-8
from PySide2.QtCore import Qt
from PySide2.QtGui import QPainterPath, QPainter, QColor
from PySide2.QtWidgets import QWidget

from ..widgets.flyout import FlyoutViewBase
from ..widgets.acrylic_label import AcrylicBrush
from ...common.style_sheet import isDarkTheme


class AcrylicWidget:
    """ Acrylic widget """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.acrylicBrush = AcrylicBrush(self, 30)

    def _updateAcrylicColor(self):
        if isDarkTheme():
            tintColor = QColor(32, 32, 32, 200)
            luminosityColor = QColor(0, 0, 0, 0)
        else:
            tintColor = QColor(255, 255, 255, 180)
            luminosityColor = QColor(255, 255, 255, 0)

        self.acrylicBrush.tintColor = tintColor
        self.acrylicBrush.luminosityColor = luminosityColor

    def acrylicClipPath(self):
        return QPainterPath()

    def _drawAcrylic(self, painter: QPainter):
        path = self.acrylicClipPath()
        if not path.isEmpty():
            self.acrylicBrush.clipPath = self.acrylicClipPath()

        self._updateAcrylicColor()
        self.acrylicBrush.paint()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self._drawAcrylic(painter)
        super().paintEvent(e)