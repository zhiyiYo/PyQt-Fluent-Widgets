# coding:utf-8
from PyQt5.QtCore import QPoint, Qt, QStandardPaths
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QWidget, QLabel, QVBoxLayout, QFileDialog, QActionGroup
from qfluentwidgets import (RoundMenu, PushButton, Action, CommandBar, Action, TransparentDropDownPushButton,
                            setFont, CommandBarView, Flyout, ImageLabel, FlyoutAnimationType, CheckableMenu,
                            MenuIndicatorType, AvatarWidget, isDarkTheme, BodyLabel, CaptionLabel, HyperlinkButton)
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

        # create actions
        self.createTimeAction = Action(FIF.CALENDAR, self.tr('Create Date'), checkable=True)
        self.shootTimeAction = Action(FIF.CAMERA, self.tr('Shooting Date'), checkable=True)
        self.modifiedTimeAction = Action(FIF.EDIT, self.tr('Modified time'), checkable=True)
        self.nameAction = Action(FIF.FONT, self.tr('Name'), checkable=True)
        self.actionGroup1 = QActionGroup(self)
        self.actionGroup1.addAction(self.createTimeAction)
        self.actionGroup1.addAction(self.shootTimeAction)
        self.actionGroup1.addAction(self.modifiedTimeAction)
        self.actionGroup1.addAction(self.nameAction)

        self.ascendAction =  Action(FIF.UP, self.tr('Ascending'), checkable=True)
        self.descendAction =  Action(FIF.DOWN, self.tr('Descending'), checkable=True)
        self.actionGroup2 = QActionGroup(self)
        self.actionGroup2.addAction(self.ascendAction)
        self.actionGroup2.addAction(self.descendAction)

        self.shootTimeAction.setChecked(True)
        self.ascendAction.setChecked(True)

        # context menu
        self.button1 = PushButton(self.tr('Show menu'))
        self.button1.clicked.connect(lambda: self.createMenu(
            self.button1.mapToGlobal(QPoint(self.button1.width()+5, -100))))

        self.addExampleCard(
            self.tr('Rounded corners menu'),
            self.button1,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/menu/demo.py'
        )

        # custom widget menu
        self.button3 = PushButton(self.tr('Show menu'))
        self.button3.clicked.connect(lambda: self.createCustomWidgetMenu(
            self.button3.mapToGlobal(QPoint(self.button3.width()+5, -100))))

        self.addExampleCard(
            self.tr('Rounded corners menu with custom widget'),
            self.button3,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/widget_menu/demo.py'
        )


        # checkable menu
        self.button2 = PushButton(self.tr('Show menu'))
        self.button2.clicked.connect(lambda: self.createCheckableMenu(
            self.button2.mapToGlobal(QPoint(self.button2.width()+5, -100))))

        self.addExampleCard(
            self.tr('Checkable menu'),
            self.button2,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/menu/demo.py'
        )

        # command bar
        self.addExampleCard(
            self.tr('Command bar'),
            self.createCommandBar(),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/menu/demo.py',
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
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/menu/demo.py',
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
            menu.actions()[-1], Action(FIF.SETTING, self.tr('Settings')))
        menu.insertActions(
            menu.actions()[-1],
            [
                Action(FIF.HELP, self.tr('Help')),
                Action(FIF.FEEDBACK, self.tr('Feedback'))
            ]
        )

        menu.exec(pos, ani=True)

    def createCustomWidgetMenu(self, pos):
        menu = RoundMenu(parent=self)

        # add custom widget
        card = ProfileCard(':/gallery/images/shoko.png', self.tr('Shoko'), 'shokokawaii@outlook.com', menu)
        menu.addWidget(card, selectable=False)

        menu.addSeparator()
        menu.addActions([
            Action(FIF.PEOPLE, self.tr('Manage account profile')),
            Action(FIF.SHOPPING_CART, self.tr('Payment method')),
            Action(FIF.CODE, self.tr('Redemption code and gift card')),
        ])
        menu.addSeparator()
        menu.addAction(Action(FIF.SETTING, self.tr('Settings')))
        menu.exec(pos)

    def createCheckableMenu(self, pos=None):
        menu = CheckableMenu(parent=self, indicatorType=MenuIndicatorType.RADIO)

        menu.addActions([
            self.createTimeAction, self.shootTimeAction,
            self.modifiedTimeAction, self.nameAction
        ])
        menu.addSeparator()
        menu.addActions([self.ascendAction, self.descendAction])

        if pos is not None:
            menu.exec(pos, ani=True)

        return menu

    def createCommandBar(self):
        bar = CommandBar(self)
        bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
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

        # add custom widget
        button = TransparentDropDownPushButton(self.tr('Sort'), self, FIF.SCROLL)
        button.setMenu(self.createCheckableMenu())
        button.setFixedHeight(34)
        setFont(button, 12)
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
            directory=QStandardPaths.writableLocation(QStandardPaths.DesktopLocation),
            filter='PNG (*.png)'
        )
        if not ok:
            return

        self.imageLabel.image.save(path)


class ProfileCard(QWidget):
    """ Profile card """

    def __init__(self, avatarPath: str, name: str, email: str, parent=None):
        super().__init__(parent=parent)
        self.avatar = AvatarWidget(avatarPath, self)
        self.nameLabel = BodyLabel(name, self)
        self.emailLabel = CaptionLabel(email, self)
        self.logoutButton = HyperlinkButton(
            'https://qfluentwidgets.com', '注销', self)

        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.emailLabel.setStyleSheet('QLabel{color: '+color.name()+'}')

        color = QColor(255, 255, 255) if isDarkTheme() else QColor(0, 0, 0)
        self.nameLabel.setStyleSheet('QLabel{color: '+color.name()+'}')
        setFont(self.logoutButton, 13)

        self.setFixedSize(307, 82)
        self.avatar.setRadius(24)
        self.avatar.move(2, 6)
        self.nameLabel.move(64, 13)
        self.emailLabel.move(64, 32)
        self.logoutButton.move(52, 48)
