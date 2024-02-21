# coding: utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from qfluentwidgets import CommandBar, Action, FluentIcon

from plugin_base import PluginBase


class ToolBarPlugin(PluginBase):

    def group(self):
        return super().group() + ' (ToolBar)'


class CommandBarPlugin(ToolBarPlugin, QPyDesignerCustomWidgetPlugin):
    """ Command bar plugin """

    def createWidget(self, parent):
        w = CommandBar(parent)
        w.addAction(Action(FluentIcon.SHARE, 'Share'))
        w.addAction(Action(FluentIcon.SAVE, 'Save'))
        w.addAction(Action(FluentIcon.DELETE, 'Delete'))
        return w

    def icon(self):
        return super().icon("CommandBar")

    def name(self):
        return "CommandBar"

