# coding: utf-8
from PyQt6.QtCore import QSize, Qt, QRectF
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QLineEdit, QToolButton

from ...common.style_sheet import setStyleSheet
from ...common.icon import FluentIcon as FIF
from .menu import LineEditMenu


class ClearButton(QToolButton):
    """ Clear button """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(29, 25)
        self.setIconSize(QSize(10, 10))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName('clearButton')
        setStyleSheet(self, 'line_edit')

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        FIF.CLOSE.render(painter, QRectF(9.5, 7, 10, 10))


class LineEdit(QLineEdit):
    """ Line edit """

    def __init__(self, contents='', parent=None):
        super().__init__(contents, parent)
        self._isClearButtonEnabled = False

        setStyleSheet(self, 'line_edit')
        self.setFixedHeight(33)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)

        self.clearButton = ClearButton(self)
        self.clearButton.move(self.width() - 33, 4)
        self.clearButton.hide()

        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self.__onTextChanged)

    def setClearButtonEnabled(self, enable: bool):
        self._isClearButtonEnabled = enable
        self.setTextMargins(0, 0, 28*enable, 0)

    def isClearButtonEnabled(self) -> bool:
        return self._isClearButtonEnabled

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self.clearButton.hide()

    def focusInEvent(self, e):
        super().focusInEvent(e)
        if self.isClearButtonEnabled():
            self.clearButton.setVisible(bool(self.text()))

    def __onTextChanged(self, text):
        """ text changed slot """
        if self.isClearButtonEnabled():
            self.clearButton.setVisible(bool(text) and self.hasFocus())

    def contextMenuEvent(self, e):
        menu = LineEditMenu(self)
        menu.exec(e.globalPos())

    def resizeEvent(self, e):
        self.clearButton.move(self.width() - 33, 4)
