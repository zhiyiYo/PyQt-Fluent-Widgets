# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import PipsScrollButtonDisplayMode, HorizontalPipsPager, VerticalPipsPager, setTheme, Theme


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background:rgb(32,32,32)}')

        self.vPager = VerticalPipsPager(self)
        self.hPager = HorizontalPipsPager(self)

        # set the number of page
        self.hPager.setPageNumber(15)
        self.vPager.setPageNumber(15)

        # set the number of displayed pips
        self.hPager.setVisibleNumber(8)
        self.hPager.setNextButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)
        self.hPager.setPreviousButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)

        # set the display mode of scroll button
        self.vPager.setNextButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)
        self.vPager.setPreviousButtonDisplayMode(PipsScrollButtonDisplayMode.ON_HOVER)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.hPager)
        self.layout().addWidget(self.vPager)

        self.resize(500, 500)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()