# coding:utf-8
from .config import qconfig, Theme
from PyQt5.QtCore import QFile


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
    f.open(QFile.ReadOnly)
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
    widget.setStyleSheet(getStyleSheet(file, theme))