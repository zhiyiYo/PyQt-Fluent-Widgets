# coding:utf-8
import sys
from PyQt6.QtCore import QEvent, QPoint, Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import setTheme, Theme, PushButton, ToolTipPosition
from qfluentwidgets.components.material import AcrylicToolTipFilter

class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.hBox = QHBoxLayout(self)
        self.button1 = PushButton('キラキラ', self)
        self.button2 = PushButton('食べた愛', self)
        self.button3 = PushButton('シアワセ', self)

        # use dark theme
        # setTheme(Theme.DARK)
        self.setStyleSheet('Demo{background:white}')

        self.button1.setToolTip('aiko - キラキラ ✨')
        self.button2.setToolTip('aiko - 食べた愛 🥰')
        self.button3.setToolTip('aiko - シアワセ 😊')
        self.button1.setToolTipDuration(1000)
        # self.button2.setToolTipDuration(-1)  # won't disappear

        self.button1.installEventFilter(AcrylicToolTipFilter(self.button1, 0, ToolTipPosition.TOP))
        self.button2.installEventFilter(AcrylicToolTipFilter(self.button2, 0, ToolTipPosition.BOTTOM))
        self.button3.installEventFilter(AcrylicToolTipFilter(self.button3, 300, ToolTipPosition.RIGHT))

        self.button1.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(
            'https://www.youtube.com/watch?v=S0bXDRY1DGM&list=RDMM&index=1')))
        self.button2.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(
            'https://www.youtube.com/watch?v=CZLs8GuCq2U&list=RDMM&index=4')))
        self.button3.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(
            'https://www.youtube.com/watch?v=fp-yJUB7sS8&list=RDMM&index=3')))

        self.hBox.setContentsMargins(24, 24, 24, 24)
        self.hBox.setSpacing(16)
        self.hBox.addWidget(self.button1)
        self.hBox.addWidget(self.button2)
        self.hBox.addWidget(self.button3)

        self.resize(480, 240)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
