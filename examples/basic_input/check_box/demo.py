# coding:utf-8
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QSizePolicy

from qfluentwidgets import CheckBox


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)
        self.checkBox = CheckBox('This is a check box', self)
        self.checkBox.setTristate(True)

        self.hBoxLayout.addWidget(self.checkBox, 1, Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet('Demo{background:white}')
        self.resize(400, 400)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()