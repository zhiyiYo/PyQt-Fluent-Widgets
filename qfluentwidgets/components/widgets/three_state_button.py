# coding:utf-8
from enum import Enum

from qtpy.QtCore import QEvent, QSize, Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QToolButton


class ButtonState(Enum):
    """ Button state """
    NORMAL = 0
    HOVER = 1
    PRESSED = 2


class ThreeStateButton(QToolButton):
    """ Three state tool button class """

    def __init__(self, iconPaths, parent=None, buttonSize=(40, 40), iconSize=None):
        """
        Parameters
        ----------
        iconPaths: Dict[ButtonState, str]
            icon path dict

        parent:
            parent window

        button: tuple
            button size

        iconSize: tuple
            icon size
        """
        super().__init__(parent)
        self.iconPaths = iconPaths
        self.resize(*buttonSize)
        self.setIconSize(self.size() if not iconSize else QSize(*iconSize))
        self.setCursor(Qt.ArrowCursor)
        self.setStyleSheet('border: none; margin: 0px; background: transparent')
        self.setState(ButtonState.NORMAL)
        self.installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self:
            if e.type() == QEvent.Enter:
                self.setState(ButtonState.HOVER)
            if e.type() in [QEvent.Leave, QEvent.MouseButtonRelease]:
                self.setState(ButtonState.NORMAL)
            if e.type() == QEvent.MouseButtonPress:
                self.setState(ButtonState.PRESSED)

        return super().eventFilter(obj, e)

    def setState(self, state):
        """ set the state of button """
        self.setIcon(QIcon(self.iconPaths[state]))