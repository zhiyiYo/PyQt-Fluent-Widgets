# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets import ImageLabel


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.imageLabel = ImageLabel("resource/Gyro.jpg")
        self.gifLabel = ImageLabel("resource/boqi.gif")
        self.vBoxLayout = QVBoxLayout(self)

        # change image
        # self.imageLabel.setImage("resource/boqi.gif")

        self.imageLabel.scaledToHeight(300)
        self.gifLabel.scaledToHeight(300)

        self.imageLabel.setBorderRadius(0, 30, 30, 0)
        self.gifLabel.setBorderRadius(10, 10, 10, 10)

        self.vBoxLayout.addWidget(self.imageLabel)
        self.vBoxLayout.addWidget(self.gifLabel)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()