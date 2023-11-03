# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QCompleter, QVBoxLayout

from qfluentwidgets import setTheme, Theme, FluentIcon, setFont, FluentThemeColor, FlyoutAnimationType
from qfluentwidgetspro import DropDownColorPalette, CustomDropDownColorPalette


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.picker = DropDownColorPalette(self)
        self.brushPicker = CustomDropDownColorPalette(self)
        self.vBoxLayout = QVBoxLayout(self)

        # self.picker.setDefaultColor("#009500")
        self.picker.setColor(FluentThemeColor.DEFAULT_BLUE.value)
        self.picker.colorChanged.connect(lambda c: print(c.name()))

        self.brushPicker.setFlyoutAnimationType(FlyoutAnimationType.PULL_UP)

        # change the icon
        # self.brushPicker.setIcon(FluentIcon.BACKGROUND_FILL)

        self.resize(700, 750)
        self.vBoxLayout.addWidget(self.picker, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.brushPicker, 0, Qt.AlignmentFlag.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # setTheme(Theme.DARK)
        # self.setStyleSheet("Demo{background: rgb(32,32,32)}")
        self.setStyleSheet('Demo{background:white}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()