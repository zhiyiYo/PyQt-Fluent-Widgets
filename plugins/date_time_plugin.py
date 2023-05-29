# coding: utf-8
from PySide6.QtCore import Qt
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

from qfluentwidgets import DatePicker, TimePicker, ZhDatePicker, AMTimePicker, CalendarPicker

from plugin_base import PluginBase


class DateTimePlugin(PluginBase):

    def group(self):
        return super().group() + ' (Date Time)'


class DatePickerPlugin(DateTimePlugin, QDesignerCustomWidgetInterface):
    """ Date picker plugin """

    def createWidget(self, parent):
        return DatePicker(parent)

    def icon(self):
        return super().icon("DatePicker")

    def name(self):
        return "DatePicker"


class ZhDatePickerPlugin(DateTimePlugin, QDesignerCustomWidgetInterface):
    """ Chinese Date picker plugin """

    def createWidget(self, parent):
        return ZhDatePicker(parent)

    def icon(self):
        return super().icon("DatePicker")

    def name(self):
        return "ZhDatePicker"

    def toolTip(self):
        return "Chinese date picker"


class TimePickerPlugin(DateTimePlugin, QDesignerCustomWidgetInterface):
    """ Time picker plugin """

    def createWidget(self, parent):
        return TimePicker(parent)

    def icon(self):
        return super().icon("TimePicker")

    def name(self):
        return "TimePicker"

    def toolTip(self):
        return "24 hours time picker"


class AMTimePickerPlugin(DateTimePlugin, QDesignerCustomWidgetInterface):
    """ AM/PM time picker plugin """

    def createWidget(self, parent):
        return AMTimePicker(parent)

    def icon(self):
        return super().icon("TimePicker")

    def name(self):
        return "AMTimePicker"

    def toolTip(self):
        return "AM/PM time picker"
