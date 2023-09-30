# coding: utf-8
from PyQt5.QtCore import QRect, QRectF
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import QApplication, QFrame

from .acrylic_widget import AcrylicWidget
from ..widgets.tool_tip import ToolTip, ToolTipFilter


class AcrylicToolTipContainer(AcrylicWidget, QFrame):
    """ Acrylic tool tip container """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setProperty("transparent", True)

    def acrylicClipPath(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect().adjusted(1, 1, -1, -1)), 3, 3)
        return path


class AcrylicToolTip(ToolTip):
    """ Acrylic tool tip """

    def _createContainer(self):
        return AcrylicToolTipContainer(self)

    def showEvent(self, e):
        pos = self.pos() + self.container.pos()
        self.container.acrylicBrush.grabImage(QRect(pos, self.container.size()))
        return super().showEvent(e)


class AcrylicToolTipFilter(ToolTipFilter):
    """ Acrylic tool tip filter """

    def _createToolTip(self):
        return AcrylicToolTip(self.parent().toolTip(), self.parent().window())
