# coding:utf-8
from PyQt5.QtCore import Qt
from qfluentwidgets import DatePicker, TimePicker, AMTimePicker, ZhDatePicker

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class DateTimeInterface(GalleryInterface):
    """ Date time interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.dateTime,
            subtitle='qfluentwidgets.components.date_time',
            parent=parent
        )

        # date picker
        self.addExampleCard(
            title=self.tr('A simple DatePicker'),
            widget=DatePicker(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/date_time/demo.py'
        )

        self.addExampleCard(
            title=self.tr('A DatePicker in another format'),
            widget=ZhDatePicker(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/date_time/demo.py'
        )

        # AM/PM time picker
        self.addExampleCard(
            title=self.tr('A simple TimePicker'),
            widget=AMTimePicker(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/date_time/demo.py'
        )

        # 24 hours time picker
        self.addExampleCard(
            title=self.tr('A TimePicker using a 24-hour clock'),
            widget=TimePicker(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/date_time/demo.py'
        )

        # 24 hours time picker
        self.addExampleCard(
            title=self.tr('A TimePicker with seconds column'),
            widget=TimePicker(self, True),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/date_time/demo.py'
        )

