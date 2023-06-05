# coding:utf-8
import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication, QWidget, QHBoxLayout
from qfluentwidgets import ProgressRing, SpinBox, setTheme, Theme


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background: rgb(32, 32, 32)}')

        self.vBoxLayout = QHBoxLayout(self)
        self.progressRing = ProgressRing(self)
        self.spinBox = SpinBox(self)

        self.progressRing.setValue(50)
        self.progressRing.setTextVisible(True)
        self.progressRing.setFixedSize(80, 80)

        # change background color
        # self.progressRing.setCustomBackgroundColor(Qt.transparent, Qt.transparent)

        # change font
        # font = QFont()
        # font.setFamilies(['Segoe UI', 'Microsoft YaHei'])
        # font.setPixelSize(15)
        # self.progressRing.setFont(font)

        self.spinBox.setRange(0, 100)
        self.spinBox.setValue(50)
        self.spinBox.valueChanged.connect(self.progressRing.setValue)

        self.vBoxLayout.addWidget(self.progressRing, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.spinBox, 0, Qt.AlignCenter)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.resize(400, 400)


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