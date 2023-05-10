# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout
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
        # self.progressRing.setCustomBackgroundColor(Qt.GlobalColor.transparent, Qt.GlobalColor.transparent)

        # change font
        # font = QFont()
        # font.setFamilies(['Segoe UI', 'Microsoft YaHei'])
        # font.setPixelSize(15)
        # self.progressRing.setFont(font)

        self.spinBox.setRange(0, 100)
        self.spinBox.setValue(50)
        self.spinBox.valueChanged.connect(self.progressRing.setValue)

        self.vBoxLayout.addWidget(self.progressRing, 0, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(self.spinBox, 0, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.resize(400, 400)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()