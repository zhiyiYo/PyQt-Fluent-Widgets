# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget, QSlider

from qfluentwidgets import setTheme, Theme
from qfluentwidgetspro import ToolTipSlider


class FloatSlider(ToolTipSlider):

    def toolTipText(self):
        return f"{(self.value()/10):.1f}"


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background: rgb(32,32,32)}')
        self.setStyleSheet('Demo2{background: white}')

        self.resize(300, 300)

        self.slider1 = ToolTipSlider(Qt.Orientation.Horizontal, self)
        self.slider1.setFixedWidth(200)
        self.slider1.move(50, 30)

        self.slider1 = FloatSlider(Qt.Orientation.Horizontal, self)
        self.slider1.setFixedWidth(200)
        self.slider1.move(50, 80)

        self.slider2 = ToolTipSlider(Qt.Orientation.Vertical, self)
        self.slider2.setFixedHeight(150)
        self.slider2.move(140, 120)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w2 = Demo()
    w2.show()
    sys.exit(app.exec())
