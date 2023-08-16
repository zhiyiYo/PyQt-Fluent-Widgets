# coding: utf-8
from PyQt5.QtWidgets import QWidget
from PyQt5.QtDesigner import (QPyDesignerCustomWidgetPlugin, QDesignerFormWindowInterface, QExtensionFactory,
                              QPyDesignerContainerExtension)

from qfluentwidgets import (ScrollArea, SmoothScrollArea, SingleDirectionScrollArea, OpacityAniStackedWidget,
                            PopUpAniStackedWidget, CardWidget, ElevatedCardWidget, SimpleCardWidget,
                            HeaderCardWidget)

from plugin_base import PluginBase


class ContainerPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Container)'

    def isContainer(self):
        return True


class CardWidgetPlugin(ContainerPlugin, QPyDesignerCustomWidgetPlugin):
    """ Card widget plugin """

    def createWidget(self, parent):
        return CardWidget(parent)

    def icon(self):
        return super().icon("CommandBar")

    def name(self):
        return "CardWidget"


class ElevatedCardWidgetPlugin(ContainerPlugin, QPyDesignerCustomWidgetPlugin):
    """ Elevated card widget plugin """

    def createWidget(self, parent):
        return ElevatedCardWidget(parent)

    def icon(self):
        return super().icon("CommandBar")

    def name(self):
        return "ElevatedCardWidget"


class SimpleCardWidgetPlugin(ContainerPlugin, QPyDesignerCustomWidgetPlugin):
    """ Simple card widget plugin """

    def createWidget(self, parent):
        return SimpleCardWidget(parent)

    def icon(self):
        return super().icon("CommandBar")

    def name(self):
        return "SimpleCardWidget"


class HeaderCardWidgetPlugin(ContainerPlugin, QPyDesignerCustomWidgetPlugin):
    """ Header card widget plugin """

    def createWidget(self, parent):
        return HeaderCardWidget(parent)

    def icon(self):
        return super().icon("CommandBar")

    def name(self):
        return "HeaderCardWidget"


class ScrollAreaPluginBase(ContainerPlugin):
    """ Scroll area plugin base """

    def domXml(self):
        return f"""
            <widget class="{self.name()}" name="{self.name()}">
                <property name="widgetResizable">
                    <bool>true</bool>
                </property>
                <widget class="QWidget" name="scrollAreaWidgetContents" />
            </widget>
        """


class ScrollAreaPlugin(ScrollAreaPluginBase, QPyDesignerCustomWidgetPlugin):
    """ Scroll area plugin """

    def createWidget(self, parent):
        return ScrollArea(parent)

    def icon(self):
        return super().icon("ScrollViewer")

    def name(self):
        return "ScrollArea"

    def toolTip(self):
        return "Smooth scroll area"


class SmoothScrollAreaPlugin(ScrollAreaPluginBase, QPyDesignerCustomWidgetPlugin):
    """ Smooth scroll area plugin """

    def createWidget(self, parent):
        return SmoothScrollArea(parent)

    def icon(self):
        return super().icon("ScrollViewer")

    def name(self):
        return "SmoothScrollArea"


class SingleDirectionScrollAreaPlugin(ScrollAreaPluginBase, QPyDesignerCustomWidgetPlugin):
    """ Single direction scroll area plugin """

    def createWidget(self, parent):
        return SingleDirectionScrollArea(parent)

    def icon(self):
        return super().icon("ScrollViewer")

    def name(self):
        return "SingleDirectionScrollArea"


class StackedWidgetPlugin(ContainerPlugin):

    def domXml(self):
        return f"""
            <widget class="{self.name()}" name="{self.name()}">'
                <widget class="QWidget" name="page" />'
            </widget>
        """

    def onCurrentIndexChanged(self, index):
        widget = self.sender()
        form = QDesignerFormWindowInterface.findFormWindow(widget)
        if form:
            form.emitSelectionChanged()


class StackedWidgetExtension(QPyDesignerContainerExtension):
    """ Stacked widget extension """

    def __init__(self, stacked, parent=None) -> None:
        super().__init__(parent)
        self.stacked = stacked

    def addWidget(self, widget) -> None:
        self.stacked.addWidget(widget)

    def count(self):
        return self.stacked.count()

    def currentIndex(self):
        return self.stacked.currentIndex()

    def insertWidget(self, index, widget):
        self.stacked.insertWidget(index, widget)

    def remove(self, index):
        self.stacked.removeWidget(self.stacked.widget(index))

    def setCurrentIndex(self, index):
        self.stacked.setCurrentIndex(index)

    def widget(self, index):
        return self.stacked.widget(index)


class StackedWidgetExtensionFactory(QExtensionFactory):
    """ Stacked widget extension factory """

    widgets = []
    IID = "org.qt-project.Qt.Designer.Container"

    def createExtension(self, object, iid, parent):
        if iid != StackedWidgetExtensionFactory.IID:
            return None

        if object.__class__.__name__ not in self.widgets:
            return None

        return StackedWidgetExtension(object, parent)

    @classmethod
    def register(cls, Plugin):
        if Plugin.__name__ not in cls.widgets:
            cls.widgets.append(Plugin().name())
            Plugin.Factory = cls

        return Plugin


@StackedWidgetExtensionFactory.register
class OpacityAniStackedWidgetPlugin(StackedWidgetPlugin, QPyDesignerCustomWidgetPlugin):
    """ opacity ani stacked widget plugin """

    def createWidget(self, parent):
        w = OpacityAniStackedWidget(parent)
        w.currentChanged.connect(self.onCurrentIndexChanged)
        return w

    def icon(self):
        return super().icon("StackPanel")

    def name(self):
        return "OpacityAniStackedWidget"


@StackedWidgetExtensionFactory.register
class PopUpAniStackedWidgetPlugin(StackedWidgetPlugin, QPyDesignerCustomWidgetPlugin):
    """ pop up ani stacked widget plugin """

    def createWidget(self, parent):
        w = PopUpAniStackedWidget(parent)
        w.currentChanged.connect(self.onCurrentIndexChanged)
        return w

    def icon(self):
        return super().icon("StackPanel")

    def name(self):
        return "PopUpAniStackedWidget"
