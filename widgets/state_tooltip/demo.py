# coding:utf-8
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

from state_tooltip import StateTooltip


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(800, 300)
        self.btn = QPushButton('点我', parent=self)
        self.btn.move(310, 225)
        self.btn.clicked.connect(self.onButtonClicked)
        self.stateTooltip = None
        with open('resource/style/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def onButtonClicked(self):
        if self.stateTooltip:
            self.stateTooltip.setContent('模型训练完成啦 😆')
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            self.stateTooltip = StateTooltip('正在训练模型', '客官请耐心等待哦~~', self)
            self.stateTooltip.move(520, 30)
            self.stateTooltip.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
