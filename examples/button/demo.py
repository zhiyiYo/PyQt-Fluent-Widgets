# coding:utf-8
import sys

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout
from qfluentwidgets import (Action, Action, DropDownPushButton, DropDownToolButton, PushButton, PrimaryPushButton,
                            HyperlinkButton, setTheme, Theme, ToolButton, ToggleButton, RoundMenu,
                            SplitPushButton, SplitToolButton, PrimaryToolButton, PrimarySplitPushButton,
                            PrimarySplitToolButton, PrimaryDropDownPushButton, PrimaryDropDownToolButton)
from qfluentwidgets import FluentIcon as FIF


class ToolButtonDemo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet("ToolButtonDemo{background: white}")

        self.menu = RoundMenu(parent=self)
        self.menu.addAction(QAction(FIF.SEND_FILL.icon(), 'Send'))
        self.menu.addAction(QAction(FIF.SAVE.icon(), 'Save'))

        # tool button
        self.toolButton = ToolButton(FIF.SETTING, self)

        # change the size of tool button
        # self.toolButton.resize(50, 50)
        # self.toolButton.setIconSize(QSize(30, 30))

        # drop down tool button
        self.dropDownToolButton = DropDownToolButton(FIF.MAIL, self)
        self.dropDownToolButton.setMenu(self.menu)

        # split tool button
        self.splitToolButton = SplitToolButton(FIF.GITHUB, self)
        self.splitToolButton.setFlyout(self.menu)

        # primary color tool button
        self.primaryToolButton = PrimaryToolButton(FIF.SETTING, self)

        # primary color drop down tool button
        self.primaryDropDownToolButton = PrimaryDropDownToolButton(FIF.MAIL, self)
        self.primaryDropDownToolButton.setMenu(self.menu)

        # primary color split tool button
        self.primarySplitToolButton = PrimarySplitToolButton(FIF.GITHUB, self)
        self.primarySplitToolButton.setFlyout(self.menu)

        # add buttons to layout
        self.gridLayout = QGridLayout(self)
        self.gridLayout.addWidget(self.toolButton, 0, 0)
        self.gridLayout.addWidget(self.dropDownToolButton, 0, 1)
        self.gridLayout.addWidget(self.splitToolButton, 0, 2)
        self.gridLayout.addWidget(self.primaryToolButton, 1, 0)
        self.gridLayout.addWidget(self.primaryDropDownToolButton, 1, 1)
        self.gridLayout.addWidget(self.primarySplitToolButton, 1, 2)

        self.resize(300, 300)


class PushButtonDemo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet('PushButtonDemo{background:white}')

        self.menu = RoundMenu(parent=self)
        self.menu.addAction(Action(FIF.BASKETBALL, 'Basketball'))
        self.menu.addAction(Action(FIF.ALBUM, 'Sing'))
        self.menu.addAction(Action(FIF.MUSIC, 'Music'))

        # push button
        self.pushButton1 = PushButton('Standard push button')
        self.pushButton2 = PushButton('Standard push button with icon', self, FIF.FOLDER)

        # primary color push button
        self.primaryButton1 = PrimaryPushButton('Accent style button', self)
        self.primaryButton2 = PrimaryPushButton('Accent style button with icon', self, FIF.UPDATE)

        # toggle button
        self.toggleButton1 = ToggleButton('Toggle Button', self)
        self.toggleButton2 = ToggleButton('Toggle Button', self, FIF.SEND)

        # drop down push button
        self.dropDownPushButton1 = DropDownPushButton('Email', self)
        self.dropDownPushButton2 = DropDownPushButton('Email', self, FIF.MAIL)
        self.dropDownPushButton1.setMenu(self.menu)
        self.dropDownPushButton2.setMenu(self.menu)

        # primary color drop down push button
        self.primaryDropDownPushButton1 = PrimaryDropDownPushButton('Email', self)
        self.primaryDropDownPushButton2 = PrimaryDropDownPushButton('Email', self, FIF.MAIL)
        self.primaryDropDownPushButton1.setMenu(self.menu)
        self.primaryDropDownPushButton2.setMenu(self.menu)

        # split push button
        self.splitPushButton1 = SplitPushButton('Split push button', self)
        self.splitPushButton2 = SplitPushButton('Split push button', self, FIF.GITHUB)
        self.splitPushButton1.setFlyout(self.menu)
        self.splitPushButton2.setFlyout(self.menu)

        # primary split push button
        self.primarySplitPushButton1 = PrimarySplitPushButton('Split push button', self)
        self.primarySplitPushButton2 = PrimarySplitPushButton('Split push button', self, FIF.GITHUB)
        self.primarySplitPushButton1.setFlyout(self.menu)
        self.primarySplitPushButton2.setFlyout(self.menu)

        # hyperlink button
        self.hyperlinkButton = HyperlinkButton(
            url='https://github.com/zhiyiYo/PyQt-Fluent-Widgets',
            text='Hyper link button',
            parent=self
        )

        self.gridLayout = QGridLayout(self)
        self.gridLayout.addWidget(self.pushButton1, 0, 0)
        self.gridLayout.addWidget(self.pushButton2, 0, 1)
        self.gridLayout.addWidget(self.primaryButton1, 1, 0)
        self.gridLayout.addWidget(self.primaryButton2, 1, 1)
        self.gridLayout.addWidget(self.toggleButton1, 2, 0)
        self.gridLayout.addWidget(self.toggleButton2, 2, 1)
        self.gridLayout.addWidget(self.splitPushButton1, 3, 0)
        self.gridLayout.addWidget(self.splitPushButton2, 3, 1)
        self.gridLayout.addWidget(self.primarySplitPushButton1, 4, 0)
        self.gridLayout.addWidget(self.primarySplitPushButton2, 4, 1)
        self.gridLayout.addWidget(self.dropDownPushButton1, 5, 0, Qt.AlignLeft)
        self.gridLayout.addWidget(self.dropDownPushButton2, 5, 1, Qt.AlignLeft)
        self.gridLayout.addWidget(self.primaryDropDownPushButton1, 6, 0, Qt.AlignLeft)
        self.gridLayout.addWidget(self.primaryDropDownPushButton2, 6, 1, Qt.AlignLeft)
        self.gridLayout.addWidget(self.hyperlinkButton, 7, 0)

        self.resize(600, 600)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = ToolButtonDemo()
    w1.show()

    w2 = PushButtonDemo()
    w2.show()
    app.exec()