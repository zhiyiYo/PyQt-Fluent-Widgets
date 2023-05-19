# coding:utf-8
from typing import Dict

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QFont
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QHBoxLayout, QSizePolicy

from ...common.style_sheet import themeColor, FluentStyleSheet
from ..widgets.scroll_area import SingleDirectionScrollArea


class PivotItem(QPushButton):
    """ Pivot item """

    itemClicked = pyqtSignal(bool)

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.isSelected = False
        self.setProperty('isSelected', False)
        self.clicked.connect(lambda: self.itemClicked.emit(True))

        font = QFont()
        font.setFamilies(['Segoe UI', 'Microsoft YaHei'])
        font.setPixelSize(18)
        self.setFont(font)

    def setSelected(self, isSelected: bool):
        if self.isSelected == isSelected:
            return

        self.isSelected = isSelected
        self.setProperty('isSelected', isSelected)
        self.setStyle(QApplication.style())
        self.update()

    def paintEvent(self, e):
        super().paintEvent(e)
        if not self.isSelected:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(themeColor())

        x = int(self.width() / 2 - 8)
        painter.drawRoundedRect(x, self.height() - 3, 16, 3, 1.5, 1.5)


class Pivot(QWidget):
    """ Pivot """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = {}  # type: Dict[str, PivotItem]

        self.hBoxLayout = QHBoxLayout(self)

        # self.setWidget(self.view)
        # self.setWidgetResizable(True)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setViewportMargins(0, 0, 0, 0)

        FluentStyleSheet.PIVOT.apply(self)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    def addItem(self, routeKey: str, text: str, onClick):
        """ add item

        Parameters
        ----------
        routeKey: str
            the unique name of item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal
        """
        return self.insertItem(-1, routeKey, text, onClick)

    def insertItem(self, index: int, routeKey: str, text: str, onClick):
        """ insert item

        Parameters
        ----------
        index: int
            insert position

        routeKey: str
            the unique name of item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal
        """
        if routeKey in self.items:
            return

        item = PivotItem(text, self)
        item.setProperty('routeKey', routeKey)
        item.itemClicked.connect(self._onItemClicked)
        item.itemClicked.connect(onClick)

        self.items[routeKey] = item
        self.hBoxLayout.insertWidget(index, item, 0, Qt.AlignmentFlag.AlignLeft)
        return item

    def setCurrentItem(self, routeKey: str):
        """ set current selected item

        Parameters
        ----------
        routeKey: str
            the unique name of item
        """
        if routeKey not in self.items:
            return

        for k, item in self.items.items():
            item.setSelected(k == routeKey)

    def setItemFontSize(self, size: int):
        """ set the pixel font size of items """
        for item in self.items.values():
            font = item.font()
            font.setPixelSize(size)
            item.setFont(font)
            item.adjustSize()

    def _onItemClicked(self):
        item = self.sender()  # type: PivotItem
        self.setCurrentItem(item.property('routeKey'))
