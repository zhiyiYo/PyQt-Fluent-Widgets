# coding: utf-8
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from qfluentwidgets import (InfoBar, ProgressBar, IndeterminateProgressBar, ProgressRing, StateToolTip, InfoBarPosition,
                            IndeterminateProgressRing, InfoBadge, DotInfoBadge, IconInfoBadge, FluentIcon)

from plugin_base import PluginBase


class StatusInfoPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Status & Info)'


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




class InfoBadgePlugin(StatusInfoPlugin, QPyDesignerCustomWidgetPlugin):
    """ Info badge plugin """

    def createWidget(self, parent):
        return InfoBadge('10', parent)

    def icon(self):
        return super().icon("InfoBadge")

    def name(self):
        return "InfoBadge"


class DotInfoBadgePlugin(StatusInfoPlugin, QPyDesignerCustomWidgetPlugin):
    """ Dot info badge plugin """

    def createWidget(self, parent):
        return DotInfoBadge(parent)

    def icon(self):
        return super().icon("InfoBadge")

    def name(self):
        return "DotInfoBadge"


class IconInfoBadgePlugin(StatusInfoPlugin, QPyDesignerCustomWidgetPlugin):
    """ Icon info badge plugin """

    def createWidget(self, parent):
        return IconInfoBadge.success(FluentIcon.ACCEPT_MEDIUM, parent)

    def icon(self):
        return super().icon("InfoBadge")

    def name(self):
        return "IconInfoBadge"
