# coding:utf-8
from enum import Enum

from PyQt5.QtCore import Qt, QSize, QRectF, QPoint
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtWidgets import (QSpinBox, QDoubleSpinBox, QToolButton, QHBoxLayout,
                             QDateEdit, QDateTimeEdit, QTimeEdit, QVBoxLayout, QApplication)

from ...common.style_sheet import FluentStyleSheet, themeColor, isDarkTheme
from ...common.icon import FluentIconBase, Theme, getIconColor
from ...common.font import setFont
from ...common.color import FluentSystemColor, autoFallbackThemeColor
from .button import TransparentToolButton
from .line_edit import LineEditMenu
from .flyout import Flyout, FlyoutViewBase, FlyoutAnimationType


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

        if not self.isEnabled():
            painter.setOpacity(0.36)
        elif self.isPressed:
            painter.setOpacity(0.7)

        self._icon.render(painter, QRectF(10, 6.5, 11, 11))


class CompactSpinButton(QToolButton):
    """ Compact spin button """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(26, 33)
        self.setCursor(Qt.IBeamCursor)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        x = (self.width() - 10) / 2
        s = 9

        SpinIcon.UP.render(painter, QRectF(x, self.height() / 2 - s + 1, s, s))
        SpinIcon.DOWN.render(painter, QRectF(x, self.height() / 2 , s, s))


class SpinFlyoutView(FlyoutViewBase):
    """ Spin flyout view """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.upButton = TransparentToolButton(SpinIcon.UP, self)
        self.downButton = TransparentToolButton(SpinIcon.DOWN, self)
        self.vBoxLayout = QVBoxLayout(self)

        self.upButton.setFixedSize(36, 36)
        self.downButton.setFixedSize(36, 36)
        self.upButton.setIconSize(QSize(13, 13))
        self.downButton.setIconSize(QSize(13, 13))

        self.vBoxLayout.setContentsMargins(6, 6, 6, 6)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.upButton)
        self.vBoxLayout.addWidget(self.downButton)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        painter.setBrush(
            QColor(46, 46, 46) if isDarkTheme() else QColor(249, 249, 249))
        painter.setPen(
            QColor(0, 0, 0, 51) if isDarkTheme() else QColor(0, 0, 0, 15))

        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 8, 8)


class SpinBoxBase:
    """ Spin box ui """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._isError = False
        self.lightFocusedBorderColor = QColor()
        self.darkFocusedBorderColor = QColor()

        self.hBoxLayout = QHBoxLayout(self)

        self.setProperty('transparent', True)
        FluentStyleSheet.SPIN_BOX.apply(self)
        self.setButtonSymbols(QSpinBox.NoButtons)
        self.setFixedHeight(33)
        setFont(self)

        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._showContextMenu)

    def isError(self):
        return self._isError

    def setError(self, isError: bool):
        """ set the error status """
        if isError == self.isError():
            return

        self._isError = isError
        self.update()

    def setReadOnly(self, isReadOnly: bool):
        super().setReadOnly(isReadOnly)
        self.setSymbolVisible(not isReadOnly)

    def setSymbolVisible(self, isVisible: bool):
        """ set whether the spin symbol is visible """
        self.setProperty("symbolVisible", isVisible)
        self.setStyle(QApplication.style())

    def setCustomFocusedBorderColor(self, light, dark):
        """ set the border color in focused status

        Parameters
        ----------
        light, dark: str | QColor | Qt.GlobalColor
            border color in light/dark theme mode
        """
        self.lightFocusedBorderColor = QColor(light)
        self.darkFocusedBorderColor = QColor(dark)
        self.update()

    def focusedBorderColor(self):
        if self.isError():
            return FluentSystemColor.CRITICAL_FOREGROUND.color()

        return autoFallbackThemeColor(self.lightFocusedBorderColor, self.darkFocusedBorderColor)

    def _showContextMenu(self, pos):
        menu = LineEditMenu(self.lineEdit())
        menu.exec_(self.mapToGlobal(pos))

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

        painter.fillPath(path, self.focusedBorderColor())

    def paintEvent(self, e):
        super().paintEvent(e)
        self._drawBorderBottom()


class InlineSpinBoxBase(SpinBoxBase):
    """ Inline spin box base """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.upButton = SpinButton(SpinIcon.UP, self)
        self.downButton = SpinButton(SpinIcon.DOWN, self)

        self.hBoxLayout.setContentsMargins(0, 4, 4, 4)
        self.hBoxLayout.setSpacing(5)
        self.hBoxLayout.addWidget(self.upButton, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.downButton, 0, Qt.AlignRight)
        self.hBoxLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.upButton.clicked.connect(self.stepUp)
        self.downButton.clicked.connect(self.stepDown)

    def setSymbolVisible(self, isVisible: bool):
        super().setSymbolVisible(isVisible)
        self.upButton.setVisible(isVisible)
        self.downButton.setVisible(isVisible)

    def setAccelerated(self, on: bool):
        super().setAccelerated(on)
        self.upButton.setAutoRepeat(on)
        self.downButton.setAutoRepeat(on)


class CompactSpinBoxBase(SpinBoxBase):
    """ Compact spin box base """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.compactSpinButton = CompactSpinButton(self)
        self.spinFlyoutView = SpinFlyoutView(self)
        self.spinFlyout = Flyout(self.spinFlyoutView, self, False)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.compactSpinButton, 0, Qt.AlignRight)
        self.hBoxLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.compactSpinButton.clicked.connect(self._showFlyout)
        self.spinFlyoutView.upButton.clicked.connect(self.stepUp)
        self.spinFlyoutView.downButton.clicked.connect(self.stepDown)

        self.spinFlyout.hide()

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self._showFlyout()

    def setAccelerated(self, on: bool):
        super().setAccelerated(on)
        self.spinFlyoutView.upButton.setAutoRepeat(on)
        self.spinFlyoutView.downButton.setAutoRepeat(on)

    def setSymbolVisible(self, isVisible: bool):
        super().setSymbolVisible(isVisible)
        self.compactSpinButton.setVisible(isVisible)

    def _showFlyout(self):
        if self.spinFlyout.isVisible() or self.isReadOnly():
            return

        y = int(self.compactSpinButton.height() / 2 - 46)
        pos = self.compactSpinButton.mapToGlobal(QPoint(-12, y))

        self.spinFlyout.exec(pos, FlyoutAnimationType.FADE_IN)


class SpinBox(InlineSpinBoxBase, QSpinBox):
    """ Spin box """


class CompactSpinBox(CompactSpinBoxBase, QSpinBox):
    """ Compact spin box """


class DoubleSpinBox(InlineSpinBoxBase, QDoubleSpinBox):
    """ Double spin box """


class CompactDoubleSpinBox(CompactSpinBoxBase, QDoubleSpinBox):
    """ Compact double spin box """


class TimeEdit(InlineSpinBoxBase, QTimeEdit):
    """ Time edit """


class CompactTimeEdit(CompactSpinBoxBase, QTimeEdit):
    """ Compact time edit """


class DateTimeEdit(InlineSpinBoxBase, QDateTimeEdit):
    """ Date time edit """


class CompactDateTimeEdit(CompactSpinBoxBase, QDateTimeEdit):
    """ Compact date time edit """


class DateEdit(InlineSpinBoxBase, QDateEdit):
    """ Date edit """


class CompactDateEdit(CompactSpinBoxBase, QDateEdit):
    """ Compact date edit """

