# coding:utf-8
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QCompleter, QHBoxLayout
from qfluentwidgets import ComboBox, setTheme, Theme, setThemeColor, EditableComboBox, setFont

class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.comboBox = ComboBox(self)
        self.hBoxLayout = QHBoxLayout(self)

        items = ['shoko 🥰', '西宫硝子', 'aiko', '柳井爱子']
        self.comboBox.addItems(items)
        self.comboBox.setCurrentIndex(0)
        self.comboBox.currentTextChanged.connect(print)

        # self.comboBox.setPlaceholderText("选择一个脑婆")
        # self.comboBox.setCurrentIndex(-1)

        # NOTE: Completer is only applicable to EditableComboBox
        # self.completer = QCompleter(items, self)
        # self.comboBox.setCompleter(self.completer)

        self.resize(500, 500)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignCenter)
        self.setStyleSheet('Demo{background:white}')

        # setTheme(Theme.DARK)
        # setThemeColor('#0078d4')
        # setFont(self.comboBox, 16)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()