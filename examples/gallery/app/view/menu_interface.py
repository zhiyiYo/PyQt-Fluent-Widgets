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

        button = PushButton(self.tr('Show menu'))
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
        menu.addAction(QAction(FIF.COPY.icon(), self.tr('Copy')))
        menu.addAction(QAction(FIF.CUT.icon(), self.tr('Cut')))

        # add sub menu
        submenu = RoundMenu(self.tr("Add to"), self)
        submenu.setIcon(FIF.ADD.icon())
        submenu.addActions([
            QAction(FIF.VIDEO.icon(), self.tr('Video')),
            QAction(FIF.MUSIC.icon(), self.tr('Music')),
        ])
        menu.addMenu(submenu)

        # add actions
        menu.addActions([
            QAction(FIF.PASTE.icon(), self.tr('Paste')),
            QAction(FIF.CANCEL.icon(), self.tr('Undo'))
        ])

        # add separator
        menu.addSeparator()
        menu.addAction(QAction(self.tr('Select all')))

        # insert actions
        menu.insertAction(
            menu.menuActions()[-1], QAction(FIF.SETTING.icon(), self.tr('Settings')))
        menu.insertActions(
            menu.menuActions()[-1],
            [
                QAction(FIF.HELP.icon(), self.tr('Help')),
                QAction(FIF.FEEDBACK.icon(), self.tr('Feedback'))
            ]
        )

        # show menu
        menu.exec(pos, ani=True)
