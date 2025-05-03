# coding:utf-8
from typing import Union

from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QDate, QPoint, pyqtProperty
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication

from ...common.style_sheet import FluentStyleSheet
from ...common.icon import FluentIcon as FIF
from ..widgets.flyout import Flyout, FlyoutAnimationType
from .calendar_view import CalendarView
from .fast_calendar_view import FastCalendarView


class CalendarPicker(QPushButton):
    """ Calendar picker """

    dateChanged = pyqtSignal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._date = QDate()
        self._dateFormat = Qt.SystemLocaleDate
        self._isResetEnabled = False

        self.setText(self.tr('Pick a date'))
        FluentStyleSheet.CALENDAR_PICKER.apply(self)

        self.clicked.connect(self._showCalendarView)

    def getDate(self):
        return self._date

    def setDate(self, date: QDate):
        """ set the selected date """
        self._onDateChanged(date)

    def reset(self):
        """ reset date """
        self._date = QDate()
        self.setText(self.tr('Pick a date'))
        self.setProperty('hasDate', False)
        self.setStyle(QApplication.style())
        self.update()

    def getDateFormat(self):
        return self._dateFormat

    def setDateFormat(self, format: Union[Qt.DateFormat, str]):
        self._dateFormat = format
        if self.date.isValid():
            self.setText(self.date.toString(self.dateFormat))

    def isRestEnabled(self):
        return self._isResetEnabled

    def setResetEnabled(self, isEnabled: bool):
        """ set the visibility of reset button """
        self._isResetEnabled = isEnabled

    def _showCalendarView(self):
        view = CalendarView(self.window())
        view.setResetEnabled(self.isRestEnabled())

        view.resetted.connect(self.reset)
        view.dateChanged.connect(self._onDateChanged)

        if self.date.isValid():
            view.setDate(self.date)

        x = int(self.width()/2 - view.sizeHint().width()/2)
        y = self.height()
        view.exec(self.mapToGlobal(QPoint(x, y)))

    def _onDateChanged(self, date: QDate):
        self._date = QDate(date)
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

    date = pyqtProperty(QDate, getDate, setDate)
    dateFormat = pyqtProperty(Qt.DateFormat, getDateFormat, setDateFormat)


class FastCalendarPicker(CalendarPicker):
    """ Pro calendar picker """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.flyoutAnimationType = FlyoutAnimationType.DROP_DOWN

    def setFlyoutAnimationType(self, aniType: FlyoutAnimationType):
        self.flyoutAnimationType = aniType

    def _showCalendarView(self):
        view = FastCalendarView(self.window())
        view.setResetEnabled(self.isRestEnabled())

        view.resetted.connect(self.reset)
        view.dateChanged.connect(self._onDateChanged)

        if self.date.isValid():
            view.setDate(self.date)

        flyout = Flyout.make(view, self, self.window(), self.flyoutAnimationType)
        view.dateChanged.connect(flyout.close)
