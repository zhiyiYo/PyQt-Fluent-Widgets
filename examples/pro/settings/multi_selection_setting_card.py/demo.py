# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import setTheme, Theme, QConfig, OptionsConfigItem, FluentIcon
from qfluentwidgetspro import MultiSelectionSettingCard, ListValidator


class Config(QConfig):
    """ Custom config """

    wifes = OptionsConfigItem(
        'Wife', '2D', [], ListValidator(['西宫硝子', '后藤波奇', '宝多六花', '雪之下雪乃', '小鸟游六花']))



class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background: rgb(32,32,32)}')
        self.setStyleSheet('Demo2{background: white}')

        self.resize(600, 500)

        config = Config()
        self.settingCard = MultiSelectionSettingCard(
            configItem=config.wifes,
            icon=FluentIcon.CHECKBOX,
            title='脑婆',
            content='二刺螈怎么了，二刺螈吃你家大米了吗？',
            texts=config.wifes.options,
            parent=self
        )

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.settingCard)
        self.settingCard.comboBox.setFixedWidth(250)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w2 = Demo()
    w2.show()
    sys.exit(app.exec())
