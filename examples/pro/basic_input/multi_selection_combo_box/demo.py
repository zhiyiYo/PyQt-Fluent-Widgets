# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QCompleter, QHBoxLayout

from qfluentwidgets import ComboBox, setTheme, Theme, setThemeColor, setFont, FluentThemeColor
from qfluentwidgetspro import MultiSelectionComboBox, MultiSelectionDisplayMode


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.comboBox = MultiSelectionComboBox(self)
        self.hBoxLayout = QHBoxLayout(self)

        items = ['西宫硝子', "中野六花", "宝多六花", "雪之下雪乃", "千反田爱瑠"]
        self.comboBox.addItems(items)
        self.comboBox.currentTextChanged.connect(print)
        self.comboBox.setFixedWidth(300)
        self.comboBox.setPlaceholderText("选择一个脑婆")

        # self.comboBox.setDisplayMode(MultiSelectionDisplayMode.DELIMITER)
        # self.comboBox.setDelimiter("/")

        self.resize(500, 500)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet('Demo{background:white}')

        # setTheme(Theme.DARK)
        # setFont(self.comboBox, 16)
        # self.setStyleSheet("Demo{background: rgb(32,32,32)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()