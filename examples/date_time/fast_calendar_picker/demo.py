# coding:utf-8
import sys

from PyQt6.QtCore import Qt, QCalendar, QDate
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import FastCalendarPicker, setTheme, Theme, FluentTranslator, FlyoutAnimationType


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet('Demo{background: white}')

        self.picker = FastCalendarPicker(self)
        self.picker.dateChanged.connect(print)

        # customize animation
        # self.picker.setFlyoutAnimationType(FlyoutAnimationType.SLIDE_RIGHT)

        # set date
        # self.picker.setDate(QDate(2023, 5, 30))

        # customize date format
        # self.picker.setDateFormat(Qt.TextDate)
        # self.picker.setDateFormat('yyyy-M-d')

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.picker, 0, Qt.AlignmentFlag.AlignCenter)
        self.resize(500, 500)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # install translator
    translator = FluentTranslator()
    app.installTranslator(translator)

    w = Demo()
    w.show()
    app.exec()