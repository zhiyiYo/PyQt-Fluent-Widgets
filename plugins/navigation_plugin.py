# coding: utf-8
from PySide6.QtCore import Qt
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

from qfluentwidgets import (NavigationInterface, NavigationPanel, Pivot, SegmentedWidget, NavigationBar,
                            FluentIcon, TabBar, SegmentedToolWidget, SegmentedToggleToolWidget)

from plugin_base import PluginBase


class NavigationPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Navigation)'


class NavigationInterfacePlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
    """ Navigation interface plugin """

    def createWidget(self, parent):
        return NavigationInterface(parent, True, True)

    def icon(self):
        return super().icon("NavigationView")

    def name(self):
        return "NavigationInterface"


class NavigationPanelPlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
    """ Navigation panel plugin """

    def createWidget(self, parent):
        return NavigationPanel(parent)

    def icon(self):
        return super().icon("NavigationView")

    def name(self):
        return "NavigationPanel"


class NavigationBarPlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
    """ Navigation bar plugin """

    def createWidget(self, parent):
        bar = NavigationBar(parent)
        bar.addItem('item', FluentIcon.HOME, 'Home')
        return bar

    def icon(self):
        return super().icon("NavigationView")

    def name(self):
        return "NavigationBar"


class PivotPlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
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


class SegmentedWidgetPlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
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


class SegmentedToolWidgetPlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
    """ Segmented widget plugin """

    def createWidget(self, parent):
        p = SegmentedToolWidget(parent)
        p.addItem(f'k1', FluentIcon.TRANSPARENT)
        p.addItem(f'k2', FluentIcon.CHECKBOX)
        p.addItem(f'k3', FluentIcon.CONSTRACT)
        p.setCurrentItem('k1')
        return p

    def icon(self):
        return super().icon("Pivot")

    def name(self):
        return "SegmentedToolWidget"


class SegmentedToggleToolWidgetPlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
    """ Segmented tool widget plugin """

    def createWidget(self, parent):
        p = SegmentedToggleToolWidget(parent)
        p.addItem(f'k1', FluentIcon.TRANSPARENT)
        p.addItem(f'k2', FluentIcon.CHECKBOX)
        p.addItem(f'k3', FluentIcon.CONSTRACT)
        p.setCurrentItem('k1')
        return p

    def icon(self):
        return super().icon("Pivot")

    def name(self):
        return "SegmentedToggleToolWidget"


class TabBarPlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
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
