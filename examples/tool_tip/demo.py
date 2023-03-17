# coding:utf-8
import sys
from PySide6.QtCore import QEvent, QPoint, Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout

from qfluentwidgets import ToolTip, ToolTipFilter, setTheme, Theme


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.hBox = QHBoxLayout(self)
        self.button1 = QPushButton('キラキラ', self)
        self.button2 = QPushButton('食べた愛', self)
        self.button3 = QPushButton('シアワセ', self)
        self._toolTip = ToolTip(parent=self)

        # use dark theme
        # setTheme(Theme.DARK)

        self.button1.setToolTip('aiko - キラキラ ✨')
        self.button2.setToolTip('aiko - 食べた愛 🥰')
        self.button3.setToolTip('aiko - シアワセ 😊')
        self.button1.setToolTipDuration(1000)
        self.button2.setToolTipDuration(5000)

        self.button1.installEventFilter(self)
        self.button2.installEventFilter(self)
        self.button3.installEventFilter(ToolTipFilter(self.button3))

        # bonus time
        self.button1.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(
            'https://m10.music.126.net/20230316233123/a3ea2bccd1945bd0b3a4dc65c49d7116/ymusic/f645/3ea3/f207/099b30242a2c4cec281b5d2ad9792bee.mp3')))
        self.button2.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(
            'https://cj-sycdn.kuwo.cn/5bfbe88f19ec31c28c7707c78198af21/641331e9/resource/n2/55/27/3449307801.mp3')))
        self.button3.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(
            'https://m10.music.126.net/20230316232817/17427b2b109105bddc803dbbc436243f/ymusic/f3b7/881a/4df7/2064989b610865dc2c792aa3c202c753.mp3')))

        self.hBox.setContentsMargins(24, 24, 24, 24)
        self.hBox.setSpacing(16)
        self.hBox.addWidget(self.button1)
        self.hBox.addWidget(self.button2)
        self.hBox.addWidget(self.button3)

        self.resize(480, 240)
        self._toolTip.hide()

        with open('resource/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def eventFilter(self, obj, e: QEvent):
        if obj is self:
            return super().eventFilter(obj, e)

        tip = self._toolTip
        if e.type() == QEvent.Enter:
            tip.setText(obj.toolTip())
            tip.setDuration(obj.toolTipDuration())
            tip.adjustPos(obj.mapToGlobal(QPoint()), obj.size())
            tip.show()
        elif e.type() == QEvent.Leave:
            tip.hide()
        elif e.type() == QEvent.ToolTip:
            return True

        return super().eventFilter(obj, e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
