# coding:utf-8

from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap, QPalette, QColor, QFont
from PySide6.QtWidgets import QLabel, QWidget

from ...common.overload import singledispatchmethod
from ...common.font import setFont, getFont
from ...common.config import qconfig, isDarkTheme


class PixmapLabel(QLabel):
    """ Label for high dpi pixmap """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__pixmap = QPixmap()

    def setPixmap(self, pixmap: QPixmap):
        self.__pixmap = pixmap
        self.setFixedSize(pixmap.size())
        self.update()

    def pixmap(self):
        return self.__pixmap

    def paintEvent(self, e):
        if self.__pixmap.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        painter.drawPixmap(self.rect(), self.__pixmap)


class FluentLabelBase(QLabel):
    """ Fluent label base class """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._init()

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.setText(text)

    def _init(self):
        self.setFont(self.getFont())
        self.setTextColor()
        qconfig.themeChanged.connect(
            lambda: self.setTextColor(self.lightColor, self.darkColor))
        return self

    def getFont(self):
        raise NotImplementedError

    def setTextColor(self, light=QColor(0, 0, 0), dark=QColor(255, 255, 255)):
        """ set the text color of label

        Parameters
        ----------
        light, dark: QColor | Qt.GlobalColor | str
            text color in light/dark mode
        """
        self.lightColor = QColor(light)
        self.darkColor = QColor(dark)

        palette = self.palette()
        color = self.darkColor if isDarkTheme() else self.lightColor
        palette.setColor(QPalette.WindowText, color)
        self.setPalette(palette)


class CaptionLabel(FluentLabelBase):
    """ Caption text label """

    def getFont(self):
        return getFont(12)


class BodyLabel(FluentLabelBase):
    """ Body text label """

    def getFont(self):
        return getFont(14)


class StrongBodyLabel(FluentLabelBase):
    """ Strong body text label """

    def getFont(self):
        return getFont(14, QFont.DemiBold)


class SubtitleLabel(FluentLabelBase):
    """ Sub title text label """

    def getFont(self):
        return getFont(20, QFont.DemiBold)


class TitleLabel(FluentLabelBase):
    """ Sub title text label """

    def getFont(self):
        return getFont(28, QFont.DemiBold)


class LargeTitleLabel(FluentLabelBase):
    """ Large title text label """

    def getFont(self):
        return getFont(40, QFont.DemiBold)


class DisplayLabel(FluentLabelBase):
    """ Display text label """

    def getFont(self):
        return getFont(68, QFont.DemiBold)

