# coding: utf-8
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QLineEdit, QToolButton

from ...common.style_sheet import setStyleSheet
from ...common.icon import FluentIcon as FIF
from .menu import LineEditMenu


class LineEdit(QLineEdit):
    """ Line edit """

    def __init__(self, contents='', parent=None):
        super().__init__(contents, parent)
        self._isClearButtonEnabled = False

        setStyleSheet(self, 'line_edit')
        self.setFixedHeight(33)
        self.clearButton = QToolButton(self)

        self.setTextMargins(0, 0, 33, 0)

        self.clearButton.setObjectName('clearButton')
        self.clearButton.move(self.width() - 33, 4)
        self.clearButton.setFixedSize(29, 25)
        self.clearButton.hide()

        self.clearButton.setIcon(FIF.CLOSE.icon())
        self.clearButton.setIconSize(QSize(10, 10))

        self.clearButton.setCursor(Qt.CursorShape.PointingHandCursor)

        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self.__onTextChanged)

    def setClearButtonEnabled(self, enable: bool):
        self._isClearButtonEnabled = enable

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


