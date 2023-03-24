# coding:utf-8
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

from qfluentwidgets import LineEdit


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.lineEdit = LineEdit('', self)
        self.resize(500, 500)
        self.lineEdit.move(150, 220)
        self.lineEdit.resize(200, 33)
        self.lineEdit.setClearButtonEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()