# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QCompleter, QVBoxLayout

from qfluentwidgets import ComboBox, setTheme, Theme, setThemeColor, EditableComboBox, setFont
from qfluentwidgets.components.material import AcrylicComboBox, AcrylicEditableComboBox


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.comboBox = AcrylicComboBox(self)
        self.hBoxLayout = QVBoxLayout(self)

        items = ['shoko 🥰', '西宫硝子', 'aiko', '柳井爱子']
        self.comboBox.addItems(items)
        self.comboBox.setCurrentIndex(0)
        self.comboBox.currentTextChanged.connect(print)

        # NOTE: Completer is only applicable to AcrylicEditableComboBox
        # self.completer = QCompleter(items, self)
        # self.comboBox.setCompleter(self.completer)

        self.resize(300, 300)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet('Demo{background:white}')

        # setTheme(Theme.DARK)
        # setThemeColor('#0078d4')
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