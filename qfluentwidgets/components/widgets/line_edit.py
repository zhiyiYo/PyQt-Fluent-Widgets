# coding: utf-8
from qtpy.QtCore import QSize, Qt, QRectF, QEvent
from qtpy.QtGui import QPainter, QPainterPath
from qtpy.QtWidgets import QLineEdit, QToolButton, QTextEdit, QPlainTextEdit

from ...common.style_sheet import setStyleSheet, themeColor
from ...common.icon import writeSvg, isDarkTheme, drawSvgIcon
from ...common.icon import FluentIcon as FIF
from ...common.smooth_scroll import SmoothMode, SmoothScroll
from .menu import LineEditMenu, TextEditMenu


class ClearButton(QToolButton):
    """ Clear button """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(29, 25)
        self.setIconSize(QSize(10, 10))
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName('clearButton')
        setStyleSheet(self, 'line_edit')

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        if isDarkTheme():
            FIF.CLOSE.render(painter, QRectF(9.5, 7, 10, 10))
        else:
            svg = writeSvg(FIF.CLOSE.path(), fill='#656565')
            drawSvgIcon(svg.encode(), painter, QRectF(9.5, 7, 10, 10))


class LineEdit(QLineEdit):
    """ Line edit """

    def __init__(self, contents='', parent=None):
        super().__init__(contents, parent)
        self._isClearButtonEnabled = False

        setStyleSheet(self, 'line_edit')
        self.setFixedHeight(33)
        self.setAttribute(Qt.WA_MacShowFocusRect, False)

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
        menu.exec_(e.globalPos())

    def resizeEvent(self, e):
        self.clearButton.move(self.width() - 33, 4)

    def paintEvent(self, e):
        super().paintEvent(e)
        if not self.hasFocus():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        w, h = self.width() - 2, self.height()
        path.addRoundedRect(QRectF(1, h-12, w, 12), 6, 6)

        rectPath = QPainterPath()
        rectPath.addRect(1, h-12, w, 9.5)
        path = path.subtracted(rectPath)

        painter.fillPath(path, themeColor())


class TextEdit(QTextEdit):
    """ Text edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.verticalSmoothScroll = SmoothScroll(self, Qt.Vertical)
        self.horizonSmoothScroll = SmoothScroll(self, Qt.Horizontal)
        setStyleSheet(self, 'line_edit')

    def contextMenuEvent(self, e):
        menu = TextEditMenu(self)
        menu.exec_(e.globalPos())

    def wheelEvent(self, e):
        if e.modifiers() == Qt.NoModifier:
            self.verticalSmoothScroll.wheelEvent(e)
        else:
            self.horizonSmoothScroll.wheelEvent(e)


class PlainTextEdit(QPlainTextEdit):
    """ Plain text edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.verticalSmoothScroll = SmoothScroll(self, Qt.Vertical)
        self.horizonSmoothScroll = SmoothScroll(self, Qt.Horizontal)
        setStyleSheet(self, 'line_edit')

    def contextMenuEvent(self, e):
        menu = TextEditMenu(self)
        menu.exec_(e.globalPos())

    def wheelEvent(self, e):
        if e.modifiers() == Qt.NoModifier:
            self.verticalSmoothScroll.wheelEvent(e)
        else:
            self.horizonSmoothScroll.wheelEvent(e)

