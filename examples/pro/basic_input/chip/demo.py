# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QButtonGroup, QHBoxLayout

from qfluentwidgets import setTheme, Theme, FluentIcon
from qfluentwidgetspro import Chip


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)

        self.resize(600, 500)
        self.hBoxLayout.setContentsMargins(30, 0, 30, 0)

        chip1 = Chip('Attach camera', self, FluentIcon.CAMERA)
        chip2 = Chip('Add friend', self, FluentIcon.PEOPLE)
        chip3 = Chip('Pin', self, FluentIcon.PIN)
        chip4 = Chip('Phone', self, FluentIcon.PHONE)

        for chip in self.findChildren(Chip):
            chip.setCheckable(True)
            self.hBoxLayout.addWidget(chip, 0, Qt.AlignmentFlag.AlignLeft)

        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.setSpacing(20)

        # chip4.setClosable(False)

        setTheme(Theme.DARK)
        self.setStyleSheet("Demo{background: rgb(32,32,32)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()