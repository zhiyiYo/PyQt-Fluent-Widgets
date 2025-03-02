# coding:utf-8
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel, QPushButton

from ...common.auto_wrap import TextWrap
from ...common.style_sheet import FluentStyleSheet
from .mask_dialog_base import MaskDialogBase


class MessageDialog(MaskDialogBase):
    """ Win10 style message dialog box with a mask """

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, title: str, content: str, parent):
        super().__init__(parent=parent)
        self.content = content
        self.titleLabel = QLabel(title, self.widget)
        self.contentLabel = QLabel(content, self.widget)
        self.yesButton = QPushButton(self.tr('OK'), self.widget)
        self.cancelButton = QPushButton(self.tr('Cancel'), self.widget)
        self.__initWidget()

    def __initWidget(self):
        """ initialize widgets """
        self.windowMask.resize(self.size())
        self.widget.setMaximumWidth(540)
        self.titleLabel.move(24, 24)
        self.contentLabel.move(24, 56)
        self.contentLabel.setText(TextWrap.wrap(self.content, 71)[0])

        self.__setQss()
        self.__initLayout()

        # connect signal to slot
        self.yesButton.clicked.connect(self.__onYesButtonClicked)
        self.cancelButton.clicked.connect(self.__onCancelButtonClicked)

    def __initLayout(self):
        """ initialize layout """
        self.contentLabel.adjustSize()
        self.widget.setFixedSize(48+self.contentLabel.width(),
                                 self.contentLabel.y() + self.contentLabel.height()+92)
        self.yesButton.resize((self.widget.width() - 54) // 2, 32)
        self.cancelButton.resize(self.yesButton.width(), 32)
        self.yesButton.move(24, self.widget.height()-56)
        self.cancelButton.move(
            self.widget.width()-24-self.cancelButton.width(), self.widget.height()-56)

    def __onCancelButtonClicked(self):
        self.cancelSignal.emit()
        self.reject()

    def __onYesButtonClicked(self):
        self.setEnabled(False)
        self.yesSignal.emit()
        self.accept()

    def __setQss(self):
        """ set style sheet """
        self.windowMask.setObjectName('windowMask')
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        FluentStyleSheet.MESSAGE_DIALOG.apply(self)
