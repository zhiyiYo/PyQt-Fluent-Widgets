# coding:utf-8
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QToolButton


class ThreeStateButton(QToolButton):
    """ Three state tool button class """

    def __init__(self, iconPaths: dict, parent=None):
        """
        Parameters
        ----------
        iconPaths: dict
            icon path dict, provide icons in `normal`, `hover` and `pressed` state

        parent:
            parent window

        iconSize: tuple
            icon size
        """
        super().__init__(parent)
        self.iconPaths = iconPaths
        self.setCursor(Qt.ArrowCursor)
        self.resize(QPixmap(iconPaths['normal']).size())
        self.setIconSize(self.size())
        self.setIcon(QIcon(self.iconPaths['normal']))
        self.setStyleSheet('border: none; margin: 0px')

    def enterEvent(self, e):
        self.setIcon(QIcon(self.iconPaths['hover']))

    def leaveEvent(self, e):
        self.setIcon(QIcon(self.iconPaths['normal']))

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            return

        self.setIcon(QIcon(self.iconPaths['pressed']))
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.RightButton:
            return

        self.setIcon(QIcon(self.iconPaths['normal']))
        super().mouseReleaseEvent(e)
