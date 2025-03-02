# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import (ProgressRing, SpinBox, setTheme, Theme, IndeterminateProgressRing, setFont,
                            FluentThemeColor, ToggleToolButton, FluentIcon)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background: rgb(32, 32, 32)}')

        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout()

        self.button = ToggleToolButton(FluentIcon.PAUSE_BOLD, self)
        self.spinner = IndeterminateProgressRing(self)
        self.progressRing = ProgressRing(self)
        self.spinBox = SpinBox(self)

        self.progressRing.setValue(50)
        self.progressRing.setTextVisible(True)
        self.progressRing.setFixedSize(80, 80)

        # self.spinner.setFixedSize(50, 50)

        # change background color
        # self.progressRing.setCustomBackgroundColor(Qt.transparent, Qt.transparent)

        # change font
        # setFont(self.progressRing, fontSize=15)

        # change size
        # self.spinner.setFixedSize(50, 50)

        # change thickness
        # self.progressRing.setStrokeWidth(4)
        # self.spinner.setStrokeWidth(4)

        # change the color of bar
        # self.progressRing.setCustomBarColor(FluentThemeColor.DEFAULT_BLUE.color(), FluentThemeColor.GOLD.color())
        # self.spinner.setCustomBarColor(FluentThemeColor.DEFAULT_BLUE.color(), FluentThemeColor.GOLD.color())

        self.spinBox.setRange(0, 100)
        self.spinBox.setValue(50)
        self.spinBox.valueChanged.connect(self.progressRing.setValue)

        self.hBoxLayout.addWidget(self.progressRing, 0, Qt.AlignHCenter)
        self.hBoxLayout.addWidget(self.spinBox, 0, Qt.AlignHCenter)

        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.spinner, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.button, 0, Qt.AlignHCenter)
        self.resize(400, 400)

        self.button.clicked.connect(self.onButtonClicked)

    def onButtonClicked(self):
        if not self.progressRing.isPaused():
            self.progressRing.pause()
            self.button.setIcon(FluentIcon.PLAY_SOLID)
        else:
            self.progressRing.resume()
            self.button.setIcon(FluentIcon.PAUSE_BOLD)



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