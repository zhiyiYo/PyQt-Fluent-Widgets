# coding:utf-8
from typing import Union
from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QPainter, QIcon, QColor
from PySide6.QtWidgets import QApplication, QWidget

from ...common.font import setFont
from ...common.icon import FluentIconBase, drawIcon, Theme
from ...common.color import autoFallbackThemeColor
from ...common.style_sheet import themeColor, FluentStyleSheet, isDarkTheme
from ..widgets.button import PushButton, ToolButton, TransparentToolButton
from .pivot import Pivot, PivotItem


class SegmentedItem(PivotItem):
    """ Segmented item """

    def _postInit(self):
        super()._postInit()
        setFont(self, 14)


class SegmentedToolItem(ToolButton):
    """ Pivot item """

    itemClicked = Signal(bool)

    def _postInit(self):
        self.isSelected = False
        self.setProperty('isSelected', False)
        self.clicked.connect(lambda: self.itemClicked.emit(True))

        self.setFixedSize(38, 33)
        FluentStyleSheet.PIVOT.apply(self)

    def setSelected(self, isSelected: bool):
        if self.isSelected == isSelected:
            return

        self.isSelected = isSelected
        self.setProperty('isSelected', isSelected)
        self.setStyle(QApplication.style())
        self.update()


class SegmentedToggleToolItem(TransparentToolButton):

    itemClicked = Signal(bool)

    def _postInit(self):
        super()._postInit()
        self.isSelected = False

        self.setFixedSize(50, 32)
        self.clicked.connect(lambda: self.itemClicked.emit(True))

    def setSelected(self, isSelected: bool):
        if self.isSelected == isSelected:
            return

        self.isSelected = isSelected
        self.setChecked(isSelected)

    def _drawIcon(self, icon, painter: QPainter, rect: QRectF, state=QIcon.State.Off):
        if self.isSelected and isinstance(icon, FluentIconBase):
            theme = Theme.DARK if not isDarkTheme() else Theme.LIGHT
            icon = icon.icon(theme)

        return drawIcon(icon, painter, rect, state)


class SegmentedWidget(Pivot):
    """ Segmented widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)

    def insertItem(self, index: int, routeKey: str, text: str, onClick=None, icon=None):
        if routeKey in self.items:
            return

        item = SegmentedItem(text, self)
        if icon:
            item.setIcon(icon)

        self.insertWidget(index, routeKey, item, onClick)
        return item

    def paintEvent(self, e):
        QWidget.paintEvent(self, e)

        if not self.currentItem():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        # draw background
        if isDarkTheme():
            painter.setPen(QColor(255, 255, 255, 14))
            painter.setBrush(QColor(255, 255, 255, 15))
        else:
            painter.setPen(QColor(0, 0, 0, 19))
            painter.setBrush(QColor(255, 255, 255, 179))

        item = self.currentItem()
        rect = item.rect().adjusted(1, 1, -1, -1).translated(int(self.slideAni.value()), 0)
        painter.drawRoundedRect(rect, 5, 5)

        # draw indicator
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(autoFallbackThemeColor(self.lightIndicatorColor, self.darkIndicatorColor))

        x = int(self.currentItem().width() / 2 - 8 + self.slideAni.value())
        painter.drawRoundedRect(QRectF(x, self.height() - 3.5, 16, 3), 1.5, 1.5)


class SegmentedToolWidget(SegmentedWidget):
    """ Segmented tool widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)

    def addItem(self, routeKey: str, icon: Union[str, QIcon, FluentIconBase], onClick=None):
        """ add item

        Parameters
        ----------
        routeKey: str
            the unique name of item

        icon: str | QIcon | FluentIconBase
            the icon of navigation item

        onClick: callable
            the slot connected to item clicked signal
        """
        return self.insertItem(-1, routeKey, icon, onClick)

    def insertItem(self, index: int, routeKey: str, icon: Union[str, QIcon, FluentIconBase], onClick=None):
        if routeKey in self.items:
            return

        item = self._createItem(icon)
        self.insertWidget(index, routeKey, item, onClick)
        return item

    def _createItem(self, icon):
        return SegmentedToolItem(icon)


class SegmentedToggleToolWidget(SegmentedToolWidget):
    """ Segmented toggle tool widget """

    def _createItem(self, icon):
        return SegmentedToggleToolItem(icon)

    def paintEvent(self, e):
        QWidget.paintEvent(self, e)

        if not self.currentItem():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(autoFallbackThemeColor(self.lightIndicatorColor, self.darkIndicatorColor))

        item = self.currentItem()
        painter.drawRoundedRect(
            QRectF(self.slideAni.value(), 0, item.width(), item.height()), 4, 4)