# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget

from qfluentwidgets import CheckBox

class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.checkBox = CheckBox('This is a check box', self)
        self.checkBox.setTristate(True)
        self.checkBox.move(120, 180)

        self.setStyleSheet('Demo{background:white}')
        self.resize(400, 400)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()