# coding:utf-8
from enum import Enum
from typing import Iterable

from PySide6.QtCore import Qt, Signal, QSize, QEvent, QRectF
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QToolButton

from .scroll_area import SmoothScrollBar
from ...common.icon import FluentIconBase, Theme, getIconColor


class ScrollIcon(FluentIconBase, Enum):
    """ Scroll icon """

    UP = "Up"
    DOWN = "Down"

    def path(self, theme=Theme.AUTO):
        if theme == Theme.AUTO:
            c = getIconColor()
        else:
            c = "white" if theme == Theme.DARK else "black"

        return f':/qfluentwidgets/images/time_picker/{self.value}_{c}.svg'


class ScrollButton(QToolButton):
    """ Scroll button """

    def __init__(self, icon: ScrollIcon, parent=None):
        super().__init__(parent=parent)
        self._icon = icon
        self.isPressed = False
        self.installEventFilter(self)

    def eventFilter(self, obj, e: QEvent):
        if obj is self:
            if e.type() == QEvent.MouseButtonPress:
                self.isPressed = True
                self.update()
            elif e.type() == QEvent.MouseButtonRelease:
                self.isPressed = False
                self.update()

        return super().eventFilter(obj, e)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        if not self.isPressed:
            w, h = 10, 10
        else:
            w, h = 8, 8

        x = (self.width() - w) / 2
        y = (self.height() - h) / 2
        self._icon.render(painter, QRectF(x, y, w, h))


class CycleListWidget(QListWidget):
    """ Cycle list widget """

    def __init__(self, items: Iterable, itemSize: QSize, align=Qt.AlignCenter, parent=None):
        """
        Parameters
        ----------
        items: Iterable[Any]
            the items to be added

        itemSize: QSize
            the size of item

        align: Qt.AlignmentFlag
            the text alignment of item

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.itemSize = itemSize
        self.upButton = ScrollButton(ScrollIcon.UP, self)
        self.downButton = ScrollButton(ScrollIcon.DOWN, self)
        self.scrollDuration = 250
        self.originItems = list(items)

        self.vScrollBar = SmoothScrollBar(self)
        self.visibleNumber = 9

        # repeat adding items to achieve circular scrolling
        self._createItems(items, itemSize, align)

        self.setVerticalScrollMode(self.ScrollMode.ScrollPerPixel)
        self.setVerticalScrollBar(self.vScrollBar)
        self.vScrollBar.setScrollAnimation(self.scrollDuration)

        self.setViewportMargins(0, 0, 0, 0)
        self.setFixedSize(itemSize.width()+8, itemSize.height()*self.visibleNumber)

        # hide scroll bar
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.upButton.hide()
        self.downButton.hide()

        self.upButton.clicked.connect(self.scrollUp)
        self.downButton.clicked.connect(self.scrollDown)
        self.itemClicked.connect(self._onItemClicked)

        self.installEventFilter(self)

    def _createItems(self, items: list, itemSize: QSize, align=Qt.AlignCenter):
        N = len(items)
        self.isCycle = N > self.visibleNumber

        if self.isCycle:
            for _ in range(2):
                self._addColumnItems(items, itemSize, align)

            self._currentIndex = len(items)
            super().scrollToItem(
                self.item(self.currentIndex()-self.visibleNumber//2), QListWidget.PositionAtTop)
        else:
            n = self.visibleNumber // 2  # add empty items to enable scrolling

            self._addColumnItems(['']*n, itemSize, align, True)
            self._addColumnItems(items, itemSize, align)
            self._addColumnItems(['']*n, itemSize, align, True)

            self._currentIndex = n

    def _addColumnItems(self, items, itemSize, align, disabled=False):
        for i in items:
            item = QListWidgetItem(str(i), self)
            item.setSizeHint(itemSize)
            item.setTextAlignment(align | Qt.AlignVCenter)
            if disabled:
                item.setFlags(Qt.NoItemFlags)

            self.addItem(item)

    def _onItemClicked(self, item):
        self.setCurrentIndex(self.row(item))
        self.scrollToItem(self.currentItem())

    def setSelectedItem(self, text: str):
        """ set the selected item """
        if text is None:
            return

        items = self.findItems(str(text), Qt.MatchExactly)
        if not items:
            return

        if len(items) >= 2:
            self.setCurrentIndex(self.row(items[1]))
        else:
            self.setCurrentIndex(self.row(items[0]))

        super().scrollToItem(self.currentItem(), QListWidget.PositionAtCenter)

    def scrollToItem(self, item: QListWidgetItem, hint=QListWidget.PositionAtCenter):
        """ scroll to item """
        # scroll to center position
        index = self.row(item)
        y = item.sizeHint().height() * (index - self.visibleNumber // 2)
        self.vScrollBar.scrollTo(y)

        # clear selection
        self.clearSelection()
        item.setSelected(False)

    def wheelEvent(self, e):
        if e.angleDelta().y() < 0:
            self.scrollDown()
        else:
            self.scrollUp()

    def scrollDown(self):
        """ scroll down an item """
        self.setCurrentIndex(self.currentIndex() + 1)
        self.scrollToItem(self.currentItem())

    def scrollUp(self):
        """ scroll up an item """
        self.setCurrentIndex(self.currentIndex() - 1)
        self.scrollToItem(self.currentItem())

    def enterEvent(self, e):
        self.upButton.show()
        self.downButton.show()

    def leaveEvent(self, e):
        self.upButton.hide()
        self.downButton.hide()

    def resizeEvent(self, e):
        self.upButton.resize(self.width(), 34)
        self.downButton.resize(self.width(), 34)
        self.downButton.move(0, self.height() - 34)

    def eventFilter(self, obj, e: QEvent):
        if obj is not self or e.type() != QEvent.KeyPress:
            return super().eventFilter(obj, e)

        if e.key() == Qt.Key_Down:
            self.scrollDown()
            return True
        elif e.key() == Qt.Key_Up:
            self.scrollUp()
            return True

        return super().eventFilter(obj, e)

    def currentItem(self):
        return self.item(self.currentIndex())

    def currentIndex(self):
        return self._currentIndex

    def setCurrentIndex(self, index: int):
        if not self.isCycle:
            n = self.visibleNumber // 2
            self._currentIndex = max(n, min(n + len(self.originItems) - 1, index))
        else:
            N = self.count() // 2
            m = (self.visibleNumber + 1) // 2
            self._currentIndex = index

            # scroll to center to achieve circular scrolling
            if index >= self.count() - m:
                self._currentIndex = N + index - self.count()
                super().scrollToItem(self.item(self.currentIndex() - 1), self.PositionAtCenter)
            elif index <= m - 1:
                self._currentIndex = N + index
                super().scrollToItem(self.item(N + index + 1), self.PositionAtCenter)
