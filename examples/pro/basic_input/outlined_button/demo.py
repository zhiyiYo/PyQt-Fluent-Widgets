# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QButtonGroup, QHBoxLayout

from qfluentwidgets import setTheme, Theme, FluentIcon
from qfluentwidgetspro import OutlinedPushButton


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)
        self.buttonGroup = QButtonGroup(self)

        self.resize(600, 500)
        self.hBoxLayout.setContentsMargins(30, 0, 30, 0)

        texts = ['应用', '游戏', '电影和电视', '设备附带']
        for text in texts:
            button = OutlinedPushButton(text, self)
            button.setFixedWidth(100)
            self.buttonGroup.addButton(button)
            self.hBoxLayout.addWidget(button)

        setTheme(Theme.DARK)
        self.setStyleSheet("Demo{background: rgb(32,32,32)}")
        # self.setStyleSheet('Demo{background:white}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()