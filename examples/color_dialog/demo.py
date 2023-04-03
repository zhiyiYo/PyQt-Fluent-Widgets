# coding:utf-8
import sys

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QApplication, QWidget
from qfluentwidgets import ColorPickerButton, setTheme, Theme


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.button = ColorPickerButton(QColor("#12aaa2"), 'Background Color', self)
        self.resize(800, 720)
        self.button.move(352, 312)
        self.setStyleSheet("Demo{background:white}")

        # setTheme(Theme.DARK)


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