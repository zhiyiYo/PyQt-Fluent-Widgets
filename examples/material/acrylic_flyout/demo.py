# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets import (PushButton, Flyout, InfoBarIcon, setTheme, Theme, FlyoutView, FlyoutViewBase,
                            BodyLabel, setFont, PrimaryPushButton, FlyoutAnimationType)
from qfluentwidgets.components.material import AcrylicFlyoutView, AcrylicFlyoutViewBase, AcrylicFlyout


class CustomFlyoutView(AcrylicFlyoutViewBase):

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


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet("Demo{background: rgb(32, 32, 32)}")

        self.vBoxLayout = QHBoxLayout(self)
        self.button1 = PushButton('Click Me', self)
        self.button2 = PushButton('Click Me', self)
        self.button3 = PushButton('Click Me', self)

        self.resize(750, 550)
        self.button1.setFixedWidth(150)
        self.button2.setFixedWidth(150)
        self.button3.setFixedWidth(150)
        self.vBoxLayout.addWidget(self.button1, 0, Qt.AlignmentFlag.AlignBottom)
        self.vBoxLayout.addWidget(self.button2, 0, Qt.AlignmentFlag.AlignBottom)
        self.vBoxLayout.addWidget(self.button3, 0, Qt.AlignmentFlag.AlignBottom)
        self.vBoxLayout.setContentsMargins(30, 50, 30, 50)

        self.button1.clicked.connect(self.showFlyout1)
        self.button2.clicked.connect(self.showFlyout2)
        self.button3.clicked.connect(self.showFlyout3)

    def showFlyout1(self):
        AcrylicFlyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='Lesson 4',
            content="表达敬意吧，表达出敬意，然后迈向回旋的另一个全新阶段！",
            target=self.button1,
            parent=self,
            isClosable=True
        )

    def showFlyout2(self):
        view = AcrylicFlyoutView(
            title='杰洛·齐贝林',
            content="触网而起的网球会落到哪一侧，谁也无法知晓。\n如果那种时刻到来，我希望「女神」是存在的。\n这样的话，不管网球落到哪一边，我都会坦然接受的吧。",
            image='resource/SBR.jpg',
            isClosable=True
            # image='resource/yiku.gif',
        )

        # add button to view
        button = PushButton('Action')
        button.setFixedWidth(120)
        view.addWidget(button, align=Qt.AlignmentFlag.AlignRight)

        # adjust layout (optional)
        view.widgetLayout.insertSpacing(1, 5)
        view.widgetLayout.addSpacing(5)

        # show view
        w = AcrylicFlyout.make(view, self.button2, self)
        view.closed.connect(w.close)

    def showFlyout3(self):
        AcrylicFlyout.make(CustomFlyoutView(), self.button3, self, aniType=FlyoutAnimationType.DROP_DOWN)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
