# coding:utf-8
from typing import Union
import sys

from PySide6.QtCore import Qt, QSize, QRectF, QEvent
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsDropShadowEffect

from ..common.icon import FluentIconBase, drawIcon, toQIcon
from ..common.style_sheet import isDarkTheme, FluentStyleSheet
from ..components.widgets import IconWidget
from qframelesswindow import TitleBar



class SplashScreen(QWidget):
    """ Splash screen """

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], parent=None, enableShadow=True):
        super().__init__(parent=parent)
        self._icon = icon
        self._iconSize = QSize(96, 96)

        self.titleBar = TitleBar(self)
        self.iconWidget = IconWidget(icon, self)
        self.shadowEffect = QGraphicsDropShadowEffect(self)

        self.iconWidget.setFixedSize(self._iconSize)
        self.shadowEffect.setColor(QColor(0, 0, 0, 50))
        self.shadowEffect.setBlurRadius(15)
        self.shadowEffect.setOffset(0, 4)

        FluentStyleSheet.FLUENT_WINDOW.apply(self.titleBar)

        if enableShadow:
            self.iconWidget.setGraphicsEffect(self.shadowEffect)

        if parent:
            parent.installEventFilter(self)

        if sys.platform == "darwin":
            self.titleBar.hide()

    def setIcon(self, icon: Union[str, QIcon, FluentIconBase]):
        self._icon = icon
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def setIconSize(self, size: QSize):
        self._iconSize = size
        self.iconWidget.setFixedSize(size)
        self.update()

    def iconSize(self):
        return self._iconSize

    def setTitleBar(self, titleBar: QWidget):
        """ set title bar """
        self.titleBar.deleteLater()
        self.titleBar = titleBar
        titleBar.setParent(self)
        titleBar.raise_()
        self.titleBar.resize(self.width(), self.titleBar.height())

    def eventFilter(self, obj, e: QEvent):
        if obj is self.parent():
            if e.type() == QEvent.Resize:
                self.resize(e.size())
            elif e.type() == QEvent.ChildAdded:
                self.raise_()

        return super().eventFilter(obj, e)

    def resizeEvent(self, e):
        iw, ih = self.iconSize().width(), self.iconSize().height()
        self.iconWidget.move(self.width()//2 - iw//2, self.height()//2 - ih//2)
        self.titleBar.resize(self.width(), self.titleBar.height())

    def finish(self):
        """ close splash screen """
        self.close()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)

        # draw background
        c = 32 if isDarkTheme() else 255
        painter.setBrush(QColor(c, c, c))
        painter.drawRect(self.rect())
