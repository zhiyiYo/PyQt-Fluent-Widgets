# coding:utf-8
import weakref

import darkdetect
from PyQt6.QtCore import QFile, QObject
from PyQt6.QtWidgets import QWidget

from .config import qconfig, Theme


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
    qss = str(f.readAll(), encoding='utf-8')
    f.close()
    return qss


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
    if theme == Theme.AUTO:
        theme = darkdetect.theme()
        theme = Theme(theme) if theme else Theme.LIGHT

    qconfig.set(qconfig.themeMode, theme, save)
    updateStyleSheet()
