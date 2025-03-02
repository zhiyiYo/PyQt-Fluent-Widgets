# coding:utf-8
import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from qfluentwidgets import IndeterminateProgressBar, ProgressBar, FluentThemeColor, ToggleToolButton, FluentIcon


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.vBoxLayout = QVBoxLayout(self)
        self.progressBar = ProgressBar(self)
        self.inProgressBar = IndeterminateProgressBar(self)
        self.button = ToggleToolButton(FluentIcon.PAUSE_BOLD, self)

        # change the color of bar
        # self.progressBar.setCustomBarColor(FluentThemeColor.DEFAULT_BLUE.color(), FluentThemeColor.GOLD.color())
        # self.inProgressBar.setCustomBarColor(FluentThemeColor.DEFAULT_BLUE.color(), FluentThemeColor.GOLD.color())

        self.progressBar.setValue(50)
        self.vBoxLayout.addWidget(self.progressBar)
        self.vBoxLayout.addWidget(self.inProgressBar)
        self.vBoxLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.resize(400, 400)

        self.button.clicked.connect(self.onButtonClicked)

    def onButtonClicked(self):
        if self.inProgressBar.isStarted():
            self.inProgressBar.pause()
            self.progressBar.pause()
            self.button.setIcon(FluentIcon.PLAY_SOLID)
        else:
            self.inProgressBar.resume()
            self.progressBar.resume()
            self.button.setIcon(FluentIcon.PAUSE_BOLD)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()