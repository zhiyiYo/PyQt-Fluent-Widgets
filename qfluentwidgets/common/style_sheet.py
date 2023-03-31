# coding:utf-8
from enum import Enum
from string import Template
import weakref

from PyQt6.QtCore import QFile, QObject
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget

from .config import qconfig, Theme, isDarkTheme


class StyleSheetManager(QObject):
    """ Style sheet manager """

    def __init__(self):
        self.widgets = weakref.WeakKeyDictionary()

    def register(self, file: str, widget: QWidget):
        """ register widget to manager

        Parameters
        ----------
        file: str
            qss file path

        widget: QWidget
            the widget to set style sheet
        """
        if widget not in self.widgets:
            widget.destroyed.connect(self.deregister)

        self.widgets[widget] = file

    def deregister(self, widget: QWidget):
        """ deregister widget from manager """
        if widget not in self.widgets:
            return

        self.widgets.pop(widget)

    def items(self):
        return self.widgets.items()


styleSheetManager = StyleSheetManager()


class QssTemplate(Template):
    """ style sheet template """

    delimiter = '--'


def getStyleSheet(file, theme=Theme.AUTO):
    """ get style sheet from `qfluentwidgets` embedded qss file

    Parameters
    ----------
    file: str
        qss file name, without `.qss` suffix

    theme: Theme
        the theme of style sheet
    """
    theme = qconfig.theme if theme == Theme.AUTO else theme
    f = QFile(f":/qfluentwidgets/qss/{theme.value.lower()}/{file}.qss")
    f.open(QFile.OpenModeFlag.ReadOnly)
    template = QssTemplate(str(f.readAll(), encoding='utf-8'))
    f.close()

    mappings = {c.value: c.name() for c in ThemeColor._member_map_.values()}
    return template.safe_substitute(mappings)


def setStyleSheet(widget, file, theme=Theme.AUTO, register=True):
    """ set the style sheet of widget using `qfluentwidgets` embedded qss file

    Parameters
    ----------
    widget: QWidget
        the widget to set style sheet

    file: str
        qss file name, without `.qss` suffix

    theme: Theme
        the theme of style sheet

    register: bool
        whether to register the widget to the style manager. If `register=True`, the style of
        the widget will be updated automatically when the theme changes
    """
    if register:
        styleSheetManager.register(file, widget)

    widget.setStyleSheet(getStyleSheet(file, theme))


def updateStyleSheet():
    """ update the style sheet of all fluent widgets """
    removes = []
    for widget, file in styleSheetManager.items():
        try:
            setStyleSheet(widget, file, qconfig.theme)
        except RuntimeError:
            removes.append(widget)

    for widget in removes:
        styleSheetManager.deregister(widget)


def setTheme(theme: Theme, save=False):
    """ set the theme of application

    Parameters
    ----------
    theme: Theme
        theme mode

    save: bool
        whether to save the change to config file
    """
    qconfig.set(qconfig.themeMode, theme, save)
    updateStyleSheet()


class ThemeColor(Enum):
    """ Theme color type """

    PRIMARY = "ThemeColorPrimary"
    DARK_1 = "ThemeColorDark1"
    DARK_2 = "ThemeColorDark2"
    DARK_3 = "ThemeColorDark3"
    LIGHT_1 = "ThemeColorLight1"
    LIGHT_2 = "ThemeColorLight2"
    LIGHT_3 = "ThemeColorLight3"

    def name(self):
        return self.color().name()

    def color(self):
        color = qconfig.get(qconfig.themeColor)  # type:QColor

        # transform color into hsv space
        h, s, v, _ = color.getHsvF()

        if isDarkTheme():
            s *= 0.84
            v = 1
            if self == self.DARK_1:
                v *= 0.9
            elif self == self.DARK_2:
                s *= 0.977
                v *= 0.82
            elif self == self.DARK_3:
                s *= 0.95
                v *= 0.7
            elif self == self.LIGHT_1:
                s *= 0.92
            elif self == self.LIGHT_2:
                s *= 0.78
            elif self == self.LIGHT_3:
                s *= 0.65
        else:
            if self == self.DARK_1:
                v *= 0.75
            elif self == self.DARK_2:
                s *= 1.05
                v *= 0.5
            elif self == self.DARK_3:
                s *= 1.1
                v *= 0.4
            elif self == self.LIGHT_1:
                v *= 1.05
            elif self == self.LIGHT_2:
                s *= 0.75
                v *= 1.05
            elif self == self.LIGHT_3:
                s *= 0.65
                v *= 1.05

        return QColor.fromHsvF(h, min(s, 1), min(v, 1))


def themeColor():
    """ get theme color """
    return ThemeColor.PRIMARY.color()


def setThemeColor(color, save=False):
    """ set theme color

    Parameters
    ----------
    color: QColor | Qt.GlobalColor | str
        theme color

    save: bool
        whether to save to change to config file
    """
    color = QColor(color)
    qconfig.set(qconfig.themeColor, color, save=save)
    updateStyleSheet()
