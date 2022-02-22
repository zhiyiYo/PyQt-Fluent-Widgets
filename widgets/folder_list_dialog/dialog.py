# coding:utf-8
import textwrap

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton


class Dialog(QDialog):

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, title: str, content: str, parent=None):
        super().__init__(parent, Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.resize(300, 200)
        self.setWindowTitle(title)
        self.content = content
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content, self)
        self.yesButton = QPushButton('确定', self)
        self.cancelButton = QPushButton('取消', self)
        self.__initWidget()

    def __initWidget(self):
        """ initialize widgets """
        self.yesButton.setFocus()
        self.titleLabel.move(30, 22)
        self.contentLabel.setMaximumWidth(900)
        self.contentLabel.setText('\n'.join(textwrap.wrap(self.content, 51)))
        self.contentLabel.move(30, self.titleLabel.y()+50)

        self.__setQss()

        # adjust window size
        rect = self.contentLabel.rect()
        w = 60 + rect.right() + self.cancelButton.width()
        h = self.contentLabel.y()+self.contentLabel.height()+self.yesButton.height()+60
        self.setFixedSize(w, h)

        # connect signal to slot
        self.yesButton.clicked.connect(self.__onYesButtonClicked)
        self.cancelButton.clicked.connect(self.__onCancelButtonClicked)

    def resizeEvent(self, e):
        self.cancelButton.move(self.width()-self.cancelButton.width()-30,
                               self.height()-self.cancelButton.height()-30)
        self.yesButton.move(self.cancelButton.x() -
                            self.yesButton.width()-30, self.cancelButton.y())

    def __onCancelButtonClicked(self):
        self.cancelSignal.emit()
        self.deleteLater()

    def __onYesButtonClicked(self):
        self.yesSignal.emit()
        self.deleteLater()

    def __setQss(self):
        """ set style sheet """
        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")

        with open('resource/style/dialog.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

        self.yesButton.adjustSize()
        self.cancelButton.adjustSize()
        self.contentLabel.adjustSize()
