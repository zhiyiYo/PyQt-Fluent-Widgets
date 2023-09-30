# coding: utf-8
from PyQt5.QtCore import QPoint, QRect, QSize
from .acrylic_widget import AcrylicWidget
from ..navigation import NavigationPanel, NavigationInterface, NavigationDisplayMode


class AcrylicNavigationPanel(AcrylicWidget, NavigationPanel):
    """ Acrylic navigation panel """

    def expand(self, useAni=True):
        self.setProperty("transparent", True)

        expandWidth = 1007 + self.expandWidth - 322
        if (self.window().width() <= expandWidth or self.isMinimalEnabled) and self._isCollapsible:
            pos = self.mapToGlobal(QPoint())
            self.acrylicBrush.grabImage(QRect(pos, QSize(expandWidth, self.height())))

        return super().expand(useAni)


class AcrylicNavigationInterface(NavigationInterface):
    """ Acrylic navigation interface """

    def __init__(self, parent=None, showMenuButton=True, showReturnButton=False, collapsible=True):
        super().__init__(parent, showMenuButton, showReturnButton, collapsible)
        self.panel.deleteLater()
        self.panel = AcrylicNavigationPanel(self)
        self.panel.setMenuButtonVisible(showMenuButton and collapsible)
        self.panel.setReturnButtonVisible(showReturnButton)
        self.panel.setCollapsible(collapsible)
        self.panel.installEventFilter(self)
        self.panel.displayModeChanged.connect(self.displayModeChanged)