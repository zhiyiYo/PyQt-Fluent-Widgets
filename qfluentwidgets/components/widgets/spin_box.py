# coding:utf-8
from enum import Enum

from PySide6.QtCore import Qt, QSize, QRectF
from PySide6.QtGui import QPainter, QPainterPath
from PySide6.QtWidgets import (QSpinBox, QDoubleSpinBox, QToolButton, QHBoxLayout,
                             QDateEdit, QDateTimeEdit, QTimeEdit, QLineEdit, QAbstractSpinBox)

from ...common.style_sheet import FluentStyleSheet, themeColor
from ...common.icon import FluentIconBase, Theme, getIconColor
from ...common.font import setFont
from ...components.widgets import LineEditMenu


class SpinIcon(FluentIconBase, Enum):
    """ Spin icon """

    UP = "Up"
    DOWN = "Down"

    def path(self, theme=Theme.AUTO):
        return f':/qfluentwidgets/images/spin_box/{self.value}_{getIconColor(theme)}.svg'



class SpinButton(QToolButton):

    def __init__(self, icon: SpinIcon, parent=None):
        super().__init__(parent=parent)
        self.isPressed = False
        self._icon = icon
        self.setFixedSize(31, 23)
        self.setIconSize(QSize(10, 10))
        FluentStyleSheet.SPIN_BOX.apply(self)

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        if self.isPressed:
            painter.setOpacity(0.7)

        self._icon.render(painter, QRectF(10, 9, 11, 11))


class SpinBoxBase:
    """ Spin box ui """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setProperty('transparent', True)
        FluentStyleSheet.SPIN_BOX.apply(self)
        self.setButtonSymbols(QSpinBox.NoButtons)
        self.setFixedHeight(33)
        setFont(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.upButton = SpinButton(SpinIcon.UP, self)
        self.downButton = SpinButton(SpinIcon.DOWN, self)

        self.hBoxLayout.setContentsMargins(0, 4, 4, 4)
        self.hBoxLayout.setSpacing(5)
        self.hBoxLayout.addWidget(self.upButton, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.downButton, 0, Qt.AlignRight)
        self.hBoxLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.upButton.clicked.connect(self.stepUp)
        self.downButton.clicked.connect(self.stepDown)

        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._showContextMenu)

    def _showContextMenu(self, pos):
        menu = LineEditMenu(self.lineEdit())
        menu.exec_(self.mapToGlobal(pos))

    def setAccelerated(self, on: bool):
        super().setAccelerated(on)
        self.upButton.setAutoRepeat(on)
        self.downButton.setAutoRepeat(on)

    def _drawBorderBottom(self):
        if not self.hasFocus():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, h-10, w, 10), 5, 5)

        rectPath = QPainterPath()
        rectPath.addRect(0, h-10, w, 8)
        path = path.subtracted(rectPath)

        painter.fillPath(path, themeColor())


class SpinBox(SpinBoxBase, QSpinBox):
    """ Spin box """

    def paintEvent(self, e):
        QSpinBox.paintEvent(self, e)
        self._drawBorderBottom()


class DoubleSpinBox(SpinBoxBase, QDoubleSpinBox):
    """ Double spin box """

    def paintEvent(self, e):
        QDoubleSpinBox.paintEvent(self, e)
        self._drawBorderBottom()


class TimeEdit(SpinBoxBase, QTimeEdit):
    """ Time edit """

    def paintEvent(self, e):
        QTimeEdit.paintEvent(self, e)
        self._drawBorderBottom()


class DateTimeEdit(SpinBoxBase, QDateTimeEdit):
    """ Date time edit """

    def paintEvent(self, e):
        QDateTimeEdit.paintEvent(self, e)
        self._drawBorderBottom()


class DateEdit(SpinBoxBase, QDateEdit):
    """ Date edit """

    def paintEvent(self, e):
        QDateEdit.paintEvent(self, e)
        self._drawBorderBottom()

