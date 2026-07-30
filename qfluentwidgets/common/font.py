from typing import List

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget

from .config import qconfig


def setFontFamilies(families: List[str], save: bool = False) -> None:
    """set the font families used by all widgets

    Parameters
    ----------
    families: List[str]
        font family names, the default value is `['Segoe UI', 'Microsoft YaHei', 'PingFang SC']`

    save: bool
        whether to save the change to config file
    """
    qconfig.set(qconfig.fontFamilies, families, save)


def fontFamilies() -> List[str]:
    """Returns the font families used by all widgets"""
    return qconfig.get(qconfig.fontFamilies).copy()


def setFont(widget: QWidget, fontSize: int = 14, weight: QFont.Weight = QFont.Weight.Normal) -> None:
    """set the font of widget

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


def getFont(fontSize: int = 14, weight: QFont.Weight = QFont.Weight.Normal) -> QFont:
    """create font

    Parameters
    ----------
    fontSize: int
        font pixel size

    weight: `QFont.Weight`
        font weight
    """
    font = QFont()
    font.setFamilies(qconfig.get(qconfig.fontFamilies))
    font.setPixelSize(fontSize)
    font.setWeight(weight)
    return font


def fontStyleSheet(font: QFont) -> str:
    """Returns the style sheet of font"""
    families = [f"'{family}'" for family in font.families()]
    return f"font: {font.pixelSize()}px {','.join(families)}"
