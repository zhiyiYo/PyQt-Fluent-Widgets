# coding:utf-8
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from qfluentwidgets import RoundMenu, setTheme, Theme
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

        # add actions
        menu.addAction(QAction(FIF.COPY.icon(), 'Copy'))
        menu.addAction(QAction(FIF.CUT.icon(), 'Cut'))

        # add sub menu
        submenu = RoundMenu("Add to", self)
        submenu.setIcon(FIF.ADD.icon())
        submenu.addActions([
            QAction(FIF.VIDEO.icon(), 'Video'),
            QAction(FIF.MUSIC.icon(), 'Music'),
        ])
        menu.addMenu(submenu)

        # add actions
        menu.addActions([
            QAction(FIF.PASTE.icon(), 'Paste'),
            QAction(FIF.CANCEL.icon(), 'Undo')
        ])

        # add separator
        menu.addSeparator()
        menu.addAction(QAction(f'Select all'))

        # insert actions
        menu.insertAction(
            menu.menuActions()[-1], QAction(FIF.SETTING.icon(), 'Settings'))
        menu.insertActions(
            menu.menuActions()[-1],
            [QAction(FIF.HELP.icon(), 'Help'), QAction(FIF.FEEDBACK.icon(), 'Feedback')]
        )

        # show menu
        menu.exec(e.globalPos(), ani=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
