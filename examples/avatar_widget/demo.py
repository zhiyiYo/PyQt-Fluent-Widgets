# coding:utf-8
import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import AvatarWidget


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.setStyleSheet('Demo {background: white}')
        self.hBoxLayout = QHBoxLayout(self)

        avatar = QPixmap('resource/shoko.png')
        # avatar = 'resource/boqi.gif'

        sizes = [96, 48, 32, 24]
        for s in sizes:
            w = AvatarWidget(avatar, self)
            w.setRadius(s // 2)
            self.hBoxLayout.addWidget(w)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
