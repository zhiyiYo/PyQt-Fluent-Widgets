# coding:utf-8
import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget, QPushButton

from qfluentwidgets import StateToolTip


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(800, 300)
        self.btn = QPushButton('Click Me', parent=self)
        self.btn.move(310, 225)
        self.btn.clicked.connect(self.onButtonClicked)
        self.stateTooltip = None
        with open('resource/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

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
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
