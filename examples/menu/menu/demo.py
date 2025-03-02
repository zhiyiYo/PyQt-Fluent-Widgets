# coding:utf-8
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from qfluentwidgets import RoundMenu, setTheme, Theme, Action, MenuAnimationType, MenuItemDelegate, CheckableMenu, MenuIndicatorType
from qfluentwidgets import FluentIcon as FIF


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.label = QLabel('Right-click your mouse', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.label)
        self.resize(400, 400)

        self.setStyleSheet('Demo{background: white} QLabel{font-size: 20px}')

        # setTheme(Theme.DARK)

    def contextMenuEvent(self, e):
        menu = RoundMenu(parent=self)
        #menu = CheckableMenu(parent=self, indicatorType=MenuIndicatorType.CHECK)

        # NOTE: hide the shortcut key
        # menu.view.setItemDelegate(MenuItemDelegate())

        # add actions
        menu.addAction(Action(FIF.COPY, 'Copy'))
        menu.addAction(Action(FIF.CUT, 'Cut'))
        menu.actions()[0].setCheckable(True)
        menu.actions()[0].setChecked(True)

        # add sub menu
        submenu = RoundMenu("Add to", self)
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
