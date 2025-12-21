# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from qfluentwidgets import FluentWidget, toggleTheme, PushButton
from qfluentwidgets import FluentIcon as FIF



class Window(FluentWidget):

    def __init__(self):
        super().__init__()
        self.button = PushButton(FIF.CONSTRACT, 'Toggle theme', self)
        self.vBoxLayout = QVBoxLayout(self)

        # disable mica effect in Win11
        # self.setMicaEffectEnabled(False)

        # customize background color
        # self.setCustomBackgroundColor(Qt.red, Qt.blue)

        # toggle theme when the button is clicked
        self.button.clicked.connect(toggleTheme)

        # leave some space for title bar
        self.vBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.vBoxLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignCenter)

        self.initWindow()

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
