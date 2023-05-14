# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import LineEdit, PushButton, SearchLineEdit


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)
        self.lineEdit = SearchLineEdit(self)
        self.button = PushButton('Search', self)

        self.resize(400, 400)
        self.hBoxLayout.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.lineEdit, 0, Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignCenter)

        self.lineEdit.setFixedSize(200, 33)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setPlaceholderText('Search icon')


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