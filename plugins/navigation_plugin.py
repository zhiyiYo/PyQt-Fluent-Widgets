# coding: utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from qfluentwidgets import NavigationInterface, NavigationPanel

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
