# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets import (PushButton, TeachingTip, TeachingTipTailPosition, InfoBarIcon, setTheme, Theme,
                            TeachingTipView, FlyoutViewBase, BodyLabel, PrimaryPushButton, PopupTeachingTip)


class CustomFlyoutView(FlyoutViewBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.label = BodyLabel(
            '这是一场「试炼」，我认为这就是一场为了战胜过去的「试炼」，\n只有战胜了那些幼稚的过去，人才能有所成长。')
        self.button = PrimaryPushButton('Action')

        self.button.setFixedWidth(140)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(20, 16, 20, 16)
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.addWidget(self.button)

    def paintEvent(self, e):
        pass


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet("Demo{background: rgb(32, 32, 32)}")

        self.hBoxLayout = QHBoxLayout(self)
        self.button1 = PushButton('Top', self)
        self.button2 = PushButton('Bottom', self)
        self.button3 = PushButton('Custom', self)

        self.resize(700, 500)
        self.button1.setFixedWidth(150)
        self.button2.setFixedWidth(150)
        self.button3.setFixedWidth(150)
        self.hBoxLayout.addWidget(self.button2, 0, Qt.AlignmentFlag.AlignHCenter)
        self.hBoxLayout.addWidget(self.button1, 0, Qt.AlignmentFlag.AlignHCenter)
        self.hBoxLayout.addWidget(self.button3, 0, Qt.AlignmentFlag.AlignHCenter)
        self.button1.clicked.connect(self.showTopTip)
        self.button2.clicked.connect(self.showBottomTip)
        self.button3.clicked.connect(self.showCustomTip)

    def showTopTip(self):
        position = TeachingTipTailPosition.BOTTOM
        view = TeachingTipView(
            icon=None,
            title='Lesson 5',
            content="最短的捷径就是绕远路，绕远路才是我的最短捷径。",
            image='resource/Gyro.jpg',
            # image='resource/boqi.gif',
            isClosable=True,
            tailPosition=position,
        )

        # add widget to view
        button = PushButton('Action')
        button.setFixedWidth(120)
        view.addWidget(button, align=Qt.AlignmentFlag.AlignRight)

        tip = TeachingTip.make(
            view, target=self.button1, duration=-1, tailPosition=position, parent=self)
        view.closed.connect(tip.close)

    def showBottomTip(self):
        TeachingTip.create(
            target=self.button2,
            icon=InfoBarIcon.SUCCESS,
            title='Lesson 4',
            content="表达敬意吧，表达出敬意，然后迈向回旋的另一个全新阶段！",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.TOP,
            duration=2000,
            parent=self
        )

    def showCustomTip(self):
        # TeachingTip.make(
        PopupTeachingTip.make(
            target=self.button3,
            view=CustomFlyoutView(),
            tailPosition=TeachingTipTailPosition.RIGHT,
            duration=2000,
            parent=self
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
