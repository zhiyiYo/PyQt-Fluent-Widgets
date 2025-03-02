# coding:utf-8
import sys
from PyQt6 import QtGui

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout

from qfluentwidgets import (RoundMenu, FluentIcon, Action, AvatarWidget, BodyLabel,
                            HyperlinkButton, CaptionLabel, setFont, setTheme, Theme, isDarkTheme)
from qfluentwidgets.components.material import AcrylicMenu


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


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background: rgb(32, 32, 32)}')
        self.setStyleSheet('Demo{background: white}')
        self.setLayout(QHBoxLayout())

        self.label = BodyLabel('Right-click your mouse', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        setFont(self.label, 18)

        self.layout().addWidget(self.label)
        self.resize(400, 400)

    def contextMenuEvent(self, e) -> None:
        menu = AcrylicMenu(parent=self)

        # add custom widget
        card = ProfileCard('resource/shoko.png', '硝子酱', 'shokokawaii@outlook.com', menu)
        menu.addWidget(card, selectable=False)
        # menu.addWidget(card, selectable=True, onClick=lambda: print('666'))

        menu.addSeparator()
        menu.addActions([
            Action(FluentIcon.PEOPLE, '管理账户和设置'),
            Action(FluentIcon.SHOPPING_CART, '支付方式'),
            Action(FluentIcon.CODE, '兑换代码和礼品卡'),
        ])
        menu.addSeparator()
        menu.addAction(Action(FluentIcon.SETTING, '设置'))
        menu.exec(e.globalPos())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
