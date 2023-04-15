# coding:utf-8
from PyQt6.QtGui import QFontMetrics, QFont
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QCalendar

from .picker_base import PickerBase, PickerPanel


class DatePickerBase(PickerBase):
    """ Date picker base class """

    dateChanged = pyqtSignal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.date = QDate()
        self.calendar = QCalendar()

    def setDate(self, date: QDate):
        """ set current date """
        raise NotImplementedError


class DatePicker(DatePickerBase):
    """ Date picker """

    MM_DD_YYYY = 0
    YYYY_MM_DD = 1

    def __init__(self, parent=None, format=MM_DD_YYYY):
        """
        Parameters
        ----------
        parent: QWidget
            parent widget

        format: int
            the format of date, could be `DatePicker.MM_DD_YYYY` or `DatePicker.YYYY_MM_DD`
        """
        super().__init__(parent=parent)
        self.months = [
            self.tr('January'), self.tr('February'), self.tr('March'),
            self.tr('April'), self.tr('May'), self.tr('June'),
            self.tr('July'), self.tr('August'), self.tr('September'),
            self.tr('October'), self.tr('November'), self.tr('December')
        ]
        self.setDateFormat(format)

    def setDateFormat(self, format: int):
        """ set the format of date

        Parameters
        ----------
        format: int
            the format of date, could be `DatePicker.MM_DD_YYYY` or `DatePicker.YYYY_MM_DD`
        """
        self.clearColumns()
        y = QDate.currentDate().year()

        font = QFont()
        font.setFamilies(['Segoe UI', 'Microsoft YaHei'])
        font.setPixelSize(14)
        fm = QFontMetrics(font)
        w = max(fm.boundingRect(i).width() for i in self.months) + 69

        if format == self.MM_DD_YYYY:
            self.monthIndex = 0
            self.dayIndex = 1
            self.yearIndex = 2

            self.addColumn(self.tr('month'), self.months, w, Qt.AlignmentFlag.AlignLeft)
            self.addColumn(self.tr('day'), range(1, 32), 80)
            self.addColumn(self.tr('year'), range(y-100, y+101), 80)
        elif format == self.YYYY_MM_DD:
            self.yearIndex = 0
            self.monthIndex = 1
            self.dayIndex = 2

            self.addColumn(self.tr('year'), range(y-100, y+101), 80)
            self.addColumn(self.tr('month'), self.months, w)
            self.addColumn(self.tr('day'), range(1, 32), 80)

        # initialize date
        date = self.date.currentDate()
        self.columns[self.monthIndex].value = self.months[date.month() - 1]
        self.columns[self.dayIndex].value = date.day()
        self.columns[self.yearIndex].value = date.year()

    def _onColumnValueChanged(self, panel: PickerPanel, index, value):
        if index == self.dayIndex:
            return

        # get days number in month
        month = panel.columnValue(self.monthIndex)
        month = self.months.index(month) + 1
        year = int(panel.columnValue(self.yearIndex))
        days = self.calendar.daysInMonth(month, year)

        # update days
        c = panel.column(self.dayIndex)
        day = c.currentItem().text()
        c.setItems(range(1, days + 1))
        c.setSelectedItem(day)
        self.columns[self.dayIndex].items = list(range(1, days + 1))

    def _onConfirmed(self, value: list):
        month = self.months.index(value[self.monthIndex]) + 1

        date = QDate(int(value[self.yearIndex]), month, int(value[self.dayIndex]))
        od = self.date
        self.setDate(date)

        if od != date:
            self.dateChanged.emit(date)

    def setDate(self, date: QDate):
        if not date.isValid() or date.isNull():
            return

        self.date = date
        self.setColumnValue(self.monthIndex, self.months[date.month() - 1])
        self.setColumnValue(self.dayIndex, date.day())
        self.setColumnValue(self.yearIndex, date.year())
        self.columns[self.dayIndex].items = list(range(1, date.daysInMonth() + 1))