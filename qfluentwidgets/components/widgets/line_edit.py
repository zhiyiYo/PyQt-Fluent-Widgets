# coding: utf-8
from typing import Union
from PyQt6.QtCore import QSize, Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QPainter, QPainterPath, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QToolButton, QTextEdit, QPlainTextEdit

from ...common.style_sheet import FluentStyleSheet, themeColor
from ...common.icon import isDarkTheme, FluentIconBase, drawIcon
from ...common.icon import FluentIcon as FIF
from ...common.smooth_scroll import SmoothMode, SmoothScroll
from .menu import LineEditMenu, TextEditMenu


class LineEditButton(QToolButton):
    """ Line edit button """

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], parent=None):
        super().__init__(parent=parent)
        self._icon = icon
        self.setFixedSize(31, 23)
        self.setIconSize(QSize(10, 10))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName('lineEditButton')
        FluentStyleSheet.LINE_EDIT.apply(self)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)

        iw, ih = self.iconSize().width(), self.iconSize().height()
        w, h = self.width(), self.height()
        rect = QRectF((w - iw)/2, (h - ih)/2, iw, ih)

        if isDarkTheme():
            drawIcon(self._icon, painter, rect)
        else:
            drawIcon(self._icon, painter, rect, fill='#656565')


class LineEdit(QLineEdit):
    """ Line edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._isClearButtonEnabled = False

        FluentStyleSheet.LINE_EDIT.apply(self)
        self.setFixedHeight(33)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)

        self.hBoxLayout = QHBoxLayout(self)
        self.clearButton = LineEditButton(FIF.CLOSE, self)

        self.clearButton.setFixedSize(29, 25)
        self.clearButton.hide()

        self.hBoxLayout.setSpacing(3)
        self.hBoxLayout.setContentsMargins(4, 4, 4, 4)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addWidget(self.clearButton, 0, Qt.AlignmentFlag.AlignRight)

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

    def paintEvent(self, e):
        super().paintEvent(e)
        if not self.hasFocus():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        path = QPainterPath()
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, h-10, w, 10), 5, 5)

        rectPath = QPainterPath()
        rectPath.addRect(0, h-10, w, 8)
        path = path.subtracted(rectPath)

        painter.fillPath(path, themeColor())


class SearchLineEdit(LineEdit):
    """ Search line edit """

    searchSignal = pyqtSignal(str)
    clearSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.searchButton = LineEditButton(FIF.SEARCH, self)

        self.hBoxLayout.addWidget(self.searchButton, 0, Qt.AlignmentFlag.AlignRight)
        self.setClearButtonEnabled(True)
        self.setTextMargins(0, 0, 59, 0)

        self.searchButton.clicked.connect(self.search)
        self.clearButton.clicked.connect(self.clearSignal)

    def search(self):
        """ emit search signal """
        text = self.text().strip()
        if text:
            self.searchSignal.emit(text)
        else:
            self.clearSignal.emit()


class TextEdit(QTextEdit):
    """ Text edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.verticalSmoothScroll = SmoothScroll(self, Qt.Orientation.Vertical)
        self.horizonSmoothScroll = SmoothScroll(self, Qt.Orientation.Horizontal)
        FluentStyleSheet.LINE_EDIT.apply(self)

    def contextMenuEvent(self, e):
        menu = TextEditMenu(self)
        menu.exec(e.globalPos())

    def wheelEvent(self, e):
        if e.modifiers() == Qt.KeyboardModifier.NoModifier:
            self.verticalSmoothScroll.wheelEvent(e)
        else:
            self.horizonSmoothScroll.wheelEvent(e)


class PlainTextEdit(QPlainTextEdit):
    """ Plain text edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.verticalSmoothScroll = SmoothScroll(self, Qt.Orientation.Vertical)
        self.horizonSmoothScroll = SmoothScroll(self, Qt.Orientation.Horizontal)
        FluentStyleSheet.LINE_EDIT.apply(self)

    def contextMenuEvent(self, e):
        menu = TextEditMenu(self)
        menu.exec(e.globalPos())

    def wheelEvent(self, e):
        if e.modifiers() == Qt.KeyboardModifier.NoModifier:
            self.verticalSmoothScroll.wheelEvent(e)
        else:
            self.horizonSmoothScroll.wheelEvent(e)


class PlainTextEdit(QPlainTextEdit):
    """ Plain text edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.verticalSmoothScroll = SmoothScroll(self, Qt.Orientation.Vertical)
        self.horizonSmoothScroll = SmoothScroll(self, Qt.Orientation.Horizontal)
        FluentStyleSheet.LINE_EDIT.apply(self)

    def contextMenuEvent(self, e):
        menu = TextEditMenu(self)
        menu.exec(e.globalPos())

    def wheelEvent(self, e):
        if e.modifiers() == Qt.KeyboardModifier.NoModifier:
            self.verticalSmoothScroll.wheelEvent(e)
        else:
            self.horizonSmoothScroll.wheelEvent(e)
