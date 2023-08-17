# coding: utf-8
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from qfluentwidgets import (PrimaryPushButton, SplitPushButton, DropDownPushButton,
                            ToolButton, SplitToolButton, DropDownToolButton, FluentIcon, ToggleButton,
                            SwitchButton, RadioButton, CheckBox, HyperlinkButton, Slider, ComboBox, IconWidget,
                            EditableComboBox, PixmapLabel, PushButton, PrimaryToolButton, PrimarySplitToolButton,
                            PrimarySplitPushButton, PrimaryDropDownPushButton, PrimaryDropDownToolButton,
                            TransparentToolButton, TransparentPushButton, ToggleToolButton, TransparentToggleToolButton,
                            TransparentTogglePushButton, TransparentDropDownPushButton, TransparentDropDownToolButton,
                            PillPushButton, PillToolButton, HorizontalSeparator, VerticalSeparator)

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


class CheckBoxPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
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


class EditableComboBoxPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Editable box plugin """

    def createWidget(self, parent):
        return EditableComboBox(parent)

    def icon(self):
        return super().icon('ComboBox')

    def name(self):
        return "EditableComboBox"


class HyperlinkButtonPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Hyperlink button plugin """

    def createWidget(self, parent):
        return HyperlinkButton('', self.toolTip(), parent)

    def icon(self):
        return super().icon('HyperlinkButton')

    def name(self):
        return "HyperlinkButton"


class PushButtonPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Push button plugin """

    def createWidget(self, parent):
        return PushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "PushButton"


class PrimaryPushButtonPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Primary push button plugin """

    def createWidget(self, parent):
        return PrimaryPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "PrimaryPushButton"


class PillPushButtonPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Pill push button plugin """

    def createWidget(self, parent):
        return PillPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "PillPushButton"


class DropDownPushButtonPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Drop down push button plugin """

    def createWidget(self, parent):
        return DropDownPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "DropDownPushButton"


class PrimaryDropDownPushButtonPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Primary drop down push button plugin """

    def createWidget(self, parent):
        return PrimaryDropDownPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "PrimaryDropDownPushButton"


@EditTextTaskMenuFactory.register
class SplitPushButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
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
class PrimarySplitPushButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
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


class ToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Tool button plugin """

    def createWidget(self, parent):
        return ToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "ToolButton"


class PrimaryToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Primary color tool button plugin """

    def createWidget(self, parent):
        return PrimaryToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "PrimaryToolButton"


class PillToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Pill tool button plugin """

    def createWidget(self, parent):
        return PillToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "PillToolButton"


class TransparentToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Primary color tool button plugin """

    def createWidget(self, parent):
        return TransparentToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "TransparentToolButton"


class DropDownToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Drop down tool button plugin """

    def createWidget(self, parent):
        return DropDownToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "DropDownToolButton"


class PrimaryDropDownToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Drop down tool button plugin """

    def createWidget(self, parent):
        return PrimaryDropDownToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "PrimaryDropDownToolButton"


class SplitToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ split tool button plugin """

    def createWidget(self, parent):
        return SplitToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('SplitButton')

    def name(self):
        return "SplitToolButton"


class PrimarySplitToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Primary color split tool button plugin """

    def createWidget(self, parent):
        return PrimarySplitToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('SplitButton')

    def name(self):
        return "PrimarySplitToolButton"


@EditTextTaskMenuFactory.register
class SwitchButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Switch button plugin """

    def createWidget(self, parent):
        return SwitchButton(parent)

    def icon(self):
        return super().icon('ToggleSwitch')

    def name(self):
        return "SwitchButton"


class RadioButtonPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Radio button plugin """

    def createWidget(self, parent):
        return RadioButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('RadioButton')

    def name(self):
        return "RadioButton"


class ToggleButtonPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Toggle push button plugin """

    def createWidget(self, parent):
        return ToggleButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('ToggleButton')

    def name(self):
        return "ToggleButton"


class ToggleToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Toggle tool button plugin """

    def createWidget(self, parent):
        return ToggleToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('ToggleButton')

    def name(self):
        return "ToggleToolButton"


class TransparentPushButtonPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Transparent push button plugin """

    def createWidget(self, parent):
        return TransparentPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "TransparentPushButton"


class TransparentTogglePushButtonPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Transparent toggle push button plugin """

    def createWidget(self, parent):
        return TransparentTogglePushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('ToggleButton')

    def name(self):
        return "TransparentTogglePushButton"


class TransparentDropDownPushButtonPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Transparent drop down push button plugin """

    def createWidget(self, parent):
        return TransparentDropDownPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "TransparentDropDownPushButton"


class TransparentToggleToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Transparent toggle tool button plugin """

    def createWidget(self, parent):
        return TransparentToggleToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('ToggleButton')

    def name(self):
        return "TransparentToggleToolButton"


class TransparentDropDownToolButtonPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Transparent drop down tool button plugin """

    def createWidget(self, parent):
        return TransparentDropDownToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "TransparentDropDownToolButton"


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


class PixmapLabelPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Pixmap label plugin """

    def createWidget(self, parent):
        return PixmapLabel(parent)

    def icon(self):
        return super().icon('Image')

    def name(self):
        return "PixmapLabel"


class HorizontalSeparatorPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Horizontal separator plugin """

    def createWidget(self, parent):
        return HorizontalSeparator(parent)

    def icon(self):
        return super().icon('Line')

    def name(self):
        return "HorizontalSeparator"


class VerticalSeparatorPlugin(BasicInputPlugin, QPyDesignerCustomWidgetPlugin):
    """ Vertical separator plugin """

    def createWidget(self, parent):
        return VerticalSeparator(parent)

    def icon(self):
        return super().icon('VerticalLine')

    def name(self):
        return "VerticalSeparator"

