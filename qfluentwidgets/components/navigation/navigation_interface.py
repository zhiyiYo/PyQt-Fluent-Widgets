# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget

from .navigation_panel import NavigationPanel, NavigationItemPostion, NavigationWidget, NavigationDisplayMode
from ...common.style_sheet import setStyleSheet


class NavigationInterface(QWidget):
    """ Navigation interface """

    def __init__(self, parent=None, showMenuButton=True):
        """
        Parameters
        ----------
        showMenuButton: bool
            whether to show menu button

        parent: widget
            parent widget
        """
        super().__init__(parent=parent)
        self.panel = NavigationPanel(self)
        self.panel.setMenuButtonVisible(showMenuButton)
        self.panel.installEventFilter(self)

        self.resize(48, self.height())
        self.setMinimumWidth(48)
        self.setAttribute(Qt.WA_StyledBackground)
        setStyleSheet(self, 'navigation_interface')

    def addItem(self, routeKey: str, iconPath: str, text: str, onClick, selectable=True, position=NavigationItemPostion.TOP):
        """ add navigation item

        Parameters
        ----------
        routKey: str
            the unique name of item

        iconPath: str
            the svg icon path of navigation item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        position: NavigationItemPostion
            where the button is added

        selectable: bool
            whether the item is selectable
        """
        self.panel.addItem(routeKey, iconPath, text, onClick, selectable, position)

    def addWidget(self, routeKey: str, widget: NavigationWidget, onClick, position=NavigationItemPostion.TOP):
        """ add custom widget

        Parameters
        ----------
        routKey: str
            the unique name of item

        widget: NavigationWidget
            the custom widget to be added

        onClick: callable
            the slot connected to item clicked signal

        position: NavigationItemPostion
            where the button is added
        """
        self.panel.addWidget(routeKey, widget, onClick, position)

    def addSeparator(self, position=NavigationItemPostion.TOP):
        """ add separator

        Parameters
        ----------
        position: NavigationPostion
            where to add the separator
        """
        self.panel.addSeparator(position)

    def setCurrentItem(self, name: str):
        """ set current selected item

        Parameters
        ----------
        name: str
            the unique name of item
        """
        self.panel.setCurrentItem(name)

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
