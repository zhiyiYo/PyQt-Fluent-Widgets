# coding:utf-8
import sys

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import ColorPickerButton


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.button = ColorPickerButton(QColor("#12aaa2"), 'Background Color', self)
        self.resize(800, 720)
        self.button.move(352, 312)
        self.setStyleSheet("Demo{background:white}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()