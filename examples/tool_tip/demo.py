# coding:utf-8
import sys
from PyQt5.QtCore import QEvent, QPoint, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout

from qfluentwidgets import ToolTip


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.hBox = QHBoxLayout(self)
        self.button1 = QPushButton('キラキラ', self)
        self.button2 = QPushButton('食べた愛', self)
        self._toolTip = ToolTip(parent=self)

        # use dark theme
        # self._toolTip.setDarkTheme(True)

        self.button1.setToolTip('aiko - キラキラ ✨')
        self.button2.setToolTip('aiko - 食べた愛 🥰')
        self.button1.setToolTipDuration(1000)
        self.button2.setToolTipDuration(5000)

        self.button1.installEventFilter(self)
        self.button2.installEventFilter(self)

        self.hBox.setContentsMargins(24, 24, 24, 24)
        self.hBox.setSpacing(16)
        self.hBox.addWidget(self.button1)
        self.hBox.addWidget(self.button2)

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
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()
