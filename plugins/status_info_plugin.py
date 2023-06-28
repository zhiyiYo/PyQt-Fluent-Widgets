# coding: utf-8
from PyQt6.QtCore import Qt
from PyQt6.QtDesigner import QPyDesignerCustomWidgetPlugin

from qfluentwidgets import (InfoBar, ProgressBar, IndeterminateProgressBar, ProgressRing, StateToolTip, InfoBarPosition,
                            IndeterminateProgressRing)

from plugin_base import PluginBase


class StatusInfoPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Status & Info)'


class InfoBarPlugin(StatusInfoPlugin, QPyDesignerCustomWidgetPlugin):
    """ Info bar plugin """

    def createWidget(self, parent):
        return InfoBar.success(
            title='Lesson 5',
            content='最短的捷径就是绕远路，绕远路才是我的最短捷径。',
            duration=-1,
            position=InfoBarPosition.NONE,
            parent=parent
        )

    def icon(self):
        return super().icon("InfoBar")

    def name(self):
        return "InfoBar"


class ProgressBarPlugin(StatusInfoPlugin, QPyDesignerCustomWidgetPlugin):
    """ Progress bar plugin """

    def createWidget(self, parent):
        return ProgressBar(parent)

    def icon(self):
        return super().icon("ProgressBar")

    def name(self):
        return "ProgressBar"


class IndeterminateProgressBarPlugin(StatusInfoPlugin, QPyDesignerCustomWidgetPlugin):
    """ Indeterminate progress bar plugin """

    def createWidget(self, parent):
        return IndeterminateProgressBar(parent)

    def icon(self):
        return super().icon("ProgressBar")

    def name(self):
        return "IndeterminateProgressBar"


class ProgressRingPlugin(StatusInfoPlugin, QPyDesignerCustomWidgetPlugin):
    """ Progress ring plugin """

    def createWidget(self, parent):
        return ProgressRing(parent)

    def icon(self):
        return super().icon("ProgressRing")

    def name(self):
        return "ProgressRing"


class IndeterminateProgressRingPlugin(StatusInfoPlugin, QPyDesignerCustomWidgetPlugin):
    """ Progress ring plugin """

    def createWidget(self, parent):
        return IndeterminateProgressRing(parent)

    def icon(self):
        return super().icon("ProgressRing")

    def name(self):
        return "IndeterminateProgressRing"


class StateToolTipPlugin(StatusInfoPlugin, QPyDesignerCustomWidgetPlugin):
    """ State tool tip plugin """

    def createWidget(self, parent):
        return StateToolTip('Running', 'Please wait patiently', parent)

    def icon(self):
        return super().icon("ProgressRing")

    def name(self):
        return "StateToolTip"
