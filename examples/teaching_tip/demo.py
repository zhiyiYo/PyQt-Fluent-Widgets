# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout

from qfluentwidgets import PushButton, TeachingTip, TeachingTipTailPosition, InfoBarIcon, setTheme, Theme


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet("Demo{background: rgb(32, 32, 32)}")

        self.hBoxLayout = QVBoxLayout(self)
        self.button1 = PushButton('Top', self)
        self.button2 = PushButton('Bottom', self)

        self.resize(600, 500)
        self.button1.setFixedWidth(150)
        self.button2.setFixedWidth(150)
        self.hBoxLayout.addWidget(self.button2, 0, Qt.AlignmentFlag.AlignHCenter)
        self.hBoxLayout.addWidget(self.button1, 0, Qt.AlignmentFlag.AlignHCenter)
        self.button1.clicked.connect(self.showTopTip)
        self.button2.clicked.connect(self.showBottomTip)

    def showTopTip(self):
        tip = TeachingTip(
            target=self.button1,
            icon=None,
            title='Lesson 5',
            content="最短的捷径就是绕远路，绕远路才是我的最短捷径。",
            image='resource/Gyro.jpg',
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=-1,
            parent=self
        )
        button = PushButton('Action')
        button.setFixedWidth(120)
        tip.addWidget(button, align=Qt.AlignmentFlag.AlignRight)
        tip.show()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
