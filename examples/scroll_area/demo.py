# coding:utf-8
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel
from qfluentwidgets import SmoothScrollArea


class Demo(SmoothScrollArea):

    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("resource/shoko.jpg"))

        self.horizontalScrollBar().setValue(1900)
        self.setWidget(self.label)
        self.resize(1200, 800)

        with open('resource/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()