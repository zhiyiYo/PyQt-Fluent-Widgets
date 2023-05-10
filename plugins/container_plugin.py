# coding: utf-8
from PyQt6.QtCore import Qt
from PyQt6.QtDesigner import QPyDesignerCustomWidgetPlugin

from qfluentwidgets import ScrollArea, SmoothScrollArea, SingleDirectionScrollArea, OpacityAniStackedWidget, PopUpAniStackedWidget
from qframelesswindow import FramelessMainWindow, FramelessWindow

from plugin_base import PluginBase


class ContainerPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Container)'

    def isContainer(self):
        return True



class FramelessMainWindowPlugin(ContainerPlugin, QPyDesignerCustomWidgetPlugin):
    """ Frameless main window plugin """

    def createWidget(self, parent):
        return FramelessMainWindow(parent)

    def icon(self):
        return super().icon("TitleBar")

    def name(self):
        return "FramelessMainWindow"


class FramelessWindowPlugin(ContainerPlugin, QPyDesignerCustomWidgetPlugin):
    """ Frameless window plugin """

    def createWidget(self, parent):
        return FramelessWindow(parent)

    def icon(self):
        return super().icon("TitleBar")

    def name(self):
        return "FramelessWindow"


class ScrollAreaPlugin(ContainerPlugin, QPyDesignerCustomWidgetPlugin):
    """ Scroll area plugin """

    def createWidget(self, parent):
        return ScrollArea(parent)

    def icon(self):
        return super().icon("ScrollViewer")

    def name(self):
        return "ScrollArea"

    def toolTip(self):
        return "Smooth scroll area"


class SmoothScrollAreaPlugin(ContainerPlugin, QPyDesignerCustomWidgetPlugin):
    """ Smooth scroll area plugin """

    def createWidget(self, parent):
        return SmoothScrollArea(parent)

    def icon(self):
        return super().icon("ScrollViewer")

    def name(self):
        return "SmoothScrollArea"


class SingleDirectionScrollAreaPlugin(ContainerPlugin, QPyDesignerCustomWidgetPlugin):
    """ Single direction scroll area plugin """

    def createWidget(self, parent):
        return SingleDirectionScrollArea(parent)

    def icon(self):
        return super().icon("ScrollViewer")

    def name(self):
        return "SingleDirectionScrollArea"


class OpacityAniStackedWidgetPlugin(ContainerPlugin, QPyDesignerCustomWidgetPlugin):
    """ opacity ani stacked widget plugin """

    def createWidget(self, parent):
        return OpacityAniStackedWidget(parent)

    def icon(self):
        return super().icon("StackPanel")

    def name(self):
        return "OpacityAniStackedWidget"


class PopUpAniStackedWidgetPlugin(ContainerPlugin, QPyDesignerCustomWidgetPlugin):
    """ pop up ani stacked widget plugin """

    def createWidget(self, parent):
        return PopUpAniStackedWidget(parent)

    def icon(self):
        return super().icon("StackPanel")

    def name(self):
        return "PopUpAniStackedWidget"
