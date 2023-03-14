# coding:utf-8
import weakref

import darkdetect
from PyQt6.QtCore import QFile

from .config import qconfig, Theme


fluentWidgets = weakref.WeakKeyDictionary()


def getStyleSheet(file, theme=Theme.AUTO):
    """ get style sheet

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


def setStyleSheet(widget, file, theme=Theme.AUTO):
    """ set the style sheet of widget

    Parameters
    ----------
    widget: QWidget
        the widget to set style sheet

    file: str
        qss file name, without `.qss` suffix

    theme: Theme
        the theme of style sheet
    """
    fluentWidgets[widget] = file
    widget.setStyleSheet(getStyleSheet(file, theme))


def setTheme(theme: Theme):
    """ set the theme of application """
    if theme == Theme.AUTO:
        theme = darkdetect.theme()
        qconfig.theme = Theme(theme) if theme else Theme.LIGHT
    else:
        qconfig.theme = theme

    for widget, file in fluentWidgets.items():
        setStyleSheet(widget, file, qconfig.theme)