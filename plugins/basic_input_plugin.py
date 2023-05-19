# coding: utf-8
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

from qfluentwidgets import (PrimaryPushButton, SplitPushButton, DropDownPushButton,
                            ToolButton, SplitToolButton, DropDownToolButton, FluentIcon, ToggleButton,
                            SwitchButton, RadioButton, CheckBox, HyperlinkButton, Slider, ComboBox, IconWidget,
                            EditableComboBox, PixmapLabel, PushButton, PrimaryToolButton, PrimarySplitToolButton,
                            PrimarySplitPushButton, PrimaryDropDownPushButton, PrimaryDropDownToolButton)

from plugin_base import PluginBase
from task_menu_factory import EditTextTaskMenuFactory



class BasicInputPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Basic Input)'


class TextPlugin(BasicInputPlugin):

    def domXml(self):
        return f"""
        <widget class="{self.name()}" name="{self.name()}">
            <property name="text">
                <string>{self.toolTip()}</string>
            </property>
        </widget>
        """


class CheckBoxPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Check box plugin """

    def createWidget(self, parent):
        return CheckBox(self.toolTip(), parent)

    def icon(self):
        return super().icon('Checkbox')

    def name(self):
        return "CheckBox"


class ComboBoxPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Combo box plugin """

    def createWidget(self, parent):
        return ComboBox(parent)

    def icon(self):
        return super().icon('ComboBox')

    def name(self):
        return "ComboBox"


class EditableComboBoxPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Editable box plugin """

    def createWidget(self, parent):
        return EditableComboBox(parent)

    def icon(self):
        return super().icon('ComboBox')

    def name(self):
        return "EditableComboBox"


class HyperlinkButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Hyperlink button plugin """

    def createWidget(self, parent):
        return HyperlinkButton('', self.toolTip(), parent)

    def icon(self):
        return super().icon('HyperlinkButton')

    def name(self):
        return "HyperlinkButton"


class PushButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Push button plugin """

    def createWidget(self, parent):
        return PushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "PushButton"


class PrimaryPushButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Primary push button plugin """

    def createWidget(self, parent):
        return PrimaryPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "PrimaryPushButton"


class DropDownPushButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Drop down push button plugin """

    def createWidget(self, parent):
        return DropDownPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "DropDownPushButton"


class PrimaryDropDownPushButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Primary drop down push button plugin """

    def createWidget(self, parent):
        return PrimaryDropDownPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "PrimaryDropDownPushButton"


@EditTextTaskMenuFactory.register
class SplitPushButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Split push button plugin """

    def createWidget(self, parent):
        return SplitPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('SplitButton')

    def name(self):
        return "SplitPushButton"

    def domXml(self):
        return f"""
        <widget class="{self.name()}" name="{self.name()}">
            <property name="text_">
                <string>{self.toolTip()}</string>
            </property>
        </widget>
        """


@EditTextTaskMenuFactory.register
class PrimarySplitPushButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Primary color split push button plugin """

    def createWidget(self, parent):
        return PrimarySplitPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('SplitButton')

    def name(self):
        return "PrimarySplitPushButton"

    def domXml(self):
        return f"""
        <widget class="{self.name()}" name="{self.name()}">
            <property name="text_">
                <string>{self.toolTip()}</string>
            </property>
        </widget>
        """


class ToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Tool button plugin """

    def createWidget(self, parent):
        return ToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "ToolButton"


class PrimaryToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Primary color tool button plugin """

    def createWidget(self, parent):
        return PrimaryToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "PrimaryToolButton"


class DropDownToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Drop down tool button plugin """

    def createWidget(self, parent):
        return DropDownToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "DropDownToolButton"


class PrimaryDropDownToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Drop down tool button plugin """

    def createWidget(self, parent):
        return PrimaryDropDownToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "PrimaryDropDownToolButton"


class SplitToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ split tool button plugin """

    def createWidget(self, parent):
        return SplitToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('SplitButton')

    def name(self):
        return "SplitToolButton"


class PrimarySplitToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Primary color split tool button plugin """

    def createWidget(self, parent):
        return PrimarySplitToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('SplitButton')

    def name(self):
        return "PrimarySplitToolButton"


@EditTextTaskMenuFactory.register
class SwitchButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Switch button plugin """

    def createWidget(self, parent):
        return SwitchButton(parent)

    def icon(self):
        return super().icon('ToggleSwitch')

    def name(self):
        return "SwitchButton"


class RadioButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Radio button plugin """

    def createWidget(self, parent):
        return RadioButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('RadioButton')

    def name(self):
        return "RadioButton"


class ToggleButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Toggle button plugin """

    def createWidget(self, parent):
        return ToggleButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('ToggleButton')

    def name(self):
        return "ToggleButton"


class SliderPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
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


class IconWidgetPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Icon widget plugin """

    def createWidget(self, parent):
        return IconWidget(FluentIcon.EMOJI_TAB_SYMBOLS, parent)

    def icon(self):
        return super().icon('IconElement')

    def name(self):
        return "IconWidget"


class PixmapLabelPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Pixmap label plugin """

    def createWidget(self, parent):
        return PixmapLabel(parent)

    def icon(self):
        return super().icon('Image')

    def name(self):
        return "PixmapLabel"

