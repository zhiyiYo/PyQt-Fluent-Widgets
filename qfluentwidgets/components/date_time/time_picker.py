# coding:utf-8
from enum import Enum

from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTime
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

from .picker_base import PickerBase


class TimePickerBase(PickerBase):
    """ Time picker base class """

    timeChanged = pyqtSignal(QTime)

    def __init__(self, parent=None, showSeconds=False):
        super().__init__(parent=parent)
        self.showSeconds = showSeconds
        self.time = QTime()

    def setTime(self, time: QTime):
        """ set current time

        Parameters
        ----------
        time: QTime
            current time
        """
        raise NotImplementedError

    def setSecondVisible(self, isVisible: bool):
        """ set the visibility of seconds column """
        raise NotImplementedError


class TimePicker(TimePickerBase):
    """ 24 hours time picker """

    def __init__(self, parent=None, showSeconds=False):
        super().__init__(parent, showSeconds)
        # add hour column
        w = 80 if showSeconds else 120
        self.addColumn(self.tr('hour'), range(0, 24), w)

        # add minute column
        minute = [str(i).zfill(2) for i in range(0, 60)]
        self.addColumn(self.tr('minute'), minute, w)

        # add seconds column
        self.addColumn(self.tr('second'), minute, w)
        self.setColumnVisible(2, showSeconds)

    def setTime(self, time):
        if not time.isValid() or time.isNull():
            return

        self.time = time
        self.setColumnValue(0, time.hour())
        self.setColumnValue(1, str(time.minute()).zfill(2))
        self.setColumnValue(2, str(time.second()).zfill(2))

    def setSecondVisible(self, isVisible: bool):
        self.setColumnVisible(2, isVisible)
        w = 80 if isVisible else 120
        for column, button in zip(self.columns, self.buttons):
            button.setFixedWidth(w)
            column.width = w

    def _onConfirmed(self, value: list):
        super()._onConfirmed(value)
        h, m = int(value[0]), int(value[1])
        s = 0 if len(value) == 2 else int(value[2])
        time = QTime(h, m, s)
        ot = self.time
        self.setTime(time)

        if ot != time:
            self.timeChanged.emit(time)


class AMTimePicker(TimePickerBase):
    """ AM/PM time picker """

    def __init__(self, parent=None, showSeconds=False):
        super().__init__(parent, showSeconds)
        self.AM = self.tr('AM')
        self.PM = self.tr('PM')

        # add hour column
        self.addColumn(self.tr('hour'), range(1, 13), 80)

        # add minute column
        minute = [str(i).zfill(2) for i in range(0, 60)]
        self.addColumn(self.tr('minute'), minute, 80)

        # add second column
        self.addColumn(self.tr('second'), minute, 80)
        self.setColumnVisible(2, showSeconds)

        # add AM/PM column
        self.addColumn(self.AM, [self.AM, self.PM], 80)

    def setSecondVisible(self, isVisible: bool):
        self.setColumnVisible(2, isVisible)

    def setTime(self, time):
        if not time.isValid() or time.isNull():
            return

        self.time = time
        h = time.hour()

        if h in [0, 12]:
            self.setColumnValue(0, 12)
        else:
            self.setColumnValue(0, h % 12)

        self.setColumnValue(1, str(time.minute()).zfill(2))
        self.setColumnValue(2, str(time.second()).zfill(2))
        self.setColumnValue(3, self.AM if h < 12 else self.PM)

    def _onConfirmed(self, value: list):
        super()._onConfirmed(value)

        if len(value) == 3:
            h, m, p = value
            s = 0
        else:
            h, m, s, p = value

        h, m, s = int(h), int(m), int(s)

        if p == self.AM:
            h = 0 if h == 12 else h
        elif p == self.PM:
            h = h if h == 12 else h + 12

        time = QTime(h, m, s)
        ot = self.time
        self.setTime(time)

        if ot != time:
            self.timeChanged.emit(time)
