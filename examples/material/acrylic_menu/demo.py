# coding:utf-8
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon
from qfluentwidgets import MessageBox, setTheme, Theme, ImageLabel, Action, MenuAnimationType, MenuItemDelegate, CheckableMenu, MenuIndicatorType
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets.components.material import AcrylicMenu, AcrylicSystemTrayMenu, AcrylicCheckableMenu


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())
        self.setToolTip('硝子酱一级棒卡哇伊🥰')

        self.menu = AcrylicSystemTrayMenu(parent=parent)
        self.menu.addActions([
            Action('🎤   唱'),
            Action('🕺   跳'),
            Action('🤘🏼   RAP'),
            Action('🎶   Music'),
            Action('🏀   篮球', triggered=self.ikun),
        ])
        self.setContextMenu(self.menu)

    def ikun(self):
        content = """巅峰产生虚伪的拥护，黄昏见证真正的使徒 🏀

                         ⠀⠰⢷⢿⠄
                   ⠀⠀⠀⠀⠀⣼⣷⣄
                   ⠀⠀⣤⣿⣇⣿⣿⣧⣿⡄
                   ⢴⠾⠋⠀⠀⠻⣿⣷⣿⣿⡀
                   ⠀⢀⣿⣿⡿⢿⠈⣿
                   ⠀⠀⠀⢠⣿⡿⠁⠀⡊⠀⠙
                   ⠀⠀⠀⢿⣿⠀⠀⠹⣿
                   ⠀⠀⠀⠀⠹⣷⡀⠀⣿⡄
                   ⠀⠀⠀⠀⣀⣼⣿⠀⢈⣧
        """
        w = MessageBox(
            title='坤家军！集合！',
            content=content,
            parent=self.parent()
        )
        w.yesButton.setText('献出心脏')
        w.cancelButton.setText('你干嘛~')
        w.exec()


class Demo(ImageLabel):

    def __init__(self):
        super().__init__()
        self.setImage("resource/chidanta.jpg")
        self.scaledToWidth(500)

        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        #self.systemTrayIcon = SystemTrayIcon(self)
        #self.systemTrayIcon.show()

        # setTheme(Theme.DARK)

    def contextMenuEvent(self, e):
        menu = AcrylicMenu(parent=self)
        # menu = AcrylicCheckableMenu(parent=self, indicatorType=MenuIndicatorType.RADIO)

        # NOTE: hide the shortcut key
        # menu.view.setItemDelegate(MenuItemDelegate())

        # add actions
        menu.addAction(Action(FIF.COPY, 'Copy'))
        menu.addAction(Action(FIF.CUT, 'Cut'))
        menu.actions()[0].setCheckable(True)
        menu.actions()[0].setChecked(True)

        # add sub menu
        submenu = AcrylicMenu("Add to", self)
        submenu.setIcon(FIF.ADD)
        submenu.addActions([
            Action(FIF.VIDEO, 'Video'),
            Action(FIF.MUSIC, 'Music'),
        ])
        menu.addMenu(submenu)

        # add actions
        menu.addActions([
            Action(FIF.PASTE, 'Paste'),
            Action(FIF.CANCEL, 'Undo')
        ])

        # add separator
        menu.addSeparator()
        menu.addAction(QAction(f'Select all', shortcut='Ctrl+A'))

        # insert actions
        menu.insertAction(
            menu.actions()[-1], Action(FIF.SETTING, 'Settings', shortcut='Ctrl+S'))
        menu.insertActions(
            menu.actions()[-1],
            [Action(FIF.HELP, 'Help', shortcut='Ctrl+H'),
             Action(FIF.FEEDBACK, 'Feedback', shortcut='Ctrl+F')]
        )
        menu.actions()[-2].setCheckable(True)
        menu.actions()[-2].setChecked(True)

        # show menu
        menu.exec(e.globalPos(), aniType=MenuAnimationType.DROP_DOWN)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
