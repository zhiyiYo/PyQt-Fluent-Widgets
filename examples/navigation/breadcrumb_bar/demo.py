# coding:utf-8
import sys

from uuid import uuid1
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QStackedWidget, QVBoxLayout

from qfluentwidgets import (BreadcrumbBar, setFont, setTheme, Theme, LineEdit, PrimaryToolButton,
                            SubtitleLabel, FluentIcon)



class Demo(QWidget):

    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setStyleSheet('Demo{background:rgb(32,32,32)}')

        self.breadcrumbBar = BreadcrumbBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.lineEdit = LineEdit(self)
        self.addButton = PrimaryToolButton(FluentIcon.SEND, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.lineEditLayout = QHBoxLayout()

        self.addButton.clicked.connect(lambda: self.addInterface(self.lineEdit.text()))
        self.lineEdit.returnPressed.connect(lambda: self.addInterface(self.lineEdit.text()))
        self.lineEdit.setPlaceholderText('Enter the name of interface')

        # NOTE: adjust the size of breadcrumb item
        setFont(self.breadcrumbBar, 26)
        self.breadcrumbBar.setSpacing(20)
        self.breadcrumbBar.currentItemChanged.connect(self.switchInterface)

        self.addInterface('Home')
        self.addInterface('Documents')

        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.addWidget(self.breadcrumbBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.addLayout(self.lineEditLayout)

        self.lineEditLayout.addWidget(self.lineEdit, 1)
        self.lineEditLayout.addWidget(self.addButton)
        self.resize(500, 500)

    def addInterface(self, text: str):
        if not text:
            return

        w = SubtitleLabel(text)
        w.setObjectName(uuid1().hex)
        w.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lineEdit.clear()
        self.stackedWidget.addWidget(w)
        self.stackedWidget.setCurrentWidget(w)

        # !IMPORTANT: add breadcrumb item
        self.breadcrumbBar.addItem(w.objectName(), text)

    def switchInterface(self, objectName):
        self.stackedWidget.setCurrentWidget(self.findChild(SubtitleLabel, objectName))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()