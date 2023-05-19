# coding:utf-8
import sys
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont
from PyQt6.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor, qrouter)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class AvatarWidget(NavigationWidget):
    """ Avatar widget """

    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.avatar = QImage('resource/shoko.png').scaled(
            24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.SmoothPixmapTransform | QPainter.RenderHint.Antialiasing)

        painter.setPen(Qt.PenStyle.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)

        # draw background
        if self.isEnter:
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        # draw avatar
        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)

        if not self.isCompacted:
            painter.setPen(Qt.GlobalColor.white if isDarkTheme() else Qt.GlobalColor.black)
            font = QFont('Segoe UI')
            font.setPixelSize(14)
            painter.setFont(font)
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignmentFlag.AlignVCenter, 'zhiyiYo')


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))

        # use dark theme mode
        # setTheme(Theme.DARK)

        # change the theme color
        # setThemeColor('#0078d4')

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.stackWidget = QStackedWidget(self)

        # create sub interface
        self.searchInterface = Widget('Search Interface', self)
        self.musicInterface = Widget('Music Interface', self)
        self.videoInterface = Widget('Video Interface', self)
        self.folderInterface = Widget('Folder Interface', self)
        self.settingInterface = Widget('Setting Interface', self)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.addSubInterface(self.searchInterface, FIF.SEARCH, 'Search')
        self.addSubInterface(self.musicInterface, FIF.MUSIC, 'Music library')
        self.addSubInterface(self.videoInterface, FIF.VIDEO, 'Video library')

        self.navigationInterface.addSeparator()

        # add navigation items to scroll area
        self.addSubInterface(self.folderInterface, FIF.FOLDER, 'Folder library', NavigationItemPosition.SCROLL)
        # for i in range(1, 21):
        #     self.navigationInterface.addItem(
        #         f'folder{i}',
        #         FIF.FOLDER,
        #         f'Folder {i}',
        #         lambda: print('Folder clicked'),
        #         position=NavigationItemPosition.SCROLL
        #     )

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=AvatarWidget(),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM
        )

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        #!IMPORTANT: don't forget to set the default route key if you enable the return button
        # qrouter.setDefaultRouteKey(self.stackWidget, self.musicInterface.objectName())

        # set the maximum width
        # self.navigationInterface.setExpandWidth(300)

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(1)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.titleBar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.setQss()

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text
        )

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/{color}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())
        
        #!IMPORTANT: This line of code needs to be uncommented if the return button is enabled
        # qrouter.push(self.stackWidget, widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            'This is a help message',
            'You clicked a customized navigation widget. You can add more custom widgets by calling `NavigationInterface.addWidget()` 😉',
            self
        )
        w.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
