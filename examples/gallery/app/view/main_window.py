# coding: utf-8
from typing import List
from PySide6.QtCore import Qt, Signal, QEasingCurve
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget

from qfluentwidgets import (NavigationInterface, NavigationItemPostion, MessageBox,
                            isDarkTheme, PopUpAniStackedWidget)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow

from .title_bar import CustomTitleBar
from .gallery_interface import GalleryInterface
from .home_interface import HomeInterface
from .basic_input_interface import BasicInputInterface
from .dialog_interface import DialogInterface
from .layout_interface import LayoutInterface
from .material_interface import MaterialInterface
from .menu_interface import MenuInterface
from .scroll_interface import ScrollInterface
from .status_info_interface import StatusInfoInterface
from .setting_interface import SettingInterface, cfg
from ..components.avatar_widget import AvatarWidget
from ..common.icon import Icon
from ..common.signal_bus import signalBus


class StackedWidget(QFrame):
    """ Stacked widget """

    currentWidgetChanged = Signal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(
            lambda i: self.currentWidgetChanged.emit(self.view.widget(i)))

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def setCurrentWidget(self, widget, popOut=False):
        widget.verticalScrollBar().setValue(0)
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.InQuad)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class MainWindow(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        self.widgetLayout = QHBoxLayout()

        self.stackWidget = StackedWidget(self)
        self.navigationInterface = NavigationInterface(self, True, True)

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.basicInputInterface = BasicInputInterface(self)
        self.dialogInterface = DialogInterface(self)
        self.layoutInterface = LayoutInterface(self)
        self.menuInterface = MenuInterface(self)
        self.materialInterface = MaterialInterface(self)
        self.scrollInterface = ScrollInterface(self)
        self.statusInfoInterface = StatusInfoInterface(self)
        self.settingInterface = SettingInterface(self)

        self.stackWidget.addWidget(self.homeInterface)
        self.stackWidget.addWidget(self.basicInputInterface)
        self.stackWidget.addWidget(self.dialogInterface)
        self.stackWidget.addWidget(self.layoutInterface)
        self.stackWidget.addWidget(self.materialInterface)
        self.stackWidget.addWidget(self.menuInterface)
        self.stackWidget.addWidget(self.scrollInterface)
        self.stackWidget.addWidget(self.statusInfoInterface)
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

        signalBus.switchToSampleCard.connect(self.switchToSample)

        self.navigationInterface.displayModeChanged.connect(
            self.titleBar.raise_)
        self.titleBar.raise_()

    def initNavigation(self):
        self.homeInterface.setObjectName('homeInterface')
        self.basicInputInterface.setObjectName('basicInputInterface')
        self.dialogInterface.setObjectName('dialogInterface')
        self.layoutInterface.setObjectName('layoutInterface')
        self.menuInterface.setObjectName('menuInterface')
        self.materialInterface.setObjectName('materialInterface')
        self.statusInfoInterface.setObjectName('statusInfoInterface')
        self.scrollInterface.setObjectName('scrollInterface')
        self.settingInterface.setObjectName('settingsInterface')

        # add navigation items
        self.navigationInterface.addItem(
            routeKey=self.homeInterface.objectName(),
            icon=Icon.HOME,
            text=self.tr('Home'),
            onClick=lambda t: self.switchTo(self.homeInterface, t)
        )
        self.navigationInterface.addSeparator()

        self.navigationInterface.addItem(
            routeKey=self.basicInputInterface.objectName(),
            icon=Icon.CHECKBOX,
            text=self.tr('Basic input'),
            onClick=lambda t: self.switchTo(self.basicInputInterface, t),
            position=NavigationItemPostion.SCROLL
        )
        self.navigationInterface.addItem(
            routeKey=self.dialogInterface.objectName(),
            icon=Icon.MESSAGE,
            text=self.tr('Dialogs'),
            onClick=lambda t: self.switchTo(self.dialogInterface, t),
            position=NavigationItemPostion.SCROLL
        )
        self.navigationInterface.addItem(
            routeKey=self.layoutInterface.objectName(),
            icon=Icon.LAYOUT,
            text=self.tr('Layout'),
            onClick=lambda t: self.switchTo(self.layoutInterface, t),
            position=NavigationItemPostion.SCROLL
        )
        self.navigationInterface.addItem(
            routeKey=self.materialInterface.objectName(),
            icon=FIF.PALETTE,
            text=self.tr('Material'),
            onClick=lambda t: self.switchTo(self.materialInterface, t),
            position=NavigationItemPostion.SCROLL
        )
        self.navigationInterface.addItem(
            routeKey=self.menuInterface.objectName(),
            icon=Icon.MENU,
            text=self.tr('Menus'),
            onClick=lambda t: self.switchTo(self.menuInterface, t),
            position=NavigationItemPostion.SCROLL
        )
        self.navigationInterface.addItem(
            routeKey=self.scrollInterface.objectName(),
            icon=Icon.SCROLL,
            text=self.tr('Scrolling'),
            onClick=lambda t: self.switchTo(self.scrollInterface, t),
            position=NavigationItemPostion.SCROLL
        )
        self.navigationInterface.addItem(
            routeKey=self.statusInfoInterface.objectName(),
            icon=Icon.CHAT,
            text=self.tr('Status & info'),
            onClick=lambda t: self.switchTo(self.statusInfoInterface, t),
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
            onClick=lambda t: self.switchTo(self.settingInterface, t),
            position=NavigationItemPostion.BOTTOM
        )

        #!IMPORTANT: don't forget to set the default route key if you enable the return button
        self.navigationInterface.setDefaultRouteKey(
            self.homeInterface.objectName())

        self.stackWidget.currentWidgetChanged.connect(
            lambda w: self.navigationInterface.setCurrentItem(w.objectName()))
        self.navigationInterface.setCurrentItem(
            self.homeInterface.objectName())
        self.stackWidget.setCurrentIndex(0)

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(580)
        self.setWindowIcon(QIcon('app/resource/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        cfg.themeChanged.connect(self.setQss)
        self.setQss()

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'app/resource/qss/{color}/main_window.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget, triggerByUser=True):
        self.stackWidget.setCurrentWidget(widget, not triggerByUser)

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width()-46, self.titleBar.height())

    def showMessageBox(self):
        w = MessageBox(
            self.tr('This is a help message'),
            self.tr('You clicked a customized navigation widget. You can add more custom widgets by calling `NavigationInterface.addWidget()` 😉'),
            self
        )
        w.exec()

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackWidget.setCurrentWidget(w)
                w.scrollToCard(index)
