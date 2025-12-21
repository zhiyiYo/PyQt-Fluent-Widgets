# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition,
                            MessageBox, FluentWindow, SubtitleLabel, setFont)
from qfluentwidgets import FluentIcon as FIF


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(FluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = Widget('Home Interface', self)
        self.musicInterface = Widget('Music Interface', self)
        self.videoInterface = Widget('Video Interface', self)
        self.settingInterface = Widget('Setting Interface', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        # add user card with custom parameters
        self.userCard = self.navigationInterface.addUserCard(
            routeKey='userCard',
            avatar='resource/shoko.png',
            title='zhiyiYo',
            subtitle='shokokawaii@outlook.com',
            onClick=self.showMessageBox,
            position=NavigationItemPosition.TOP,
            aboveMenuButton=False  # place below the expand/collapse button
        )

        # customize user card (optional)
        # self.userCard.setTitleFontSize(15)
        # self.userCard.setSubtitleFontSize(11)
        # self.userCard.setAnimationDuration(300)

        # placement: set aboveMenuButton=True to place card above expand/collapse button
        # default: aboveMenuButton=False (card placed below menu button)

        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')
        self.addSubInterface(self.musicInterface, FIF.MUSIC, 'Music library')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.videoInterface, FIF.VIDEO, 'Video library')
        self.addSubInterface(self.settingInterface, FIF.SETTING,
                             'Settings', NavigationItemPosition.BOTTOM)

        self.navigationInterface.setUpdateIndicatorPosOnCollapseFinished(True)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('Navigation User Card')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def showMessageBox(self):
        w = MessageBox(
            'User Card',
            'This is a navigation user card that displays avatar, title and subtitle.\n\n'
            'Placement:\n'
            '• aboveMenuButton=True: Place above expand/collapse button\n'
            '• aboveMenuButton=False: Place below menu button (default)',
            self
        )
        w.exec_()


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
