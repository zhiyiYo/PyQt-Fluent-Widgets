# coding:utf-8
from enum import Enum
from typing import Dict, Union

from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QSize, QEvent, QEasingCurve
from PySide6.QtGui import QResizeEvent, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QApplication

from .navigation_widget import NavigationButton, MenuButton, NavigationWidget, NavigationSeparator
from ..widgets.scroll_area import ScrollArea
from ...common.style_sheet import setStyleSheet, getStyleSheet
from ...common.icon import FluentIconBase


class NavigationDisplayMode(Enum):
    """ Navigation display mode """
    MINIMAL = 0
    COMPACT = 1
    EXPAND = 2
    MENU = 3


class NavigationItemPostion(Enum):
    """ Navigation item position """
    TOP = 0
    SCROLL = 1
    BOTTOM = 2


class NavigationPanel(QFrame):
    """ Navigation panel """

    def __init__(self, parent=None, isMinimalEnabled=False):
        super().__init__(parent=parent)
        self._parent = parent   # type: QWidget
        self.scrollArea = ScrollArea(self)
        self.scrollWidget = QWidget()

        self.menuButton = MenuButton(self)

        self.vBoxLayout = NavigationItemLayout(self)
        self.topLayout = NavigationItemLayout()
        self.bottomLayout = NavigationItemLayout()
        self.scrollLayout = NavigationItemLayout(self.scrollWidget)
        self.items = {}   # type: Dict[str, NavigationWidget]

        self.expandAni = QPropertyAnimation(self, b'geometry', self)

        self.isMinimalEnabled = isMinimalEnabled
        if isMinimalEnabled:
            self.displayMode = NavigationDisplayMode.MINIMAL
        else:
            self.displayMode = NavigationDisplayMode.COMPACT

        self.__initWidget()

    def __initWidget(self):
        self.resize(48, self.height())
        self.setAttribute(Qt.WA_StyledBackground)
        self.window().installEventFilter(self)

        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)

        self.expandAni.setEasingCurve(QEasingCurve.OutQuad)
        self.expandAni.setDuration(150)

        self.menuButton.clicked.connect(self.toggle)
        self.expandAni.finished.connect(self._onExpandAniFinished)

        self.scrollWidget.setObjectName('scrollWidget')
        self.setProperty('menu', False)
        setStyleSheet(self, 'navigation_interface')
        self.__initLayout()

    def __initLayout(self):
        self.vBoxLayout.setContentsMargins(0, 5, 0, 5)
        self.topLayout.setContentsMargins(4, 0, 4, 0)
        self.bottomLayout.setContentsMargins(4, 0, 4, 0)
        self.scrollLayout.setContentsMargins(4, 0, 4, 0)
        self.vBoxLayout.setSpacing(4)
        self.topLayout.setSpacing(4)
        self.bottomLayout.setSpacing(4)
        self.scrollLayout.setSpacing(4)

        self.vBoxLayout.addLayout(self.topLayout, 0)
        self.vBoxLayout.addWidget(self.scrollArea, 1, Qt.AlignTop)
        self.vBoxLayout.addLayout(self.bottomLayout, 0)

        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.topLayout.setAlignment(Qt.AlignTop)
        self.scrollLayout.setAlignment(Qt.AlignTop)
        self.bottomLayout.setAlignment(Qt.AlignBottom)

        self.topLayout.addWidget(self.menuButton, 0, Qt.AlignTop)

    def addItem(self, routeKey: str, icon: Union[str, QIcon, FluentIconBase], text: str, onClick, selectable=True, position=NavigationItemPostion.TOP):
        """ add navigation item

        Parameters
        ----------
        routeKey: str
            the unique name of item

        icon: str | QIcon | FluentIconBase
            the icon of navigation item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        position: NavigationItemPostion
            where the button is added

        selectable: bool
            whether the item is selectable
        """
        if text in self.items:
            return

        button = NavigationButton(icon, text, selectable, self)
        self.addWidget(routeKey, button, onClick, position)

    def addWidget(self, routeKey: str, widget: NavigationWidget, onClick, position=NavigationItemPostion.TOP):
        """ add custom widget

        Parameters
        ----------
        routeKey: str
            the unique name of item

        widget: NavigationWidget
            the custom widget to be added

        onClick: callable
            the slot connected to item clicked signal

        position: NavigationItemPostion
            where the button is added
        """
        if routeKey in self.items:
            return

        widget.clicked.connect(self._onWidgetClicked)
        widget.clicked.connect(onClick)
        widget.setProperty('routeKey', routeKey)
        self.items[routeKey] = widget

        self._addWidgetToLayout(widget, position)

    def addSeparator(self, position=NavigationItemPostion.TOP):
        """ add separator

        Parameters
        ----------
        position: NavigationPostion
            where to add the separator
        """
        separator = NavigationSeparator(self)
        self._addWidgetToLayout(separator, position)

    def _addWidgetToLayout(self, widget: NavigationWidget, position: NavigationItemPostion):
        """ add widget to layout """
        if position == NavigationItemPostion.TOP:
            widget.setParent(self)
            self.topLayout.addWidget(widget, 0, Qt.AlignTop)
        elif position == NavigationItemPostion.SCROLL:
            widget.setParent(self.scrollWidget)
            self.scrollLayout.addWidget(widget, 0, Qt.AlignTop)
        else:
            widget.setParent(self)
            self.bottomLayout.addWidget(widget, 0, Qt.AlignBottom)

        widget.show()

    def setMenuButtonVisible(self, isVisible: bool):
        """ set whether the menu button is visible """
        self.menuButton.setVisible(isVisible)

    def expand(self):
        """ expand navigation panel """
        self._setWidgetCompacted(False)
        self.expandAni.setProperty('expand', True)

        # determine the display mode according to the width of window
        # https://learn.microsoft.com/en-us/windows/apps/design/controls/navigationview#default
        if self.window().width() > 1007 and not self.isMinimalEnabled:
            self.displayMode = NavigationDisplayMode.EXPAND
        else:
            self.setProperty('menu', True)
            self.setStyle(QApplication.style())
            self.displayMode = NavigationDisplayMode.MENU
            if not self._parent.isWindow():
                pos = self.parent().pos()
                self.setParent(self.window())
                self.move(pos)

            self.show()

        self.expandAni.setStartValue(
            QRect(self.pos(), QSize(48, self.height())))
        self.expandAni.setEndValue(
            QRect(self.pos(), QSize(322, self.height())))
        self.expandAni.start()

    def collapse(self):
        """ collapse navigation panel """
        if self.expandAni.state() == QPropertyAnimation.Running:
            return

        self.expandAni.setStartValue(
            QRect(self.pos(), QSize(self.width(), self.height())))
        self.expandAni.setEndValue(
            QRect(self.pos(), QSize(48, self.height())))
        self.expandAni.setProperty('expand', False)
        self.expandAni.start()

    def toggle(self):
        """ toggle navigation panel """
        if self.displayMode in [NavigationDisplayMode.COMPACT, NavigationDisplayMode.MINIMAL]:
            self.expand()
        else:
            self.collapse()

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

    def _onWidgetClicked(self):
        widget = self.sender()  # type: NavigationWidget
        if not widget.isSelectable:
            return

        self.setCurrentItem(widget.property('routeKey'))
        if widget is not self.menuButton and self.displayMode == NavigationDisplayMode.MENU:
            self.collapse()

    def resizeEvent(self, e: QResizeEvent):
        if e.oldSize().width() == self.width():
            return

        th = self.topLayout.minimumSize().height()
        bh = self.bottomLayout.minimumSize().height()
        self.scrollArea.setFixedHeight(self.height()-th-bh-20)

    def eventFilter(self, obj, e: QEvent):
        if obj is not self.window():
            return super().eventFilter(obj, e)

        if e.type() == QEvent.MouseButtonRelease:
            if not self.geometry().contains(e.pos()) and self.displayMode == NavigationDisplayMode.MENU:
                self.collapse()
        elif e.type() == QEvent.Resize:
            w = QResizeEvent(e).size().width()
            if w < 1008 and self.displayMode == NavigationDisplayMode.EXPAND:
                self.collapse()
            elif w >= 1008 and self.displayMode == NavigationDisplayMode.COMPACT and \
                    not self.menuButton.isVisible():
                self.expand()

        return super().eventFilter(obj, e)

    def _onExpandAniFinished(self):
        if not self.expandAni.property('expand'):
            if self.isMinimalEnabled:
                self.displayMode = NavigationDisplayMode.MINIMAL
            else:
                self.displayMode = NavigationDisplayMode.COMPACT

        s = getStyleSheet('navigation_interface')
        if self.displayMode == NavigationDisplayMode.MINIMAL:
            self.hide()
            self.setProperty('menu', False)
            self.setStyle(QApplication.style())
        elif self.displayMode == NavigationDisplayMode.COMPACT:
            self.setProperty('menu', False)
            self.setStyle(QApplication.style())

            for item in self.items.values():
                item.setCompacted(True)

            if not self._parent.isWindow():
                self.setParent(self._parent)
                self.move(0, 0)
                self.show()

    def _setWidgetCompacted(self, isCompacted: bool):
        """ set whether the navigation widget is compacted """
        for item in self.findChildren(NavigationWidget):
            item.setCompacted(isCompacted)


class NavigationItemLayout(QVBoxLayout):
    """ Navigation layout """

    def setGeometry(self, rect: QRect):
        super().setGeometry(rect)
        for i in range(self.count()):
            item = self.itemAt(i)
            if isinstance(item.widget(), NavigationSeparator):
                geo = item.geometry()
                item.widget().setGeometry(0, geo.y(), geo.width(), geo.height())
