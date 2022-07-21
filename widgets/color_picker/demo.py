# coding:utf-8
import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget
from color_picker import ColorPicker


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(500, 600)
        self.colorPicker = ColorPicker(QColor(0, 153, 188), self)
        self.colorPicker.move(50, 50)
        self.setStyleSheet("Demo{background:white}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()
