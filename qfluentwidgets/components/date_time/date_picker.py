# coding:utf-8
from PySide6.QtCore import Qt, Signal, QDate, QCalendar, Property

from .picker_base import PickerBase, PickerPanel, PickerColumnFormatter, DigitFormatter


class DatePickerBase(PickerBase):
    """ Date picker base class """

    dateChanged = Signal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._date = QDate()
        self.calendar = QCalendar()
        self._yearFormatter = None
        self._monthFormatter = None
        self._dayFormatter = None

    def getDate(self):
        return self._date

    def setDate(self, date: QDate):
        """ set current date """
        raise NotImplementedError

    def setYearFormatter(self, formatter: PickerColumnFormatter):
        self._yearFormatter = formatter

    def setMonthFormatter(self, formatter: PickerColumnFormatter):
        self._monthFormatter = formatter

    def setDayFormatter(self, formatter: PickerColumnFormatter):
        self._dayFormatter = formatter

    def yearFormatter(self):
        return self._yearFormatter or DigitFormatter()

    def dayFormatter(self):
        return self._dayFormatter or DigitFormatter()

    def monthFormatter(self):
        return self._monthFormatter or MonthFormatter()


class MonthFormatter(PickerColumnFormatter):
    """ Month formatter """

    def __init__(self):
        super().__init__()
        self.months = [
            self.tr('January'), self.tr('February'), self.tr('March'),
            self.tr('April'), self.tr('May'), self.tr('June'),
            self.tr('July'), self.tr('August'), self.tr('September'),
            self.tr('October'), self.tr('November'), self.tr('December')
        ]

    def encode(self, month):
        return self.months[int(month) - 1]

    def decode(self, value):
        return self.months.index(value) + 1


class DatePicker(DatePickerBase):
    """ Date picker """

    MM_DD_YYYY = 0
    YYYY_MM_DD = 1

    def __init__(self, parent=None, format=MM_DD_YYYY, isMonthTight=True):
        """
        Parameters
        ----------
        parent: QWidget
            parent widget

        format: int
            the format of date, could be `DatePicker.MM_DD_YYYY` or `DatePicker.YYYY_MM_DD`

        isMonthTight: bool
            is the month column tight
        """
        super().__init__(parent=parent)
        self.MONTH = self.tr('month')
        self.YEAR = self.tr('year')
        self.DAY = self.tr('day')

        self.isMonthTight = isMonthTight
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
        self.dateFormat = format

        if format == self.MM_DD_YYYY:
            self.monthIndex = 0
            self.dayIndex = 1
            self.yearIndex = 2

            self.addColumn(self.MONTH, range(1, 13),
                           80, Qt.AlignLeft, self.monthFormatter())
            self.addColumn(self.DAY, range(1, 32),
                           80, formatter=self.dayFormatter())
            self.addColumn(self.YEAR, range(y-100, y+101),
                           80, formatter=self.yearFormatter())
        elif format == self.YYYY_MM_DD:
            self.yearIndex = 0
            self.monthIndex = 1
            self.dayIndex = 2

            self.addColumn(self.YEAR, range(y-100, y+101),
                           80, formatter=self.yearFormatter())
            self.addColumn(self.MONTH, range(1, 13),
                           80, formatter=self.monthFormatter())
            self.addColumn(self.DAY, range(1, 32), 80,
                           formatter=self.dayFormatter())

        self.setColumnWidth(self.monthIndex, self._monthColumnWidth())

    def panelInitialValue(self):
        if any(self.value()):
            return self.value()

        date = QDate.currentDate()
        y = self.encodeValue(self.yearIndex, date.year())
        m = self.encodeValue(self.monthIndex, date.month())
        d = self.encodeValue(self.dayIndex, date.day())
        return [y, m, d] if self.dateFormat == self.YYYY_MM_DD else [m, d, y]

    def setMonthTight(self, isTight: bool):
        """ set whether the month column is tight """
        if self.isMonthTight == isTight:
            return

        self.isMonthTight = isTight
        self.setColumnWidth(self.monthIndex, self._monthColumnWidth())

    def _monthColumnWidth(self):
        fm = self.fontMetrics()
        wm = max(fm.boundingRect(i).width()
                 for i in self.columns[self.monthIndex].items()) + 20

        # don't use tight layout for english
        if self.MONTH == 'month':
            return wm + 49

        return max(80, wm) if self.isMonthTight else wm + 49

    def _onColumnValueChanged(self, panel: PickerPanel, index, value):
        if index == self.dayIndex:
            return

        # get days number in month
        month = self.decodeValue(
            self.monthIndex, panel.columnValue(self.monthIndex))
        year = self.decodeValue(
            self.yearIndex, panel.columnValue(self.yearIndex))
        days = self.calendar.daysInMonth(month, year)

        # update days
        c = panel.column(self.dayIndex)
        day = c.currentItem().text()
        self.setColumnItems(self.dayIndex, range(1, days + 1))

        c.setItems(self.columns[self.dayIndex].items())
        c.setSelectedItem(day)

    def _onConfirmed(self, value: list):
        year = self.decodeValue(self.yearIndex, value[self.yearIndex])
        month = self.decodeValue(self.monthIndex, value[self.monthIndex])
        day = self.decodeValue(self.dayIndex, value[self.dayIndex])

        date, od = QDate(year, month, day), self.date
        self.setDate(date)

        if od != date:
            self.dateChanged.emit(date)

    def getDate(self):
        return self._date

    def setDate(self, date: QDate):
        if not date.isValid() or date.isNull():
            return

        self._date = date
        self.setColumnValue(self.monthIndex, date.month())
        self.setColumnValue(self.dayIndex, date.day())
        self.setColumnValue(self.yearIndex, date.year())
        self.setColumnItems(self.dayIndex, range(1, date.daysInMonth() + 1))

    date = Property(QDate, getDate, setDate)


class ZhFormatter(PickerColumnFormatter):
    """ Chinese date formatter """

    suffix = ""

    def encode(self, value):
        return str(value) + self.suffix

    def decode(self, value: str):
        return int(value[:-1])


class ZhYearFormatter(ZhFormatter):
    """ Chinese year formatter """

    suffix = "年"


class ZhMonthFormatter(ZhFormatter):
    """ Chinese month formatter """

    suffix = "月"


class ZhDayFormatter(ZhFormatter):
    """ Chinese day formatter """

    suffix = "日"


class ZhDatePicker(DatePicker):
    """ Chinese date picker """

    def __init__(self, parent=None):
        super().__init__(parent, DatePicker.YYYY_MM_DD)
        self.MONTH = "月"
        self.YEAR = "年"
        self.DAY = "日"
        self.setDayFormatter(ZhDayFormatter())
        self.setYearFormatter(ZhYearFormatter())
        self.setMonthFormatter(ZhMonthFormatter())
        self.setDateFormat(self.YYYY_MM_DD)