# coding: utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from qfluentwidgets import (PushButton, PrimaryPushButton, SplitPushButton, DropDownPushButton,
                            ToolButton, SplitToolButton, DropDownToolButton, FluentIcon, ToggleButton,
                            SwitchButton, RadioButton, CheckBox, HyperlinkButton, Slider, ComboBox, IconWidget)

from plugin_base import PluginBase


class BasicInputPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Basic Input)'


class CheckBoxPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Check box plugin """

    def createWidget(self, parent):
        return CheckBox(self.toolTip(), parent)

    def icon(self):
        return super().icon('Checkbox')

    def name(self):
        return "CheckBox"


class ComboBoxPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Combo box plugin """

    def createWidget(self, parent):
        return ComboBox(parent)

    def icon(self):
        return super().icon('ComboBox')

    def name(self):
        return "ComboBox"


class HyperlinkButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Hyperlink button plugin """

    def createWidget(self, parent):
        return HyperlinkButton('', self.toolTip(), parent)

    def icon(self):
        return super().icon('HyperlinkButton')

    def name(self):
        return "HyperlinkButton"


class PushButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Push button plugin """

    def createWidget(self, parent):
        return PushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "PushButton"


class PrimaryPushButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Primary push button plugin """

    def createWidget(self, parent):
        return PrimaryPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "PrimaryPushButton"


class DropDownPushButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Drop down push button plugin """

    def createWidget(self, parent):
        return DropDownPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "DropDownPushButton"


class SplitPushButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Split push button plugin """

    def createWidget(self, parent):
        return SplitPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('SplitButton')

    def name(self):
        return "SplitPushButton"


class ToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Tool button plugin """

    def createWidget(self, parent):
        return ToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "ToolButton"


class DropDownToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Drop down tool button plugin """

    def createWidget(self, parent):
        return DropDownToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "DropDownToolButton"


class SplitToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ split tool button plugin """

    def createWidget(self, parent):
        return SplitToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('SplitButton')

    def name(self):
        return "SplitToolButton"


class SwitchButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Switch button plugin """

    def createWidget(self, parent):
        return SwitchButton(parent)

    def icon(self):
        return super().icon('ToggleSwitch')

    def name(self):
        return "SwitchButton"


class RadioButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Radio button plugin """

    def createWidget(self, parent):
        return RadioButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('RadioButton')

    def name(self):
        return "RadioButton"


class ToggleButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Toggle button plugin """

    def createWidget(self, parent):
        return ToggleButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('ToggleButton')

    def name(self):
        return "ToggleButton"


class SliderPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """  Slider  plugin """

    def createWidget(self, parent):
        slider = Slider(parent)
        slider.setRange(0, 100)
        slider.setMinimumWidth(200)
        return slider

    def icon(self):
        return super().icon('Slider')

    def name(self):
        return "Slider"


class IconWidgetPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Icon widget plugin """

    def createWidget(self, parent):
        return IconWidget(FluentIcon.EMOJI_TAB_SYMBOLS, parent)

    def icon(self):
        return super().icon('IconElement')

    def name(self):
        return "IconWidget"

