# coding: utf-8
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget


def setFont(widget: QWidget, fontSize=14, weight=QFont.Weight.Normal):
    """ set the font of widget

    Parameters
    ----------
    widget: QWidget
        the widget to set font

    fontSize: int
        font pixel size

    weight: `QFont.Weight`
        font weight
    """
    widget.setFont(getFont(fontSize, weight))


def getFont(fontSize=14, weight=QFont.Weight.Normal):
    """ create font

    Parameters
    ----------
    fontSize: int
        font pixel size

    weight: `QFont.Weight`
        font weight
    """
    font = QFont()
    font.setFamilies(['Segoe UI', 'Microsoft YaHei', 'PingFang SC'])
    font.setPixelSize(fontSize)
    font.setWeight(weight)
    return font