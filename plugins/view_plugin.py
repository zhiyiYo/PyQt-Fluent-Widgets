# coding: utf-8
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from qfluentwidgets import (ListWidget, ListView, TreeView, TreeWidget, TableView, TableWidget,
                            HorizontalFlipView, VerticalFlipView, HorizontalPipsPager, VerticalPipsPager)

from plugin_base import PluginBase


class ViewPlugin(PluginBase):

    def group(self):
        return super().group() + ' (View)'


class ListWidgetPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ List widget plugin """

    def createWidget(self, parent):
        return ListWidget(parent)

    def icon(self):
        return super().icon("ListView")

    def name(self):
        return "ListWidget"


class ListViewPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ List view plugin """

    def createWidget(self, parent):
        return ListView(parent)

    def icon(self):
        return super().icon("ListView")

    def name(self):
        return "ListView"


class TableWidgetPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ Table widget plugin """

    def createWidget(self, parent):
        return TableWidget(parent)

    def icon(self):
        return super().icon("DataGrid")

    def name(self):
        return "TableWidget"


class TableViewPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ Table widget plugin """

    def createWidget(self, parent):
        return TableView(parent)

    def icon(self):
        return super().icon("DataGrid")

    def name(self):
        return "TableView"


class TreeWidgetPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ Tree widget plugin """

    def createWidget(self, parent):
        return TreeWidget(parent)

    def icon(self):
        return super().icon("TreeView")

    def name(self):
        return "TreeWidget"


class TreeViewPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ Tree view plugin """

    def createWidget(self, parent):
        return TreeView(parent)

    def icon(self):
        return super().icon("TreeView")

    def name(self):
        return "TreeView"


class HorizontalFlipViewPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ Horizontal flip view plugin """

    def createWidget(self, parent):
        return HorizontalFlipView(parent)

    def icon(self):
        return super().icon("FlipView")

    def name(self):
        return "HorizontalFlipView"


class VerticalFlipViewPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ Vertical flip view plugin """

    def createWidget(self, parent):
        return VerticalFlipView(parent)

    def icon(self):
        return super().icon("FlipView")

    def name(self):
        return "VerticalFlipView"


class HorizontalPipsPagerPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ Horizontal flip view plugin """

    def createWidget(self, parent):
        w = HorizontalPipsPager(parent)
        w.setPageNumber(5)
        return w

    def icon(self):
        return super().icon("PipsPager")

    def name(self):
        return "HorizontalPipsPager"


class VerticalPipsPagerPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ Vertical flip view plugin """

    def createWidget(self, parent):
        w = VerticalPipsPager(parent)
        w.setPageNumber(5)
        return w

    def icon(self):
        return super().icon("PipsPager")

    def name(self):
        return "VerticalPipsPager"
