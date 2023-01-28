# coding:utf-8
import sys
from PyQt6.QtWidgets import QApplication, QWidget

from qfluentwidgets import SwitchButton


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(160, 80)
        self.switchButton = SwitchButton(parent=self)
        self.switchButton.move(48, 24)
        self.switchButton.checkedChanged.connect(self.onCheckedChanged)

    def onCheckedChanged(self, isChecked):
        text = 'On' if isChecked else 'Off'
        self.switchButton.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
