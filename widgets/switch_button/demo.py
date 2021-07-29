# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

from switch_button import SwitchButton


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(200, 100)
        self.switchButton = SwitchButton(parent=self)
        self.switchButton.move(60, 30)
        self.switchButton.checkedChanged.connect(self.onCheckedChanged)
        with open('resource/switch_button.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def onCheckedChanged(self, isChecked: bool):
        """ 开关按钮选中状态改变的槽函数 """
        text = '开' if isChecked else '关'
        self.switchButton.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
