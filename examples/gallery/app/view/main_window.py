# coding: utf-8
from typing import List
from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, MessageBox,
                            isDarkTheme, PopUpAniStackedWidget)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow

from .title_bar import CustomTitleBar
from .gallery_interface import GalleryInterface
from .home_interface import HomeInterface
from .basic_input_interface import BasicInputInterface
from .dialog_interface import DialogInterface
from .layout_interface import LayoutInterface
from .icon_interface import IconInterface
from .material_interface import MaterialInterface
from .menu_interface import MenuInterface
from .scroll_interface import ScrollInterface
from .status_info_interface import StatusInfoInterface
from .setting_interface import SettingInterface, cfg
from .text_interface import TextInterface
from .view_interface import ViewInterface
from ..components.avatar_widget import AvatarWidget
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet
from ..common import resource


class StackedWidget(QFrame):
    """ Stacked widget """

    currentWidgetChanged = pyqtSignal(QWidget)

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

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def add_sub_interface(self, sub, key, icon, position=NavigationItemPosition.TOP):
        self.stackWidget.addWidget(sub)
        self.navigationInterface.addItem(
            routeKey=key,
            icon=icon if icon else FIF.INFO,
            text=self.tr(key),
            onClick=lambda t: self.switchTo(sub, t),
            position=position
        )

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

        self.add_sub_interface(HomeInterface(self), 'Home', FIF.HOME, )
        self.add_sub_interface(IconInterface(self), 'Icons', Icon.EMOJI_TAB_SYMBOLS, )

        self.navigationInterface.addSeparator()

        self.add_sub_interface(BasicInputInterface(self), 'Basic input', Icon.CHECKBOX,
                               position=NavigationItemPosition.SCROLL)
        self.add_sub_interface(DialogInterface(self), 'Dialogs', FIF.MESSAGE, position=NavigationItemPosition.SCROLL)
        self.add_sub_interface(LayoutInterface(self), 'Layout', FIF.LAYOUT, position=NavigationItemPosition.SCROLL)
        self.add_sub_interface(MenuInterface(self), 'Menus', Icon.MENU, position=NavigationItemPosition.SCROLL)
        self.add_sub_interface(MaterialInterface(self), 'Material', FIF.PALETTE, position=NavigationItemPosition.SCROLL)
        self.add_sub_interface(ScrollInterface(self), 'Scrolling', FIF.SCROLL, position=NavigationItemPosition.SCROLL)
        self.add_sub_interface(StatusInfoInterface(self), 'Status & info', FIF.CHAT,
                               position=NavigationItemPosition.SCROLL)
        self.add_sub_interface(TextInterface(self), 'Text', Icon.TEXT, position=NavigationItemPosition.SCROLL)
        self.add_sub_interface(ViewInterface(self), 'View', Icon.GRID, position=NavigationItemPosition.SCROLL)

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=AvatarWidget(':/gallery/images/shoko.png'),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM
        )
        self.add_sub_interface(SettingInterface(self), 'Setting', FIF.SETTING, position=NavigationItemPosition.BOTTOM)

        # !IMPORTANT: don't forget to set the default route key if you enable the return button
        self.navigationInterface.setDefaultRouteKey('Home')

        # TODO: this part seems to useless, please check
        # self.stackWidget.currentWidgetChanged.connect(
        #     lambda w: self.navigationInterface.setCurrentItem(w.objectName()))
        # self.navigationInterface.setCurrentItem('Home')
        # self.stackWidget.setCurrentIndex(0)

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        StyleSheet.MAIN_WINDOW.apply(self)

    def switchTo(self, widget, triggerByUser=True):
        self.stackWidget.setCurrentWidget(widget, not triggerByUser)

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width() - 46, self.titleBar.height())

    def showMessageBox(self):
        w = MessageBox(
            self.tr('This is a help message'),
            self.tr(
                'You clicked a customized navigation widget. You can add more custom widgets by calling `NavigationInterface.addWidget()` 😉'),
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
