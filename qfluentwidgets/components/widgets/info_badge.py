# coding:utf-8
from enum import Enum
from typing import Union

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy

from ...common.font import setFont
from ...common.overload import singledispatchmethod
from ...common.style_sheet import themeColor, FluentStyleSheet, isDarkTheme


class InfoLevel(Enum):
    """ Info level """
    INFOAMTION = 'Info'
    SUCCESS = 'Success'
    ATTENTION = 'Attension'
    WARNING = "Warning"
    ERROR = "Error"


class InfoBadge(QLabel):
    """ Information badge """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None, level=InfoLevel.ATTENTION):
        super().__init__(parent=parent)
        self.level = InfoLevel.INFOAMTION
        self.lightBackgroundColor = None
        self.darkBackgroundColor = None
        self.setLevel(level)

        setFont(self, 11)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        FluentStyleSheet.INFO_BADGE.apply(self)

    @__init__.register
    def _(self, text: str, parent: QWidget = None, level=InfoLevel.ATTENTION):
        self.__init__(parent, level)
        self.setText(text)

    @__init__.register
    def _(self, num: int, parent: QWidget = None, level=InfoLevel.ATTENTION):
        self.__init__(parent, level)
        self.setNum(num)

    @__init__.register
    def _(self, num: float, parent: QWidget = None, level=InfoLevel.ATTENTION):
        self.__init__(parent, level)
        self.setNum(num)

    def setLevel(self, level: InfoLevel):
        """ set infomation level """
        if level == self.level:
            return

        self.level = level
        self.setProperty('level', level.value)
        self.update()

    def setProperty(self, name: str, value):
        super().setProperty(name, value)
        if name != "level":
            return

        values = [i.value for i in InfoLevel._member_map_.values()]
        if value in values:
            self.level = InfoLevel(value)

    def setCustomBackgroundColor(self, light, dark):
        """ set the custom background color

        Parameters
        ----------
        light, dark: str | Qt.GlobalColor | QColor
            background color in light/dark theme mode
        """
        self.lightBackgroundColor = QColor(light)
        self.darkBackgroundColor = QColor(dark)
        self.update()

    def paintEvent(self, e):
        isDark = isDarkTheme()

        if self.lightBackgroundColor:
            color = self.darkBackgroundColor if isDark else self.lightBackgroundColor
        elif self.level == InfoLevel.INFOAMTION:
            color = QColor(157, 157, 157) if isDark else QColor(138, 138, 138)
        elif self.level == InfoLevel.SUCCESS:
            color = QColor(108, 203, 95) if isDark else QColor(15, 123, 15)
        elif self.level == InfoLevel.ATTENTION:
            color = themeColor()
        elif self.level == InfoLevel.WARNING:
            color = QColor(255, 244, 206) if isDark else QColor(157, 93, 0)
        else:
            color = QColor(255, 153, 164) if isDark else QColor(196, 43, 28)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)

        r = self.height() / 2
        painter.drawRoundedRect(self.rect(), r, r)

        super().paintEvent(e)

    @staticmethod
    def info(text: Union[str, float], parent=None):
        return InfoBadge(text, parent, InfoLevel.INFOAMTION)

    @staticmethod
    def success(text: Union[str, float], parent=None):
        return InfoBadge(text, parent, InfoLevel.SUCCESS)

    @staticmethod
    def attension(text: Union[str, float], parent=None):
        return InfoBadge(text, parent, InfoLevel.ATTENTION)

    @staticmethod
    def warning(text: Union[str, float], parent=None):
        return InfoBadge(text, parent, InfoLevel.WARNING)

    @staticmethod
    def error(text: Union[str, float], parent=None):
        return InfoBadge(text, parent, InfoLevel.ERROR)

    @staticmethod
    def custom(text: Union[str, float], light: QColor, dark: QColor, parent=None):
        """ create a badge with custom background color

        Parameters
        ----------
        text: str | float
            the text of badge

        light, dark: str | Qt.GlobalColor | QColor
            background color in light/dark theme mode

        parent: QWidget
            parent widget
        """
        w = InfoBadge(text, parent)
        w.setCustomBackgroundColor(light, dark)
        return w
