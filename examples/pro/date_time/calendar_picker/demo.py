# coding:utf-8
import sys

from PySide6.QtCore import Qt, QCalendar, QDate
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import setTheme, Theme, FlyoutAnimationType
from qfluentwidgetspro import ProCalendarPicker, DateValidator


class WeekendDateValidator(DateValidator):
    """ Weekend date validator """

    def canBlackout(self, date: QDate):
        return date.dayOfWeek() > 5


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setStyleSheet('Demo{background: rgb(32,32,32)}')

        self.picker = ProCalendarPicker(self)
        self.picker.dateChanged.connect(print)

        # set custom date validator
        self.picker.setDateValidator(WeekendDateValidator())

        # set date
        # self.picker.setDate(QDate(2023, 5, 30))

        # set flyout animation
        # self.picker.setFlyoutAnimationType(FlyoutAnimationType.SLIDE_RIGHT)

        # customize date format
        # self.picker.setDateFormat(Qt.TextDate)
        # self.picker.setDateFormat('yyyy/M/d')

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.picker, 0, Qt.AlignCenter)
        self.resize(500, 500)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()