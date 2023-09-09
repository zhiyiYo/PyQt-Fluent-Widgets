# coding:utf-8
import sys

from PyQt6.QtCore import QDate, Qt, QTime
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout

from qfluentwidgets import TimePicker, AMTimePicker, DatePicker, ZhDatePicker, setTheme, Theme, PickerColumnFormatter


class SecondsFormatter(PickerColumnFormatter):
    """ Seconds formatter """

    def encode(self, value):
        return str(value) + "秒"

    def decode(self, value: str):
        return int(value[:-1])



class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet('Demo{background: white}')
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background: rgb(32, 32, 32)}')

        self.vBoxLayout = QVBoxLayout(self)

        self.datePicker1 = DatePicker(self)
        self.datePicker2 = ZhDatePicker(self)
        self.timePicker1 = AMTimePicker(self)
        self.timePicker2 = TimePicker(self)
        self.timePicker3 = TimePicker(self, showSeconds=True)

        # customize column format
        self.timePicker3.setColumnFormatter(2, SecondsFormatter())

        self.datePicker1.dateChanged.connect(lambda t: print(t.toString()))
        self.datePicker2.dateChanged.connect(lambda t: print(t.toString()))
        self.timePicker1.timeChanged.connect(lambda t: print(t.toString()))
        self.timePicker2.timeChanged.connect(lambda t: print(t.toString()))
        self.timePicker3.timeChanged.connect(lambda t: print(t.toString()))

        # set current date/time
        # self.datePicker1.setDate(QDate.currentDate())
        # self.timePicker1.setTime(QTime(13, 15))
        # self.timePicker2.setTime(QTime(13, 15))

        self.resize(500, 500)
        self.vBoxLayout.addWidget(self.datePicker1, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout.addWidget(self.datePicker2, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout.addWidget(self.timePicker1, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout.addWidget(self.timePicker2, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout.addWidget(self.timePicker3, 0, Qt.AlignmentFlag.AlignHCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
