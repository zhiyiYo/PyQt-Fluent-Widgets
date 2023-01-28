# coding:utf-8
from PyQt6.QtCore import QPoint, QRect, QRectF, QSize, Qt
from PyQt6.QtGui import QIcon, QIconEngine, QImage, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer

from .config import qconfig


class PixmapIconEngine(QIconEngine):
    """ Pixmap icon engine """

    def __init__(self, iconPath):
        self.iconPath = iconPath
        super().__init__()

    def paint(self, painter: QPainter, rect, mode, state):
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)
        if not self.iconPath.lower().endswith('svg'):
            painter.drawImage(rect, QImage(self.iconPath))
        else:
            renderer = QSvgRenderer(self.iconPath)
            renderer.render(painter, QRectF(rect))

    def pixmap(self, size: QSize, mode: QIcon.Mode, state):
        pixmap = QPixmap(size)
        pixmap.fill(Qt.GlobalColor.transparent)
        self.paint(QPainter(pixmap), QRect(QPoint(0, 0), size), mode, state)
        return pixmap


class Icon(QIcon):

    def __init__(self, iconPath):
        self.iconPath = iconPath
        super().__init__(PixmapIconEngine(iconPath))


def getIconColor():
    """ get the color of icon based on theme """
    return "white" if qconfig.theme == 'dark' else 'black'
