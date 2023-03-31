# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)

        self.hBoxLayout = QHBoxLayout(self)
        self.button1 = PushButton('Information', self)
        self.button2 = PushButton('Success', self)
        self.button3 = PushButton('Warning', self)
        self.button4 = PushButton('Error', self)

        self.button1.clicked.connect(self.createInfoInfoBar)
        self.button2.clicked.connect(self.createSuccessInfoBar)
        self.button3.clicked.connect(self.createWarningInfoBar)
        self.button4.clicked.connect(self.createErrorInfoBar)

        self.hBoxLayout.addWidget(self.button1)
        self.hBoxLayout.addWidget(self.button2)
        self.hBoxLayout.addWidget(self.button3)
        self.hBoxLayout.addWidget(self.button4)
        self.hBoxLayout.setContentsMargins(30, 0, 30, 0)

        self.resize(700, 700)

    def createInfoInfoBar(self):
        content = "A long essential app message for your users to be informed of, acknowledge, or take action on. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dapibus dolor vitae justo rutrum, ut lobortis nibh mattis. Aenean id elit commodo, semper felis nec."
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title='Title',
            content=content,
            orient=Qt.Vertical,    # vertical layout
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )
        w.addWidget(PushButton('Action'))
        w.show()

    def createSuccessInfoBar(self):
        content = "A short essential success app message."
        # convenient static mothod
        InfoBar.success(
            title='Title',
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    def createWarningInfoBar(self):
        InfoBar.warning(
            title='Title',
            content="A short essential app warning message.",
            orient=Qt.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP_LEFT,
            duration=2000,
            parent=self
        )

    def createErrorInfoBar(self):
        InfoBar.error(
            title='Title',
            content="A short essential app error message.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,    # won't disappear automatically
            parent=self
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
