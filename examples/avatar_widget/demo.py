# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout

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
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()
