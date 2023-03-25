# coding: utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QStackedWidget, QHBoxLayout, QFrame, QWidget

from qfluentwidgets import (NavigationInterface, NavigationItemPostion, MessageBox,
                            isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow

from .title_bar import CustomTitleBar
from .setting_interface import SettingInterface, cfg
from .basic_input_interface import BasicInputInterface
from .dialog_interface import DialogInterface
from ..components.avatar_widget import AvatarWidget
from ..common.icon import Icon


class StackedWidget(QFrame):
    """ Stacked widget """

    currentWidgetChanged = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = QStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(
            lambda i: self.currentWidgetChanged.emit(self.view.widget(i)))

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def setCurrentWidget(self, widget):
        self.view.setCurrentWidget(widget)

    def setCurrentIndex(self, index):
        self.view.setCurrentIndex(index)


class MainWindow(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        self.widgetLayout = QHBoxLayout()

        self.stackWidget = StackedWidget(self)
        self.navigationInterface = NavigationInterface(self, True, True)

        # create sub interface
        self.basicInputInterface = BasicInputInterface(self)
        self.dialogInterface = DialogInterface(self)
        self.settingInterface = SettingInterface(self)

        self.stackWidget.addWidget(self.basicInputInterface)
        self.stackWidget.addWidget(self.dialogInterface)
        self.stackWidget.addWidget(self.settingInterface)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addLayout(self.widgetLayout)
        self.hBoxLayout.setStretchFactor(self.widgetLayout, 1)

        self.widgetLayout.addWidget(self.stackWidget)
        self.widgetLayout.setContentsMargins(0, 48, 0, 0)

        self.navigationInterface.displayModeChanged.connect(
            self.titleBar.raise_)
        self.titleBar.raise_()

    def initNavigation(self):
        self.basicInputInterface.setObjectName('basicInterface')
        self.dialogInterface.setObjectName('dialogInterface')
        self.settingInterface.setObjectName('settingsInterface')

        self.navigationInterface.addItem(
            routeKey='Home',
            icon=Icon.HOME,
            text=self.tr('Home'),
            onClick=print
        )
        self.navigationInterface.addSeparator()

        self.navigationInterface.addItem(
            routeKey=self.basicInputInterface.objectName(),
            icon=Icon.CHECKBOX,
            text=self.tr('Basic input'),
            onClick=lambda: self.switchTo(self.basicInputInterface),
            position=NavigationItemPostion.SCROLL
        )
        self.navigationInterface.addItem(
            routeKey=self.dialogInterface.objectName(),
            icon=Icon.MESSAGE,
            text=self.tr('Dialogs'),
            onClick=lambda: self.switchTo(self.dialogInterface),
            position=NavigationItemPostion.SCROLL
        )
        self.navigationInterface.addItem(
            routeKey='Status&info',
            icon=Icon.LAYOUT,
            text=self.tr('Layout'),
            onClick=print,
            position=NavigationItemPostion.SCROLL
        )
        self.navigationInterface.addItem(
            routeKey='Menus',
            icon=Icon.MENU,
            text=self.tr('Menus'),
            onClick=print,
            position=NavigationItemPostion.SCROLL
        )
        self.navigationInterface.addItem(
            routeKey='Material',
            icon=FIF.PALETTE,
            text=self.tr('Material'),
            onClick=print,
            position=NavigationItemPostion.SCROLL
        )
        self.navigationInterface.addItem(
            routeKey='Layout',
            icon=Icon.CHAT,
            text=self.tr('Status & info'),
            onClick=print,
            position=NavigationItemPostion.SCROLL
        )

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=AvatarWidget('app/resource/images/shoko.png'),
            onClick=self.showMessageBox,
            position=NavigationItemPostion.BOTTOM
        )

        self.navigationInterface.addItem(
            routeKey=self.settingInterface.objectName(),
            icon=FIF.SETTING,
            text='Settings',
            onClick=lambda: self.switchTo(self.settingInterface),
            position=NavigationItemPostion.BOTTOM
        )

        #!IMPORTANT: don't forget to set the default route key if you enable the return button
        self.navigationInterface.setDefaultRouteKey(
            self.basicInputInterface.objectName())

        self.stackWidget.currentWidgetChanged.connect(
            lambda w: self.navigationInterface.setCurrentItem(w.objectName()))
        self.navigationInterface.setCurrentItem(self.basicInputInterface.objectName())
        self.stackWidget.setCurrentIndex(0)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('app/resource/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        cfg.themeChanged.connect(self.setQss)
        self.setQss()

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'app/resource/qss/{color}/main_window.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width()-46, self.titleBar.height())

    def showMessageBox(self):
        w = MessageBox(
            'This is a help message',
            'You clicked a customized navigation widget. You can add more custom widgets by calling `NavigationInterface.addWidget()` 😉',
            self
        )
        w.exec()
