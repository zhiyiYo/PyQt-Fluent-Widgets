# coding: utf-8
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget


def setFont(widget: QWidget, fontSize=14):
    """ set the font of widget

    Parameters
    ----------
    widget: QWidget
        the widget to set font

    fontSize: int
        font pixel size
    """
    widget.setFont(getFont(fontSize))


def getFont(fontSize=14):
    """ create font

    Parameters
    ----------
    fontSize: int
        font pixel size
    """
    font = QFont()
    font.setFamilies(['Segoe UI', 'Microsoft YaHei'])
    font.setPixelSize(fontSize)
    return font