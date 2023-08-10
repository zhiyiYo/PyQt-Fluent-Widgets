# coding:utf-8
import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets import (CardWidget, setTheme, Theme, IconWidget, BodyLabel, CaptionLabel, PushButton,
                            TransparentToolButton, FluentIcon, RoundMenu, Action, ElevatedCardWidget,
                            ImageLabel, isDarkTheme, FlowLayout, MSFluentTitleBar)

def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000

if isWin11() :
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window



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
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

        self.moreButton.setFixedSize(32, 32)
        self.moreButton.clicked.connect(self.onMoreButtonClicked)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FluentIcon.SHARE, '共享', self))
        menu.addAction(Action(FluentIcon.CHAT, '写评论', self))
        menu.addAction(Action(FluentIcon.PIN, '固定到任务栏', self))

        x = (self.moreButton.width() - menu.width()) // 2 + 10
        pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        menu.exec(pos)


class EmojiCard(ElevatedCardWidget):
    """ Emoji card """

    def __init__(self, iconPath: str, parent=None):
        super().__init__(parent)
        self.iconWidget = ImageLabel(iconPath, self)
        self.label = CaptionLabel(Path(iconPath).stem, self)

        self.iconWidget.scaledToHeight(68)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        self.setFixedSize(168, 176)



class Demo1(Window):

    def __init__(self):
        super().__init__()
        self.setTitleBar(MSFluentTitleBar(self))
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('Fluent Emoji gallery')

        if isWin11():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())

        self.flowLayout = FlowLayout(self)

        self.resize(580, 680)
        self.flowLayout.setSpacing(6)
        self.flowLayout.setContentsMargins(30, 60, 30, 30)
        self.flowLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        for path in Path('./resource').glob('*.png'):
            self.addCard(str(path))

    def addCard(self, iconPath: str):
        card = EmojiCard(iconPath, self)
        self.flowLayout.addWidget(card)


class Demo2(Window):

    def __init__(self):
        super().__init__()
        self.setTitleBar(MSFluentTitleBar(self))
        self.resize(600, 600)

        if isWin11():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())

        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(30, 60, 30, 30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

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
        self.vBoxLayout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)


if __name__ == '__main__':
    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w1 = Demo1()
    w1.show()
    w2 = Demo2()
    w2.show()
    app.exec()
