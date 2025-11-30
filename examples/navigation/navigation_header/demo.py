# coding: utf-8
import sys
#from pathlib import Path
#sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QStackedWidget, QFrame
from qfluentwidgets import NavigationInterface, NavigationItemPosition, FluentIcon as FIF


class DemoInterface(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setObjectName(text.replace(' ', '-'))


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Navigation Header Demo')
        self.resize(900, 600)

        # layout
        self.hBox = QHBoxLayout(self)
        self.hBox.setContentsMargins(0, 0, 0, 0)
        self.hBox.setSpacing(0)

        # navigation
        self.navigationInterface = NavigationInterface(self)
        self.stackedWidget = QStackedWidget(self)

        # interfaces
        self.interfaces = {}
        self.initNavigation()

        # add to layout
        self.hBox.addWidget(self.navigationInterface)
        self.hBox.addWidget(self.stackedWidget)
        self.hBox.setStretchFactor(self.stackedWidget, 1)

    def initNavigation(self):
        # home
        self.addInterface('home', FIF.HOME, 'Home')
        self.navigationInterface.addSeparator()

        # basic group
        self.navigationInterface.addItemHeader('Basic Input', NavigationItemPosition.SCROLL)
        self.addInterface('button', FIF.CHECKBOX, 'Button', NavigationItemPosition.SCROLL)
        self.addInterface('input', FIF.EDIT, 'Input', NavigationItemPosition.SCROLL)

        # data group
        self.navigationInterface.addItemHeader('Data', NavigationItemPosition.SCROLL)
        self.addInterface('table', FIF.DOCUMENT, 'Table', NavigationItemPosition.SCROLL)
        self.addInterface('list', FIF.MENU, 'List', NavigationItemPosition.SCROLL)

        # settings
        self.addInterface('settings', FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        # default
        self.stackedWidget.setCurrentIndex(0)
        self.navigationInterface.setCurrentItem('home')

        self.navigationInterface.setUpdateIndicatorPosOnCollapseFinished(True)

    def addInterface(self, routeKey: str, icon, text: str, position=NavigationItemPosition.TOP):
        interface = DemoInterface(text, self)
        self.interfaces[routeKey] = interface
        self.stackedWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=routeKey,
            icon=icon,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(interface),
            position=position
        )


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
