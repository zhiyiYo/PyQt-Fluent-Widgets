# coding:utf-8
import sys

from PySide2.QtCore import Qt, QPoint
from PySide2.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets import (CardWidget, setTheme, Theme, IconWidget, BodyLabel, CaptionLabel, PushButton,
                            TransparentToolButton, FluentIcon, RoundMenu, Action)


class AppCard(CardWidget):
    """ App card """

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.openButton = PushButton('打开', self)
        self.moreButton = TransparentToolButton(FluentIcon.MORE, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.openButton.setFixedWidth(120)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignRight)

        self.moreButton.setFixedSize(32, 32)
        self.moreButton.clicked.connect(self.onMoreButtonClicked)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FluentIcon.SHARE, '共享', self))
        menu.addAction(Action(FluentIcon.CHAT, '写评论', self))
        menu.addAction(Action(FluentIcon.PIN, '固定到任务栏', self))

        x = (self.moreButton.width() - menu.sizeHint().width()) // 2 + 10
        pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        menu.exec(pos)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # self.setStyleSheet("Demo {background: rgb(39, 39, 39)}")
        # setTheme(Theme.DARK)
        self.resize(600, 600)

        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        suffix = ":/qfluentwidgets/images/controls"
        self.addCard(f":/qfluentwidgets/images/logo.png", "PyQt-Fluent-Widgets", 'Shokokawaii Inc.')
        self.addCard(f"{suffix}/TitleBar.png", "PyQt-Frameless-Window", 'Shokokawaii Inc.')
        self.addCard(f"{suffix}/RatingControl.png", "反馈中心", 'Microsoft Corporation')
        self.addCard(f"{suffix}/Checkbox.png", "Microsoft 使用技巧", 'Microsoft Corporation')
        self.addCard(f"{suffix}/Pivot.png", "MSN 天气", 'Microsoft Corporation')
        self.addCard(f"{suffix}/MediaPlayerElement.png", "电影和电视", 'Microsoft Corporation')
        self.addCard(f"{suffix}/PersonPicture.png", "照片", 'Microsoft Corporation')

    def addCard(self, icon, title, content):
        card = AppCard(icon, title, content, self)
        self.vBoxLayout.addWidget(card, alignment=Qt.AlignTop)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()
