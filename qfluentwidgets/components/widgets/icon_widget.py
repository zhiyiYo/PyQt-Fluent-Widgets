# coding:utf-8
from typing import Union

from PySide6.QtGui import QIcon, QPainter
from PySide6.QtWidgets import QWidget

from ...common.icon import FluentIconBase, drawIcon
from ...common.overload import singledispatchmethod


class IconWidget(QWidget):
    """ Icon widget """

    @singledispatchmethod
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon())

    @__init__.register
    def _(self, icon: FluentIconBase, parent: QWidget = None):
        self.__init__(parent)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: QIcon, parent: QWidget = None):
        self.__init__(parent)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: str, parent: QWidget = None):
        self.__init__(parent)
        self.setIcon(icon)

    def setIcon(self, icon: Union[str, QIcon, FluentIconBase]):
        self.icon = icon
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        drawIcon(self.icon, painter, self.rect())
