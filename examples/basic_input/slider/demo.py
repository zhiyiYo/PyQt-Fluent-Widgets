# coding:utf-8
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QWidget, QSlider

from qfluentwidgets import HollowHandleStyle, Slider, setTheme, Theme


class Demo1(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(300, 150)
        self.setStyleSheet("Demo1{background: rgb(184, 106, 106)}")

        # customize style
        style = {
            "sub-page.color": QColor(70, 23, 180)
        }
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setStyle(HollowHandleStyle(style))

        # need adjust height
        self.slider.resize(200, 28)
        self.slider.move(50, 61)


class Demo2(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo2{background: rgb(32,32,32)}')
        self.setStyleSheet('Demo2{background: white}')

        self.resize(300, 300)

        self.slider1 = Slider(Qt.Orientation.Horizontal, self)
        self.slider1.setFixedWidth(200)
        self.slider1.move(50, 30)

        self.slider2 = Slider(Qt.Orientation.Vertical, self)
        self.slider2.setFixedHeight(150)
        self.slider2.move(140, 80)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = Demo1()
    w1.show()
    w2 = Demo2()
    w2.show()
    app.exec()
