# coding:utf-8
import sys

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from qfluentwidgets import (Action, Action, DropDownPushButton, DropDownToolButton, PushButton, PrimaryPushButton,
                            HyperlinkButton, setTheme, Theme, ToolButton, ToggleButton, RoundMenu,
                            SplitPushButton, SplitToolButton)
from qfluentwidgets import FluentIcon as FIF


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)

        # tool button
        self.toolButton = ToolButton(FIF.SETTING, self)

        # change the size of tool button
        # self.toolButton.resize(50, 50)
        # self.toolButton.setIconSize(QSize(30, 30))

        # push button
        self.pushButton1 = PushButton('Standard push button')
        self.pushButton2 = PushButton('Standard push button with icon', self, FIF.FOLDER)

        # primary color button
        self.primaryButton1 = PrimaryPushButton('Accent style button', self)
        self.primaryButton2 = PrimaryPushButton('Accent style button with icon', self, FIF.UPDATE)

        # toggle button
        self.toggleButton = ToggleButton('Toggle Button', self, FIF.SEND)

        # drop down button
        self.dropDownPushButton = DropDownPushButton('Email', self, FIF.MAIL)
        self.dropDownToolButton = DropDownToolButton(FIF.MAIL, self)
        self.menu = RoundMenu(parent=self)
        self.menu.addAction(Action(FIF.SEND_FILL, 'Send'))
        self.menu.addAction(QAction(FIF.SAVE.icon(), 'Save'))
        self.dropDownPushButton.setMenu(self.menu)
        self.dropDownToolButton.setMenu(self.menu)

        # split button
        self.splitPushButton = SplitPushButton('Split push button', self, FIF.GITHUB)
        self.splitToolButton = SplitToolButton(FIF.GITHUB, self)
        self.splitMenu = RoundMenu(parent=self)
        self.splitMenu.addAction(Action(FIF.BASKETBALL, 'Basketball'))
        self.splitMenu.addAction(Action(FIF.ALBUM, 'Sing'))
        self.splitMenu.addAction(Action(FIF.MUSIC, 'Music'))
        self.splitPushButton.setFlyout(self.splitMenu)
        self.splitToolButton.setFlyout(self.splitMenu)

        # hyperlink button
        self.hyperlinkButton = HyperlinkButton(
            url='https://github.com/zhiyiYo/PyQt-Fluent-Widgets',
            text='Hyper link button',
            parent=self
        )

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.toolButton, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.pushButton1, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.pushButton2, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.primaryButton1, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.primaryButton2, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.toggleButton, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.dropDownPushButton, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.dropDownToolButton, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.splitPushButton, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.splitToolButton, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.hyperlinkButton, 0, Qt.AlignCenter)
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)

        self.resize(500, 600)
        self.setStyleSheet('Demo{background:white}')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()