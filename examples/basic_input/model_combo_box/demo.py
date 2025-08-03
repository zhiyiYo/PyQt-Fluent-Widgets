# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QCompleter, QHBoxLayout
from qfluentwidgets import ModelComboBox, setTheme, Theme, setThemeColor, EditableModelComboBox, setFont, FluentThemeColor

class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.comboBox = ModelComboBox(self)
        self.hBoxLayout = QHBoxLayout(self)

        self.comboBox.setPlaceholderText("选择一个脑婆")

        items = ['shoko 🥰', '西宫硝子', '宝多六花', '小鸟游六花']
        self.comboBox.addItems(items)
        self.comboBox.setCurrentIndex(-1)

        self.comboBox.currentTextChanged.connect(print)

        # self.comboBox.setPlaceholderText("选择一个脑婆")
        # self.comboBox.setCurrentIndex(-1)

        # NOTE: Completer is only applicable to EditableModelComboBox
        # self.completer = QCompleter(items, self)
        # self.comboBox.setCompleter(self.completer)

        self.resize(500, 500)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignCenter)
        self.setStyleSheet('Demo{background:white}')

        # setTheme(Theme.DARK)
        # setThemeColor(FluentThemeColor.DEFAULT_BLUE.color())
        # setFont(self.comboBox, 16)


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