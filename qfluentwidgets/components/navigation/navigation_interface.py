# coding:utf-8
from typing import Union

from PySide6.QtCore import Qt, QEvent, Signal
from PySide6.QtGui import QResizeEvent, QIcon
from PySide6.QtWidgets import QWidget

from .navigation_panel import NavigationPanel, NavigationItemPosition, NavigationWidget, NavigationDisplayMode
from .navigation_widget import NavigationTreeWidget
from ...common.style_sheet import FluentStyleSheet
from ...common.icon import FluentIconBase


class NavigationInterface(QWidget):
    """ Navigation interface """

    displayModeChanged = Signal(NavigationDisplayMode)

    def __init__(self, parent=None, showMenuButton=True, showReturnButton=False, collapsible=True):
        """
        Parameters
        ----------
        parent: widget
            parent widget

        showMenuButton: bool
            whether to show menu button

        showReturnButton: bool
            whether to show return button

        collapsible: bool
            Is the navigation interface collapsible
        """
        super().__init__(parent=parent)
        self.panel = NavigationPanel(self)
        self.panel.setMenuButtonVisible(showMenuButton and collapsible)
        self.panel.setReturnButtonVisible(showReturnButton)
        self.panel.setCollapsible(collapsible)
        self.panel.installEventFilter(self)
        self.panel.displayModeChanged.connect(self.displayModeChanged)

        self.resize(48, self.height())
        self.setMinimumWidth(48)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def addItem(self, routeKey: str, icon: Union[str, QIcon, FluentIconBase], text: str, onClick=None,
                selectable=True, position=NavigationItemPosition.TOP, tooltip: str = None,
                parentRouteKey: str = None) -> NavigationTreeWidget:
        """ add navigation item

        Parameters
        ----------
        routKey: str
            the unique name of item

        icon: str | QIcon | FluentIconBase
            the icon of navigation item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        selectable: bool
            whether the item is selectable

        position: NavigationItemPosition
            where the button is added

        tooltip: str
            the tooltip of item

        parentRouteKey: str
            the route key of parent item, the parent item should be `NavigationTreeWidgetBase`
        """
        return self.insertItem(-1, routeKey, icon, text, onClick, selectable, position, tooltip, parentRouteKey)

    def addWidget(self, routeKey: str, widget: NavigationWidget, onClick=None, position=NavigationItemPosition.TOP,
                  tooltip: str = None, parentRouteKey: str = None):
        """ add custom widget

        Parameters
        ----------
        routKey: str
            the unique name of item

        widget: NavigationWidget
            the custom widget to be added

        onClick: callable
            the slot connected to item clicked signal

        position: NavigationItemPosition
            where the widget is added

        tooltip: str
            the tooltip of widget

        parentRouteKey: str
            the route key of parent item, the parent item should be `NavigationTreeWidgetBase`
        """
        self.insertWidget(-1, routeKey, widget, onClick, position, tooltip, parentRouteKey)

    def insertItem(self, index: int, routeKey: str, icon: Union[str, QIcon, FluentIconBase], text: str,
                   onClick=None, selectable=True, position=NavigationItemPosition.TOP, tooltip: str = None,
                   parentRouteKey: str = None) -> NavigationTreeWidget:
        """ insert navigation item

        Parameters
        ----------
        index: int
            insert position

        routKey: str
            the unique name of item

        icon: str | QIcon | FluentIconBase
            the icon of navigation item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        selectable: bool
            whether the item is selectable

        position: NavigationItemPosition
            where the item is added

        tooltip: str
            the tooltip of item

        parentRouteKey: str
            the route key of parent item, the parent item should be `NavigationTreeWidgetBase`
        """
        w = self.panel.insertItem(index, routeKey, icon, text, onClick, selectable, position, tooltip, parentRouteKey)
        self.setMinimumHeight(self.panel.layoutMinHeight())
        return w

    def insertWidget(self, index: int, routeKey: str, widget: NavigationWidget, onClick=None,
                     position=NavigationItemPosition.TOP, tooltip: str = None, parentRouteKey: str = None):
        """ insert custom widget

        Parameters
        ----------
        index: int
            insert position

        routKey: str
            the unique name of item

        widget: NavigationWidget
            the custom widget to be added

        onClick: callable
            the slot connected to item clicked signal

        position: NavigationItemPosition
            where the widget is added

        tooltip: str
            the tooltip of widget

        parentRouteKey: str
            the route key of parent item, the parent item should be `NavigationTreeWidgetBase`
        """
        self.panel.insertWidget(index, routeKey, widget, onClick, position, tooltip, parentRouteKey)
        self.setMinimumHeight(self.panel.layoutMinHeight())

    def addSeparator(self, position=NavigationItemPosition.TOP):
        """ add separator

        Parameters
        ----------
        position: NavigationPostion
            where to add the separator
        """
        self.insertSeparator(-1, position)

    def insertSeparator(self, index: int, position=NavigationItemPosition.TOP):
        """ add separator

        Parameters
        ----------
        index: int
            insert position

        position: NavigationPostion
            where to add the separator
        """
        self.panel.insertSeparator(index, position)
        self.setMinimumHeight(self.panel.layoutMinHeight())

    def removeWidget(self, routeKey: str):
        """ remove widget

        Parameters
        ----------
        routKey: str
            the unique name of item
        """
        self.panel.removeWidget(routeKey)

    def setCurrentItem(self, name: str):
        """ set current selected item

        Parameters
        ----------
        name: str
            the unique name of item
        """
        self.panel.setCurrentItem(name)

    def expand(self, useAni=True):
        """ expand navigation panel """
        self.panel.expand(useAni)

    def toggle(self):
        """ toggle navigation panel """
        self.panel.toggle()

    def setExpandWidth(self, width: int):
        """ set the maximum width """
        self.panel.setExpandWidth(width)

    def setMinimumExpandWidth(self, width: int):
        """ Set the minimum window width that allows panel to be expanded """
        self.panel.setMinimumExpandWidth(width)

    def setMenuButtonVisible(self, isVisible: bool):
        """ set whether the menu button is visible """
        self.panel.setMenuButtonVisible(isVisible)

    def setReturnButtonVisible(self, isVisible: bool):
        """ set whether the return button is visible """
        self.panel.setReturnButtonVisible(isVisible)

    def setCollapsible(self, collapsible: bool):
        self.panel.setCollapsible(collapsible)

    def isAcrylicEnabled(self):
        return self.panel.isAcrylicEnabled()

    def setAcrylicEnabled(self, isEnabled: bool):
        """ set whether the acrylic background effect is enabled """
        self.panel.setAcrylicEnabled(isEnabled)

    def widget(self, routeKey: str):
        return self.panel.widget(routeKey)

    def eventFilter(self, obj, e: QEvent):
        if obj is not self.panel or e.type() != QEvent.Resize:
            return super().eventFilter(obj, e)

        if self.panel.displayMode != NavigationDisplayMode.MENU:
            event = QResizeEvent(e)
            if event.oldSize().width() != event.size().width():
                self.setFixedWidth(event.size().width())

        return super().eventFilter(obj, e)

    def resizeEvent(self, e: QResizeEvent):
        if e.oldSize().height() != self.height():
            self.panel.setFixedHeight(self.height())
