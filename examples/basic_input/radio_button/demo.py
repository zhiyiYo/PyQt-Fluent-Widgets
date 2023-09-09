# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from qfluentwidgets import RadioButton


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.vBoxLayout = QVBoxLayout(self)
        self.button1 = RadioButton('Option 1', self)
        self.button2 = RadioButton('Option 2', self)
        self.button3 = RadioButton('Option 3', self)

        self.vBoxLayout.addWidget(self.button1, 0, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(self.button2, 0, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(self.button3, 0, Qt.AlignmentFlag.AlignCenter)
        self.resize(300, 150)
        self.setStyleSheet('Demo{background:white}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()