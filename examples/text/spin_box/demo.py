# coding:utf-8
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout

from qfluentwidgets import (SpinBox, CompactSpinBox, DoubleSpinBox, CompactDoubleSpinBox,
                            DateTimeEdit, CompactDateTimeEdit, DateEdit, CompactDateEdit,
                            TimeEdit, CompactTimeEdit, setTheme, Theme)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet('Demo{background: rgb(255, 255, 255)}')

        self.gridLayout = QGridLayout(self)

        self.spinBox = SpinBox(self)
        self.compactSpinBox = CompactSpinBox(self)
        self.spinBox.setAccelerated(True)
        self.compactSpinBox.setAccelerated(True)

        self.timeEdit = TimeEdit(self)
        self.compactTimeEdit = CompactTimeEdit(self)

        self.dateEdit = DateEdit(self)
        self.compactDateEdit = CompactDateEdit(self)

        self.dateTimeEdit = DateTimeEdit(self)
        self.compactDateTimeEdit = CompactDateTimeEdit(self)

        self.doubleSpinBox = DoubleSpinBox(self)
        self.compactDoubleSpinBox = CompactDoubleSpinBox(self)

        self.resize(500, 500)
        self.gridLayout.setHorizontalSpacing(30)

        self.gridLayout.setContentsMargins(100, 50, 100, 50)
        self.gridLayout.addWidget(self.spinBox, 0, 0)
        self.gridLayout.addWidget(self.compactSpinBox, 0, 1, Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addWidget(self.doubleSpinBox, 1, 0)
        self.gridLayout.addWidget(self.compactDoubleSpinBox, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addWidget(self.timeEdit, 2, 0)
        self.gridLayout.addWidget(self.compactTimeEdit, 2, 1, Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addWidget(self.dateEdit, 3, 0)
        self.gridLayout.addWidget(self.compactDateEdit, 3, 1, Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addWidget(self.dateTimeEdit, 4, 0)
        self.gridLayout.addWidget(self.compactDateTimeEdit, 4, 1, Qt.AlignmentFlag.AlignLeft)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
