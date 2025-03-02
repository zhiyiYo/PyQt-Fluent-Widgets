# coding:utf-8
import sys

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout
from qfluentwidgets import (Action, Action, DropDownPushButton, DropDownToolButton, PushButton, PrimaryPushButton,
                            HyperlinkButton, setTheme, Theme, ToolButton, ToggleButton, RoundMenu,
                            SplitPushButton, SplitToolButton, PrimaryToolButton, PrimarySplitPushButton,
                            PrimarySplitToolButton, PrimaryDropDownPushButton, PrimaryDropDownToolButton,
                            TogglePushButton, ToggleToolButton, TransparentPushButton, TransparentToolButton,
                            TransparentToggleToolButton, TransparentTogglePushButton, TransparentDropDownToolButton,
                            TransparentDropDownPushButton, PillPushButton, PillToolButton, setCustomStyleSheet,
                            CustomStyleSheet)
from qfluentwidgets import FluentIcon as FIF


class ButtonView(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet("ButtonView{background: rgb(255,255,255)}")



class ToolButtonDemo(ButtonView):

    def __init__(self):
        super().__init__()

        self.menu = RoundMenu(parent=self)
        self.menu.addAction(QAction(FIF.SEND_FILL.icon(), 'Send'))
        self.menu.addAction(QAction(FIF.SAVE.icon(), 'Save'))

        # tool button
        self.toolButton = ToolButton(FIF.SETTING, self)

        # !IMPORTANT: add custom style sheet
        # lightQss = 'ToolButton{border-radius: 9px}'
        # darkQss = 'ToolButton{border-radius: 0px; background: red}'
        # setCustomStyleSheet(self.toolButton, lightQss, darkQss)

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

        # toggle tool button
        self.toggleToolButton = ToggleToolButton(FIF.SETTING, self)
        self.toggleToolButton.toggled.connect(lambda: print('Toggled'))
        self.toggleToolButton.toggle()

        # transparent toggle tool button
        self.transparentToggleToolButton = TransparentToggleToolButton(FIF.GITHUB, self)

        # transparent tool button
        self.tranparentToolButton = TransparentToolButton(FIF.MAIL, self)

        # transparent drop down tool button
        self.transparentDropDownToolButton = TransparentDropDownToolButton(FIF.MAIL, self)
        self.transparentDropDownToolButton.setMenu(self.menu)

        # pill tool button
        self.pillToolButton1 = PillToolButton(FIF.CALENDAR, self)
        self.pillToolButton2 = PillToolButton(FIF.CALENDAR, self)
        self.pillToolButton3 = PillToolButton(FIF.CALENDAR, self)
        self.pillToolButton2.setDisabled(True)
        self.pillToolButton3.setChecked(True)
        self.pillToolButton3.setDisabled(True)

        # add buttons to layout
        self.gridLayout = QGridLayout(self)
        self.gridLayout.addWidget(self.toolButton, 0, 0)
        self.gridLayout.addWidget(self.dropDownToolButton, 0, 1)
        self.gridLayout.addWidget(self.splitToolButton, 0, 2)
        self.gridLayout.addWidget(self.primaryToolButton, 1, 0)
        self.gridLayout.addWidget(self.primaryDropDownToolButton, 1, 1)
        self.gridLayout.addWidget(self.primarySplitToolButton, 1, 2)
        self.gridLayout.addWidget(self.toggleToolButton, 2, 0)
        self.gridLayout.addWidget(self.transparentToggleToolButton, 2, 1)
        self.gridLayout.addWidget(self.tranparentToolButton, 3, 0)
        self.gridLayout.addWidget(self.transparentDropDownToolButton, 3, 1)
        self.gridLayout.addWidget(self.pillToolButton1, 4, 0)
        self.gridLayout.addWidget(self.pillToolButton2, 4, 1)
        self.gridLayout.addWidget(self.pillToolButton3, 4, 2)

        self.resize(300, 300)


class PushButtonDemo(ButtonView):

    def __init__(self):
        super().__init__()

        self.menu = RoundMenu(parent=self)
        self.menu.addAction(Action(FIF.BASKETBALL, 'Basketball'))
        self.menu.addAction(Action(FIF.ALBUM, 'Sing'))
        self.menu.addAction(Action(FIF.MUSIC, 'Music'))

        # push button
        self.pushButton1 = PushButton('Standard push button')
        self.pushButton2 = PushButton(FIF.FOLDER, 'Standard push button with icon', self)

        # primary color push button
        self.primaryButton1 = PrimaryPushButton('Accent style button', self)
        self.primaryButton2 = PrimaryPushButton(FIF.UPDATE, 'Accent style button with icon', self)

        # transparent push button
        self.transparentPushButton1 = TransparentPushButton('Transparent push button', self)
        self.transparentPushButton2 = TransparentPushButton(FIF.BOOK_SHELF, 'Transparent push button', self)

        # toggle button
        self.toggleButton1 = TogglePushButton('Toggle push button', self)
        self.toggleButton2 = TogglePushButton(FIF.SEND, 'Toggle push button', self)

        # transparent toggle push button
        self.transparentTogglePushButton1 = TransparentTogglePushButton('Transparent toggle button', self)
        self.transparentTogglePushButton2 = TransparentTogglePushButton(FIF.BOOK_SHELF, 'Transparent toggle button', self)

        # drop down push button
        self.dropDownPushButton1 = DropDownPushButton('Email', self)
        self.dropDownPushButton2 = DropDownPushButton(FIF.MAIL, 'Email', self)
        self.dropDownPushButton1.setMenu(self.menu)
        self.dropDownPushButton2.setMenu(self.menu)

        # primary color drop down push button
        self.primaryDropDownPushButton1 = PrimaryDropDownPushButton('Email', self)
        self.primaryDropDownPushButton2 = PrimaryDropDownPushButton(FIF.MAIL, 'Email', self)
        self.primaryDropDownPushButton1.setMenu(self.menu)
        self.primaryDropDownPushButton2.setMenu(self.menu)

        # primary color drop down push button
        self.transparentDropDownPushButton1 = TransparentDropDownPushButton('Email', self)
        self.transparentDropDownPushButton2 = TransparentDropDownPushButton(FIF.MAIL, 'Email', self)
        self.transparentDropDownPushButton1.setMenu(self.menu)
        self.transparentDropDownPushButton2.setMenu(self.menu)

        # split push button
        self.splitPushButton1 = SplitPushButton('Split push button', self)
        self.splitPushButton2 = SplitPushButton(FIF.GITHUB, 'Split push button', self)
        self.splitPushButton1.setFlyout(self.menu)
        self.splitPushButton2.setFlyout(self.menu)
        # self.splitPushButton1.setDropIcon(FIF.SEND_FILL)
        # self.splitPushButton1.setDropIconSize(QSize(14, 14))

        # primary split push button
        self.primarySplitPushButton1 = PrimarySplitPushButton('Split push button', self)
        self.primarySplitPushButton2 = PrimarySplitPushButton(FIF.GITHUB, 'Split push button', self)
        self.primarySplitPushButton1.setFlyout(self.menu)
        self.primarySplitPushButton2.setFlyout(self.menu)
        # self.primarySplitPushButton1.setDropIcon(FIF.SEND_FILL)
        # self.primarySplitPushButton1.setDropIconSize(QSize(14, 14))

        # hyperlink button
        self.hyperlinkButton1 = HyperlinkButton(
            url='https://qfluentwidgets.com',
            text='Hyper link button',
            parent=self
        )
        self.hyperlinkButton2 = HyperlinkButton(
            url='https://qfluentwidgets.com',
            text='Hyper link button',
            parent=self,
            icon=FIF.LINK
        )

        # pill push button
        self.pillPushButton1 = PillPushButton('Pill Push Button', self)
        self.pillPushButton2 = PillPushButton(FIF.CALENDAR, 'Pill Push Button', self)

        self.gridLayout = QGridLayout(self)
        self.gridLayout.addWidget(self.pushButton1, 0, 0)
        self.gridLayout.addWidget(self.pushButton2, 0, 1)
        self.gridLayout.addWidget(self.primaryButton1, 1, 0)
        self.gridLayout.addWidget(self.primaryButton2, 1, 1)
        self.gridLayout.addWidget(self.transparentPushButton1, 2, 0)
        self.gridLayout.addWidget(self.transparentPushButton2, 2, 1)

        self.gridLayout.addWidget(self.toggleButton1, 3, 0)
        self.gridLayout.addWidget(self.toggleButton2, 3, 1)
        self.gridLayout.addWidget(self.transparentTogglePushButton1, 4, 0)
        self.gridLayout.addWidget(self.transparentTogglePushButton2, 4, 1)

        self.gridLayout.addWidget(self.splitPushButton1, 5, 0)
        self.gridLayout.addWidget(self.splitPushButton2, 5, 1)
        self.gridLayout.addWidget(self.primarySplitPushButton1, 6, 0)
        self.gridLayout.addWidget(self.primarySplitPushButton2, 6, 1)

        self.gridLayout.addWidget(self.dropDownPushButton1, 7, 0, Qt.AlignLeft)
        self.gridLayout.addWidget(self.dropDownPushButton2, 7, 1, Qt.AlignLeft)
        self.gridLayout.addWidget(self.primaryDropDownPushButton1, 8, 0, Qt.AlignLeft)
        self.gridLayout.addWidget(self.primaryDropDownPushButton2, 8, 1, Qt.AlignLeft)
        self.gridLayout.addWidget(self.transparentDropDownPushButton1, 9, 0, Qt.AlignLeft)
        self.gridLayout.addWidget(self.transparentDropDownPushButton2, 9, 1, Qt.AlignLeft)

        self.gridLayout.addWidget(self.pillPushButton1, 10, 0, Qt.AlignLeft)
        self.gridLayout.addWidget(self.pillPushButton2, 10, 1, Qt.AlignLeft)

        self.gridLayout.addWidget(self.hyperlinkButton1, 11, 0, Qt.AlignLeft)
        self.gridLayout.addWidget(self.hyperlinkButton2, 11, 1, Qt.AlignLeft)

        self.resize(600, 700)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = ToolButtonDemo()
    w1.show()

    w2 = PushButtonDemo()
    w2.show()
    app.exec()