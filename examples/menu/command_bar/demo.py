# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import (FluentIcon, TransparentDropDownPushButton, RoundMenu, CommandBar, Action,
                            setTheme, Theme, setFont, CommandBarView, Flyout, FlyoutAnimationType,
                            ImageLabel, ToolButton, PushButton)
from qframelesswindow import FramelessWindow, StandardTitleBar


class Demo1(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo1{background: rgb(32, 32, 32)}')

        self.hBoxLayout = QHBoxLayout(self)
        self.commandBar = CommandBar(self)
        self.dropDownButton = self.createDropDownButton()

        self.hBoxLayout.addWidget(self.commandBar, 0)

        # change button style
        self.commandBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        # self.commandBar.setMenuDropDown(False)
        # self.commandBar.setButtonTight(True)
        # setFont(self.commandBar, 14)

        self.addButton(FluentIcon.ADD, 'Add')
        self.commandBar.addSeparator()

        self.commandBar.addAction(Action(FluentIcon.EDIT, 'Edit', triggered=self.onEdit, checkable=True))
        self.addButton(FluentIcon.COPY, 'Copy')
        self.addButton(FluentIcon.SHARE, 'Share')

        # add custom widget
        self.commandBar.addWidget(self.dropDownButton)

        # add hidden actions
        self.commandBar.addHiddenAction(Action(FluentIcon.SCROLL, 'Sort', triggered=lambda: print('排序')))
        self.commandBar.addHiddenAction(Action(FluentIcon.SETTING, 'Settings', shortcut='Ctrl+S'))

        self.resize(240, 40)
        self.setWindowTitle('Drag window')

    def addButton(self, icon, text):
        action = Action(icon, text, self)
        action.triggered.connect(lambda: print(text))
        self.commandBar.addAction(action)

    def onEdit(self, isChecked):
        print('Enter edit mode' if isChecked else 'Exit edit mode')

    def createDropDownButton(self):
        button = TransparentDropDownPushButton('Menu', self, FluentIcon.MENU)
        button.setFixedHeight(34)
        setFont(button, 12)

        menu = RoundMenu(parent=self)
        menu.addActions([
            Action(FluentIcon.COPY, 'Copy'),
            Action(FluentIcon.CUT, 'Cut'),
            Action(FluentIcon.PASTE, 'Paste'),
            Action(FluentIcon.CANCEL, 'Cancel'),
            Action('Select all'),
        ])
        button.setMenu(menu)
        return button


class Demo2(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))
        self.vBoxLayout = QHBoxLayout(self)
        self.imageLabel = ImageLabel('resource/pink_memory.jpg')

        self.imageLabel.scaledToWidth(380)
        self.imageLabel.clicked.connect(self.showCommandBar)
        self.vBoxLayout.addWidget(self.imageLabel)

        self.vBoxLayout.setContentsMargins(0, 80, 0, 0)
        self.setStyleSheet('Demo2{background: white}')
        self.setWindowTitle('Click Image 👇️🥵')
        self.setWindowIcon(QIcon(":/qfluentwidgets/images/logo.png"))

    def showCommandBar(self):
        view = CommandBarView(self)

        view.addAction(Action(FluentIcon.SHARE, 'Share'))
        view.addAction(Action(FluentIcon.SAVE, 'Save'))
        view.addAction(Action(FluentIcon.DELETE, 'Delete'))

        view.addHiddenAction(Action(FluentIcon.APPLICATION, 'App', shortcut='Ctrl+A'))
        view.addHiddenAction(Action(FluentIcon.SETTING, 'Settings', shortcut='Ctrl+S'))
        view.resizeToSuitableWidth()

        Flyout.make(view, self.imageLabel, self, FlyoutAnimationType.FADE_IN)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = Demo1()
    w1.show()
    w2 = Demo2()
    w2.show()
    app.exec()
