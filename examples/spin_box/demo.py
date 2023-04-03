# coding:utf-8
import sys
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout

from qfluentwidgets import SpinBox, DoubleSpinBox, DateTimeEdit, DateEdit, TimeEdit


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.vBoxLayout = QVBoxLayout(self)

        self.spinBox = SpinBox(self)
        self.timeEdit = TimeEdit(self)
        self.dateEdit = DateEdit(self)
        self.dateTimeEdit = DateTimeEdit(self)
        self.doubleSpinBox = DoubleSpinBox(self)

        self.resize(500, 500)
        self.setStyleSheet('Demo{background: white}')

        self.vBoxLayout.setContentsMargins(100, 50, 100, 50)
        self.vBoxLayout.addWidget(self.spinBox)
        self.vBoxLayout.addWidget(self.doubleSpinBox)
        self.vBoxLayout.addWidget(self.timeEdit)
        self.vBoxLayout.addWidget(self.dateEdit)
        self.vBoxLayout.addWidget(self.dateTimeEdit)


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
