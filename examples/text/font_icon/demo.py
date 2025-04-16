# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QAction, QLabel

from qfluentwidgets import FluentFontIconBase, Theme, PushButton, SwitchButton, TogglePushButton, toggleTheme, HyperlinkButton


class PhotoFontIcon(FluentFontIconBase):
    """ Custom icon font icon """

    def path(self, theme=Theme.AUTO):
        return "font/PhotosIcons.ttf"

    def iconNameMapPath(self):
        """ Not necessary, but if you want to use `fromName`, you have to implement this method """
        return "font/PhotoIcons.json"


class MediaPlayerFontIcon(FluentFontIconBase):
    """ Custom icon font icon """

    def path(self, theme=Theme.AUTO):
        return "font/MediaPlayerIcons.ttf"


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.themeButton = SwitchButton(self)

        self.button1 = PushButton(PhotoFontIcon("\ue77b"), "Default")
        self.button2 = PushButton(PhotoFontIcon.fromName("cloud").colored("#275EFF", Qt.GlobalColor.darkCyan), "Custom")
        self.button3 = TogglePushButton(PhotoFontIcon.fromName("smile"), "Toggle")
        self.button4 = HyperlinkButton(MediaPlayerFontIcon("\uf414"), "http://qfluentwidgets.com", "Hyperlink")
        self.hBoxLayout = QHBoxLayout(self)

        self.hBoxLayout.addWidget(self.button1)
        self.hBoxLayout.addWidget(self.button2)
        self.hBoxLayout.addWidget(self.button3)
        self.hBoxLayout.addWidget(self.button4)

        self.resize(500, 500)
        self.themeButton.move(200, 50)
        self.themeButton.setOnText("Dark")
        self.themeButton.setOffText("Light")

        self.themeButton.checkedChanged.connect(self.toggleTheme)

    def toggleTheme(self, isCheked):
        toggleTheme()
        if isCheked:
            self.setStyleSheet("Demo{background:rgb(32,32,32)}")
        else:
            self.setStyleSheet("Demo{background:rgb(242,242,242)}")



if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()