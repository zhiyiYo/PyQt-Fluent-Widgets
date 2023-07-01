# coding:utf-8
from PyQt6.QtCore import QPoint, Qt, QStandardPaths
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFileDialog
from qfluentwidgets import (RoundMenu, PushButton, Action, CommandBar, Action, TransparentDropDownPushButton,
                            setFont, CommandBarView, Flyout, ImageLabel, FlyoutAnimationType)
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
        self.setObjectName('menuInterface')

        # context menu
        button = PushButton(self.tr('Show menu'))
        button.clicked.connect(lambda: self.createMenu(
            button.mapToGlobal(QPoint()) + QPoint(button.width()+5, -100)))

        self.addExampleCard(
            self.tr('Rounded corners menu'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PyQt6/examples/menu/demo.py'
        )

        # command bar
        self.addExampleCard(
            self.tr('Command bar'),
            self.createCommandBar(),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/demo.py',
            stretch=1
        )

        # command bar flyout
        widget = QWidget(self)
        widget.setLayout(QVBoxLayout())
        widget.layout().setContentsMargins(0, 0, 0, 0)
        widget.layout().setSpacing(10)

        label = QLabel(self.tr('Click the image to open a command bar flyout 👇️🥵'))
        self.imageLabel = ImageLabel(':/gallery/images/chidanta5.jpg')
        self.imageLabel.scaledToWidth(350)
        self.imageLabel.setBorderRadius(8, 8, 8, 8)
        self.imageLabel.clicked.connect(self.createCommandBarFlyout)

        widget.layout().addWidget(label)
        widget.layout().addWidget(self.imageLabel)

        self.addExampleCard(
            self.tr('Command bar flyout'),
            widget,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/demo.py',
            stretch=1
        )

    def createMenu(self, pos):
        menu = RoundMenu(parent=self)

        # add actions
        menu.addAction(Action(FIF.COPY, self.tr('Copy')))
        menu.addAction(Action(FIF.CUT, self.tr('Cut')))

        # add sub menu
        submenu = RoundMenu(self.tr("Add to"), self)
        submenu.setIcon(FIF.ADD)
        submenu.addActions([
            Action(FIF.VIDEO, self.tr('Video')),
            Action(FIF.MUSIC, self.tr('Music')),
        ])
        menu.addMenu(submenu)

        # add actions
        menu.addActions([
            Action(FIF.PASTE, self.tr('Paste')),
            Action(FIF.CANCEL, self.tr('Undo'))
        ])

        # add separator
        menu.addSeparator()
        menu.addAction(QAction(self.tr('Select all')))

        # insert actions
        menu.insertAction(
            menu.menuActions()[-1], Action(FIF.SETTING, self.tr('Settings')))
        menu.insertActions(
            menu.menuActions()[-1],
            [
                Action(FIF.HELP, self.tr('Help')),
                Action(FIF.FEEDBACK, self.tr('Feedback'))
            ]
        )

        menu.exec(pos, ani=True)

    def createCommandBar(self):
        bar = CommandBar(self)
        bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        bar.addActions([
            Action(FIF.ADD, self.tr('Add')),
            Action(FIF.ROTATE, self.tr('Rotate')),
            Action(FIF.ZOOM_IN, self.tr('Zoom in')),
            Action(FIF.ZOOM_OUT, self.tr('Zoom out')),
        ])
        bar.addSeparator()
        bar.addActions([
            Action(FIF.EDIT, self.tr('Edit'), checkable=True),
            Action(FIF.INFO, self.tr('Info')),
            Action(FIF.DELETE, self.tr('Delete')),
            Action(FIF.SHARE, self.tr('Share'))
        ])

        button = TransparentDropDownPushButton(self.tr('Sort'), self, FIF.SCROLL)
        button.setFixedHeight(34)
        setFont(button, 12)

        menu = RoundMenu(parent=self)
        menu.addActions([
            Action(FIF.CALENDAR, self.tr('Create Date')),
            Action(FIF.CAMERA, self.tr('Shooting Date')),
            Action(FIF.FONT, self.tr('Name')),
        ])
        menu.addSeparator()
        menu.addActions([
            Action(FIF.UP, self.tr('Ascending')),
            Action(FIF.DOWN, self.tr('Descending')),
        ])

        button.setMenu(menu)
        bar.addWidget(button)

        bar.addHiddenActions([
            Action(FIF.SETTING, self.tr('Settings'), shortcut='Ctrl+I'),
        ])
        return bar

    def createCommandBarFlyout(self):
        view = CommandBarView(self)

        view.addAction(Action(FIF.SHARE, self.tr('Share')))
        view.addAction(Action(FIF.SAVE, self.tr('Save'), triggered=self.saveImage))
        view.addAction(Action(FIF.HEART, self.tr('Add to favorate')))
        view.addAction(Action(FIF.DELETE, self.tr('Delete')))

        view.addHiddenAction(Action(FIF.PRINT, self.tr('Print'), shortcut='Ctrl+P'))
        view.addHiddenAction(Action(FIF.SETTING, self.tr('Settings'), shortcut='Ctrl+S'))
        view.resizeToSuitableWidth()

        x = self.imageLabel.width()
        pos = self.imageLabel.mapToGlobal(QPoint(x, 0))
        Flyout.make(view, pos, self, FlyoutAnimationType.FADE_IN)

    def saveImage(self):
        path, ok = QFileDialog.getSaveFileName(
            parent=self,
            caption=self.tr('Save image'),
            directory=QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DesktopLocation),
            filter='PNG (*.png)'
        )
        if not ok:
            return

        self.imageLabel.image.save(path)