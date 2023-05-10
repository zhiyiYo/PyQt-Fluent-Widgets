# coding: utf-8
from PySide6.QtCore import Qt
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

from qfluentwidgets import ScrollArea, SmoothScrollArea, SingleDirectionScrollArea, OpacityAniStackedWidget, PopUpAniStackedWidget
from qframelesswindow import FramelessMainWindow, FramelessWindow

from plugin_base import PluginBase


class ContainerPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Container)'

    def isContainer(self):
        return True



class FramelessMainWindowPlugin(ContainerPlugin, QDesignerCustomWidgetInterface):
    """ Frameless main window plugin """

    def createWidget(self, parent):
        return FramelessMainWindow(parent)

    def icon(self):
        return super().icon("TitleBar")

    def name(self):
        return "FramelessMainWindow"


class FramelessWindowPlugin(ContainerPlugin, QDesignerCustomWidgetInterface):
    """ Frameless window plugin """

    def createWidget(self, parent):
        return FramelessWindow(parent)

    def icon(self):
        return super().icon("TitleBar")

    def name(self):
        return "FramelessWindow"


class ScrollAreaPlugin(ContainerPlugin, QDesignerCustomWidgetInterface):
    """ Scroll area plugin """

    def createWidget(self, parent):
        return ScrollArea(parent)

    def icon(self):
        return super().icon("ScrollViewer")

    def name(self):
        return "ScrollArea"

    def toolTip(self):
        return "Smooth scroll area"


class SmoothScrollAreaPlugin(ContainerPlugin, QDesignerCustomWidgetInterface):
    """ Smooth scroll area plugin """

    def createWidget(self, parent):
        return SmoothScrollArea(parent)

    def icon(self):
        return super().icon("ScrollViewer")

    def name(self):
        return "SmoothScrollArea"


class SingleDirectionScrollAreaPlugin(ContainerPlugin, QDesignerCustomWidgetInterface):
    """ Single direction scroll area plugin """

    def createWidget(self, parent):
        return SingleDirectionScrollArea(parent)

    def icon(self):
        return super().icon("ScrollViewer")

    def name(self):
        return "SingleDirectionScrollArea"


class OpacityAniStackedWidgetPlugin(ContainerPlugin, QDesignerCustomWidgetInterface):
    """ opacity ani stacked widget plugin """

    def createWidget(self, parent):
        return OpacityAniStackedWidget(parent)

    def icon(self):
        return super().icon("StackPanel")

    def name(self):
        return "OpacityAniStackedWidget"


class PopUpAniStackedWidgetPlugin(ContainerPlugin, QDesignerCustomWidgetInterface):
    """ pop up ani stacked widget plugin """

    def createWidget(self, parent):
        return PopUpAniStackedWidget(parent)

    def icon(self):
        return super().icon("StackPanel")

    def name(self):
        return "PopUpAniStackedWidget"
