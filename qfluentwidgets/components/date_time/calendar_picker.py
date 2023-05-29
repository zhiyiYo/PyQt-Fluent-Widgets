# coding:utf-8
from typing import Union

from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QDate, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication

from ...common.style_sheet import FluentStyleSheet
from ...common.icon import FluentIcon as FIF
from .calendar_view import CalendarView


class CalendarPicker(QPushButton):
    """ Calendar picker """

    dateChanged = pyqtSignal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.date = QDate()
        self.dateFormat = Qt.SystemLocaleDate

        self.view = CalendarView(self.window())
        self.view.hide()

        self.setText(self.tr('Pick a date'))
        FluentStyleSheet.CALENDAR_PICKER.apply(self)

        self.clicked.connect(self._showCalendarView)
        self.view.dateChanged.connect(self._onDateChanged)

    def setDate(self, date: QDate):
        """ set the selected date """
        self._onDateChanged(date)
        self.view.setDate(date)

    def setDateFormat(self, format: Union[Qt.DateFormat, str]):
        self.dateFormat = format
        if self.date.isValid():
            self.setText(self.date.toString(self.dateFormat))

    def _showCalendarView(self):
        x = int(self.width()/2 - self.view.sizeHint().width()/2)
        y = self.height()
        self.view.exec(self.mapToGlobal(QPoint(x, y)))

    def _onDateChanged(self, date: QDate):
        self.date = QDate(date)
        self.setText(date.toString(self.dateFormat))
        self.setProperty('hasDate', True)
        self.setStyle(QApplication.style())
        self.update()

        self.dateChanged.emit(date)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        if not self.property('hasDate'):
            painter.setOpacity(0.6)

        w = 12
        rect = QRectF(self.width() - 23, self.height()/2 - w/2, w, w)
        FIF.CALENDAR.render(painter, rect)
