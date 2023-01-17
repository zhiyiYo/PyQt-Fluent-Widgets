# coding:utf-8
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QIcon, QIconEngine, QImage, QPainter, QPixmap

from .config import qconfig


class PixmapIconEngine(QIconEngine):
    """ Pixmap icon engine """

    def __init__(self, iconPath: str):
        self.iconPath = iconPath
        super().__init__()

    def paint(self, painter: QPainter, rect: QRect, mode: QIcon.Mode, state: QIcon.State):
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.drawImage(rect, QImage(self.iconPath))

    def pixmap(self, size: QSize, mode: QIcon.Mode, state: QIcon.State) -> QPixmap:
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        self.paint(QPainter(pixmap), QRect(QPoint(0, 0), size), mode, state)
        return pixmap


class Icon(QIcon):

    def __init__(self, iconPath: str):
        self.iconPath = iconPath
        super().__init__(PixmapIconEngine(iconPath))


def getIconColor():
    """ get the color of icon based on theme """
    return "white" if qconfig.theme == 'dark' else 'black'
