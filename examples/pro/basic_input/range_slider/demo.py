# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget, QSlider

from qfluentwidgets import setTheme, Theme
from qfluentwidgetspro import RangeSlider


class FloatRangeSlider(RangeSlider):

    def rangeStartToolTipText(self):
        return f"{(self.rangeStart/10):.1f}"

    def rangeEndToolTipText(self):
        return f"{(self.rangeEnd/10):.1f}"


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background: rgb(32,32,32)}')
        self.setStyleSheet('Demo2{background: white}')

        self.resize(500, 500)

        self.slider1 = RangeSlider(Qt.Orientation.Horizontal, self)
        self.slider1.setFixedWidth(300)
        self.slider1.move(100, 30)
        self.slider1.setRangeStart(20)
        self.slider1.setRangeEnd(80)

        self.slider1 = FloatRangeSlider(Qt.Orientation.Horizontal, self)
        self.slider1.setFixedWidth(300)
        self.slider1.move(100, 100)

        self.slider2 = RangeSlider(Qt.Orientation.Vertical, self)
        self.slider2.setFixedHeight(300)
        self.slider2.move(240, 160)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w2 = Demo()
    w2.show()
    sys.exit(app.exec())
