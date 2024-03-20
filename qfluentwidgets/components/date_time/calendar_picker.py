# coding:utf-8
from typing import Union

from PySide6.QtCore import Qt, Signal, QRectF, QDate, QPoint, Property
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget, QPushButton, QApplication

from ...common.style_sheet import FluentStyleSheet
from ...common.icon import FluentIcon as FIF
from .calendar_view import CalendarView


class CalendarPicker(QPushButton):
    """ Calendar picker """

    dateChanged = Signal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._date = QDate()
        self._dateFormat = Qt.DateFormat.ISODate

        self.setText(self.tr('Pick a date'))
        FluentStyleSheet.CALENDAR_PICKER.apply(self)

        # Initialize CalendarView as a member variable
        self.calendar_view = CalendarView(self.window())
        self.calendar_view.dateChanged.connect(self._onDateChanged)

        self.clicked.connect(self._showCalendarView)
        self.parent().destroyed.connect(self._onDelCalendarView)

    def getDate(self):
        return self._date

    def setDate(self, date: QDate):
        """ set the selected date """
        self._onDateChanged(date)

    def getDateFormat(self):
        return self._dateFormat

    def setDateFormat(self, format: Union[Qt.DateFormat, str]):
        self._dateFormat = format
        if self._date.isValid():
            self.setText(self._date.toString(self._dateFormat))

    def _showCalendarView(self):
        if self._date.isValid():
            self.calendar_view.setDate(self._date)

        x = int(self.width()/2 - self.calendar_view.sizeHint().width()/2)
        y = self.height()
        self.calendar_view.exec(self.mapToGlobal(QPoint(x, y)))

    def _onDateChanged(self, date: QDate):
        self._date = QDate(date)
        self.setText(date.toString(self.dateFormat))
        self.setProperty('hasDate', True)
        self.setStyle(QApplication.style())
        self.update()

        self.dateChanged.emit(date)

    def _onDelCalendarView(self):
        if self.calendar_view is not None:
            self.calendar_view.deleteLater()
            self.calendar_view = None


    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        if not self.property('hasDate'):
            painter.setOpacity(0.6)

        w = 12
        rect = QRectF(self.width() - 23, self.height()/2 - w/2, w, w)
        FIF.CALENDAR.render(painter, rect)

    date = Property(QDate, getDate, setDate)
    dateFormat = Property(Qt.DateFormat, getDateFormat, setDateFormat)
