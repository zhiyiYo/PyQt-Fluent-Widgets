# coding:utf-8
from typing import Union
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QIcon
from PyQt5.QtWidgets import QApplication

from ...common.font import setFont
from ...common.icon import FluentIconBase
from ...common.style_sheet import themeColor, FluentStyleSheet
from ..widgets.button import PushButton, ToolButton, TransparentToggleToolButton
from .pivot import Pivot, PivotItem


class SegmentedItem(PivotItem):
    """ Segmented item """

    def _postInit(self):
        super()._postInit()
        setFont(self, 14)

    def paintEvent(self, e):
        PushButton.paintEvent(self, e)

        # draw indicator
        if not self.isSelected:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(themeColor())

        w = 16 if not self.isPressed else 10
        x = int(self.width() / 2 - w / 2)
        painter.drawRoundedRect(x, self.height() - 4, w, 3, 1.5, 1.5)


class SegmentedToolItem(ToolButton):
    """ Pivot item """

    itemClicked = pyqtSignal(bool)

    def _postInit(self):
        self.isSelected = False
        self.setProperty('isSelected', False)
        self.clicked.connect(lambda: self.itemClicked.emit(True))

        FluentStyleSheet.PIVOT.apply(self)

    def setSelected(self, isSelected: bool):
        if self.isSelected == isSelected:
            return

        self.isSelected = isSelected
        self.setProperty('isSelected', isSelected)
        self.setStyle(QApplication.style())
        self.update()

    def paintEvent(self, e):
        super().paintEvent(e)

        # draw indicator
        if not self.isSelected:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(themeColor())

        x = int(self.width() / 2 - 8)
        painter.drawRoundedRect(x, self.height() - 3, 16, 3, 1.5, 1.5)


class SegmentedToggleToolItem(TransparentToggleToolButton):

    itemClicked = pyqtSignal(bool)

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


class SegmentedToolWidget(Pivot):
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