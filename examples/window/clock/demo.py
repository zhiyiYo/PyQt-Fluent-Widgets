# coding:utf-8
import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme,
                            NavigationAvatarWidget,  SplitFluentWindow, FluentTranslator)
from qfluentwidgets import FluentIcon as FIF

import resource_rc
from view.focus_interface import FocusInterface
from view.stop_watch_interface import StopWatchInterface


class Window(SplitFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.focusInterface = FocusInterface(self)
        self.stopWatchInterface = StopWatchInterface(self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        # add sub interface
        self.addSubInterface(self.focusInterface, FIF.RINGER, '专注时段')
        self.addSubInterface(self.stopWatchInterface, FIF.STOP_WATCH, '秒表')

        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('zhiyiYo', 'resource/images/shoko.png'),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM,
        )
        self.navigationInterface.addItem(
            routeKey='settingInterface',
            icon=FIF.SETTING,
            text='设置',
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setExpandWidth(280)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def showMessageBox(self):
        w = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))


if __name__ == '__main__':
    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)

    # install translator
    translator = FluentTranslator()
    app.installTranslator(translator)

    w = Window()
    w.show()
    app.exec()
