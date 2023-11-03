# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QCompleter, QVBoxLayout

from qfluentwidgets import setTheme, Theme, FluentIcon, setFont, FluentThemeColor, FlyoutAnimationType
from qfluentwidgetspro import DropDownColorPalette, Pager, ProTranslator


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.pager = Pager(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.pager.setTotal(100)
        self.pager.setPageSize(5)
        self.pager.setVisiblePageCount(7)

        # set the visibility of ...
        # self.pager.setLeftElideVisible(False)
        # self.pager.setRightElideVisible(False)

        # set the visibility of button
        # self.pager.setFirstPageButtonVisible(False)
        # self.pager.setPreviousPageButtonVisible(False)
        # self.pager.setLastPageButtonVisible(False)
        # self.pager.setNextPageButtonVisible(False)
        # self.pager.setPageEditVisible(False)

        # change the icon
        # self.brushPicker.setIcon(FluentIcon.BACKGROUND_FILL)

        self.resize(700, 500)
        self.vBoxLayout.addWidget(self.pager)
        self.vBoxLayout.setContentsMargins(30, 0, 30, 0)

        setTheme(Theme.DARK)
        self.setStyleSheet("Demo{background: rgb(32,32,32)}")
        # self.setStyleSheet('Demo{background:white}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = ProTranslator()
    app.installTranslator(translator)
    w = Demo()
    w.show()
    app.exec()