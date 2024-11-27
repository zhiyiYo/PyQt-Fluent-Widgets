# coding:utf-8
import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton, CaptionLabel, setTheme, Theme


class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('打开 URL', self)
        self.urlLineEdit = LineEdit(self)

        self.urlLineEdit.setPlaceholderText('输入文件、流或者播放列表的 URL')
        self.urlLineEdit.setClearButtonEnabled(True)

        self.warningLabel = CaptionLabel("The url is invalid")
        self.warningLabel.setTextColor("#cf1010", QColor(255, 28, 32))

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.urlLineEdit)
        self.viewLayout.addWidget(self.warningLabel)
        self.warningLabel.hide()

        # change the text of button
        self.yesButton.setText('打开')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(350)

        # self.hideYesButton()

    def validate(self):
        """ Rewrite the virtual method """
        isValid = QUrl(self.urlLineEdit.text()).isValid()
        self.warningLabel.setHidden(isValid)
        return isValid


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background:rgb(32,32,32)}')

        self.hBxoLayout = QHBoxLayout(self)
        self.button = PushButton('打开 URL', self)

        self.resize(600, 600)
        self.hBxoLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignCenter)
        self.button.clicked.connect(self.showDialog)

    def showDialog(self):
        w = CustomMessageBox(self)
        if w.exec():
            print(w.urlLineEdit.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()