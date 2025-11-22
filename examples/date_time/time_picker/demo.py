# coding:utf-8
import sys

#from pathlib import Path
#sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from PyQt5.QtCore import QDate, Qt, QTime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

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

        # create pickers with scroll button repeat enabled by default
        self.datePicker1 = DatePicker(self)
        self.datePicker2 = ZhDatePicker(self)
        self.timePicker1 = AMTimePicker(self)
        self.timePicker2 = TimePicker(self)
        self.timePicker3 = TimePicker(self, showSeconds=True)

        # enable reset button
        # self.datePicker1.setResetEnabled(True)
        # self.timePicker1.setResetEnabled(True)

        # disable scroll button repeat if needed
        # self.datePicker1.setScrollButtonRepeatEnabled(False)
        # self.timePicker1.setScrollButtonRepeatEnabled(False)

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
        self.vBoxLayout.addWidget(self.datePicker1, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.datePicker2, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.timePicker1, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.timePicker2, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.timePicker3, 0, Qt.AlignHCenter)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()
