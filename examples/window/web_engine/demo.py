# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import setTheme, Theme, SubtitleLabel, setFont, SplitFluentWindow
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow.webengine import FramelessWebEngineView


class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("homeInterface")

        self.webView = FramelessWebEngineView(self)
        self.webView.load(QUrl("https://www.baidu.com/"))

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.vBoxLayout.addWidget(self.webView)


class Window(SplitFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = Widget(self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, "Home")

        # NOTE: enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.setMicaEffectEnabled(True)
    app.exec_()
