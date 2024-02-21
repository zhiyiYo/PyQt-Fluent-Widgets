# coding: utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from qfluentwidgets import (SpinBox, CompactSpinBox, DoubleSpinBox, CompactDoubleSpinBox, TextEdit,
                            TimeEdit, CompactTimeEdit, DateTimeEdit, CompactDateTimeEdit,
                            LineEdit, PlainTextEdit, DateEdit, CompactDateEdit, SearchLineEdit,
                            PasswordLineEdit)

from plugin_base import PluginBase


class TextPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Text)'


class LineEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Line edit plugin """

    def createWidget(self, parent):
        return LineEdit(parent)

    def icon(self):
        return super().icon("TextBox")

    def name(self):
        return "LineEdit"


class SearchLineEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Search line edit plugin """

    def createWidget(self, parent):
        return SearchLineEdit(parent)

    def icon(self):
        return super().icon("TextBox")

    def name(self):
        return "SearchLineEdit"


class PasswordLineEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Password line edit plugin """

    def createWidget(self, parent):
        return PasswordLineEdit(parent)

    def icon(self):
        return super().icon("PasswordBox")

    def name(self):
        return "PasswordLineEdit"


class TextEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Text edit plugin """

    def createWidget(self, parent):
        return TextEdit(parent)

    def icon(self):
        return super().icon("RichEditBox")

    def name(self):
        return "TextEdit"


class PlainTextEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Plain text edit plugin """

    def createWidget(self, parent):
        return PlainTextEdit(parent)

    def icon(self):
        return super().icon("RichEditBox")

    def name(self):
        return "PlainTextEdit"


class DateEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Date edit plugin """

    def createWidget(self, parent):
        return DateEdit(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "DateEdit"


class TimeEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Time edit plugin """

    def createWidget(self, parent):
        return TimeEdit(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "TimeEdit"


class DateTimeEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Date time edit plugin """

    def createWidget(self, parent):
        return DateTimeEdit(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "DateTimeEdit"


class SpinBoxPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Spin box plugin """

    def createWidget(self, parent):
        return SpinBox(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "SpinBox"


class DoubleSpinBoxPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Double spin box plugin """

    def createWidget(self, parent):
        return DoubleSpinBox(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "DoubleSpinBox"


class CompactDateEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Compact date edit plugin """

    def createWidget(self, parent):
        return CompactDateEdit(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "CompactDateEdit"


class CompactTimeEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Compact time edit plugin """

    def createWidget(self, parent):
        return CompactTimeEdit(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "CompactTimeEdit"


class CompactDateTimeEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Date time edit plugin """

    def createWidget(self, parent):
        return CompactDateTimeEdit(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "CompactDateTimeEdit"


class CompactSpinBoxPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Compact spin box plugin """

    def createWidget(self, parent):
        return CompactSpinBox(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "CompactSpinBox"


class CompactDoubleSpinBoxPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Compact double spin box plugin """

    def createWidget(self, parent):
        return CompactDoubleSpinBox(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "CompactDoubleSpinBox"
