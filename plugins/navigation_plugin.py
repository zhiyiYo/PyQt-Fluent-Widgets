# coding: utf-8
from PySide6.QtCore import Qt
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

from qfluentwidgets import NavigationInterface, NavigationPanel

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
