# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from qfluentwidgets import RoundMenu
from qfluentwidgets import FluentIconFactory as FIF


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.label = QLabel('Right-click your mouse', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.label)
        self.resize(400, 400)

        self.setStyleSheet('Demo{background: white} QLabel{font-size: 20px}')

    def contextMenuEvent(self, e):
        menu = RoundMenu(parent=self)

        # add actions
        menu.addAction(QAction(FIF.icon(FIF.COPY), 'Copy'))
        menu.addAction(QAction(FIF.icon(FIF.CUT), 'Cut'))

        # add sub menu
        submenu = RoundMenu("Add to", self)
        submenu.setIcon(FIF.icon(FIF.ADD))
        submenu.addActions([
            QAction(FIF.icon(FIF.VIDEO), 'Video'),
            QAction(FIF.icon(FIF.MUSIC), 'Music'),
        ])
        menu.addMenu(submenu)

        # add actions
        menu.addActions([
            QAction(FIF.icon(FIF.PASTE), 'Paste'),
            QAction(FIF.icon(FIF.CANCEL), 'Undo')
        ])

        # add separator
        menu.addSeparator()
        menu.addAction(QAction(f'Select all'))

        # insert actions
        menu.insertAction(
            menu.menuActions()[-1], QAction(FIF.icon(FIF.SETTING), 'Settings'))
        menu.insertActions(
            menu.menuActions()[-1],
            [QAction(FIF.icon(FIF.HELP), 'Help'), QAction(FIF.icon(FIF.FEEDBACK), 'Feedback')]
        )

        # show menu
        menu.exec(e.globalPos(), ani=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
