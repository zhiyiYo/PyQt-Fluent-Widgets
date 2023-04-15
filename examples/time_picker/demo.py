# coding:utf-8
import sys

from PyQt5.QtCore import QDate, Qt, QTime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from qfluentwidgets import TimePicker, AMTimePicker, DatePicker


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.vBoxLayout = QVBoxLayout(self)

        self.picker0 = DatePicker(self, DatePicker.YYYY_MM_DD)
        self.picker1 = AMTimePicker(self)
        self.picker2 = TimePicker(self)
        self.picker3 = TimePicker(self, True)

        self.picker0.dateChanged.connect(lambda t: print(t.toString()))
        self.picker1.timeChanged.connect(lambda t: print(t.toString()))
        self.picker2.timeChanged.connect(lambda t: print(t.toString()))
        self.picker3.timeChanged.connect(lambda t: print(t.toString()))

        # set current date/time
        # self.picker0.setDate(QDate.currentDate())
        # self.picker1.setTime(QTime(13, 15))
        # self.picker2.setTime(QTime(13, 15))

        self.resize(500, 500)
        self.vBoxLayout.addWidget(self.picker0, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.picker1, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.picker2, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.picker3, 0, Qt.AlignHCenter)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()
