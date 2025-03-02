# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QWidget
from qfluentwidgets import ColorPickerButton, setTheme, Theme


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.button = ColorPickerButton(QColor("#5012aaa2"), 'Background Color', self, enableAlpha=True)
        self.resize(800, 720)
        self.button.move(352, 312)
        self.setStyleSheet("Demo{background:white}")

        # setTheme(Theme.DARK)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()