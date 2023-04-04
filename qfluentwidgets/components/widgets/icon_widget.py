# coding:utf-8
from typing import Union

from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtWidgets import QWidget

from ...common.icon import FluentIconBase, drawIcon


class IconWidget(QWidget):
    """ Icon widget """

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], parent=None):
        super().__init__(parent=parent)
        self.icon = icon

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        drawIcon(self.icon, painter, self.rect())
