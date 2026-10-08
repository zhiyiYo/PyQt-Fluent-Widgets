# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets import (FluentIcon, TransparentDropDownPushButton, RoundMenu, CommandBar, Action,
                            setTheme, Theme, setFont, CommandBarView, Flyout, FlyoutAnimationType,
                            ImageLabel, PushButton, CheckBox, CaptionLabel)
from qframelesswindow import FramelessWindow, StandardTitleBar


class Demo1(QWidget):
    """ Command bar with collapsible custom widget """

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo1{background: rgb(32, 32, 32)}')

        self.hBoxLayout = QHBoxLayout(self)
        self.commandBar = CommandBar(self)
        self.dropDownButton = self.createDropDownButton()

        self.hBoxLayout.addWidget(self.commandBar, 0)

        # change button style
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # self.commandBar.setMenuDropDown(False)
        # self.commandBar.setButtonTight(True)
        # setFont(self.commandBar, 14)

        self.addButton(FluentIcon.ADD, 'Add')
        self.commandBar.addSeparator()

        self.commandBar.addAction(Action(FluentIcon.EDIT, 'Edit', triggered=self.onEdit, checkable=True))
        self.addButton(FluentIcon.COPY, 'Copy')
        self.addButton(FluentIcon.SHARE, 'Share')

        # the custom widget will be collapsed into the more actions menu
        # when the window is not wide enough
        self.commandBar.addCollapsibleWidget(self.dropDownButton, self.createDropDownMenu)

        # add hidden actions
        self.commandBar.addHiddenAction(Action(FluentIcon.SCROLL, 'Sort', triggered=lambda: print('排序')))
        self.commandBar.addHiddenAction(Action(FluentIcon.SETTING, 'Settings', shortcut='Ctrl+S'))

        self.resize(240, self.sizeHint().height())
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
        button.setMenu(self.createDropDownMenu())
        return button

    def createDropDownMenu(self):
        menu = RoundMenu('Menu', parent=self)
        menu.addActions([
            Action(FluentIcon.COPY, 'Copy'),
            Action(FluentIcon.CUT, 'Cut'),
            Action(FluentIcon.PASTE, 'Paste'),
            Action(FluentIcon.CANCEL, 'Cancel'),
            Action('Select all'),
        ])
        return menu


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


class Demo3(QWidget):
    """ Command bar with alignment, inserted action and collapsible widget """

    def __init__(self):
        super().__init__()
        self.commandBar = CommandBar(self)
        self.alignButton = self.createAlignButton()
        self.checkBox = CheckBox('Show widget', self)
        self.hintLabel = CaptionLabel(
            'Drag the right edge of window to collapse the menu button')

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(16, 16, 16, 16)
        self.vBoxLayout.setSpacing(12)

        self.vBoxLayout.addWidget(self.commandBar)

        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.addWidget(self.alignButton)
        self.hBoxLayout.addWidget(self.checkBox)
        self.hBoxLayout.addStretch(1)
        self.vBoxLayout.addLayout(self.hBoxLayout)

        # the wrapped label won't prevent the window from being resized smaller
        self.hintLabel.setWordWrap(True)
        self.hintLabel.setAlignment(Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.hintLabel)

        # change the alignment of commands
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commandBar.setLayoutAlignment(Qt.AlignHCenter)

        for icon, text in [(FluentIcon.ADD, 'Add'), (FluentIcon.DELETE, 'Delete'),
                           (FluentIcon.SHARE, 'Share'), (FluentIcon.SAVE, 'Save')]:
            self.commandBar.addAction(
                Action(icon, text, triggered=lambda c=text: print(c)))

        # insert a command at the specified position
        self.commandBar.insertActionAt(
            1, Action(FluentIcon.EDIT, 'Edit', triggered=lambda: print('Edit')))

        # the menu button becomes a submenu of the more actions menu
        # after it is collapsed
        self.menuButton = self.createMenuButton()
        self.commandBar.addCollapsibleWidget(self.menuButton, self.createMenu)

        # the widget disappears from the more actions menu after it is
        # collapsed because it is not registered as a collapsible widget
        self.pushButton = PushButton('Widget', self)
        self.commandBar.addWidget(self.pushButton)

        # hide or show the widget from the command bar
        self.checkBox.setChecked(True)
        self.checkBox.toggled.connect(
            lambda: self.commandBar.setCommandWidgetVisible(
                self.pushButton, self.checkBox.isChecked()))

        self.resize(620, self.sizeHint().height())
        self.setWindowTitle('Alignment & visibility')

    def createAlignButton(self):
        button = TransparentDropDownPushButton('Alignment', self)

        menu = RoundMenu(parent=self)
        menu.addAction(
            Action('Left', triggered=lambda: self.commandBar.setLayoutAlignment(Qt.AlignLeft)))
        menu.addAction(
            Action('Center', triggered=lambda: self.commandBar.setLayoutAlignment(Qt.AlignHCenter)))
        menu.addAction(
            Action('Right', triggered=lambda: self.commandBar.setLayoutAlignment(Qt.AlignRight)))
        button.setMenu(menu)
        return button

    def createMenuButton(self):
        button = TransparentDropDownPushButton('Menu', self, FluentIcon.MENU)
        button.setFixedHeight(34)
        setFont(button, 12)
        button.setMenu(self.createMenu())
        return button

    def createMenu(self):
        menu = RoundMenu('Menu', parent=self)
        menu.addActions([Action(FluentIcon.COPY, f'Copy {i}') for i in range(8)])
        menu.addAction(Action(FluentIcon.CUT, 'Cut'))
        menu.addAction(Action(FluentIcon.PASTE, 'Paste'))
        return menu


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w1 = Demo1()
    w3 = Demo3()

    # arrange windows to avoid overlapping
    w1.move(60, 60)
    w3.move(60, 60 + w1.height() + 28)

    for w in (w1, w3):
        w.show()

    sys.exit(app.exec_())
