# coding:utf-8
import sys
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager


@InfoBarManager.register('Custom')
class CustomInfoBarManager(InfoBarManager):
    """ Custom info bar manager """

    def _pos(self, infoBar: InfoBar, parentSize=None):
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        # the position of first info bar
        x = (parentSize.width() - infoBar.width()) // 2
        y = (parentSize.height() - infoBar.height()) // 2

        # get the position of current info bar
        index = self.infoBars[p].index(infoBar)
        for bar in self.infoBars[p][0:index]:
            y += (bar.height() + self.spacing)

        return QPoint(x, y)

    def _slideStartPos(self, infoBar: InfoBar):
        pos = self._pos(infoBar)
        return QPoint(pos.x(), pos.y() - 16)



class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)

        self.hBoxLayout = QHBoxLayout(self)
        self.button1 = PushButton('Information', self)
        self.button2 = PushButton('Success', self)
        self.button3 = PushButton('Warning', self)
        self.button4 = PushButton('Error', self)
        self.button5 = PushButton('Custom', self)
        self.button6 = PushButton('Desktop', self)

        self.button1.clicked.connect(self.createInfoInfoBar)
        self.button2.clicked.connect(self.createSuccessInfoBar)
        self.button3.clicked.connect(self.createWarningInfoBar)
        self.button4.clicked.connect(self.createErrorInfoBar)
        self.button5.clicked.connect(self.createCustomInfoBar)
        self.button6.clicked.connect(self.createDeskTopBottomRightInfoBar)

        self.hBoxLayout.addWidget(self.button1)
        self.hBoxLayout.addWidget(self.button2)
        self.hBoxLayout.addWidget(self.button3)
        self.hBoxLayout.addWidget(self.button4)
        self.hBoxLayout.addWidget(self.button5)
        self.hBoxLayout.addWidget(self.button6)
        self.hBoxLayout.setContentsMargins(30, 0, 30, 0)

        self.resize(700, 700)

    def createInfoInfoBar(self):
        content = "My name is kira yoshikake, 33 years old. Living in the villa area northeast of duwangting, unmarried. I work in Guiyou chain store. Every day I have to work overtime until 8 p.m. to go home. I don't smoke. The wine is only for a taste. Sleep at 11 p.m. for 8 hours a day. Before I go to bed, I must drink a cup of warm milk, then do 20 minutes of soft exercise, get on the bed, and immediately fall asleep. Never leave fatigue and stress until the next day. Doctors say I'm normal."
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title='Title',
            content=content,
            orient=Qt.Orientation.Vertical,    # vertical layout
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )
        w.addWidget(PushButton('Action'))
        w.show()

    def createSuccessInfoBar(self):
        # convenient class mothod
        InfoBar.success(
            title='Lesson 4',
            content="With respect, let's advance towards a new stage of the spin.",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=2000,
            parent=self
        )

    def createWarningInfoBar(self):
        InfoBar.warning(
            title='Lesson 3',
            content="Believe in the spin, just keep believing!",
            orient=Qt.Orientation.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP_LEFT,
            duration=2000,
            parent=self
        )

    def createErrorInfoBar(self):
        InfoBar.error(
            title='Lesson 5',
            content="迂回路を行けば最短ルート。",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,    # won't disappear automatically
            parent=self
        )

    def createCustomInfoBar(self):
        w = InfoBar.new(
            icon=FluentIcon.GITHUB,
            title='Zeppeli',
            content="人間讃歌は「勇気」の讃歌ッ！！ 人間のすばらしさは勇気のすばらしさ！！",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=2000,
            parent=self
        )
        w.setCustomBackgroundColor('white', '#202020')

    def createDeskTopBottomRightInfoBar(self):
        InfoBar.warning(
            title='Plugged Out Notify',
            content="Battery is 64%",
            orient=Qt.Orientation.Vertical,
            position=InfoBarPosition.BOTTOM_RIGHT,
            parent=InfoBar.desktopView()
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
