# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import ComboBox, setTheme, Theme, setThemeColor

class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.comboBox = ComboBox(self)

        self.comboBox.addItems(['shoko 🥰', '西宫硝子', 'aiko', '柳井爱子'])
        self.comboBox.setCurrentIndex(0)
        self.comboBox.currentTextChanged.connect(print)
        self.comboBox.move(200, 200)

        self.resize(500, 500)
        self.setStyleSheet('Demo{background:white}')

        # setTheme(Theme.DARK)
        # setThemeColor('#0078d4')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()