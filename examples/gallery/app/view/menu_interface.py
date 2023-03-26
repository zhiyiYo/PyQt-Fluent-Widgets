# coding:utf-8
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QAction
from qfluentwidgets import RoundMenu, PushButton
from qfluentwidgets import FluentIcon as FIF

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class MenuInterface(GalleryInterface):
    """ Menu interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.menus,
            subtitle='qfluentwidgets.components.widgets',
            parent=parent
        )

        button = PushButton('Show menu')
        button.clicked.connect(lambda: self.createMenu(
            button.mapToGlobal(QPoint()) + QPoint(button.width()+5, -100)))

        self.addExampleCard(
            self.tr('Rounded corners menu'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/demo.py'
        )

    def createMenu(self, pos):
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
            [QAction(FIF.HELP.icon(), 'Help'), QAction(
                FIF.FEEDBACK.icon(), 'Feedback')]
        )

        # show menu
        menu.exec(pos, ani=True)
