# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QHBoxLayout, QLabel
from qfluentwidgets import RoundMenu, setTheme, Theme, Action, MenuAnimationType
from qfluentwidgets import FluentIcon as FIF


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.label = QLabel('Right-click your mouse', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.label)
        self.resize(400, 400)

        self.setStyleSheet('Demo{background: white} QLabel{font-size: 20px}')

        # setTheme(Theme.DARK)

    def contextMenuEvent(self, e):
        menu = RoundMenu(parent=self)

        # add actions
        menu.addAction(Action(FIF.COPY, 'Copy'))
        menu.addAction(Action(FIF.CUT, 'Cut'))

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
        menu.addAction(QAction(f'Select all'))

        # insert actions
        menu.insertAction(
            menu.menuActions()[-1], Action(FIF.SETTING, 'Settings'))
        menu.insertActions(
            menu.menuActions()[-1],
            [Action(FIF.HELP, 'Help'), Action(FIF.FEEDBACK, 'Feedback')]
        )

        # show menu
        menu.exec(e.globalPos(), aniType=MenuAnimationType.DROP_DOWN)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()
