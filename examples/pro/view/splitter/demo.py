# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QButtonGroup, QHBoxLayout

from qfluentwidgets import setTheme, Theme, FluentIcon, StrongBodyLabel, themeColor
from qfluentwidgetspro import Splitter


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)

        self.splitter = Splitter(Qt.Orientation.Horizontal, self)
        self.leftLabel = StrongBodyLabel('Side Content')

        self.splitter.addWidget(self.leftLabel)
        self.splitter.addWidget(QWidget())

        self.leftLabel.setStyleSheet(f"QLabel{{background: {themeColor().name()}; color: white}}")
        self.leftLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.leftLabel.setMinimumWidth(200)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.splitter)
        self.resize(600, 500)

        # setTheme(Theme.DARK)
        # self.setStyleSheet("Demo{background: rgb(32,32,32)}")
        self.setStyleSheet('Demo{background:white}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()