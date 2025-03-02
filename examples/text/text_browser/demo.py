# coding:utf-8
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QCompleter

from qfluentwidgets import LineEdit, PushButton, TextBrowser, setTheme, Theme


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # self.setStyleSheet("Demo {background: rgb(32, 32, 32)}")
        # setTheme(Theme.DARK)

        self.hBoxLayout = QHBoxLayout(self)
        self.textBrowser = TextBrowser(self)

        # add completer
        self.resize(400, 400)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.textBrowser, 0, Qt.AlignmentFlag.AlignCenter)

        self.textBrowser.setPlaceholderText('Search stand')
        self.textBrowser.setMarkdown("## Steel Ball Run \n * Johnny Joestar 🦄 \n * Gyro Zeppeli 🐴")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
