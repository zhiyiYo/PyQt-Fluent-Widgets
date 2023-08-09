# coding: utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from qfluentwidgets import (NavigationInterface, NavigationPanel, Pivot, SegmentedWidget, NavigationBar,
                            FluentIcon, TabBar)

from plugin_base import PluginBase


class NavigationPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Navigation)'


class NavigationInterfacePlugin(NavigationPlugin, QPyDesignerCustomWidgetPlugin):
    """ Navigation interface plugin """

    def createWidget(self, parent):
        return NavigationInterface(parent, True, True)

    def icon(self):
        return super().icon("NavigationView")

    def name(self):
        return "NavigationInterface"


class NavigationPanelPlugin(NavigationPlugin, QPyDesignerCustomWidgetPlugin):
    """ Navigation panel plugin """

    def createWidget(self, parent):
        return NavigationPanel(parent)

    def icon(self):
        return super().icon("NavigationView")

    def name(self):
        return "NavigationPanel"


class NavigationBarPlugin(NavigationPlugin, QPyDesignerCustomWidgetPlugin):
    """ Navigation bar plugin """

    def createWidget(self, parent):
        bar = NavigationBar(parent)
        bar.addItem('item', FluentIcon.HOME, 'Home')
        return bar

    def icon(self):
        return super().icon("NavigationView")

    def name(self):
        return "NavigationBar"


class PivotPlugin(NavigationPlugin, QPyDesignerCustomWidgetPlugin):
    """ Navigation panel plugin """

    def createWidget(self, parent):
        p = Pivot(parent)
        for i in range(1, 4):
            p.addItem(f'Item{i}', f'Item{i}', print)

        p.setCurrentItem('Item1')
        return p

    def icon(self):
        return super().icon("Pivot")

    def name(self):
        return "Pivot"


class SegmentedWidgetPlugin(NavigationPlugin, QPyDesignerCustomWidgetPlugin):
    """ Segmented widget plugin """

    def createWidget(self, parent):
        p = SegmentedWidget(parent)
        for i in range(1, 4):
            p.addItem(f'Item{i}', f'Item{i}', print)

        p.setCurrentItem('Item1')
        return p

    def icon(self):
        return super().icon("Pivot")

    def name(self):
        return "SegmentedWidget"


class TabBarPlugin(NavigationPlugin, QPyDesignerCustomWidgetPlugin):
    """ Tab bar plugin """

    def createWidget(self, parent):
        p = TabBar(parent)
        for i in range(1, 4):
            p.addTab(f'Tab {i}', f'Tab {i}', FluentIcon.BASKETBALL)

        return p

    def icon(self):
        return super().icon("TabView")

    def name(self):
        return "TabBar"
