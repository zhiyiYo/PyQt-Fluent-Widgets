# coding:utf-8
from copy import deepcopy
from enum import Enum
from typing import List, Union
from PyQt5.QtCore import Qt, pyqtSignal, pyqtProperty, QRectF, QSize
from PyQt5.QtGui import QPixmap, QPainter, QColor, QIcon, QPainterPath, QLinearGradient, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QHBoxLayout, QSizePolicy

from ...common.icon import FluentIcon, FluentIconBase, drawIcon
from ...common.style_sheet import isDarkTheme, FluentStyleSheet
from ...common.font import setFont
from .button import TransparentToolButton, PushButton
from .scroll_area import SingleDirectionScrollArea


class TabCloseButtonDisplayMode(Enum):
    """ Tab close button display mode """
    ALWAYS = 0
    ON_HOVER = 1
    NEVER = 2


def checkIndex(*default):
    """ decorator for index checking

    Parameters
    ----------
    *default:
        the default value returned when an index overflow
    """

    def outer(func):

        def inner(tabBar, index: int, *args, **kwargs):
            if 0 <= index < len(tabBar.items):
                return func(tabBar, index, *args, **kwargs)

            value = deepcopy(default)
            if len(value) == 0:
                return None
            elif len(value) == 1:
                return value[0]

            return value

        return inner

    return outer


class TabItem(PushButton):
    """ Tab item """

    closed = pyqtSignal()

    def _postInit(self):
        super()._postInit()
        self.borderRadius = 6
        self.isSelected = False
        self.textColor = None
        self.closeButtonDisplayMode = TabCloseButtonDisplayMode.ALWAYS

        self.closeButton = TransparentToolButton(FluentIcon.CLOSE, self)
        self.shadowEffect = QGraphicsDropShadowEffect(self)

        self.__initWidget()

    def __initWidget(self):
        setFont(self, 12)
        self.setFixedSize(240, 36)

        self.closeButton.setFixedSize(32, 24)
        self.closeButton.setIconSize(QSize(10, 10))

        self.shadowEffect.setBlurRadius(12)
        self.shadowEffect.setOffset(0, 0)
        self.setGraphicsEffect(self.shadowEffect)
        self.setSelected(False)

        self.closeButton.clicked.connect(self.closed)

    def setBorderRadius(self, radius: int):
        self.borderRadius = radius
        self.update()

    def setSelected(self, isSelected: bool):
        self.isSelected = isSelected
        self.shadowEffect.setColor(QColor(0, 0, 0, 50*isSelected))
        self.update()

        if self.closeButtonDisplayMode == TabCloseButtonDisplayMode.ON_HOVER:
            self.closeButton.setVisible(isSelected)

    def setCloseButtonDisplayMode(self, mode: TabCloseButtonDisplayMode):
        """ set close button display mode """
        if mode == self.closeButtonDisplayMode:
            return

        self.closeButtonDisplayMode = mode

        if mode == TabCloseButtonDisplayMode.NEVER:
            self.closeButton.hide()
        elif mode == TabCloseButtonDisplayMode.ALWAYS:
            self.closeButton.show()
        else:
            self.closeButton.setVisible(self.isHover or self.isSelected)

    def setTextColor(self, color: QColor):
        self.textColor = color
        self.update()

    def resizeEvent(self, e):
        self.closeButton.move(
            self.width()-6-self.closeButton.width(), int(self.height()/2-self.closeButton.height()/2))

    def enterEvent(self, e):
        super().enterEvent(e)
        if self.closeButtonDisplayMode == TabCloseButtonDisplayMode.ON_HOVER:
            self.closeButton.show()

    def leaveEvent(self, e):
        super().leaveEvent(e)
        if self.closeButtonDisplayMode == TabCloseButtonDisplayMode.ON_HOVER and not self.isSelected:
            self.closeButton.hide()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        if self.isSelected:
            self._drawSelectedBackground(painter)
        else:
            self._drawNotSelectedBackground(painter)

        # draw icon
        if not self.isSelected:
            painter.setOpacity(0.79 if isDarkTheme() else 0.61)

        drawIcon(self._icon, painter, QRectF(10, 10, 16, 16))

        # draw text
        self._drawText(painter)

    def _drawSelectedBackground(self, painter: QPainter):
        w, h = self.width(), self.height()
        r = self.borderRadius
        d = 2 * r

        isDark = isDarkTheme()

        # draw top border
        path = QPainterPath()
        path.arcMoveTo(1, h - d - 1, d, d, 225)
        path.arcTo(1, h - d - 1, d, d, 225, -45)
        path.lineTo(1, r)
        path.arcTo(1, 1, d, d, -180, -90)
        path.lineTo(w - r, 1)
        path.arcTo(w - d - 1, 1, d, d, 90, -90)
        path.lineTo(w - 1, h - r)
        path.arcTo(w - d - 1, h - d - 1, d, d, 0, -45)

        topBorderColor = QColor(0, 0, 0, 20)
        if isDark:
            if self.isPressed:
                topBorderColor = QColor(255, 255, 255, 18)
            elif self.isHover:
                topBorderColor = QColor(255, 255, 255, 13)
        else:
            topBorderColor = QColor(0, 0, 0, 16)

        painter.strokePath(path, topBorderColor)

        # draw bottom border
        path = QPainterPath()
        path.arcMoveTo(1, h - d - 1, d, d, 225)
        path.arcTo(1, h - d - 1, d, d, 225, 45)
        path.lineTo(w - r - 1, h - 1)
        path.arcTo(w - d - 1, h - d - 1, d, d, 270, 45)

        bottomBorderColor = topBorderColor
        if not isDark:
            bottomBorderColor = QColor(0, 0, 0, 63)

        painter.strokePath(path, bottomBorderColor)

        # draw background
        painter.setPen(Qt.NoPen)
        rect = self.rect().adjusted(1, 1, -1, -1)

        if isDark:
            color = QColor(40, 40, 40)
        else:
            color = QColor(246, 246, 246)

        painter.setBrush(color)
        painter.drawRoundedRect(rect, r, r)

    def _drawNotSelectedBackground(self, painter: QPainter):
        if not (self.isPressed or self.isHover):
            return

        isDark = isDarkTheme()

        if self.isPressed:
            color = QColor(255, 255, 255, 12) if isDark else QColor(0, 0, 0, 7)
        else:
            color = QColor(255, 255, 255, 15) if isDark else QColor(
                0, 0, 0, 10)

        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), self.borderRadius, self.borderRadius)

    def _drawText(self, painter: QPainter):
        tw = self.fontMetrics().width(self.text())

        if self.icon().isNull():
            dw = 55 if self.closeButton.isVisible() else 18
            rect = QRectF(18, 0, self.width() - dw, self.height())
        else:
            dw = 40 if self.closeButton.isVisible() else 12
            rect = QRectF(35, 0, self.width() - dw, self.height())

        pen = QPen()
        color = Qt.white if isDarkTheme() else Qt.black
        color = self.textColor or color

        if tw > rect.width():
            gradient = QLinearGradient(0, 0, rect.width(), 0)
            gradient.setColorAt(0, color)
            gradient.setColorAt(0.95, color)
            gradient.setColorAt(1, Qt.transparent)
            pen.setBrush(QBrush(gradient))
        else:
            pen.setColor(color)

        painter.setPen(pen)
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignVCenter | Qt.AlignLeft, self.text())


class TabBar(SingleDirectionScrollArea):
    """ Tab bar """

    currentChanged = pyqtSignal(int)
    tabBarClicked = pyqtSignal(int)
    tabCloseRequested = pyqtSignal(int)
    tabAddRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent, orient=Qt.Horizontal)
        self.items = []  # type: List[TabItem]
        self._currentIndex = -1
        self.closeButtonDisplayMode = TabCloseButtonDisplayMode.ALWAYS

        self.view = QWidget(self)
        self.hBoxLayout = QHBoxLayout(self.view)
        self.itemLayout = QHBoxLayout()
        self.widgetLayout = QHBoxLayout()

        self.addButton = TransparentToolButton(FluentIcon.ADD, self)

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(46)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.addButton.setFixedSize(32, 24)
        self.addButton.setIconSize(QSize(12, 12))
        self.addButton.clicked.connect(self.tabAddRequested)

        self.view.setObjectName('view')
        FluentStyleSheet.TAB_VIEW.apply(self)
        FluentStyleSheet.TAB_VIEW.apply(self.view)

        self.hBoxLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.itemLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.widgetLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.itemLayout.setContentsMargins(5, 5, 5, 5)
        self.widgetLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.hBoxLayout.setSpacing(0)
        self.itemLayout.setSpacing(0)

        self.hBoxLayout.addLayout(self.itemLayout)
        self.hBoxLayout.addSpacing(3)

        self.widgetLayout.addWidget(self.addButton, 0, Qt.AlignLeft)
        self.hBoxLayout.addLayout(self.widgetLayout)
        self.hBoxLayout.addStretch(1)

    def setAddButtonVisible(self, isVisible: bool):
        self.addButton.setVisible(isVisible)

    def addTab(self, text: str, icon: Union[QIcon, str, FluentIconBase] = None):
        """ add tab

        Parameters
        ----------
        text: str
            the text of tab item

        text: str
            the icon of tab item
        """
        self.insertTab(-1, text, icon)

    def insertTab(self, index: int, text: str, icon: Union[QIcon, str, FluentIconBase] = None):
        """ insert tab

        Parameters
        ----------
        index: int
            the insert position of tab item

        text: str
            the text of tab item

        text: str
            the icon of tab item
        """
        if index == -1:
            index = len(self.items)

        # adjust current index
        if index <= self.currentIndex() and self.currentIndex() >= 0:
            self._currentIndex += 1

        item = TabItem(text, self.view, icon)
        item.setCloseButtonDisplayMode(self.closeButtonDisplayMode)

        item.clicked.connect(self._onItemClicked)
        item.closed.connect(lambda: self.tabCloseRequested.emit(
            self.items.index(item)))

        self.itemLayout.insertWidget(index, item, 1)
        self.items.insert(index, item)

        if len(self.items) == 1:
            self.setCurrentIndex(0)

    def removeTab(self, index: int):
        if not 0 <= index < len(self.items):
            return

        # adjust current index
        if index < self.currentIndex():
            self._currentIndex -= 1
        elif index == self.currentIndex():
            if self.currentIndex() > 0:
                self.setCurrentIndex(self.currentIndex() - 1)
            elif len(self.items) == 0:
                self._currentIndex = -1
            else:
                self.setCurrentIndex(1)
                self._currentIndex = 0

        item = self.items.pop(index)
        self.hBoxLayout.removeWidget(item)
        item.deleteLater()

    def setCurrentIndex(self, index: int):
        """ set current index """
        if index == self._currentIndex:
            return

        if self.currentIndex() >= 0:
            self.items[self.currentIndex()].setSelected(False)

        self._currentIndex = index
        self.items[index].setSelected(True)

    def currentIndex(self):
        return self._currentIndex

    def _onItemClicked(self):
        for item in self.items:
            item.setSelected(item is self.sender())

        index = self.items.index(self.sender())
        self.tabBarClicked.emit(index)

        if index != self.currentIndex():
            self.setCurrentIndex(index)
            self.currentChanged.emit(index)

    def setCloseButtonDisplayMode(self, mode: TabCloseButtonDisplayMode):
        """ set close button display mode """
        if mode == self.closeButtonDisplayMode:
            return

        self.closeButtonDisplayMode = mode
        for item in self.items:
            item.setCloseButtonDisplayMode(mode)

    @checkIndex()
    def tabItem(self, index: int):
        return self.items[index]

    @checkIndex('')
    def tabText(self, index: int):
        return self.tabItem(index).text()

    @checkIndex()
    def tabIcon(self, index: int):
        return self.tabItem(index).icon()

    @checkIndex('')
    def tabToolTip(self, index: int):
        return self.tabItem(index).toolTip()

    def setTabsClosable(self, isClosable: bool):
        if isClosable:
            self.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ALWAYS)
        else:
            self.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.NEVER)

    def tabsClosable(self):
        return self.closeButtonDisplayMode != TabCloseButtonDisplayMode.NEVER

    @checkIndex()
    def setTabIcon(self, index: int, icon: Union[QIcon, FluentIconBase, str]):
        """ set tab icon """
        self.tabItem(index).setIcon(icon)

    @checkIndex()
    def setTabText(self, index: int, text: str):
        """ set tab text """
        self.tabItem(index).setText(text)

    @checkIndex()
    def setTabVisible(self, index: int, isVisible: bool):
        self.tabItem(index).setVisible(isVisible)

        if isVisible and self.currentIndex() < 0:
            self.setCurrentIndex(0)
        elif not isVisible:
            if self.currentIndex() > 0:
                self.setCurrentIndex(self.currentIndex() - 1)
            elif len(self.items) == 1:
                self._currentIndex = -1
            else:
                self.setCurrentIndex(1)
                self._currentIndex = 0

    def paintEvent(self, e):
        painter = QPainter(self.viewport())
        painter.setRenderHints(QPainter.Antialiasing)

        # draw separators
        if isDarkTheme():
            color = QColor(255, 255, 255, 21)
        else:
            color = QColor(0, 0, 0, 15)

        painter.setPen(color)

        for i, item in enumerate(self.items):
            canDraw = not (item.isHover or item.isSelected)
            if i < len(self.items) - 1:
                nextItem = self.items[i + 1]
                if nextItem.isHover or nextItem.isSelected:
                    canDraw = False

            if canDraw:
                x = item.geometry().right()
                y = self.height() / 2 - 8
                painter.drawLine(x, y, x, y + 16)