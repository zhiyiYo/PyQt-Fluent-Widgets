# coding:utf-8
from enum import Enum

from PyQt5.QtCore import Qt, pyqtSignal, QSize, QTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from .picker_base import PickerBase


class TimePickerBase(PickerBase):
    """ Time picker base class """

    timeChanged = pyqtSignal(QTime)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.time = QTime()
        self._addColumns()

    def _addColumns(self):
        """ add column to time picker """
        raise NotImplementedError

    def setTime(self, time: QTime):
        """ set current time

        Parameters
        ----------
        time: QTime
            current time
        """
        raise NotImplementedError


class TimePicker(TimePickerBase):
    """ 24 hours time picker """

    def _addColumns(self):
        self.addColumn(self.tr('hour'), range(0, 24), 120)

        minute = [str(i).zfill(2) for i in range(0, 60)]
        self.addColumn(self.tr('minute'), minute, 120)

    def setTime(self, time):
        if not time.isValid() or time.isNull():
            return

        self.time = time
        self.setColumnValue(0, time.hour())
        self.setColumnValue(1, str(time.minute()).zfill(2))

    def _onConfirmed(self, value: list):
        super()._onConfirmed(value)
        h, m = int(value[0]), int(value[1])
        time = QTime(h, m)
        ot = self.time
        self.setTime(time)

        if ot != time:
            self.timeChanged.emit(time)


class AMTimePicker(TimePickerBase):
    """ AM/PM time picker """

    def __init__(self, parent=None):
        super().__init__(parent)

    def _addColumns(self):
        self.addColumn(self.tr('hour'), range(1, 13), 80)

        minute = [str(i).zfill(2) for i in range(0, 60)]
        self.addColumn(self.tr('minute'), minute, 80)

        self.addColumn(self.tr('AM'), [self.tr('AM'), self.tr('PM')], 80)

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
        self.setColumnValue(2, self.tr('AM') if h < 12 else self.tr('PM'))

    def _onConfirmed(self, value: list):
        super()._onConfirmed(value)

        h, m, p = value
        h, m = int(h), int(m)

        if p == self.tr('AM'):
            h = 0 if h == 12 else h
        elif p == self.tr('PM'):
            h = h if h == 12 else h + 12

        time = QTime(h, m)
        ot = self.time
        self.setTime(time)

        if ot != time:
            self.timeChanged.emit(time)
