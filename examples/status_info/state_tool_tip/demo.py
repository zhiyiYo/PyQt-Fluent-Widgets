# coding:utf-8
import sys
from PyQt6.QtWidgets import QApplication, QWidget

from qfluentwidgets import StateToolTip, PushButton, setTheme, Theme


class Demo(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # setTheme(Theme.DARK)

        self.resize(800, 300)
        self.btn = PushButton('Click Me', parent=self)
        self.btn.move(360, 225)
        self.btn.clicked.connect(self.onButtonClicked)
        self.stateTooltip = None

        self.setStyleSheet('Demo{background:white}')

    def onButtonClicked(self):
        if self.stateTooltip:
            self.stateTooltip.setContent('模型训练完成啦 😆')
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            self.stateTooltip = StateToolTip('正在训练模型', '客官请耐心等待哦~~', self)
            self.stateTooltip.move(510, 30)
            self.stateTooltip.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
