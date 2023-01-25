# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QPushButton, QFrame, QVBoxLayout, QHBoxLayout
from qframelesswindow import FramelessDialog

from ...common.auto_wrap import TextWrap
from ...common.style_sheet import setStyleSheet


class Dialog(FramelessDialog):
    """ Dialog box """

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, title: str, content: str, parent=None):
        super().__init__(parent)
        self.resize(300, 240)
        self.titleBar.hide()

        self.content = content
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content, self)
        self.windowTitleLabel = QLabel(title, self)

        self.buttonGroup = QFrame(self)
        self.yesButton = QPushButton(self.tr('OK'), self.buttonGroup)
        self.cancelButton = QPushButton(self.tr('Cancel'), self.buttonGroup)

        self.vBoxLayout = QVBoxLayout(self)
        self.textLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout(self.buttonGroup)

        self.__initWidget()

    def __initWidget(self):
        self.__setQss()
        self.__initLayout()

        self.yesButton.setFocus()
        self.buttonGroup.setFixedHeight(101)
        self.contentLabel.setText(TextWrap.wrap(self.content, 100, False)[0])
        self.setResizeEnabled(False)

        self.yesButton.clicked.connect(self.__onYesButtonClicked)
        self.cancelButton.clicked.connect(self.__onCancelButtonClicked)

    def __initLayout(self):
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.windowTitleLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addLayout(self.textLayout, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignBottom)

        self.textLayout.setSpacing(15)
        self.textLayout.setContentsMargins(30, 30, 30, 30)
        self.textLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)
        self.textLayout.addWidget(self.contentLabel, 0, Qt.AlignTop)

        self.buttonLayout.setSpacing(15)
        self.buttonLayout.setContentsMargins(30, 30, 30, 30)
        self.buttonLayout.addWidget(self.yesButton, 1, Qt.AlignVCenter)
        self.buttonLayout.addWidget(self.cancelButton, 1, Qt.AlignVCenter)

    def __onCancelButtonClicked(self):
        self.cancelSignal.emit()
        self.reject()

    def __onYesButtonClicked(self):
        self.yesSignal.emit()
        self.accept()

    def __setQss(self):
        """ 设置层叠样式 """
        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")
        self.yesButton.setObjectName('yesButton')
        self.buttonGroup.setObjectName('buttonGroup')
        self.windowTitleLabel.setObjectName('windowTitleLabel')

        setStyleSheet(self, 'dialog')

        self.yesButton.adjustSize()
        self.cancelButton.adjustSize()
